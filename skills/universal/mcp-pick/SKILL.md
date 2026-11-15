---
name: mcp-pick
description: Choose which MCP servers and app integrations stay enabled for the current project and disable the rest. Use to trim MCP servers or connectors for a repo, reduce MCP tool context, or decide which MCPs a project actually needs.
---

# MCP Picker

Invoke as `/mcp-pick` (Claude Code, GitHub Copilot) or `$mcp-pick` (Codex). Work in the conversation in plain text: no terminal work for the user, no question widgets, HTML, or picker files.

1. Read the one reference for your host: [Claude Code](references/claude.md), [Codex](references/codex.md), or [GitHub Copilot](references/copilot.md). Change only that host's project-scoped enablement; never edit another client's configuration, remove a server definition, or expose credentials or raw configuration.
2. Run the host's read-only inventory.
3. Read `README.md` plus whichever manifests exist (`package.json`, `pyproject.toml`, `*.csproj`, `Package.swift`, `pubspec.yaml`, `.github/workflows/`) in one or two tool calls: enough to justify each keep or drop.
4. Show every discovered server in the host's menu format with your picks marked, then ask in one line for the numbers or names to keep, `recommended`, `all`, or `none`. An earlier selection or `recommended` needs no second confirmation. A blank reply is not a selection; for an ambiguous one, ask only about the unclear part.
5. Apply with the host's command, mapping numbers to exact names or IDs. Unkept discovered servers are disabled for this project; settings for undiscovered servers are preserved.
6. Report from the helper's output: kept, disabled, exact scope, and that a new session is needed. Never claim success after an error; enablement is not authentication or server health.
