## 4 — Ensure the correct PR

Query PRs explicitly by captured repository and head branch, including closed state when resuming. Distinguish "no PR" from an API/authentication error. If multiple PRs match, determine the intended one before acting. Reuse an open PR only when its head repository, branch, and base match. Retargeting, marking a draft ready, or creating a new PR for a previously closed one requires authority covering that action.

Otherwise create a PR against `SLAM_BASE`. Use a body file for multiline descriptions. Describe the concrete change, why, verification, and material limitations; don't add automatic Claude/OpenAI footers. Capture `SLAM_PR`, URL, head repository, and head SHA. Same-name fork branches are different targets; don't operate on or delete a fork's ref by assuming it is `origin`.

If the PR is already merged, verify the exact head, base, and merge commit before proceeding only to cleanup. A closed-unmerged PR is not success.
