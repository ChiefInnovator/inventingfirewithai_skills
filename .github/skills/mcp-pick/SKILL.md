---
name: mcp-pick
description: Choose the MCP servers GitHub Copilot needs for the current project using a numbered chat menu. Use to reduce MCP tool context in Copilot CLI or VS Code while preserving unrelated settings and respecting session, workspace, and global scope.
---

# MCP Picker

Use `/mcp-pick` in GitHub Copilot. Follow applicable repository instructions and host permissions. Reading or installing this skill does not change MCP settings.

## Inspect and propose

1. Identify the active Copilot host: CLI, VS Code, or a remote/cloud agent. Default to the current workspace or a new CLI session, not global changes. Ask only if the host or intended scope cannot be established.
2. Read the README and relevant package/build manifests to understand which services this project needs. Inspect the host's actual MCP inventory. An installed connector is not necessarily connected, and a configured server is not necessarily running.
3. In CLI, run `python3 <skill-dir>/scripts/inventory.py` from the project directory. It uses `copilot mcp list --json` and emits only server names and enablement; commands, arguments, environment values, and URLs are omitted. Errors and unknown schemas fail closed. In VS Code, use supported MCP inventory tools or **MCP: List Servers**. Do not dump raw configurations containing credentials.
4. Present every server in a compact numbered chat list with **On**, **Off**, or **Unknown**, a short project-specific reason, and an arrow beside recommendations. Keep the reviewed names and order. Ask for numbers to keep, `recommended`, `all`, or `none`. Do not change anything before the selection; ambiguous names or numbers need clarification.
5. Re-read the inventory before applying the selection. If names or states changed, reconcile with the user before changing settings. Map numbers to exact server names, never substring matches. Preserve unknown or undiscovered settings.

## Apply through the actual host

### Copilot CLI

Check the installed CLI help before using these commands. The CLI supports different operations from editor workspace settings:

- For project/session scope, prepare a launch command using `copilot -C <project>` and repeated `--disable-mcp-server <name>` for discovered servers omitted from the selection. Add `--enable-mcp-server <name>` for selected servers that are currently disabled. Quote paths and names safely as individual arguments; do not interpolate them as executable shell text.
- Present the command for the next session, or launch it only when the environment supports an interactive session and the user requested that. Preparing a command does not modify the current session or persist a project preference. Never run a blocking nested agent merely to claim completion.
- Use supported controls in an already-running session only when their documented scope matches the request. If the CLI cannot persist workspace-only enablement, say so; do not edit an undocumented settings key.
- `copilot mcp enable <name>` and `copilot mcp disable <name>` persist CLI configuration. Use them only for an explicitly requested persistent change after confirming the installed version's target scope. A request to trim this project does not authorize global changes.
- Never remove a server definition, edit another client's configuration, or rewrite credentials to implement enable/disable. Built-in or forwarded servers may have separate controls; inspect support and disclose any server that cannot be controlled in the selected scope.

### VS Code

Use **MCP: List Servers** and its enable/disable actions with **workspace** scope. Enablement is stored separately from `mcp.json`; do not invent an `enabled` property or edit private state databases. If no authorized UI/tool access exists, give the exact remaining editor step and report the selection as pending. A file edit alone is not proof the server was disabled. Per-tool selection and disabling a whole server are different operations.

### Remote/cloud agents

Inspect the host's documented repository MCP settings and available management tools. Local CLI or editor configuration is not evidence of remote enablement. Apply only supported, authorized controls; otherwise report the chosen set and the missing capability without claiming a change.

## Verify and report

Re-read state through the same host after actual changes. Report selected servers, disabled servers, exact scope, and whether a new session is needed. Distinguish **applied**, **launch command prepared**, and **pending user/editor action**. Configuration enablement, authentication, startup, and availability in the current tool context are separate results.
