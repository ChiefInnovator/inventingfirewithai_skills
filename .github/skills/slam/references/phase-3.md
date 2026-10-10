## 3 — Push and capture the head

Push the captured feature branch to `origin`. If rejected, fetch and inspect both histories. Never force or blindly retry. A remote-only fast-forward can be incorporated when safe; divergent local/remote history requires the user's direction under the no-rebase rule.

Verify the live remote branch SHA equals the intended local commit using `git ls-remote`. Capture it as `SLAM_HEAD`. Refresh this value only after an intentional, verified change; unexpected advancement sends the run back to inspection and review.
