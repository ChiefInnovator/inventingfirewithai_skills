---
name: mcp-pick
description: Choose which MCP servers and installed app integrations stay enabled for a Codex project. Use to trim project tool context, limit MCP servers per repository, or recommend which integrations a project needs.
---

# Pick this project's MCP servers and apps

Use the bundled helper to write only the selected project's `.codex/config.toml`. Keep the conversation-based selection workflow: do the inspection and commands yourself. Preserve an explicit keep/drop selection or authorization to use your recommendations from earlier in the conversation.

## Inspect and recommend

Resolve `scripts/mcp_pick.py` relative to this skill directory and run it by absolute path:

```sh
uv run --no-project --script <helper> list --json
```

The default target is the current Git root, or the current directory outside Git. Check the returned `project` before proceeding. Use `--project /absolute/project/path` when the user chose a different project or a subfolder. Match any explicit Codex profile with `--profile NAME` on every call.

The helper uses Codex's effective configuration and installed-plugin inventory, including apps declared by those plugins and existing app overrides. It does not scan the public app catalog or verify account connections. It prints only names, selector IDs, enabled preferences, blockers, and a review fingerprint; never dump raw configuration, MCP transport arguments, headers, credentials, or app-server responses.

Read enough project context to justify recommendations: `README.md`, relevant manifests, or the main specification if implementation has not started. Keep helpers the project actually needs, considering the user's workflow as well as its programming language.

If the user supplied a keep/drop selection or authorized `recommended`, apply it without another confirmation. For incremental changes such as “disable Calendar,” preserve the other reviewed settings. When the user invokes the picker without new changes, show the text chooser with their current settings marked; previous choices remain defaults, not a reason to skip the chooser.

### Text chooser

Present compact numbered lists directly in the response, grouped under bold On and Off labels, with On first. Sort each group alphabetically by the displayed name, case-insensitively; break identical-name ties by exact inventory ID. Number continuously across both groups after sorting, and preserve that displayed number-to-ID mapping for the reviewed selection. Include every discovered entry. Put blocked entries in Off with a short blocker note. Use the group label instead of repeating status on each row; omit table columns, redundant app/server suffixes, and per-entry explanations unless needed to distinguish entries or explain a blocker. Distinguish explicit servers from same-named plugin servers with concise labels. Put any useful recommendation in one short sentence after the list.

Ask the user to reply with the numbers or names to keep, `recommended`, `all`, or `none`. Keep the number-to-exact-ID mapping, project, scope, profile, and `inventory_version` from the reviewed inventory in the conversation. Use those exact IDs and that fingerprint for the guarded apply flow. A request such as “disable Calendar” changes only that setting and preserves the others. Resolve ambiguous duplicate names before writing. A blank response is not `none` or authorization to change settings.

Use text only. Do not generate HTML, visualizations, checkbox widgets, browser pages, or temporary picker files. Read the sanitized inventory directly from the helper output. When reopening, show current preferences again; do not silently reuse a previous selection as authorization for a new change.

## Apply the selection

Use the reviewed list's `inventory_version` as `--expect`. All entries in the chosen scope that are not named are disabled for this project:

```sh
uv run --no-project --script <helper> keep --expect <inventory_version> --project /absolute/project/path mcp:example app:connector_example
```

Modes: `list` reads only; `keep` enables the named IDs and disables the remaining listed entries; `none` disables every listed entry; `all` enables every unblocked listed entry and leaves blocked entries disabled. `--dry-run` previews changes. `--json` returns structured output. Use `--scope servers` on **all** calls when the user's scope is MCP servers without app integrations.

The helper rejects unknown selections, stale reviews, symlinked config targets, global config targets, ignored/untrusted project layers, and incomplete discovery. If the inventory changed, refresh it and reconcile the changes with the user's selection; do not silently approve new entries. It does not grant project trust, authenticate apps, enable a disabled parent plugin, or install anything. Explain the exact blocker when one of those separate actions is needed.

If app discovery is unavailable, disclose that limitation. A servers-only operation is appropriate when already requested or accepted; do not claim that it also trimmed app connectors. Integrations injected only into a running session, legacy account connections without installed-plugin metadata, or integrations supplied by a different Codex installation may not appear in this CLI inventory.

## Verify and report

The helper preserves TOML comments and unrelated settings, creates private backups of existing project configuration under the Codex home, writes atomically, and checks that Codex loads the resulting preferences. A failed verification restores the previous contents when no concurrent edit would be overwritten. Do not claim success after an error; inspect the reported project config and any backup as needed without exposing secrets.

After a successful write, run `list` again with the same project, scope, and profile. Report the enabled and disabled entries and the actual scope. Explain that a new Codex session in the trusted project loads the selection. Existing per-tool restrictions, approval policies, and managed requirements still apply; configuration read-back does not prove server health or authentication. Re-run the picker after installing additional integrations; this is a selection over the discovered inventory, not a wildcard policy for future servers.

## Codex-specific boundaries

- Explicit servers use `mcp_servers.<name>.enabled`.
- Plugin servers use `plugins.<plugin-id>.mcp_servers.<server>.enabled`. Keep the parent plugin's skills, hooks, and other capabilities unchanged. A same-named explicit server shadows a plugin server and is identified separately.
- App preferences use `apps.<app-id>.enabled`, with the actual ID returned by Codex. Enabled preferences do not establish authentication or availability through an enabled parent plugin.
- Do not call `codex mcp remove`, edit global enablement, remove plugins, or edit Claude configuration to accomplish project scoping. Never copy global server definitions or credentials into the project file.
- Do not disable built-in Codex tools or change trust/approval settings as a substitute for MCP selection.

The helper requires Python 3.11+, uv, and Codex CLI 0.153.4 or newer on PATH. Its TOML dependency is pinned in the script. If uv is unavailable but a suitable Python and the declared dependency are already installed, running the helper with that Python is equivalent. Tested against Codex CLI 0.155.1 with tomlkit 0.15.1 on macOS; its metadata APIs are experimental, so errors on another version require checking compatibility rather than guessing a configuration format.

Official references: [project configuration and trust](https://learn.chatgpt.com/docs/config-file/config-basic), [MCP and plugin server controls](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), and [app enablement](https://learn.chatgpt.com/docs/config-file/config-reference).
