---
name: figma-to-flutter
description: Convert Figma frames into reviewable Flutter widgets, update existing conversions without overwriting unrelated work, and audit source-to-render fidelity. Use for Figma-to-Flutter capture, conversion, drift checks, visual repair, or a shared screen explorer.
---

# Figma to Flutter

Invoke as `/figma-to-flutter` (Claude Code, GitHub Copilot) or `$figma-to-flutter` (Codex) with a frame URL or a mode below. Convert the actual design into maintainable Dart with traceable source evidence and honest validation status, within the target repository's instructions, architecture, and authorized scope.

## Ground rules

The references assume these and do not repeat them.

- **Evidence is immutable and never invented.** Save each capture to a new capture-ID directory and never overwrite one. Do not invent source measurements, fonts, approvals, or results; missing evidence stays unknown or unchecked.
- **Results are separate.** Capture, analyzer success, a generated golden, pixel agreement, human approval, and production adoption are different facts. Never report one as another.
- **Bundled here:** a draft compiler, a URL resolver, a pixel checker, and a run timer with optional history export. Font preflight, capture scheduling, render caches, explorers, hosted checks, and promotion are target-project adapters; never invoke a helper that is not installed.
- **State belongs to the project.** Ledgers, decisions, and captures live in the target project's design root, never in this skill folder. Query large ledgers and decision files for the entries you need (`jq` or a script) instead of reading them whole.
- **Scope.** A conversion request does not authorize changing routes or backend behavior, shipping a PR, installing scheduled jobs, publishing captures, contacting teammates, or modifying the Figma document.

## Start

1. Start the whole-run timer before anything else, including report-only runs. Scripts are relative to this skill folder; the state directory is worktree-specific and outside tracked source:

   ```sh
   python3 scripts/run_state.py --state-dir "$FIGMA_STATE_DIR" start --command 'sync selected page'   # returns run
   python3 scripts/run_state.py --state-dir "$FIGMA_STATE_DIR" progress --run "$FIGMA_RUN_ID" --collection app --outcome pending|completed|skipped|failed|blocked <slug>...
   python3 scripts/run_state.py --state-dir "$FIGMA_STATE_DIR" finish --run "$FIGMA_RUN_ID" --status completed|blocked|failed|interrupted
   ```

   Register selected screens as `pending`, replace each with its verified outcome, and `finish` on every exit path. Read [performance.md](references/performance.md) only for parts/flow cards, stage measurements, history export, incremental capture selection, or render caches.
2. Inspect the project's instructions, Flutter package, SDK constraints, design system, existing conversions, assets, tests, and explorer. Resolve the requested Figma file/node and destination. Ask only for missing essentials; never assume a customer, file key, repository layout, branch, theme class, or target platform.
3. Preserve an existing output layout. For a new collection, propose a repository-relative design root with `raw/<slug>/<capture>/`, `flutter/<slug>/`, `ledger.json`, and `decisions.json`, and record the chosen paths in that ledger.
4. Establish whether the request concerns reference widgets, production integration, or both, and follow existing authorization for any integration or check-in.

## Modes and what to read

Read only the rows you are running. For an update or repair, read just the [mapping.md](references/mapping.md) sections for the node kinds you touch (text, layout, or assets/paints/effects).

| Input | Work | Read first |
|---|---|---|
| Frame URL or identified screen | Capture, create or update that scope, render, compare, record evidence. | [capture.md](references/capture.md), [typography.md](references/typography.md), [mapping.md](references/mapping.md); [fidelity.md](references/fidelity.md) before comparing |
| `sync` | Reconcile the explicitly selected file/page scope and update changed frames. | As above, plus [performance.md](references/performance.md#source-selection-and-capture-scheduling) |
| `continue` | Resume pending, failing, or stale work from the project ledger. | [workflow.md](references/workflow.md#project-state), then as for a frame |
| `audit [all|screen]` | Compare the inventory, source captures, Flutter renders, and any requested production implementation; report missing states and evidence separately. | [fidelity.md](references/fidelity.md) |
| `explore [web|android|ios]` | Refresh or run the shared Flutter explorer on the requested targets, reusing captures unless live refresh is requested. | [workflow.md](references/workflow.md#shared-explorer) |
| `draft <JSON>` | Run the bundled compiler into scratch space; never promote its output automatically. | [conversion.md](references/conversion.md) |
| `status` / `drift` | Read-only report. Drift may read live Figma when authorized; neither writes captures, ledgers, or skill files. | [workflow.md](references/workflow.md#project-state) |
| `decide` | Present unresolved project decisions and record actual answers in the project's decision file. | [workflow.md](references/workflow.md#decisions) |
| `upstream-review` / `upgrade` | Review public conversion guidance or improve this skill within the requested scope. | [workflow.md](references/workflow.md#repairs-and-upstream-knowledge) |

For batches or parallel workers, read [workflow.md](references/workflow.md#batches-and-interruption). For live work, verify the Figma connection and required provider skills before calling tools. An offline artifact is labeled with its age and coverage, never called a live sync.

## Conversion contract

- Source measurements prevail over generated CSS shortcuts. Inspect repository components before choosing replacements.
- Missing registered fonts, styles, axes, or glyphs block the affected work.
- Preserve identity by effective file key plus original node ID. Keep existing slugs and public widget interfaces on renames. Update changed subtrees and their dependencies; do not regenerate a whole working screen to repair one node.
- Retain original URLs, dimensions, variable bindings, font metadata, asset bytes, capture time, and call provenance. Truncated or stale context cannot establish complete coverage.
- Parameterize application text, data, assets, and callbacks during canonical adoption. Deterministic fixture values belong in tests or explicitly scoped preview fixtures. No mock services in implementation code, and no business action inferred from a visual label.
- Make unsupported content visible and traceable with `FIGMA-TODO(reason): <node-id> <gap>`. Do not silently omit vectors, masks, text, keyboard states, navigation, or system chrome the reference includes. A warning is a remaining gap, not a fix.
- Reuse source-matching project tokens by variable identity and resolved values. Keep captured values when a token differs and report the drift; do not quietly change the application's shared theme.

## Validate and repair

Scripts need Python 3; the pixel checker needs Python 3.11+ with `requirements.txt` installed in an isolated environment. Run the target project's analyzer, widget tests, and actual Flutter renders, then compare as [fidelity.md](references/fidelity.md) describes.

Each repair round: fix every worst-differing node whose box does not overlap another, worst first, from source values; rerender; compare. Revert a repair that makes its own node worse. Stop after five rounds, two unchanged renders, two rounds that each improve the changed fraction by under 0.5 percentage points, a source or asset blocker, or only rasterization differences. Report residual failures. Never loosen thresholds, hide regions, or copy source pixels into the render.

Refresh an existing shared explorer when its screens change. Validate requested platforms separately; a narrow browser viewport is not an Android or iOS run.

## Finish

Report changed screens/files, source freshness, tests and platform results, pixel findings, open decisions, and remaining acceptance work. Include whole-run elapsed time, completed screens, screens/minute and screens/hour, separate skipped/failed/blocked/pending counts and parts, and the metrics path.
