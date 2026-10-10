## 0 — Move protected-branch work safely

If already on an unprotected feature branch, continue. If on a protected branch, compare it with its own remote ref and inspect staged, unstaged, untracked, and local-only changes.

- Clean and no local-only work: inspect existing PR context before reporting there is nothing to ship.
- Uncommitted work only: create a new feature branch with a name derived from the diff and project convention; carry the working tree across.
- Local commits strictly ahead: create a feature branch at the current commit, preserving the commits and dirty tree. Leave the protected ref intact and report its retention. Rewinding it is a separate operation requiring explicit authorization; it is not necessary to ship the feature branch.
- Diverged protected history, unknown upstream, or unrelated work with unclear scope: report the specific decision needed before moving anything.

Capture the feature name as `SLAM_BRANCH` and refuse protected names again.
