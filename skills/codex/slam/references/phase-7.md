## 7 — Verify cleanup before deletion

Skip cleanup if the user requested retention. Otherwise re-query the PR and require its merged state, timestamp, merge SHA, base, head repository/branch, and `headRefOid` to match the captured run. Refuse cross-repository deletion. Confirm every `origin` fetch/push URL still identifies the captured repository.

Refresh applicable rulesets and legacy branch protection. Protect the base, remote default, `main`, `master`, `develop`, and branches restricted by protection policy. Inspect the actual rules: an automatic-review-only rule does not prohibit deletion, even when the branch API reports `protected: true`. Deletion/update restrictions, required-PR policy, or unknown policy mean retain. Never change protections to permit cleanup.

Fetch with pruning immediately before the guard. Resolve `SLAM_SKILL_DIR` to the installed skill directory. Restore the captured `SLAM_HEAD` and `SLAM_MERGE_SHA`; do not infer them from the current checkout. Pass every additional protected name with repeated `--protected` options:

```bash
python3 "$SLAM_SKILL_DIR/scripts/check_cleanup.py" \
  --repo-dir "$SLAM_ROOT" --base "$SLAM_BASE" --branch "$SLAM_BRANCH" \
  --head "$SLAM_HEAD" --merge-commit "$SLAM_MERGE_SHA" \
  --protected "$SLAM_DEFAULT"
```

The read-only guard requires a clean checkout of the synchronized base (or a detached checkout at that exact live base commit), exact local/live remote feature heads, merged ancestry, and no worktree using the feature. It does not verify GitHub PR identity or policy and never grants deletion authority. Refusal means preserve the branch and investigate; never escalate to force deletion. Squash merges may fail ancestry checks and require retention.

For an authorized remote deletion, use the bundled guarded helper with the exact captured origin URL:

```bash
python3 "$SLAM_SKILL_DIR/scripts/delete_remote_branch.py" \
  --repo-dir "$SLAM_ROOT" --base "$SLAM_BASE" --branch "$SLAM_BRANCH" \
  --head "$SLAM_HEAD" --merge-commit "$SLAM_MERGE_SHA" \
  --expected-origin "$SLAM_ORIGIN" --protected "$SLAM_DEFAULT"
```

It repeats the containment check and runs an ordinary non-force push with a temporary pre-push guard. The guard verifies the server-advertised deletion head, preserves existing hooks, and lets Git reject a racing ref update. It changes no persistent Git configuration. Do not replace it with a bare delete, force/lease flag, or skipped hook. A missing remote is already removed. A failure or a newly present ref is a retention result, not permission to retry blindly.

After verification, delete the matching local feature with `git branch -d -- <feature>` if it exists, then verify both refs are absent. Never delete another run's branch merely because the current checkout changed. A separate explicit cleanup request may cover additional branches, each with its own captured merge/ancestry and policy evidence.

Remove worktrees only when the user requests that cleanup. Require merged/pushed work, a clean tree, and no lock or active use; preserve base and dedicated protected worktrees. Use normal `git worktree remove`, never `--force`. Unique uncommitted or untracked work blocks removal. A duplicated skill edit may be reconciled only after its exact bytes are recorded in the merged canonical source and no other work exists in that tree. Preserve every exception and report retained paths/reasons. Prune only stale worktree metadata after successful removal.
