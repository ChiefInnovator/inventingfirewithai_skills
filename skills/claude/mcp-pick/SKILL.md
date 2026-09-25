---
name: mcp-pick
description: Choose which MCP servers stay enabled in the current repo and disable the rest. Use when the user wants to trim MCP servers/connectors for a project, reduce MCP tool context, or asks which MCPs a repo actually needs.
---

# Pick the MCP servers for this repo

You do the whole thing in the conversation. The user answers in chat. Never make them open a terminal, and never use `AskUserQuestion` — its tabbed groups hide the submit button below the fold.

Resolve `scripts/mcp-pick.sh` relative to this skill directory and use its absolute path as `<helper>` in the commands below. Run it from the project directory.

## 1. Read the current state

```bash
bash <helper> list
```

`[x]` = enabled here, `[ ]` = disabled here. Writes nothing.

## 2. Work out what the repo is

Read `README.md`, plus whichever exist: `package.json`, `pyproject.toml`, `*.csproj`, `Package.swift`, `pubspec.yaml`, `.github/workflows/`. One or two tool calls, not a survey. You need enough to justify each keep/drop, not a full architecture review.

## 3. Present the choice in chat

Print a numbered list — every server, in the order `list` returned them, with `[x]`/`[ ]` preserved. After each, half a line on why it does or doesn't belong in *this* repo. Mark your picks with `←`.

Then ask, in one line: reply with the numbers to keep, or `recommended`, or `none`.

Keep the whole thing scannable. This is a menu, not an essay — no headers, no table.

## 4. Write the answer

Map their reply back to full server names and run:

```bash
bash <helper> keep "claude.ai HubSpot" "claude.ai Microsoft Learn"
```

Every discovered server not named is disabled for this repo. Existing disabled settings for undiscovered servers are preserved. Other modes: `all`, `none`, `list`. Do not run `ask` — it needs a TTY the Bash tool doesn't have, so it would silently keep every current value.

If the user's reply is ambiguous (a name that matches two servers, a number out of range), say which part was unclear and ask only about that. Don't re-print the menu.

## 5. Report

Two lines from the script's own output — what stayed, what went. Then: takes effect in a **new session**, since this one already loaded its tool definitions.

Don't run `claude mcp list` to verify. It lists configured servers, not per-repo enablement; use `bash <helper> list`.

## Notes

- State lives in `~/.claude.json` → `projects["<absolute cwd>"].disabledMcpServers`, the same store the `/mcp` panel writes to. It covers claude.ai connectors, plugin servers (`plugin:<plugin>:<server>`), and user/local servers.
- Unrelated to `enabledMcpjsonServers` / `disabledMcpjsonServers`, which only apply to project `.mcp.json` servers.
- The script backs up `~/.claude.json` before every write and only touches the current cwd's entry. Never use `claude mcp remove` — that deletes the server for every repo.
