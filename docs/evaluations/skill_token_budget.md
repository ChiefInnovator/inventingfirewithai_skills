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

Forty relocated sections were checked against the baseline verbatim, allowing only relative-link fixes and the shared instruction-file name. Package links resolve; fourteen compatible entrypoints pass the Codex format validator. Native Claude Slam frontmatter is parsed separately and unchanged, because that validator does not accept its existing Claude-specific fields. Copilot CLI discovery was verified before relocation. The five packages now live under `skills/copilot/` for download, not automatic activation in this repository. No scripts changed.

Relocation reduces initial and irrelevant instruction loading, not the total information needed for a complete task. Loading every reference would consume roughly the previous full detail plus routing overhead: whole Markdown bundles grew by about 2% due to routing instructions. Do not preload all references. No behavioral comparison or runtime cost benchmark was performed; structural checks do not establish unchanged agent decisions or guaranteed monetary savings. Discovery catalogs still contain the same skill descriptions.

## November 14, 2026: one shared package per skill

The three per-client folders were replaced by `skills/universal/<name>/`, one package that Codex, Claude Code, and GitHub Copilot load unchanged. Discovery was checked with `copilot skill list` (CLI 1.0.112) and `codex debug prompt-input` (CLI 0.169.0) against a scratch project holding all five folders, including Slam with its Claude-only `hooks` frontmatter. Sizes below are characters (about four per token), measured against `develop` at `a76f5cf`.

| Skill | Entrypoint before (Claude / Codex / Copilot) | Entrypoint now | References before | References now |
|---|---:|---:|---:|---:|
| figma-to-flutter | 6,704 / 6,704 / 6,797 | 8,392 | 41,782 | 43,090 |
| mcp-pick | 2,885 / 7,873 / 4,673 | 1,735 | 0 | 1,710 / 3,858 / 3,366 per host |
| pragmatic-coder | 3,828 / 3,793 / 3,864 | 3,874 | 0 | 0 |
| slam | 8,029 / 6,070 / 5,909 | 8,466 | 24,360 / 21,022 / 21,023 | 24,099 (20,748 without the Claude gate) |
| travel-like-a-local | 6,853 / 6,655 / 6,963 | 6,175 | 26,517 | 24,802 |

What changed in practice:

- **Figma to Flutter:** the entrypoint grew because it now carries the timer commands, a per-mode reading table, and the ground rules the references used to repeat. In exchange `performance.md` (8,605 characters) is no longer read on every run. A frame conversion reads about 31,800 characters instead of 37,300; `status` reads about 14,500 instead of 22,200.
- **MCP Picker:** each host reads the shared entrypoint plus its own reference: Claude Code 3,445 (was 2,885), Codex 5,593 (was 7,873), Copilot 5,101 (was 4,673). Claude Code and Copilot pay a few hundred characters for the single codebase.
- **Slam:** text is nearly unchanged; twelve reference files became three (plus a Claude-only gate file), so a full run makes three or four reads instead of twelve. On Codex and Copilot the entrypoint now includes the 3 KB Claude hook, because Claude Code documents no way for a skill hook to reference a bundled script.
- **Travel:** duplicated rules were merged and `venue-research.md` fell from 8,384 to 6,765 characters. Full checks now apply to the main pick and its comparison; further backups get a lighter Google-listing check.

`tests/test_skill_budgets.py` now fails the build when an entrypoint exceeds its budget, a per-client folder reappears, or a package link breaks.
