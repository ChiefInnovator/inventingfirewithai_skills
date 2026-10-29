## 0 — Move protected-branch work safely

If already on an unprotected feature branch, continue. If on a protected branch, compare it with its own remote ref and inspect staged, unstaged, untracked, and local-only changes.

- Clean and no local-only work: inspect existing PR context before reporting there is nothing to ship.
- Uncommitted work only: create a new feature branch with a name derived from the diff and project convention; carry the working tree across.
- Local commits, including divergent history: create a feature branch at the current commit, preserving the commits and dirty tree. Leave the protected ref intact and report its retention. Merge remote changes into the feature branch during preflight; never rewind the protected ref as part of shipping.
- Unknown remote history or unrelated work with unclear scope: resolve repository identity or scope before moving anything.

Capture the feature name as `SLAM_BRANCH` and refuse protected names again.
