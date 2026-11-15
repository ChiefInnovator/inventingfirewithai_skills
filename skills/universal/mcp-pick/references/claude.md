# Claude Code

Resolve `scripts/claude_mcp_pick.sh` in this skill directory to an absolute path (`<helper>`) and run it from the project directory. Never use `AskUserQuestion` for the menu; its tabbed groups hide the submit button.

```bash
bash <helper> list                    # [x] enabled here, [ ] disabled here; writes no settings
bash <helper> keep "claude.ai HubSpot" "claude.ai Microsoft Learn"
```

**Menu:** every server in the order `list` returned, `[x]`/`[ ]` preserved, half a line each on why it does or doesn't belong in this repo, and `←` on your picks. No headers or tables.

**Apply:** `keep <names...>` disables every discovered server not named and preserves disabled entries for undiscovered servers. Other modes: `all`, `none`. Do not run `ask`; it needs a TTY and would silently keep every current value. `list` saves the discovered names so the write that follows within ten minutes skips the slow health-checked discovery; run `list` again if servers were added since.

**Verify** with `bash <helper> list`, not `claude mcp list`, which shows configured servers rather than per-repo enablement.

- State lives in `~/.claude.json` under `projects["<absolute cwd>"].disabledMcpServers`, the store the `/mcp` panel writes. It covers claude.ai connectors, plugin servers (`plugin:<plugin>:<server>`), and user/local servers. It is unrelated to `enabledMcpjsonServers`/`disabledMcpjsonServers`, which apply only to project `.mcp.json` servers.
- The script writes atomically, touches only the current directory's entry, skips the write when nothing changes, and keeps the three newest `~/.claude.json.bak.*` backups. Never use `claude mcp remove`; it deletes the server for every repo.
