## 2 — Inspect, stage, verify, commit

Read both staged and unstaged diffs and inspect candidate untracked files. Select only scoped paths/hunks; use `git add -- <paths>` when scope is known, and ask only when ownership/scope is ambiguous. Do not commit unrelated pre-staged work.

For git-crypt-managed paths, validate the actual staged blobs after staging and before every commit. Use NUL-delimited changed-file lists, skip deletions, query staged attributes, and confirm the ciphertext header for managed blobs. Plaintext in a managed staged blob is a stop. Do not print contents or "fix" leaked history by rewriting it.

Run the project's relevant tests/builds and inspect `git diff --check`. Write a concise commit subject matching project convention (conventional commits when used); include the reason in a body when useful. Use a properly quoted body file or structured input. No attribution footer. After any base merge or review fix, repeat affected checks before pushing.

A clean tree may still contain unpushed commits or an existing PR. Continue accordingly. Don't manufacture a commit just to follow the phase list.
