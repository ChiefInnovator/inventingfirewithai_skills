# Finish: merge, cleanup, report

## 6 — Verify gates, merge, and sync

Immediately before merging, re-read the PR's base/head identities, `headRefOid`, mergeability, required current-head completed review (or the optional absence/user instruction not to wait recorded in Phase 5), unresolved threads, applicable policy, and latest checks for `SLAM_HEAD`. If the head changed, return to inspection and automatic review. Resolve base conflicts on the feature branch as in Phase 1, then push and repeat the head-specific gates. Investigate unknown state instead of treating it as clean. Address actionable human change requests and wait for reviewer action; never dismiss or override the human review gate. If only external action remains, report that dependency and wait or stop according to host capabilities.

Inspect all checks and identify which are required by policy. `gh pr checks "$SLAM_PR" --repo "$SLAM_REPO" --required --json name,state,bucket,link` can summarize required checks; verify the PR head again after reading results. Exit code 8 means checks are pending, not failed. For failures, inspect logs, fix in-scope causes, verify, push, and recheck the new head. A previous successful attempt does not clear a later pending/failed attempt. Empty checks mean "no checks configured" only after policy and API access are verified; never call that "CI passed." Missing or inaccessible required evidence keeps the gate closed.

Use the supported CLI's head-match guard and the captured repository/PR:

```bash
gh pr merge "$SLAM_PR" --repo "$SLAM_REPO" --merge --match-head-commit "$SLAM_HEAD"
```

Use `--squash` instead of `--merge` only if requested. Do not use `--delete-branch` here. Honor required merge queues; a successful enqueue/auto-merge request is not a merge. Wait until GitHub reports `state=MERGED`, a real merge timestamp, and merge commit SHA, with the captured base, head repository/branch, and `headRefOid=SLAM_HEAD`. Re-query after ambiguous responses before retrying. Capture the verified full merge commit SHA as `SLAM_MERGE_SHA` in persistent task state alongside `SLAM_PR`, `SLAM_HEAD`, base, head repository/branch, and merge timestamp. Restore these captured values before cleanup; independent tool calls do not preserve shell variables. Never substitute a current base tip for the captured merge commit.

Fetch successfully. Preserve dirty trees and branches checked out in other worktrees. If safe, switch to the local base and fast-forward it with `git merge --ff-only origin/<base>`; if absent, create a tracking base. Never reset a divergent/ahead local base to sync it. Report any local sync blocker separately from an already successful remote merge.

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

Remove worktrees only when the user requests that cleanup. Require merged/pushed work, a clean tree, and no lock or active use; preserve base and dedicated protected worktrees. Use normal `git worktree remove`, never `--force`. Inspect ignored files explicitly; a clean `git status` does not establish that a tree is disposable. Unique uncommitted, untracked, or ignored work blocks removal. Under an explicit cleanup request, preserve unique ignored evidence, local settings, and state in a private archive outside Git, recording original paths and checksums and verifying the archived bytes before removal; discard only clearly regenerable caches. Never upload the archive or print credential contents. A duplicated skill edit may be reconciled only after its exact bytes are recorded in the merged canonical source and no other work exists in that tree. Preserve every exception and report retained paths/reasons. Prune only stale worktree metadata after successful removal.

## Final report

State repository, base selection, commit SHA(s), PR URL, actual AI review outcome and comment dispositions, checks at merge time, merge SHA, local base sync, and local/remote branch deletion or retention. State skipped work and blockers plainly. If halted, name the phase, evidence, attempted remedies, remaining work, and required decision or external change. Distinguish completed, blocked, and explicitly abandoned outcomes; for abandonment, record the decision-maker and reason. Do not call a pending queue, failed gate, or unresolved goal "done."

A verified merge establishes source delivery. If deployment or live acceptance is part of the user's request, report its evidence and remaining gates separately; local checks and CI alone do not establish it.

**Claude Code only:** release the session gate as [claude-gate.md](claude-gate.md) describes.
