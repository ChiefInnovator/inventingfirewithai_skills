## 7 — Verify cleanup before deletion

Skip cleanup if the user requested retention. Otherwise re-query the PR and require its merged state, timestamp, merge SHA, base, head repository, head branch, and `headRefOid` to match the captured run. Refuse cross-repository deletion. Confirm `origin` still identifies the same repository. Refresh GitHub branch protections/rules; protected or unknown protection state means retain. A confirmed missing remote branch is already removed, not a failed merge.

Fetch with pruning immediately before the following guard. Resolve `SLAM_SKILL_DIR` to this skill's actual directory. Pass the remote default and all extra protected branch names with repeated `--protected` options:

```bash
python3 "$SLAM_SKILL_DIR/scripts/check_cleanup.py" \
  --repo-dir "$SLAM_ROOT" --base "$SLAM_BASE" --branch "$SLAM_BRANCH" \
  --head "$SLAM_HEAD" --merge-commit "$SLAM_MERGE_SHA" \
  --protected "$SLAM_DEFAULT"
```

This read-only helper fails closed on invalid/protected names, a dirty or wrong checkout, stale base refs, unmerged commits, newer local/remote feature commits, or a feature checked out in another worktree. It reads live remote refs and reports whether local and remote deletion candidates exist. It does not check GitHub policy/PR state or grant deletion authority; the preceding checks remain required. Do not proceed on a nonzero exit.

The guard is a point-in-time observation, not a lock against concurrent writers. Retain the remote feature by default: an ordinary remote delete can remove work pushed after the guard ran. Remote deletion requires repository-supported exclusive control that prevents updates between verification and deletion; do not infer exclusivity from a quiet branch or use force/force-with-lease to bypass the no-force rule. If that protection is unavailable, report remote retention. After all checks, the matching local branch may be deleted with `git branch -d -- <feature>` if it exists. Recheck changed state after any delay. Never upgrade a refusal to force deletion. Squash merges may fail ancestry checks; retain the branch and explain why. Verify both refs are absent afterwards, or report partial cleanup and retention precisely. Do not remove worktrees automatically.
