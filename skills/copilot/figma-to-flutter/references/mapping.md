# Source-to-Flutter mapping

These rules guide reviewed adoption and repair. The scratch compiler covers only a subset; its warnings and the actual render determine what remains. Never infer a missing source measurement from a prior customer or example.

## Design system and text

- Match a color token by captured variable identity, active mode, and resolved RGBA value. Equal RGB alone does not establish semantic equivalence. If the application's token value differs, retain the source in a reference token and record drift. Do not import a particular theme extension by convention.
- Reuse an existing component only when its rendered state, metrics, typography, assets, and behavior fit the source. Discover constructors and callbacks in the repository. A similar name is insufficient evidence.
- Preserve resolved font family, weight, style, variable axes, tracking, line height, and every styled run. Load real licensed font assets for comparison. A Material role label does not guarantee matching metrics; avoid ambient theme overrides and fallback test fonts.
- Convert percentage tracking and line height relative to font size. Keep measured text-box dimensions separately from paragraph metrics. Fixed vertical CENTER/BOTTOM alignment needs an outer measured box and natural-height paragraph; preserve full paragraph width for wrapping. HUG, FILL, and auto-resize do not imply fixed vertical slack.
- Preserve newlines, paragraph spacing, blank line boxes, underline, italics, and mixed spans. Do not flatten mixed fonts to one style. Use ellipsis only when source truncation/max-lines requires it; do not solve overflow by deleting text or reducing font size.
- Where source line boxes distribute leading evenly, use a measured text-height/strut policy and verify actual glyph bounds. Do not apply forced struts to arbitrary wrapping content or add per-screen offsets to compensate for the wrong font.
- Escape Dart strings, including interpolation markers. Canonical widgets receive application content and callbacks through the project's public API; fixture values belong in tests or previews.

## Layout

| Source evidence | Mapping and review |
|---|---|
| Horizontal/vertical Auto Layout | Row/Column; preserve alignment, gaps, padding, and each axis's FIXED/HUG/FILL independently. |
| HUG main axis | `MainAxisSize.min`; avoid Expanded/Flexible in an unbounded or intrinsically sized main axis. A row filling width does not force its child column to fill height. |
| FILL main axis | Flex only beneath a compatible, bounded parent. Preserve cross-axis sizing separately. |
| Wrap | Wrap with spacing/runSpacing; Expanded is not a direct Wrap child. |
| Mixed flow and absolute layers | Stack with a flow subtree and positioned overlays. Keep flow padding inside that subtree so overlay coordinates are not shifted twice. |
| Absolute position | Resolve against the actual containing block, not the nearest convenient widget. Apply local transforms once. Preserve paint order separately from flow order. |
| Trailing/MAX constraint | Derive trailing inset from parent size minus local position minus child size. Retain the measured child height; generated sticky viewport wrappers are not geometry evidence. |
| Percentage/center offset | Resolve from the measured containing box. For known width, center at `(parentWidth - childWidth) / 2 + offset`; preserve the source offset. |
| Negative item spacing | Preserve full child paint with a smaller layout slot or equivalent measured composition. Verify overlap and hit-testing; painted overflow is not automatically interactive. |
| Zero opacity | Retain layout space while suppressing paint and input. Explicitly hidden nodes may be omitted. These are different source states. |
| Stroke plus padding | Inspect `strokesIncludedInLayout` and child bounds. Count each inset once. Use foreground painting when the source stroke is paint-only. Do not apply one interpretation to an entire screen. |
| Fixed child larger than parent | Preserve source overflow only when evidenced. Verify global painted and tappable bounds; interactive overflow may require placement in the common containing Stack. |
| Rotation/group transform | Preserve local size and transform. Rotated axis-aligned bounding boxes alone may not reconstruct the original geometry. |
| Clip/scroll | Preserve actual clip shapes and scroll direction. Do not hide accidental RenderFlex overflow by adding a scroll view. |

Preserve fractional measurements. Do not round or simplify containers when that changes constraints, decoration, clipping, transforms, or node traceability. Validate bottom groups with and without captured keyboard space; a deterministic reference keyboard is separate from real device keyboard behavior.

## Assets, paints, and effects

- Use exact local assets and source crop/fit transforms. FILL, FIT, stretch, and tile are distinct. Export complex static decoration if necessary, but keep controls, text, and semantics as real widgets. A screenshot of the whole screen is never an implementation.
- Preserve fill order, alpha multiplication, gradient stops, and geometry. Convert source gradient handles into Flutter coordinates; CSS gradient angles depend on box aspect ratio. Unsupported elliptical/angular/diamond transforms need an explicit warning or faithful asset/painter.
- Preserve individual corner radii and stroke weights/alignment. Nonuniform borders with rounded corners require validation; don't discard radii globally. Gradient strokes need correct transformed direction, contour, and paint bounds.
- Distinguish outer shadow, inner shadow, layer blur, and backdrop blur. Blur-radius and sigma conventions differ. Clip the BackdropFilter itself when the source has rounded clipping. SVG filters may need exported pixels or explicit painting; do not assume the renderer implements every SVG effect.
- Preserve masks and alpha. Do not flatten an effect against a guessed background. Separate decorative exports from tappable content so rasterization does not remove interaction.
- Missing vectors, fonts, custom effects, image transforms, or component semantics remain node-specific TODOs. Provide a visible placeholder only in draft output and keep the status draft.

## Full-frame reference versus application behavior

Render every visible region required by the selected frame, including navigation, sheets, empty/loading/error states, and captured system chrome. Production status bars and keyboards use platform behavior; deterministic reference fixtures may paint them for comparison. Inspect both separately.

Implement navigation, state, accessibility, and data behavior only from the requested requirements and repository contracts. A label or prototype arrow does not establish a backend operation, authentication flow, or successful transaction.
