# Why a Figma-to-Flutter skill

The goal is repeatable, reviewable Flutter integration: preserve existing application work, trace each widget to its design, and show what was actually validated. A useful generated starting point is one part of that workflow.

## Community reference

The community **Figma to Code** plugin generates editable Flutter scaffolds and exports assets. Its documented strengths include local deterministic generation, warnings, and no external design uploads. Its stated limits include no repository connection or ongoing synchronization, no application logic, human accessibility review, and target-dependent vector/effect support. Large selections can also cost memory. These are scope boundaries, not evidence that the plugin is generally defective. The official plugin and repository links are in [references.md](../../references.md#figma-to-flutter).

## What this skill adds

| Need | Specific improvement | Implementation boundary |
|---|---|---|
| Integrate into an existing app | Inspect project components, token identities, SDK constraints, public widget APIs, and destination paths before adoption. | Agent workflow; no automatic private-theme assumptions. |
| Update designs safely | Match file key plus node ID, preserve stable slugs/APIs, and repair changed subtrees instead of replacing entire screens. | Bundled URL resolver plus ledger/update guidance. |
| Preserve source details | Retain fractional geometry, rich-text runs, font axes, alpha, transforms, flow/absolute layout, and node-specific gaps. | Bundled draft compiler and regression tests, with manual mapping for unsupported cases. |
| Verify actual Flutter output | Render Dart independently and compare immutable source/render pixels, dimensions, alpha, and critical control regions. | Bundled pixel checker; rendering uses the target project's Flutter harness. |
| Repair with evidence | Inspect differences, fix measured causes, rerender, and stop with explicit residual failures when progress stalls. | Bounded agent repair workflow; no promise of automatic pixel perfection. |
| Distinguish completion states | Track generation, analysis, pixel results, human review, platform checks, and production adoption separately. | Acceptance instructions; no automatic project-wide promotion validator. |
| Review screens across targets | Maintain one catalog of shared widgets with original Figma links, metadata, and platform-specific checks. | Explorer workflow; a project adapter is still required. |
| Reuse across clients/projects | Self-contained Claude and Codex packages, explicit target paths, synthetic tests, and no customer captures, decisions, or machine jobs. | Portable package adaptation. |

## Why we built this

We need an agent to carry design work through source capture, repository-aware implementation, measured repair, and reviewable acceptance. The plugin's own documentation positions its output as a starting point. This skill adds the surrounding engineering process and independent helpers while treating every generated widget as a draft until the required checks are complete.

The tradeoff is more setup, agent/tool usage, and rendering time. Live capture needs an authorized Figma connection; the connected agent workflow does not inherit the plugin's local-only privacy model. Native validation needs platform toolchains. Production behavior and accessibility still require explicit requirements and testing.

This is a capability comparison, not a benchmark claiming better accuracy or speed. The current community documentation was reviewed October 10, 2026. No customer design corpus, historical approval, or plugin implementation source is included in these packages. Unsupported conversion features remain explicit warnings.
