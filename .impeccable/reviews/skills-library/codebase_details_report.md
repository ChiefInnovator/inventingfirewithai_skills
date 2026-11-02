# Codebase Details Review

## Read receipts

- Mode: `REVIEW`
- Persona: `agents/codebase_details.md` — full file.
- Standard: `resources/document_standards/implementation-readiness-standard.md` — full file.
- Target: `docs/designs/skills-library-design.md:171–258`; preceding lines read for context.
- Source inspected: `AGENTS.md`, `README.md`, `tests/requirements.txt`, both source-guard/check workflows relevant to develop, `docs/_config.yml`, homepage CSS/install/scorecard code, visibility and accessibility helpers, reference catalog, scorecard, evaluation documents, package test locations, and Codex MCP subprocess/test infrastructure.
- No memory, history, other review reports, tests, builds, mutations, or model calls used.

## Verdict

**Needs revision.** Existing implementation references examined are accurate, and proposed new paths are correctly presented as additions. Two implementation decisions remain insufficiently specified.

## B1 — Major: Installation destinations and discovery checks remain undecided

**Affected scope:** `docs/designs/skills-library-design.md:208–211`.

**Evidence:** The plan requires “Codex/Claude personal paths” without spelling out either destination or the client-specific discovery procedure. The current implementation provides no reusable answer: `README.md:25` and `docs/index.html:1028–1029` identify source package folders, provide Copilot’s project destination, and mention only Copilot’s reload command.

**Rationale:** Goal 3 explicitly requires complete-folder destinations and discovery checks for each client. A fresh implementer must still choose the Codex and Claude installation locations and determine how users verify discovery. That is a product-facing decision under the zero-decision standard.

**Required clarification:** Specify the exact destination pattern, full-folder example, invocation, and discovery/restart procedure for each supported client, then identify the same copy for both documentation surfaces.

## B2 — Major: Suite timeout handling does not specify descendant cleanup

**Affected scope:** `docs/designs/skills-library-design.md:182–190,219–220`.

**Evidence:** The runner is assigned a 180-second timeout per suite, but no process-tree cleanup contract. The Codex suite constructs persistent clients and registers cleanup through unittest (`skills/codex/mcp-pick/tests/test_mcp_pick.py:43–44`). Those clients launch `codex app-server --stdio` through `Popen` (`skills/codex/mcp-pick/scripts/mcp_pick.py:43–47`); their termination normally occurs in `Codex.close()` (`:94–103`). The suite also launches direct Codex subprocesses without individual timeouts (`skills/codex/mcp-pick/tests/test_mcp_pick.py:54–56,181–182`).

**Rationale:** Killing a timed-out unittest process prevents its registered cleanup from running. An ordinary timeout on that direct process does not guarantee termination of its descendants. The planned runner can therefore report a timeout and continue while leaving Codex processes behind. Existing helper cleanup cannot establish the runner’s promised bounded execution.

**Required clarification:** Define suite process isolation and whole-process-tree termination, including bounded escalation and reaping, and add a disposable descendant-process timeout fixture to the runner tests.

## Limits

- Review establishes source consistency, not successful execution.
- External package availability, action commit identity, client installation documentation, Impeccable CLI behavior, GitHub settings, and deployed Pages behavior were not verified.
- Simple unit-test bodies were consulted only to understand shared execution and subprocess assumptions; no comparative behavioral assessment was performed.
