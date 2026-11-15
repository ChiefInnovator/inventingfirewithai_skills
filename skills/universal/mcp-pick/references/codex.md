# Codex

Resolve `scripts/codex_mcp_pick.py` in this skill directory to an absolute path (`<helper>`). It needs Python 3.11+, uv, and Codex CLI 0.153.4 or newer; without uv, a Python that already has the script's pinned TOML dependency is equivalent. It writes only the selected project's `.codex/config.toml`.

```sh
uv run --no-project --script <helper> list --json
uv run --no-project --script <helper> keep --expect <inventory_version> --project /absolute/project/path mcp:example app:connector_example
```

**Inventory:** the default target is the current Git root, or the current directory outside Git; check the returned `project`. Use `--project` for another project or a subfolder, `--profile NAME` for an explicit Codex profile, and `--scope servers` when the request excludes app integrations; repeat these on every call. The output holds only names, selector IDs, enabled preferences, blockers, and an `inventory_version` fingerprint. It covers effective configuration and installed plugins, including their apps; it does not scan the public app catalog or verify account connections, so integrations injected into a running session or supplied by another Codex installation may be missing. If app discovery is unavailable, say so and do not claim app connectors were trimmed.

**Menu:** compact numbered lists under bold **On** and **Off** labels, On first, each sorted case-insensitively by displayed name with ties broken by exact ID, numbered continuously. Include every entry; put blocked entries in Off with a short blocker note. Omit status columns, redundant app/server suffixes, and per-entry explanations unless needed to tell entries apart; label an explicit server and a same-named plugin server distinctly. Put any recommendation in one sentence after the list. Keep the number-to-ID mapping, project, scope, profile, and `inventory_version` for the apply step. When invoked again without new changes, show the chooser with current settings; an earlier choice is a default, not authorization.

**Apply:** pass the reviewed fingerprint as `--expect`. `keep` enables the named IDs and disables the other listed entries; `none` disables all; `all` enables every unblocked entry. `--dry-run` previews. An incremental request such as "disable Calendar" changes only that entry. The helper refuses unknown selections, stale reviews, symlinked or global config targets, untrusted project layers, and incomplete discovery, and it restores the previous file if Codex cannot load the result; relay its exact blocker. If the inventory changed, refresh and reconcile with the user instead of approving new entries. It never grants project trust, authenticates apps, enables a disabled parent plugin, or installs anything.

**Report:** run `list` again with the same project, scope, and profile and report from it. A new Codex session in the trusted project loads the selection. Per-tool restrictions, approval policies, and managed requirements still apply. Re-run the picker after installing integrations; the selection is not a wildcard for future servers.

**Boundaries:** explicit servers use `mcp_servers.<name>.enabled`, plugin servers `plugins.<plugin-id>.mcp_servers.<server>.enabled`, and apps `apps.<app-id>.enabled`. Do not call `codex mcp remove`, edit global enablement, remove plugins, copy global server definitions or credentials into the project file, or disable built-in tools or trust/approval settings as a substitute. The metadata APIs are experimental: on a version error, check compatibility instead of guessing a configuration format.

Official references: [project configuration and trust](https://learn.chatgpt.com/docs/config-file/config-basic), [MCP and plugin server controls](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), and [app enablement](https://learn.chatgpt.com/docs/config-file/config-reference).
