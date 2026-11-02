# Stage 5 Initial Zoom Out Review

## Read receipt

- Persona: `google/elephant-goldfish-model@403d8881/agents/zoom_out.md`
- Standard: `google/elephant-goldfish-model@403d8881/resources/document_standards/zoom-out-standard.md`
- Target: `docs/designs/skills-library-design.md`, complete file, lines 1–241.
- Repository evidence: `README.md`, `AGENTS.md`, `.github/workflows/skills-checks.yml`, site configuration and homepage, existing visibility/accessibility tests, test requirements, and the Codex/Copilot MCP test implementations.
- Reuse search: repository file and content searches found no existing repository-wide suite runner or scorecard synchronization utility. Existing package-specific helpers serve different purposes.

## Verdict

**Revise: one Major finding.** Context is sufficient, and the architecture otherwise satisfies the Zoom-Out Standard.

The design addresses real gaps in test coverage, installation guidance, and deployed scorecard consistency. It preserves the existing static site, client packages, renderer, tests, and deployment route. Process isolation and a byte-checked static asset are proportionate solutions; no speculative framework, service, cache, or generalized package compiler is proposed.

The high-level specification stays at an appropriate altitude. Concrete paths, timeouts, and CSS values appear principally in the explicitly labeled Detailed Implementation Plan and do not constitute an altitude violation.

## Findings

### Z1 — Major: The unified verification environment omits an existing required runtime

**Affected scope:** Technical Plan, lines 93–98; Non-Functional Requirements, lines 136–139; Detailed Implementation Plan, steps 3–4 and 7.

**Evidence:** The plan adds the Codex MCP suite but describes provisioning only Python and pinned Python dependencies. The existing workflow installs Python and `tests/requirements.txt` (`.github/workflows/skills-checks.yml:22–31`). However:

- `skills/codex/mcp-pick/tests/test_mcp_pick.py:43` constructs the real `picker.Codex` client.
- `skills/codex/mcp-pick/scripts/mcp_pick.py:33–47` requires Codex CLI **0.153.4 or newer** and launches its local app server.
- The suite also invokes `codex mcp list` and local plugin installation (`test_mcp_pick.py:54–56,181–183`).

**Simplicity rationale:** The promised complete local/CI command cannot be reproduced from the documented Python dependency setup alone. This is an omitted dependency boundary, not a reason to introduce another testing abstraction or replace existing behavioral checks with mocks.

**Required revision:** Include a reproducible compatible Codex CLI installation in CI and document the matching local prerequisite. State explicitly that these tests use isolated local configuration/app-server operations without creating model threads or making provider calls. Report a missing or incompatible CLI clearly while preserving the runner’s requirement to report the other suites.

## Limitations

This was a read-only document and source review. No tests, builds, browser sessions, Git/GitHub mutations, or paid model calls were performed. Package availability, Pillow metadata, current remote protections, and live deployment behavior were not independently verified. Proposed files were assessed as proposed additions; their absence was not treated as a defect.
