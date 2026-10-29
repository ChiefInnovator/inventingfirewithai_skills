## 3 — Push and capture the head

Push the captured feature branch to `origin` with an explicit refspec (`refs/heads/<feature>:refs/heads/<feature>`); do not rely on push defaults. If rejected, fetch and inspect both histories. Never force or blindly retry. Incorporate a remote-only fast-forward when safe; merge divergent history on the feature branch and resolve routine conflicts as in Phase 1. Inspect newly introduced changes and repeat affected checks before retrying.

Verify the live remote branch SHA equals the intended local commit using `git ls-remote`. Capture it as `SLAM_HEAD`. Refresh this value only after an intentional, verified change; unexpected advancement sends the run back to inspection and review.
