# Skill instruction token audit

Measured October 10, 2026 against commit `ee6b43b558659eda650a2070419f7c7d5d5203fb`. Counts use `tiktoken` with `cl100k_base`, a repeatable comparison proxy; actual host/model tokenization and billing can differ. Each count includes the entire SKILL.md, including frontmatter.

## Entrypoint counts

| Platform | Skill | Before | After | Reduction |
|---|---|---:|---:|---:|
| Codex | pragmatic-coder | 835 | 730 | 12.6% |
| Codex | slam | 3,399 | 1,162 | 65.8% |
| Codex | travel-like-a-local | 3,424 | 1,155 | 66.3% |
| Codex | mcp-pick | 1,532 | 1,532 | 0.0% |
| Codex | figma-to-flutter | 1,170 | 1,170 | 0.0% |
| Claude Code | pragmatic-coder | 836 | 733 | 12.3% |
| Claude Code | slam | 8,029 | 931 | 88.4% |
| Claude Code | travel-like-a-local | 3,458 | 1,191 | 65.6% |
| Claude Code | mcp-pick | 721 | 721 | 0.0% |
| Claude Code | figma-to-flutter | 1,170 | 1,170 | 0.0% |
| GitHub Copilot | pragmatic-coder | 848 | 743 | 12.4% |
| GitHub Copilot | slam | 3,347 | 1,120 | 66.5% |
| GitHub Copilot | travel-like-a-local | 3,479 | 1,210 | 65.2% |
| GitHub Copilot | mcp-pick | 906 | 906 | 0.0% |
| GitHub Copilot | figma-to-flutter | 1,185 | 1,185 | 0.0% |

Across all fifteen entrypoints: **34,339 → 15,659 tokens (54.4% reduction)**. This inventory total is not a single-session prompt: a host normally loads only the relevant platform and skills.

## Changes and preserved behavior

- **Slam:** keep invocation, authority, hard rules, blocker handling, and phase routing in the entrypoint. Load a phase immediately before its actions. All phase instructions remain in the standalone package; helper scripts are unchanged.
- **Travel:** load venue evidence, day planning, and experience/history guidance only for applicable requests. Each routing instruction requires its relevant reference before recommendations. The original detailed rules remain in the package; booking authority and state accuracy stay in the entrypoint.
- **Pragmatic Coder:** compress wording while retaining all six areas, including the five recently adopted recommendations. The three platforms share identical coding rules.
- **MCP Picker and Figma to Flutter:** entrypoints unchanged; their distinctions and guards earn the existing context cost. Neither executable helpers nor discovery descriptions were shortened.
- **Repository instructions:** merge unique CLAUDE.md rules into AGENTS.md and remove CLAUDE.md. The combined instruction text falls from **944 to 303 tokens (67.9%)**. Claude Code 2.1.296 is installed; the [official documentation](https://code.claude.com/docs/en/memory#agentsmd) supports direct AGENTS.md loading. Actual loading depends on the host mode and ancestor/local instruction files.

## Limits and verification

Forty relocated sections were checked against the baseline verbatim, allowing only relative-link fixes and the shared instruction-file name. Package links resolve; fourteen compatible entrypoints pass the Codex format validator. Native Claude Slam frontmatter is parsed separately and unchanged, because that validator does not accept its existing Claude-specific fields. Copilot CLI still discovers all five project skills. No scripts changed.

Relocation reduces initial and irrelevant instruction loading, not the total information needed for a complete task. Loading every reference would consume roughly the previous full detail plus routing overhead: whole Markdown bundles grew by about 2% due to routing instructions. Do not preload all references. No behavioral comparison or runtime cost benchmark was performed; structural checks do not establish unchanged agent decisions or guaranteed monetary savings. Discovery catalogs still contain the same skill descriptions.
