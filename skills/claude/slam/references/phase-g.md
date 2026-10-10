## Phase G — Set the ship goal (before Phase 0)

`/slam` is a long unattended pipeline with two unavoidable waits — the AI review and CI — and a turn can end at either one with the PR still open. Claude Code's `/goal` exists for exactly that: it registers a Stop hook that blocks the session from stopping until a separate evaluator confirms the condition **from the conversation**, and clears itself once it does. Run `/slam` under a goal and the run survives to the merge instead of trailing off at a natural turn boundary.

**Set it first, before Phase 0 touches the tree.**

Propose it with the `ProposeGoal` tool — the user approves with one keypress. If that tool is unavailable (non-interactive or agent context, plan mode, or model-proposed goals disabled in settings), print the `/goal` line for the user to paste and **carry on either way**. A missing goal is a missing safety net, never a reason not to ship.

**The condition** — name the branch and base and state the completion evidence:

```
/goal the PR for <branch> reports MERGED into <base> with the merge commit SHA reported, and the feature branch is deleted or its retention explained
```

Keep it under ~500 characters so the whole thing fits the approval dialog (a typed `/goal` allows 4000).

**A halt is not completion.** Resolve fixable blockers and continue. If no authorized path remains, stop shipping actions and report the unfinished goal and what would enable resumption. Follow the host's supported goal lifecycle; never claim a merge occurred merely to satisfy an evaluator. Abandonment requires an explicit user decision, with the decision-maker and reason recorded.

**The goal never outranks a hard rule.** If continuing means a rebase, a force-push, an `--admin` merge, or deleting a protected branch, the rule wins: report and stop. A Stop hook cannot authorize what a hard rule forbids.

**Use it on the waits.** Poll for the AI review (Phase 5) and CI (Phase 6) as background work — goal evaluation defers while background work runs and a check-in is injected instead, which is the "keep waiting" behavior those phases want.

**Clearing.** The goal auto-clears when the evaluator confirms it met. It does not clear on a halt, and nothing in this skill can clear it — if you stopped early and a goal is still active, say so in the final report and tell the user to run `/goal clear`.

---
