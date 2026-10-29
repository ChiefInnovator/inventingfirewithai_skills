# GitHub Review Workflow

Use the repository, PR, host, and head SHA captured by Slam. These command examples require an authenticated `gh` CLI; equivalent available GitHub tools can be used when they preserve identity, pagination, and error handling. For REST calls use `SLAM_OWNER_REPO` without the host and `--hostname "$SLAM_HOST"` explicitly. Keep request text in structured arguments or properly quoted files, never interpolated shell code.

## Observe automatic review

Read existing review state and applicable automatic-review settings. Rulesets must be active and match the target branch; inspect their definitions, including review-on-push, draft handling, and exclusions. Personal or organization settings may also trigger automatic review, so absence of a repository rule alone does not prove it is disabled. Do not change rulesets, reviewer assignments, or subscriptions.

Never manually request or re-request a review through any tool, API, comment, or delegate. Observe automatic reviews after PR creation and real code pushes; honor an explicit user instruction not to wait for optional AI review, recording its absence without claiming approval. Mandatory GitHub approvals and protections still apply; never create an empty commit or no-op push as a trigger. If required automatic review cannot run, report the actual dependency and retain the merge gate. Use returned evidence for quota, size, permissions, or availability limits rather than a remembered product cap. A pending review remains pending.

Copilot feedback does not by itself satisfy required human approvals; check the actual repository configuration and review state. An earlier review does not cover a newer head. A quota refusal or skipped-review message does not count even if attached to the correct commit.

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

- [Configuring automatic Copilot review](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review)
- [GitHub CLI merge and head matching](https://cli.github.com/manual/gh_pr_merge)
- [GitHub CLI check status](https://cli.github.com/manual/gh_pr_checks)
