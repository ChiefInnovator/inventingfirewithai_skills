# Prepare: resolve, branch, preflight, commit, push

## R — Resolve repository and base

Before changing the tree, verify Git and authenticated GitHub access. Inspect the working tree, current branch, all `origin` fetch/push URLs, and worktrees. Stop on detached HEAD. Resolve the GitHub host and owner/repository from `origin`, explicitly using that repository for all GitHub calls; don't rely on a CLI default that could point to a fork or another repository. Require every push destination to match the intended repository; stop on a mismatched or ambiguous push URL before publishing or deleting a ref.

If `origin` is missing, inspect the work and proposed outgoing history for secrets first, reporting paths and types without exposing credential values. Ask for any missing owner/name and authority before creating a private repository; public visibility requires an explicit request. Do not create or push a repository merely to complete migration/inspection of this skill. After authorized creation, restart repository resolution. Never interpret a failed fetch or denied API request as an empty repository or absent policy.

Fetch `origin` successfully with pruning. Resolve the base from explicit user/project instructions; otherwise use remote `develop` if present, then `main`, then the actual remote default. This is a selection policy, not proof of the repository's branching model. Confirm the selected remote ref exists.

Capture values in task state: `SLAM_ROOT`, `SLAM_HOST`, `SLAM_OWNER_REPO` (owner/repo), `SLAM_REPO` (host/owner/repo), `SLAM_ORIGIN`, `SLAM_BASE`, `SLAM_DEFAULT`, and protected branch names/rules. Inspect applicable GitHub protection/rulesets, including their target conditions. Recheck protections before merge and cleanup. Use `SLAM_BRANCH` only after Phase 0; never replace it with the current branch during cleanup. Shell variables do not persist between independent tool calls: restore captured values explicitly and verify repository identity before mutations.

## 0 — Move protected-branch work safely

If already on an unprotected feature branch, continue. If on a protected branch, compare it with its own remote ref and inspect staged, unstaged, untracked, and local-only changes.

- Clean and no local-only work: inspect existing PR context before reporting there is nothing to ship.
- Uncommitted work only: create a new feature branch with a name derived from the diff and project convention; carry the working tree across.
- Local commits, including divergent history: create a feature branch at the current commit, preserving the commits and dirty tree. Leave the protected ref intact and report its retention. Merge remote changes into the feature branch during preflight; never rewind the protected ref as part of shipping.
- Unknown remote history or unrelated work with unclear scope: resolve repository identity or scope before moving anything.

Capture the feature name as `SLAM_BRANCH` and refuse protected names again.

## 1 — Preflight and synchronize

Confirm repository identity, remote, branch, base, authorization, and scope. Inspect the entire outgoing diff and local-only history, not only uncommitted files. Check for secrets, generated/large files, deleted-path references, debug leftovers, and relevant project requirements. Redact secret values from outputs. A scan result is evidence, not a guarantee that no secrets exist.

Require common history with the base before any merge. Preserve dirty work by reviewing and committing the scoped changes in Phase 2 before synchronizing when necessary; never auto-stash unrelated work. Merge `origin/<base>` into the feature branch when needed, using a merge commit for divergent history. Resolve routine conflicts by inspecting both sides and their callers/tests, preserving their intended behavior. Do not blanket-select ours/theirs. Ask only for a genuine product/scope decision or an explicit project approval requirement. Run affected checks after the merge; stop on unrelated histories or a merge that cannot preserve the user's work.

## 2 — Inspect, stage, verify, commit

Read both staged and unstaged diffs and inspect candidate untracked files. Select only scoped paths/hunks; use `git add -- <paths>` when scope is known, and ask only when ownership/scope is ambiguous. Do not commit unrelated pre-staged work.

For git-crypt-managed paths, validate the actual staged blobs after staging and before every commit. Use NUL-delimited changed-file lists, skip deletions, query staged attributes, and confirm the ciphertext header for managed blobs. Plaintext in a managed staged blob is a stop. Do not print contents or "fix" leaked history by rewriting it.

Run the project's relevant tests/builds and inspect `git diff --check`. Write a concise commit subject matching project convention (conventional commits when used); include the reason in a body when useful. Use a properly quoted body file or structured input. No attribution footer. After any base merge or review fix, repeat affected checks before pushing.

A clean tree may still contain unpushed commits or an existing PR. Continue accordingly. Don't manufacture a commit just to follow the phase list.

## 3 — Push and capture the head

Push the captured feature branch to `origin` with an explicit refspec (`refs/heads/<feature>:refs/heads/<feature>`); do not rely on push defaults. If rejected, fetch and inspect both histories. Never force or blindly retry. Incorporate a remote-only fast-forward when safe; merge divergent history on the feature branch and resolve routine conflicts as in Phase 1. Inspect newly introduced changes and repeat affected checks before retrying.

Verify the live remote branch SHA equals the intended local commit using `git ls-remote`. Capture it as `SLAM_HEAD`. Refresh this value only after an intentional, verified change; unexpected advancement sends the run back to inspection and review.
