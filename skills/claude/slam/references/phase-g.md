## Phase G — Keep the run alive to the merge (before Phase 0)

`/slam` is a long unattended pipeline with two unavoidable waits — the AI review and CI — and a turn can end at either one with the PR still open. Claude Code gives skills no way to set a `/goal`, so slam carries its own **ship gate**: a `Stop` hook in this skill's frontmatter, registered the moment `/slam` is invoked and kept for the rest of the session.

**Do not print a `/goal` line for the user to paste.** The gate replaces it. If the user already set a `/goal`, leave it alone — never replace or clear it.

**How the gate works.** In Phase 4, once the PR number is known, record it in this session's gate file (path in SKILL.md). From then on, whenever the session would stop, the hook asks GitHub for the PR's state:

| PR state | Hook result |
| --- | --- |
| `OPEN` | Blocks the stop and tells you to keep going. |
| `MERGED`, gate file still present | Blocks until Phase 7 cleanup and the final report are done. |
| `CLOSED`, or no gate file, or `gh` fails | Allows the stop (fails open). |

Remove the gate file as the last action of the final report — completed, blocked, or abandoned. Nothing else releases it short of the PR leaving `OPEN`.

**A halt is not completion.** Resolve fixable blockers and continue. Stop only when no authorized path remains or the next step is a decision only the user can make; then remove the gate file and report the unfinished run and what would enable resumption. Never claim a merge occurred to get past the gate. Abandonment requires an explicit user decision, with the decision-maker and reason recorded.

**The gate never outranks a hard rule.** If continuing means a rebase, a force-push, an `--admin` merge, or deleting a protected branch, the rule wins: remove the gate file, report, and stop. A Stop hook cannot authorize what a hard rule forbids.

**Waiting under the gate.** The hook cannot see background work, and ending the turn while the PR is open only brings you straight back. Poll the AI review (Phase 5) and CI (Phase 6) with bounded foreground waits (a few minutes per call), re-checking until the state changes.

---
