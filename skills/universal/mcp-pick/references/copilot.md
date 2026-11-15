# GitHub Copilot

Identify the active host first: CLI, VS Code, or a remote/cloud agent. Default to the current workspace or a new CLI session, never global changes.

**Inventory:** in the CLI, run `python3 <skill-dir>/scripts/copilot_inventory.py` from the project directory. It wraps `copilot mcp list --json`, prints only server names and enablement, and fails closed on errors or unknown schemas. In VS Code, use supported MCP inventory tools or **MCP: List Servers**. An installed connector is not necessarily connected, and a configured server is not necessarily running.

**Menu:** every server in a compact numbered list with **On**, **Off**, or **Unknown**, a short project-specific reason, and an arrow beside recommendations. Re-read the inventory before applying; if names or states changed, reconcile with the user first.

## Copilot CLI

Check the installed CLI help before using these commands. The CLI supports different operations from editor workspace settings:

- For project/session scope, prepare a launch command using `copilot -C <project>` and repeated `--disable-mcp-server <name>` for discovered servers omitted from the selection. Add `--enable-mcp-server <name>` for selected servers that are currently disabled. Quote paths and names safely as individual arguments; do not interpolate them as executable shell text.
- Present the command for the next session, or launch it only when the environment supports an interactive session and the user requested that. Preparing a command does not modify the current session or persist a project preference. Never run a blocking nested agent merely to claim completion.
- Use supported controls in an already-running session only when their documented scope matches the request. If the CLI cannot persist workspace-only enablement, say so; do not edit an undocumented settings key.
- `copilot mcp enable <name>` and `copilot mcp disable <name>` persist CLI configuration. Use them only for an explicitly requested persistent change after confirming the installed version's target scope. A request to trim this project does not authorize global changes.
- Never remove a server definition, edit another client's configuration, or rewrite credentials to implement enable/disable. Built-in or forwarded servers may have separate controls; inspect support and disclose any server that cannot be controlled in the selected scope.

## VS Code

Use **MCP: List Servers** and its enable/disable actions with **workspace** scope. Enablement is stored separately from `mcp.json`; do not invent an `enabled` property or edit private state databases. If no authorized UI/tool access exists, give the exact remaining editor step and report the selection as pending. A file edit alone is not proof the server was disabled. Per-tool selection and disabling a whole server are different operations.

## Remote/cloud agents

Inspect the host's documented repository MCP settings and available management tools. Local CLI or editor configuration is not evidence of remote enablement. Apply only supported, authorized controls; otherwise report the chosen set and the missing capability without claiming a change.

## Report

Re-read state through the same host after actual changes. Distinguish **applied**, **launch command prepared**, and **pending user/editor action**, and say whether a new session is needed.
