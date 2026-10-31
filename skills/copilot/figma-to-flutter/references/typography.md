# Font, glyph, and text checks

## Preflight the selected scope

Before conversion, rendering, or reuse of a rendered result, inspect every selected screen's visible text runs and actual Flutter font registrations. Use the target project's preflight when available; this package does not bundle a project font resolver. A desktop font installation alone cannot supply web assets or an isolated test harness.

- Verify readable, materialized font bytes, declared family, required static weight and italic style, variable-axis values within actual font ranges, and glyph coverage for the selected run. Check registration and any explicitly configured fallback as well as the file. Corrupt files, Git LFS pointers, Ahem/LastResort, and replacement boxes cannot establish coverage.
- Keep source missing-font conflicts distinct from missing local assets or registration. An explicit `hasMissingFont: true` or invalid flag blocks affected work. If a historical capture omits the flag, report source font status as unknown; absence alone is not a missing local font and must not become an invented `false`.
- Report the affected screen/node/text, family, weight/style/axes, and missing glyphs with `U+` code points. Empty non-rendering text does not introduce a glyph requirement. Obtain an unknown private-use glyph's supplying font from source evidence or its owner; do not guess an icon font.
- On a failure, retain captures and existing outputs, stop affected conversion/rendering, and notify the coordinator so workers sharing the dependency stop too. Diagnose or acquire the exact font; do not substitute a family, suppress a glyph, relax pixel checks, or call old results current.
- Identify the original provider and licensing/bundling requirements. Register permitted source files consistently for previews, native tests, and web; record provenance and hashes. Resume affected work after the entire selected dependency scope passes.

## Preserve paragraph metrics

Carry resolved line height into any Material `TextStyle.copyWith`; a role name does not establish its metrics. Resolve AUTO from a genuine content-sized source line box where possible. A fixed box can contain alignment slack and is not automatically a line box. Unresolved inherited metrics remain a draft gap.

Keep styled runs, natural paragraph height, width for wrapping, tracking, blank lines, and paragraph spacing distinct. Flutter centering can exclude a trailing space's advance in an unconstrained single-line hugging run. Keep CENTER alignment for multiline text, including Unicode line separators, and for width-constrained runs; a correction to one line cannot left-align the whole paragraph. Any tracking half-lead, button-label width rounding, or font-baseline correction must have matching source/font/renderer measurements and a regression; do not apply a project-specific offset or threshold universally.

Occluded text is still source content. Account for later opaque or blurred overlays when diagnosing visible glyph bounds; do not remove covered layers merely to improve a geometry score.

## Native system keyboard fixtures

Production uses the real native keyboard. A project may explicitly permit a deterministic preview exception for a captured OS keyboard. Establish component identity and actual descendant ancestry; a layer name or code point alone is insufficient. Preserve layout space and key roles, use licensed registered legend fonts or role-correct vector keys, and record the affected runs and comparison scope.

Do not extend an exception to application text, composers, custom keyboards, status bars, or other chrome. Do not fabricate a hidden or absent keyboard. An exception does not establish exact whole-frame pixel fidelity and does not authorize masking source pixels or weakening the bundled checker.
