## 1 — Preflight and synchronize

Confirm repository identity, remote, branch, base, authorization, and scope. Inspect the entire outgoing diff and local-only history, not only uncommitted files. Check for secrets, generated/large files, deleted-path references, debug leftovers, and relevant project requirements. Redact secret values from outputs. A scan result is evidence, not a guarantee that no secrets exist.

Require common history with the base before any merge. Preserve dirty work by reviewing and committing the scoped changes in Phase 2 before synchronizing when necessary. Merge `origin/<base>` into the feature branch only when project rules and existing authorization allow it; never rebase. If branches have diverged and approval is required by the user's rules, stop and ask. Conflicts stop this workflow with a concrete file list; don't silently choose one side or undo the user's work.
