## 6 — Verify gates, merge, and sync

Re-read the PR's base/head identities, `headRefOid`, mergeability, current reviews, unresolved threads, applicable policy, and checks for `SLAM_HEAD`. Investigate unknown state instead of treating it as clean. Wait for pending required checks. For failures, inspect logs, fix in-scope causes, verify, push, and recheck the new head. Address actionable human change requests and request re-review; never dismiss or override the human review gate. If only reviewer action remains, report the dependency and wait or stop according to host capabilities. Stop on an unresolved failure only after no authorized remedy remains. Empty configured checks mean "no checks configured," not "CI passed." A denied policy lookup is not absence of requirements.

Use the supported CLI's head-match guard and the captured repository/PR:

```bash
gh pr merge "$SLAM_PR" --repo "$SLAM_REPO" --merge --match-head-commit "$SLAM_HEAD"
```

Use `--squash` instead of `--merge` only if requested. Do not use `--delete-branch` here. Honor required merge queues; a successful enqueue/auto-merge request is not a merge. Wait until GitHub reports `state=MERGED`, a real merge timestamp, and merge commit SHA. Re-query after ambiguous responses before retrying.

Fetch successfully. Preserve dirty trees and branches checked out in other worktrees. If safe, switch to the local base and fast-forward it with `git merge --ff-only origin/<base>`; if absent, create a tracking base. Never reset a divergent/ahead local base to sync it. Report any local sync blocker separately from an already successful remote merge.
