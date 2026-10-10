---
name: slam
description: Ship the current branch end-to-end under a session /goal that keeps the run alive to the merge — preflight checks, commit, push, ensure a PR against the repo's base branch (develop if it exists, else main), request and address GitHub Copilot / AI review comments, merge, then delete the merged branch. Resolves in-scope blockers and stops when no authorized path remains.
user_invocable: true
arguments: message-or-scope
---

# /slam Skill

You take the current branch from "work in the tree" to "merged into the repo's base branch", unattended where it's safe and stopping where it isn't.

The user passed: `$ARGUMENTS` (optional — a commit message or subject hint; derive one from the diff if empty).

This skill is repo-agnostic. It detects the base branch, the review bot, and the repo's protection rules rather than assuming them. Follow applicable repository instructions, including `AGENTS.md`, under the host's instruction hierarchy.

**Hard rules, no exceptions:**

- **NEVER REBASE.** Do not run `git rebase`, `git pull` in any form, GitHub's "Rebase and merge", or delegate a rebase to another agent or tool. Git configuration can make a pull rebase implicitly. Fetch explicitly, then use `git merge --ff-only` for synchronization; merge the base into a feature branch only within existing authorization. Stop and ask before handling divergence or resolving conflicts. Never change Git configuration to work around this rule.
- **Never `--admin`-merge**, never force-push.
- **Never delete a protected branch** — `$BASE`, `main`, `master`, or `develop` — under any circumstance. Not as cleanup, not to "recreate it clean", not because a command suggested it. Some repos also have server-side rulesets that would reject it, but **never rely on the server to stop you.** Refuse locally first.
- **Delete the feature branch only after the merge is verified** (Phase 7). Invoking this skill is the approval for that one deletion — the branch this run just merged, once GitHub reports it `MERGED` — and it extends to nothing else.
- **Never add `Co-Authored-By` or AI-attribution lines** to commits.
- Merge with a **merge commit** (`gh pr merge --merge`). Not `--rebase`. Use `--squash` only if the user explicitly asks.

Work the phases in order. Report a one-line status per phase as you go.

Resolve blockers within the authorized scope: inspect evidence, fix valid in-scope defects or review findings, run the affected checks, and resume the shipping phases. Retry transient failures when evidence supports a retry. After repeated failures, change the approach rather than repeating the same action indefinitely. A failed gate prevents merging; it does not by itself end the run. Stop only when no safe, authorized path forward remains, or an explicit stop rule applies. Report what was tried, the remaining obstacle, and the access, decision, or external change needed to resume. Never broaden scope, bypass a gate, or resolve conflicts/divergence without the required user approval.

---

## Required phase instructions

Read only the current phase reference before performing its actions; do not preload every reference. Start with G before touching the tree. Work in order; when resuming, verify the captured repository, branch, base, PR, and head before choosing remaining phases. Preserve completed evidence rather than repeating mutations. Read cleanup guards before any deletion.

- [Phase G — Set the ship goal (before Phase 0)](references/phase-g.md)
- [Phase R — Resolve the repo's shape](references/phase-r.md)
- [Phase 0 — Get the work onto a feature branch](references/phase-0.md)
- [Phase 1 — Preflight](references/phase-1.md)
- [Phase 2 — Inspect and commit](references/phase-2.md)
- [Phase 3 — Push](references/phase-3.md)
- [Phase 4 — Ensure a PR exists](references/phase-4.md)
- [Phase 5 — Review and address AI comments](references/phase-5.md)
- [Phase 6 — Merge](references/phase-6.md)
- [Phase 7 — Clean up the branch](references/phase-7.md)
- [Final report](references/phase-report.md)
