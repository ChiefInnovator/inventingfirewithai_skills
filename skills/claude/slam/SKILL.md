---
name: slam
description: Ship the current branch end-to-end under a session /goal that keeps the run alive to the merge — preflight checks, commit, push, ensure a PR against the repo's base branch (develop if it exists, else main), request and address GitHub Copilot / AI review comments, merge, then delete the merged branch. Stops on anything ambiguous rather than guessing.
user_invocable: true
arguments: message-or-scope
---

# /slam Skill

You take the current branch from "work in the tree" to "merged into the repo's base branch", unattended where it's safe and stopping where it isn't.

The user passed: `$ARGUMENTS` (optional — a commit message or subject hint; derive one from the diff if empty).

This skill is repo-agnostic. It detects the base branch, the review bot, and the repo's protection rules rather than assuming them. **A project's own `CLAUDE.md` outranks this file** wherever the two differ.

**Hard rules, no exceptions:**

- **NEVER REBASE.** Not `git rebase` in any form, not `git pull --rebase`, not GitHub's "Rebase and merge", not asking a bot to rebase. If the branch is behind, `git merge origin/$BASE` into it.
- **Never `--admin`-merge**, never force-push.
- **Never delete a protected branch** — `$BASE`, `main`, `master`, or `develop` — under any circumstance. Not as cleanup, not to "recreate it clean", not because a command suggested it. Some repos also have server-side rulesets that would reject it, but **never rely on the server to stop you.** Refuse locally first.
- **Delete the feature branch only after the merge is verified** (Phase 7). Invoking this skill is the approval for that one deletion — the branch this run just merged, once GitHub reports it `MERGED` — and it extends to nothing else.
- **Never add `Co-Authored-By` or AI-attribution lines** to commits.
- Merge with a **merge commit** (`gh pr merge --merge`). Not `--rebase`. Use `--squash` only if the user explicitly asks.

Work the phases in order. Report a one-line status per phase as you go. If a **stop condition** fires, halt and tell the user exactly what's blocking and the options — do not improvise past it.

---

## Phase G — Set the ship goal (before Phase 0)

`/slam` is a long unattended pipeline with two unavoidable waits — the AI review and CI — and a turn can end at either one with the PR still open. Claude Code's `/goal` exists for exactly that: it registers a Stop hook that blocks the session from stopping until a separate evaluator confirms the condition **from the conversation**, and clears itself once it does. Run `/slam` under a goal and the run survives to the merge instead of trailing off at a natural turn boundary.

**Set it first, before Phase 0 touches the tree.**

Propose it with the `ProposeGoal` tool — the user approves with one keypress. If that tool is unavailable (non-interactive or agent context, plan mode, or model-proposed goals disabled in settings), print the `/goal` line for the user to paste and **carry on either way**. A missing goal is a missing safety net, never a reason not to ship.

**The condition** — name the branch and base, state the evidence, and include the halt state:

```
/goal the PR for <branch> reports MERGED into <base> with the merge commit SHA reported, and the feature branch is deleted or its retention explained — or /slam halted at a named stop condition with the blocker and the options reported
```

Keep it under ~500 characters so the whole thing fits the approval dialog (a typed `/goal` allows 4000).

**That second clause is not decoration.** Every stop condition in this skill — a conflict, red CI, a human requesting changes, a diverged protected branch — is a *correct* ending. Word the goal as "merged" alone and the evaluator reads a legitimate halt as failure and pushes the session to keep grinding, straight into the improvisation the stop conditions exist to prevent. Halting with the blocker reported must satisfy the goal.

**The goal never outranks a hard rule.** If continuing means a rebase, a force-push, an `--admin` merge, or deleting a protected branch, the rule wins: report and stop. A Stop hook cannot authorize what a hard rule forbids.

**Use it on the waits.** Poll for the AI review (Phase 5) and CI (Phase 6) as background work — goal evaluation defers while background work runs and a check-in is injected instead, which is the "keep waiting" behavior those phases want.

**Clearing.** The goal auto-clears when the evaluator confirms it met. It does not clear on a halt, and nothing in this skill can clear it — if you stopped early and a goal is still active, say so in the final report and tell the user to run `/goal clear`.

---

## Phase R — Resolve the repo's shape

Everything downstream depends on three facts. Establish them once, here, and carry them through the whole run: **`$BASE`, `$BRANCH`, `$REPO`.** Re-deriving any of them mid-run is how a later phase acts on the wrong branch.

### The base branch: `develop` if it exists, else `main`

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  || { echo "REFUSE: not a git repository"; exit 1; }

git fetch origin --quiet \
  || { echo "REFUSE: git fetch failed — every check below would run on stale refs"; exit 1; }

if   git show-ref --verify --quiet refs/remotes/origin/develop; then BASE=develop
elif git show-ref --verify --quiet refs/remotes/origin/main;    then BASE=main
else BASE=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null)
fi
[ -n "$BASE" ] || { echo "REFUSE: cannot determine a base branch"; exit 1; }
git show-ref --verify --quiet "refs/remotes/origin/$BASE" \
  || { echo "REFUSE: origin/$BASE does not exist"; exit 1; }
echo "base: $BASE"
```

`develop` wins whenever it exists — a repo with both is running a develop→main promotion flow, and feature work targets `develop`. The `gh` fallback catches repos on `master` or another custom default.

**Never hardcode `develop` or `main` anywhere below.** Use `$BASE`.

### The protected set

`$BASE` is protected, and so are `main`, `master`, and `develop` **even when they are not the base** — a repo with a develop flow still must not have `main` deleted or reset by this skill. Use this test everywhere a branch name is about to be deleted, reset, or committed to:

```bash
is_protected() {
  case "$1" in
    ""|main|master|develop|"$BASE"|origin/*) return 0;;
    *) return 1;;
  esac
}
```

The empty string is in that list deliberately: an unset variable expands to nothing, and `git push origin --delete ""` must never be one typo away from running.

---

## Phase 0 — Get the work onto a feature branch

Only runs when the current branch is protected. Otherwise skip straight to Phase 1.

The work is on a protected branch and cannot ship from there. **Move it — don't stop, and don't commit where it stands.** How you move it depends entirely on whether anything has been committed yet, so establish that first:

```bash
PROT=$(git branch --show-current)

# Anything uncommitted (staged, unstaged, or untracked)?
dirty=$(git status --porcelain)

# Local commits that origin does not have? These are the dangerous case.
ahead=$(git log --oneline "origin/$PROT..HEAD")

echo "dirty: $([ -n "$dirty" ] && echo yes || echo no)"
# grep -c exits 1 when it counts zero, which `set -e` would treat as failure —
# and "no local commits" is the normal case, not an error.
echo "local commits ahead of origin/$PROT: $(printf '%s' "$ahead" | grep -c . || true)"
[ -n "$dirty$ahead" ] || { echo "nothing to ship — clean tree, nothing ahead"; exit 0; }
```

**Name the branch** from the dominant change. Use the repo's existing prefix convention — check what's already there (`git branch -a --format='%(refname:short)'`) rather than assuming; `feature/` for new work and `fix/` for a repair are the common default. Derive it from the diff — don't ask. Creating a branch is cheap and reversible; that is not the part that needs confirmation.

### Case A — uncommitted only (`ahead` empty)

The easy case, and the common one. `git checkout -b` carries the working tree across untouched and leaves the protected branch exactly where it was:

```bash
git checkout -b "$NEW_BRANCH"   # dirty tree comes along; protected branch not modified
```

Nothing else to undo. Proceed to Phase 1, which will capture `$BRANCH` as the new branch.

### Case B — local commits on the protected branch (`ahead` non-empty)

Commits already exist where they must not. Moving them means pointing the protected branch back at its remote — **the one step in this skill that discards local state, so it is gated on the user.**

```bash
# The local branch must be strictly AHEAD of its remote — a fast-forward and
# nothing else. If origin/$PROT is not an ancestor of HEAD the branch has
# diverged, which means someone else's commits are tangled in and rewinding
# would take them too.
git merge-base --is-ancestor "origin/$PROT" HEAD \
  || { echo "REFUSE: $PROT has diverged from origin/$PROT — resolve by hand"; exit 1; }
```

Show the user the exact commits from `$ahead` and confirm before touching anything. Then:

```bash
git checkout -b "$NEW_BRANCH"          # commits + dirty tree now live here
git branch -f "$PROT" "origin/$PROT"   # rewind the protected branch to its remote
```

Use `git branch -f` while standing on the **new** branch, never `git reset --hard` while standing on the protected one — `-f` only moves the ref and cannot touch the working tree, so a mistake costs a ref update and not your uncommitted edits. `git reflog` still holds the old position either way.

**Stop conditions:**

| Condition | Why it stops |
| --- | --- |
| `git fetch` fails | Cannot tell a local commit from a pushed one; every decision below depends on it. |
| The protected branch has diverged from its remote | Rewinding would discard commits that aren't yours to move. Hand the user the divergence. |
| Case B and the user does not confirm | Discarding local history is never unattended. |
| Tree holds clearly unrelated bodies of work | Don't sweep them onto one branch — ask which belong, as Phase 2 requires. |

Never `git branch -f` or reset a protected branch to anything but its own remote ref, and never delete a protected branch as a way of "moving" work.

---

## Phase 1 — Preflight

Run these and evaluate before touching anything:

```bash
# Capture the branch ONCE. Empty means detached HEAD — stop here rather than
# letting an empty $BRANCH flow into push/delete commands downstream.
BRANCH=$(git branch --show-current)
[ -n "$BRANCH" ] || { echo "REFUSE: detached HEAD — no branch to ship"; exit 1; }

# This skill ships FEATURE branches. Refuse a protected branch outright:
# committing straight to one is forbidden, and Phase 7 must never receive its name.
is_protected "$BRANCH" \
  && { echo "REFUSE: '$BRANCH' is protected — /slam ships feature branches"; exit 1; }
echo "branch: $BRANCH  ->  base: $BASE"

gh auth status >/dev/null || { echo "REFUSE: gh not authenticated — run 'gh auth login'"; exit 1; }
git remote get-url origin >/dev/null 2>&1 || { echo "NO_REMOTE"; }
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null)
```

**Every row in the table below is enforced by the block above, not left to your judgement.** A stop condition that is only described is a stop condition that does not fire.

**Record `$BRANCH` now and carry it through the whole run.** Phase 6 checks out `$BASE`, so from that point on `git branch --show-current` no longer names the feature branch — and Phase 7 deletes by name. Re-deriving it after the checkout is how you delete the wrong branch.

**Stop conditions:**

| Condition | Why it stops |
| --- | --- |
| Current branch is protected | This skill ships *feature branches*. Phase 0 should already have moved the work off; if you reach here still on one, that is a bug, so stop. |
| Detached HEAD | Nothing to push. |
| `gh` not authenticated | Cannot manage the PR. Tell the user to run `gh auth login`. |
| No `origin` remote | Handled below — offer to create one; don't silently ship nowhere. |

### No remote — create one

Every repo should have a remote. If `origin` is missing, the local history is a single disk failure from gone, and none of Phases 3–7 can run at all.

**Confirm with the user before creating it, and default to private.** Creating a repo publishes code — that is outward-facing and not reversible in the way a local commit is. Before you offer, **scan the tree for anything that must not leave the machine**:

```bash
git ls-files -z | xargs -0 grep -nEI \
  '(api[_-]?key|secret|password|client[_-]?secret|connection[_-]?string|BEGIN [A-Z ]*PRIVATE KEY|xox[bp]-|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})' \
  2>/dev/null | grep -viE '(process\.env|import\.meta\.env|placeholder|example|your-|\$\{)' | head -25
git ls-files | grep -iE '\.env$|\.pem$|\.pfx$|credential' || echo "no credential files tracked"
```

Report what you find — including tenant/subscription/account identifiers, which are not credentials but do name real infrastructure — then create it:

```bash
gh repo create "<owner>/<name>" --private --source=. --remote=origin --push
```

Only propose `--public` if the user asks for it, and only after the scan came back clean. Then re-run Phase R so `$BASE` and `$REPO` reflect the new remote.

### Branch-off-base check

Confirm the branch actually descends from `$BASE`:

```bash
git merge-base --is-ancestor "origin/$BASE" HEAD && echo "up to date with $BASE" \
  || echo "BEHIND: origin/$BASE has commits not in HEAD"
```

If it reports BEHIND, the branch is stale. **Merge the base in — never rebase:**

```bash
git merge "origin/$BASE"
```

If that conflicts, stop and hand the conflict list to the user. Do not attempt clever resolutions on someone else's code.

If `git merge-base "origin/$BASE" HEAD` is empty, the branch shares no history with the base — stop, something is wrong.

---

## Phase 2 — Inspect and commit

```bash
git status
git diff --stat
git diff --cached --stat
```

If the tree is clean **and** there are no unpushed commits, skip to Phase 4 — there may still be an open PR needing attention. Say so rather than reporting "nothing to do".

**Before staging, look at what you're committing.** Read the actual diff, not just the stat. Specifically check for:

- **Secrets / credentials** — keys, tokens, connection strings, passwords, `.env` files. A secret in a diff is a stop condition, in any repo.
- **Encrypted paths committed as plaintext.** If the repo uses git-crypt, a file that should be ciphertext but got staged as plaintext is a hard stop — once pushed, removing it means rewriting history, which this skill will not do. This check auto-detects and no-ops in repos without git-crypt:
  ```bash
  viol=0
  while IFS= read -r f; do
    [ "$(git check-attr filter -- "$f" | sed 's/.*: //')" = "git-crypt" ] || continue
    hdr=$(git cat-file blob ":$f" 2>/dev/null | head -c 10 | xxd -p)
    case "$hdr" in
      00474954435259505400) : ;;   # \0GITCRYPT\0 — correctly encrypted
      *) echo "HARD STOP: $f is git-crypt-managed but staged as PLAINTEXT"; viol=1;;
    esac
  done < <(git diff --cached --name-only)
  [ "$viol" -eq 0 ] || exit 1
  ```
- **Large or generated files that belong in `.gitignore`** — build output, local databases (`*.sqlite3`), `node_modules`, editor state. Mention them; don't silently sweep them in with `git add -A`.
- **Files referencing deleted paths** — e.g. a `docker-compose.yml` service whose build context was removed in the same change. Grep for the removed path across the repo.
- **Debug leftovers** — stray `print`/`console.log`, commented-out blocks, `.orig`/`.rej` files.

Stage with `git add -A` unless the diff contains unrelated work; if it does, ask which changes belong in this commit rather than lumping them together.

**Commit message** — conventional commits (`type(scope): subject`), matched to the repo's own history (`git log --oneline -20` shows the house style):

- Subject in the imperative, no trailing period, ~72 chars.
- A body that explains **why**, not a restatement of the diff. Wrap at ~76.
- Multiple logical changes in one commit: lead with the dominant one, cover the rest in the body.
- No AI attribution, no `Co-Authored-By`.

Use a heredoc so the body survives intact:

```bash
git commit -F - <<'EOF'
type(scope): subject

Body.
EOF
```

---

## Phase 3 — Push

```bash
git push -u origin "$BRANCH"
```

If rejected as non-fast-forward, the remote has commits you don't. **`git pull` (merge, never `--rebase`)**, resolve, then push. Never `--force`.

Confirm it landed:

```bash
git log origin/"$BRANCH"..HEAD --oneline   # expect empty
```

---

## Phase 4 — Ensure a PR exists

```bash
gh pr view --json number,state,url,isDraft,mergeable,baseRefName 2>/dev/null
```

**If no PR exists**, create one against `$BASE`:

```bash
gh pr create --base "$BASE" --head "$BRANCH" \
  --title "<conventional-commit-style title>" --body "<body>"
```

Body should cover: what changed and why, how it was verified, and anything the reviewer should look at closely. PR bodies, unlike commits, may carry the Claude Code attribution footer — follow whatever the repo's recent PRs already do.

**If a PR exists** but targets something other than `$BASE`, stop and ask — retargeting changes the review surface.

**If the PR is a draft**, ask before marking it ready.

Capture the PR number once, alongside `$BRANCH` and `$BASE`:

```bash
PR=$(gh pr view --json number -q .number)
```

---

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

Watch for AI suggestions that conflict with the repo's documented decisions — deliberate deviations recorded in `CLAUDE.md` or the repo's architecture docs are not defects. Cite the doc in your reply when you decline.

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

## Phase 6 — Merge

**Check mergeability and CI first:**

```bash
gh pr view "$PR" --json mergeable,mergeStateStatus,statusCheckRollup \
  -q '{mergeable, mergeStateStatus, checks: [.statusCheckRollup[]? | {name, conclusion}]}'
```

**Stop conditions — do not merge:**

| Condition | Action |
| --- | --- |
| Any required check failing or still running | Wait for running checks; report failures and stop. Never merge red. |
| `mergeable: CONFLICTING` | Merge `origin/$BASE` into the branch (**not rebase**), resolve, push, re-check. |
| A human reviewer requested changes | Stop — an AI pass doesn't clear a human's block. |
| Unresolved review comments you couldn't triage | Stop and ask. |

A repo with no CI configured returns an empty check list. That is "nothing to wait for", not "checks passed" — report it as such.

**Merge with a merge commit:**

```bash
gh pr merge "$PR" --merge
```

Do **not** pass `--rebase`. Do **not** pass `--admin` to bypass protections. Do **not** pass `--delete-branch` here either — deletion is Phase 7, gated on verifying the merge actually happened.

**Verify it actually merged**, then sync the local base branch:

```bash
gh pr view "$PR" --json state,mergedAt,mergeCommit
git checkout "$BASE" && git pull origin "$BASE"
```

---

## Phase 7 — Clean up the branch

Delete the feature branch once the work is genuinely landed. **Every one of these must hold — if any fails, stop and leave the branch alone:**

```bash
# $BRANCH is the value captured in Phase 1. Do NOT reassign it here and do NOT
# re-derive it — Phase 6 has already checked out $BASE, so any fresh
# `git branch --show-current` now yields the base branch, not the branch to delete.

# 0. NEVER a protected branch, and never an empty name. Check this FIRST —
#    an unset $BRANCH would otherwise expand to nothing and corrupt the
#    delete commands below.
is_protected "$BRANCH" && { echo "REFUSE: '$BRANCH' is protected or invalid"; exit 1; }

# 1. GitHub reports the PR merged — state MERGED *and* a real timestamp
read -r state merged_at <<<"$(gh pr view "$PR" --json state,mergedAt -q '"\(.state) \(.mergedAt)"')"
[ "$state" = "MERGED" ] && [ -n "$merged_at" ] && [ "$merged_at" != "null" ] \
  || { echo "REFUSE: PR $PR is not merged (state=$state mergedAt=$merged_at)"; exit 1; }

# 2. You are NOT standing on the branch you're deleting
[ "$(git branch --show-current)" = "$BASE" ] \
  || { echo "REFUSE: not on $BASE — Phase 6 should have checked it out"; exit 1; }

# 3. The branch is an ancestor of the base — its commits really are in.
#    Re-fetch IMMEDIATELY BEFORE the check. Phase R's fetch is minutes old by
#    now and Phase 6's pull refreshed only $BASE. If anyone pushed to the
#    feature branch during this run, a stale origin/$BRANCH points at an older
#    commit that IS contained in the base — the gate would pass and the delete
#    would take the newer commits with it.
git fetch origin --quiet \
  || { echo "REFUSE: git fetch failed — cannot judge containment on stale refs"; exit 1; }
git merge-base --is-ancestor "origin/$BRANCH" "origin/$BASE" \
  || { echo "REFUSE: origin/$BRANCH is NOT contained in origin/$BASE"; exit 1; }
```

Every check above **exits non-zero on failure** rather than printing a verdict for you to read past. That is deliberate: a gate that only narrates is not a gate. In particular, note that `--is-ancestor ... && echo ok || echo "NOT CONTAINED"` would *swallow* the non-zero exit and let the deletion proceed — never write the containment check that way.

Only with all four satisfied:

```bash
git push origin --delete "$BRANCH"   # remote
git branch -d "$BRANCH"              # local — -d, never -D
```

Use `git branch -d`, never `-D`. `-d` refuses to delete a branch whose commits aren't reachable from the current HEAD, which is a free second opinion on check 3. **If `-d` refuses, that is a real signal** — the commits are not in the base. Stop and investigate rather than reaching for `-D`.

Note this ordering matters if the merge was ever done as a squash: squashed commits are not literally ancestors of the base, so checks 3 and `-d` will both correctly refuse. That is the desired behavior — report it rather than forcing.

**Skip deletion entirely** (and say so) if the merge did not happen, if the user asked to keep the branch, or if the branch has commits that never made it into the PR.

---

## Final report

Summarize concretely:

- Repo and the detected `$BASE`, and why (`develop` present, or fell back to `main`/default)
- Commit SHA(s) and subject(s)
- PR number and URL, and whether you created it or reused an existing one
- Whether an AI review actually ran — and if not, why (no ruleset, no subscription, over the 300-file cap). Never let silence read as approval.
- Every AI comment: what it said, and whether you fixed it or declined (with the reason)
- CI status at merge time, or "no checks configured"
- Merge commit SHA, and confirmation the local base branch is synced
- Whether the feature branch was deleted (local + remote), or why it was kept
- **Anything you skipped or that remains open** — state it plainly rather than implying a clean sweep

If you stopped early, say exactly which phase, why, and what the user's options are.

**Under a Phase G goal the report is also the evidence.** The evaluator judges the condition from the conversation and cannot run `gh` for itself, so put the literal facts in the text — PR number, `state=MERGED`, the merge commit SHA, the deleted branch name, or the named stop condition and its blocker. A report that says "all done" gives the evaluator nothing to confirm and the session keeps grinding. If you halted and the goal is still active, close with the reminder that `/goal clear` releases it.
