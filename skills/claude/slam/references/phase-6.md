## 6 — Verify gates, merge, and sync

Immediately before merging, re-read the PR's base/head identities, `headRefOid`, mergeability, required current-head completed review (or the optional absence/user instruction not to wait recorded in Phase 5), unresolved threads, applicable policy, and latest checks for `SLAM_HEAD`. If the head changed, return to inspection and automatic review. Resolve base conflicts on the feature branch as in Phase 1, then push and repeat the head-specific gates. Investigate unknown state instead of treating it as clean. Address actionable human change requests and wait for reviewer action; never request re-review, dismiss, or override the human review gate. If only external action remains, report that dependency and wait or stop according to host capabilities.

Inspect all checks and identify which are required by policy. `gh pr checks "$SLAM_PR" --repo "$SLAM_REPO" --required --json name,state,bucket,link` can summarize required checks; verify the PR head again after reading results. Exit code 8 means checks are pending, not failed. For failures, inspect logs, fix in-scope causes, verify, push, and recheck the new head. A previous successful attempt does not clear a later pending/failed attempt. Empty checks mean "no checks configured" only after policy and API access are verified; never call that "CI passed." Missing or inaccessible required evidence keeps the gate closed.

Use the supported CLI's head-match guard and the captured repository/PR:

```bash
gh pr merge "$SLAM_PR" --repo "$SLAM_REPO" --merge --match-head-commit "$SLAM_HEAD"
```

Use `--squash` instead of `--merge` only if requested. Do not use `--delete-branch` here. Honor required merge queues; a successful enqueue/auto-merge request is not a merge. Wait until GitHub reports `state=MERGED`, a real merge timestamp, and merge commit SHA, with the captured base, head repository/branch, and `headRefOid=SLAM_HEAD`. Re-query after ambiguous responses before retrying. Capture the verified full merge commit SHA as `SLAM_MERGE_SHA` in persistent task state alongside `SLAM_PR`, `SLAM_HEAD`, base, head repository/branch, and merge timestamp. Restore these captured values before cleanup; independent tool calls do not preserve shell variables. Never substitute a current base tip for the captured merge commit.

Fetch successfully. Preserve dirty trees and branches checked out in other worktrees. If safe, switch to the local base and fast-forward it with `git merge --ff-only origin/<base>`; if absent, create a tracking base. Never reset a divergent/ahead local base to sync it. Report any local sync blocker separately from an already successful remote merge.
