# GitHub Review Workflow

Use the repository, PR, host, and head SHA captured by Slam. These command examples require an authenticated `gh` CLI; equivalent available GitHub tools can be used when they preserve identity, pagination, and error handling. For REST calls use `SLAM_OWNER_REPO` without the host and `--hostname "$SLAM_HOST"` explicitly. Keep request text in structured arguments or properly quoted files, never interpolated shell code.

## Request review

Read existing review requests and applicable automatic-review settings first. Rulesets must be active and match the branch; the mere presence of a Copilot rule somewhere is insufficient. The ruleset list does not include every rule's details, so inspect applicable ruleset definitions when needed. Do not change rulesets or buy a subscription.

Check the installed CLI's help before choosing the supported request syntax. Current CLI:

```bash
gh pr edit "$SLAM_PR" --repo "$SLAM_REPO" --add-reviewer '@copilot'
```

The documented REST reviewer identifier is `copilot-pull-request-reviewer[bot]`. Returned inline-comment identities may differ. Read all feedback rather than filtering by one alias. Distinguish a failed request from an unavailable product, permission denial, or pending review. Use actual error/review evidence for limits; don't assume every large PR hit a fixed cap.

By default, a Copilot review is a comment and does not satisfy required approvals; check the actual repository configuration and review state. A push does not guarantee a re-review. Request one on the new head if automatic review of new pushes is not active.

## Retrieve all feedback

Fetch all pages of each REST endpoint; retain IDs, users, commit IDs, timestamps, paths, and bodies. Do not swallow API errors as empty lists.

```bash
gh api --hostname "$SLAM_HOST" --paginate "repos/$SLAM_OWNER_REPO/pulls/$SLAM_PR/reviews?per_page=100"
gh api --hostname "$SLAM_HOST" --paginate "repos/$SLAM_OWNER_REPO/pulls/$SLAM_PR/comments?per_page=100"
gh api --hostname "$SLAM_HOST" --paginate "repos/$SLAM_OWNER_REPO/issues/$SLAM_PR/comments?per_page=100"
```

Review `commit_id` must match `SLAM_HEAD` for a current-head review claim. Older unresolved findings still need triage. Distinguish the latest effective review from superseded or dismissed reviews; do not treat every historical human change request as still active, and never dismiss an active one yourself to unblock merging.

For a valid in-scope comment, fix, test, commit, push, and link the fix in the discussion. For a declined or out-of-scope comment, reply with a specific reason. Replies are visible to people and form the record; they are not proof the bot reconsidered. After an uncertain reply response, look for the posted reply before retrying to avoid duplicates.

Reply using the original inline comment ID:

```bash
gh api --hostname "$SLAM_HOST" --method POST \
  "repos/$SLAM_OWNER_REPO/pulls/$SLAM_PR/comments/$SLAM_COMMENT_ID/replies" \
  --input "$SLAM_REPLY_JSON"
```

The JSON input contains `body`. Use available structured tools or the host's file-editing tool to create exact multiline bodies.

## Review threads

Use GraphQL variables; never concatenate reviewer text into a query. Paginate `reviewThreads` with its own cursor until `hasNextPage=false`. If reading thread comments, paginate their separate connection too; the REST inline-comment retrieval above can supply complete bodies.

```graphql
query($owner: String!, $name: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $cursor) {
        nodes { id isResolved isOutdated path }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}
```

Map handled comments to their thread before resolving; fetch that thread's comment IDs with pagination where needed. Fixing or replying does not automatically resolve a thread. `isOutdated` alone does not mean handled. Resolve only after a fix or an evidence-based disposition is recorded, and never resolve a human disagreement without authority.

```graphql
mutation($id: ID!) {
  resolveReviewThread(input: {threadId: $id}) {
    thread { id isResolved }
  }
}
```

Refresh all threads and reviews before merging. A query returning GraphQL `errors` or incomplete data is a failed check, even if its HTTP response is successful.

## Official references

- [Requesting and handling Copilot review](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review)
- [GitHub CLI review requests](https://cli.github.com/manual/gh_pr_edit)
- [GitHub CLI merge and head matching](https://cli.github.com/manual/gh_pr_merge)
- [GitHub CLI check status](https://cli.github.com/manual/gh_pr_checks)
