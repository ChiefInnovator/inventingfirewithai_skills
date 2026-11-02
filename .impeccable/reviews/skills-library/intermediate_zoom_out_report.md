# Stage 8 Intermediate Zoom Out Review

## Read receipt

- Persona: `google/elephant-goldfish-model/agents/zoom_out.md`, complete installed EGM 0.1.0 copy.
- Standard: `google/elephant-goldfish-model/resources/document_standards/zoom-out-standard.md`, complete installed EGM 0.1.0 copy.
- Target: `docs/designs/skills-library-design.md`, complete file, lines 1–256.
- Required prior context: `.impeccable/reviews/skills-library/zoom_out_report.md`, complete file.
- Repository evidence: complete `README.md`, `AGENTS.md`, `.github/workflows/skills-checks.yml`, `tests/requirements.txt`, and `docs/_config.yml`; relevant sections of `docs/index.html`, `tests/test_pages_visibility.py`, both MCP test suites, and `skills/codex/mcp-pick/scripts/mcp_pick.py`.
- Reuse searches: repository script inventory and searches for discovery orchestration, subprocess execution, scorecard synchronization, and package dependencies. No existing repository-wide suite runner or scorecard synchronization utility was found.

## Verdict

**Revise: one Major finding.**

The architecture remains proportionate: retain the static site and existing renderer, copy the canonical scorecard without transformation, and isolate existing test suites rather than introduce a testing framework or package compiler. Conditional layout adjustments preserve scope. Keeping raw development records outside the Pages source addresses publication boundaries without claiming repository privacy.

The prior Z1 Codex-runtime omission is addressed explicitly by the Node/Codex installation, local prerequisite, version check, and continued execution of other suites. One additional existing dependency remains absent from the proposed reproducible environment.

## Findings

### IZ1 — Major: The complete verification environment still omits the MCP suite’s Python dependency

**Affected scope:** Technical Plan, lines 93–99; Non-Functional Requirements, lines 145–150; Detailed Implementation Plan, steps 3–4 and 7.

**Evidence:**

- `tests/requirements.txt:1` currently contains only `PyYAML==6.0.3`.
- The design adds Pillow and the Codex CLI, but does not add the existing TOML dependency.
- `skills/codex/mcp-pick/scripts/mcp_pick.py:4` declares `tomlkit==0.15.2` in script metadata.
- `skills/codex/mcp-pick/scripts/mcp_pick.py:263–269` imports `tomlkit` during `apply_selection` and raises an error when unavailable.
- `skills/codex/mcp-pick/tests/test_mcp_pick.py:13–17` imports the helper directly; tests at lines 68–105 exercise configuration writes through that function. Plain unittest discovery does not provision the helper’s script metadata dependencies.

**Consequence:** A clean environment containing the proposed requirements and Codex CLI still fails existing MCP behavioral checks. This contradicts the promised reproducible complete local/CI command.

**Simplicity rationale:** This is another omitted dependency boundary. It does not justify a new environment manager, fallback implementation, or replacement of the existing behavioral checks.

**Required revision:** Include `tomlkit==0.15.2` in the shared test requirements and document that the unified command provisions the existing helper’s pinned dependency. Preserve the helper’s current package boundary and implementation.

## Limitations

Read-only design and source review only. No edits, tests, builds, browser sessions, Git/GitHub mutations, or model calls were performed. No other review reports, memory, history, or private user data were consulted. Package availability, remote protections, runtime duration, and deployed behavior were not independently verified. Proposed files were treated as intentional additions; their absence was not considered a defect.
