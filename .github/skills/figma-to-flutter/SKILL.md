---
name: figma-to-flutter
description: Convert Figma frames into reviewable Flutter widgets, update existing conversions without overwriting unrelated work, and audit source-to-render fidelity. Use for Figma-to-Flutter capture, conversion, drift checks, visual repair, or a shared screen explorer.
---

# Figma to Flutter

Use `/figma-to-flutter` in GitHub Copilot with a frame URL or one of the modes below. Convert the actual design into maintainable Dart, with traceable source evidence and honest validation status. Work within the target repository's architecture and authorized scope.

## Start with the project

1. Follow applicable repository instructions and the host's tool permissions. Inspect its instructions, Flutter package, SDK constraints, design system, existing conversions, assets, tests, and explorer. Resolve the requested Figma file/node and destination. Ask only for missing essentials; never assume a customer, file key, repository layout, branch, theme class, or target platform.
2. Preserve an existing output layout. For a new reference collection, propose a repository-relative design root with `raw/<slug>/<capture>/`, `flutter/<slug>/`, `ledger.json`, and `decisions.json`. Record chosen paths in that project's ledger. Keep shared skill files free of project state and captures.
3. Establish whether the request concerns reference widgets, production integration, or both. A conversion request alone does not authorize changing routes, backend behavior, shipping a PR, installing scheduled jobs, or publishing captured designs. Follow existing authorization for any requested integration or check-in.
4. For live work, read [capture.md](references/capture.md). Verify the available Figma connection and required provider skills before calling tools. For offline drafts, use the supplied artifact and label its age and coverage; do not call it a live sync.

## Modes

| Input | Work |
|---|---|
| Frame URL or identified screen | Capture, create or update that scope, render, compare, and record evidence. |
| `sync` | Reconcile the explicitly selected file/page scope and update changed frames. |
| `continue` | Resume pending, failing, or stale work using the project ledger. |
| `audit [all|screen]` | Compare the selected inventory, source captures, Flutter renders, and any requested production implementation. Report missing states and evidence separately. |
| `explore [web|android|ios]` | Refresh or run the shared Flutter explorer on the requested targets; reuse captures when live refresh is not requested. |
| `draft <JSON>` | Run the bundled compiler into scratch space; never promote its output automatically. |
| `status` / `drift` | Read-only report. Drift may read live Figma when authorized; neither mode writes captures, ledgers, or skill files. |
| `decide` | Present unresolved project decisions and record actual answers in the project's decision file. |
| `upstream-review` / `upgrade` | Review public conversion guidance or improve this skill within the requested scope. |

Read [workflow.md](references/workflow.md) for state, explorer, batch, and maintenance work. No mode implicitly grants authority to contact teammates or modify a Figma document.

## Conversion contract

- Read [mapping.md](references/mapping.md) for layout, typography, assets, component reuse, and unsupported cases. Source measurements prevail over generated CSS shortcuts. Inspect repository components before choosing replacements.
- Preserve identity by effective file key plus original node ID. Keep existing slugs and public widget interfaces on renames. Update changed subtrees and their dependencies; do not regenerate an entire working screen to repair one node.
- Keep raw captures immutable. Retain original URLs, dimensions, variable bindings, font metadata, asset bytes, capture time, and call provenance. Truncated or stale context cannot establish complete coverage.
- Parameterize application text, data, assets, and callbacks during canonical adoption. Put deterministic fixture values in tests or explicitly scoped preview fixtures. Do not add mock services to implementation code or infer successful business actions from visual labels.
- Make unsupported content visible and traceable with `FIGMA-TODO(reason): <node-id> <gap>`. Do not silently omit vectors, masks, text, keyboard states, navigation, or system chrome that the selected reference includes. A warning is a remaining gap, not a fix.
- Reuse source-matching project tokens by variable identity and resolved values. Keep captured values when a token differs and report the drift; do not quietly change the application's shared theme.

## Tools and validation

The scripts are relative to this installed skill folder, not the target repository. Run Python 3; install `requirements.txt` into an isolated environment for image checks. The compiler and URL resolver use only the standard library. Read [conversion.md](references/conversion.md) for commands and input/output contracts.

Run the target project's relevant analyzer, widget tests, and actual Flutter renders. Read [fidelity.md](references/fidelity.md) before comparison or visual approval. Capture generation, analyzer success, a generated golden, pixel agreement, human approval, and production adoption are separate results.

Repair the largest source-supported mismatch, rerender, and compare again. Stop after five actual repair rounds, two unchanged renders, negligible repeated improvement, a source/asset blocker, or only diagnosed renderer differences. Report residual failures. Do not loosen thresholds, hide regions, or copy source pixels into the render to claim success.

Refresh an existing shared explorer when its screens change. Validate the requested platforms separately; a narrow browser viewport is not an Android or iOS run. Preserve unavailable checks as unchecked.

Finish with changed screens/files, source freshness, tests and platform results, pixel findings, open decisions, and remaining acceptance work. Do not claim production integration or visual approval without its evidence.
