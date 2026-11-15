# Claude Code session ship gate

Claude Code only. Other hosts have no Stop hook; skip this file.

The skill's session-scoped Stop hook reads only this session's ship gate. Use the session ID supplied by SKILL.md (`CLAUDE_SESSION_ID`), require `[A-Za-z0-9][A-Za-z0-9_-]{0,127}`, and construct `~/.claude/slam-gates/<session-id>`. If the ID is missing or still literal substitution text, skip arming the gate. Arm it after the repository and PR identities are verified. The gate is JSON with `repo` and a positive `pr` number; optional `root`, `branch`, `base`, and `head` fields preserve resume context. Use a JSON serializer and restrictive file permissions. Never overwrite another run's gate or follow a symlink. Python 3 and authenticated `gh` are required for the hook; missing capabilities do not waive shipping gates.

| PR state | Hook result |
| --- | --- |
| `stop_hook_active: true` | Allow stopping without contacting GitHub or deleting the gate; this breaks recursive continuation. It does not prove completion. |
| `OPEN` | Continue remaining review, checks, and merge phases. |
| `MERGED`, gate present | Verify merge evidence, finish cleanup and the final report. |
| `CLOSED` | Remove this session's gate and allow stopping; closed is not shipped. |
| Missing/invalid gate, unknown state, or failed GitHub access | Allow stopping and retain any gate; report the unverified state. |

Remove only this session's gate when the final outcome is ready, when no authorized path remains, or when the user asks to stop or pause. Removal is best-effort: a denied or failed deletion never authorizes another continuation or prevents the user from stopping. Preserve the gate as unfinished resume evidence when it remains. User instructions and hard rules always win. Report unfinished phases and what would enable resumption; never claim a merge merely to release the gate. Abandonment requires the user's explicit decision. Preserve any user-created goal; do not replace or clear it.

Poll review and checks with individual blocking waits of at most 60 seconds. Inspect changed evidence before continuing. The hook checks GitHub with a 15-second timeout and allows at most one continuation per stop cycle; it is a continuation aid, not a durable background scheduler or a completion signal. Repeated `stop_hook_active` events allow stopping while retaining the gate and do not prove success. Respect the host's continuation limits and interruptions; if execution ends, preserve captured identities and report the actual remaining gates when resuming.

## Arm

After verifying the PR identity, use the validated gate path. Write a JSON object with `repo` set to `SLAM_REPO` and positive integer `pr` set to `SLAM_PR`; record `root`, `branch`, `base`, and `head` from the captured run as resume context. Use a JSON serializer or structured file edit, never interpolate repository data into shell/JSON code. Create the gate directory if needed; refuse a symlink gate. If resuming an existing gate, verify its repository and PR before replacing it. Refresh its head after each verified push. Missing gate support does not prevent authorized shipping.

## Release

Release only this session's gate after recording completed cleanup/retention, a concrete blocker, or an explicit user stop/pause/abandonment. Removing the gate is not merge evidence.
