## Phase 5 — Review and address AI comments

### Copilot's two logins

This trips up every filter written from memory, so take it as verified fact:

| Where it appears | Login |
| --- | --- |
| The **review** (summary + verdict) | `copilot-pull-request-reviewer[bot]` |
| Its **inline file/line comments** | `Copilot` |
| As a **requested reviewer** | `Copilot` |

A filter for `copilot-pull-request-reviewer[bot]` against the inline-comments endpoint matches nothing while the findings sit there unread. Prefer listing all comments and reading them, as below.

### Make sure a review is actually coming

Copilot reviews when a repository ruleset with a `copilot_code_review` rule is `active`, **or** when someone requests `Copilot` as a reviewer. A repo with neither produces no review at all — and silence from Copilot is not an approval.

Check whether a ruleset already covers it, and only request manually if none does:

```bash
# Any ACTIVE ruleset carrying a copilot_code_review rule? Note that the rule is
# often bundled into a general branch-protection ruleset (e.g. "Protect Develop")
# rather than living in one obviously named for Copilot — so match on rule TYPE,
# never on the ruleset's name.
auto=$(gh api "/repos/$REPO/rulesets" --paginate -q '.[].id' 2>/dev/null | while read -r id; do
  gh api "/repos/$REPO/rulesets/$id" \
    -q 'select(.enforcement=="active") | select(any(.rules[]?; .type=="copilot_code_review")) | .name' 2>/dev/null
done)

if [ -n "$auto" ]; then
  echo "Copilot auto-review active via ruleset(s): $auto"
else
  gh pr edit "$PR" --add-reviewer Copilot 2>/dev/null \
    || gh api -X POST "/repos/$REPO/pulls/$PR/requested_reviewers" \
         -f 'reviewers[]=Copilot' >/dev/null 2>&1 \
    || echo "NOTE: could not request a Copilot review on $REPO"
fi
```

The listing endpoint does **not** expand `.rules`, so you must fetch each ruleset by id to see its rule types. A filter written against the list alone silently finds nothing.

If neither path works, Copilot code review is not available on this repo (no Copilot subscription covering it, or the org disallows it). **Say so explicitly in the final report — "no AI review happened" is not the same as "reviewed clean."**

### The 300-file cap

```bash
gh pr view "$PR" --json changedFiles -q '.changedFiles'
```

Copilot hard-refuses any PR over **300 changed files** — *"Copilot wasn't able to review this pull request because it exceeds the maximum number of files (300)"*. It is a GitHub product limit with no setting to raise it, and it counts **every** changed file including pure deletions, generated files, and paths covered by content exclusion or `.gitattributes` `linguist-generated`. If the PR is over the cap, report that no AI review happened. Bulk deletions and generated-file churn belong in their own PR so the review-worthy changes stay under the cap.

### Fetch the feedback

Review bodies and inline comments are different endpoints, and the inline ones carry the actionable findings:

```bash
# Top-level reviews (summary + verdict). Check commit.oid against HEAD —
# a review from an earlier commit is stale.
gh pr view "$PR" --json reviews \
  -q '.reviews[] | "\(.author.login) [\(.state)] @\(.commit.oid[0:7])\n\(.body)\n---"'

# Inline file/line comments — where the real findings live.
# --paginate is REQUIRED: this endpoint returns 30 per page by default, and a
# finding on page 2 that you never fetched is a finding you never triaged.
gh api --paginate "/repos/$REPO/pulls/$PR/comments?per_page=100" \
  -q '.[] | "ID:\(.id) \(.user.login) \(.path):\(.line)\n\(.body)\n---"'

# Human/other-bot issue comments
gh pr view "$PR" --json comments \
  -q '.comments[] | "\(.author.login)\n\(.body)\n---"'
```

The review usually lands within a few minutes of the push. If it hasn't, wait and re-poll a couple of times before concluding there's nothing. If it never appears, say so — don't claim it approved.

### Triage

**Triage every AI comment on its merits. Do not reflexively "fix" all of them.** Copilot is frequently wrong about repo-specific intent. For each:

- **Valid** → fix it, in a separate commit (`fix: address review feedback on X`), then push. The PR updates automatically.
- **Wrong or not applicable** → leave the code alone and **reply on the PR explaining why**, so the reasoning is on the record:
  ```bash
  gh api "/repos/$REPO/pulls/$PR/comments/<comment-id>/replies" -f body="..."
  ```
- **Out of scope** (a real issue, but not this PR's job) → don't expand the PR. Note it in a reply and tell the user it needs its own change.

Watch for AI suggestions that conflict with the repo's documented decisions — deliberate deviations recorded in `AGENTS.md` or other applicable repository instructions or the repo's architecture docs are not defects. Cite the doc in your reply when you decline.

Re-verify after pushing fixes: new commits can trigger a fresh review round. Loop Phase 5 until no new actionable comments arrive.

### Resolve the threads — replying is not resolving

Some repos carry a ruleset with `required_review_thread_resolution: true`, and there an unresolved thread blocks the merge with *"the base branch policy prohibits the merge"* even when every check is green and no approval is required — a policy error with no hint that a thread is behind it. Resolving handled threads is correct practice regardless, so do it either way:

```bash
# List threads and their resolution state
gh api graphql -f query='
{ repository(owner:"'"${REPO%/*}"'", name:"'"${REPO#*/}"'") {
    pullRequest(number:'"$PR"') {
      reviewThreads(first:100) {
        nodes { id isResolved path }
        pageInfo { hasNextPage endCursor } } } } }' \
  --jq '.data.repository.pullRequest.reviewThreads |
        (.nodes[] | "\(.id) resolved=\(.isResolved) \(.path)"),
        (.pageInfo | select(.hasNextPage) | "MORE THREADS after \(.endCursor)")'

# Resolve one (only after it is genuinely handled — fixed, or declined with a reply on the record)
gh api graphql -f query='
mutation { resolveReviewThread(input:{threadId:"<THREAD_ID>"}) { thread { isResolved } } }'
```

100 is the GraphQL page maximum. If the listing prints `MORE THREADS`, page through with `reviewThreads(first:100, after:"<endCursor>")` until it stops.

Resolve a thread only once it has been dealt with. Resolving to clear a merge block, without a fix or a stated reason, silently discards review feedback.

---
