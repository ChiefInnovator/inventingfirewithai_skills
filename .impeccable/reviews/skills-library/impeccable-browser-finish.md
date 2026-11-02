# Targeted post-fix browser acceptance

Target: `docs/index.html` / `docs-index-html`. Date: November 2, 2026. This is acceptance of the settled fixes, not a second independent critique or a replacement for Assessments A/B.

**Result: requested local browser checks pass.** No source changes were made by this assessor.

## Method and artifact

Used a fresh isolated Playwright CLI session with headless Chrome 156 and the parent's existing local static server. No user browser, tab, persistent profile, overlay, or external destination was used. Each top capture followed a fresh navigation, completed scorecard loading, font readiness, two animation frames, and a settling interval.

Served homepage bytes matched the current repository file. SHA-256: `3f7418155799cfeaa19c5ec00adc1516caa9c3039c087421bf863e1aa48c1ac3`. This is local served-source acceptance, not deployed GitHub Pages acceptance.

## Responsive layout and routes

| CSS width | Document/body scroll width | Mark | Package targets | Skill columns |
| ---: | --- | --- | --- | ---: |
| 320 | 320 / 320 | loaded, 36×36px | 15, minimum 48.5625×44px | 1 |
| 390 | 390 / 390 | loaded, 36×36px | 15, minimum 48.5625×44px | 1 |
| 768 | 768 / 768 | loaded, 36×36px | 15, minimum 48.5625×44px | 1 |
| 1024 | 1024 / 1024 | loaded, 36×36px | 15, minimum 48.5625×44px | 2 |
| 1440 | 1440 / 1440 | loaded, 36×36px | 15, minimum 48.5625×44px | 3 |

There was no document-level horizontal overflow at any tested width. The 36px mark and the browse action remain visible in each 900px-high first viewport. Package-link focus and wrapping were visually checked on phone captures. Settled screenshots at all five widths were inspected; they retain the incumbent charcoal/paper/Chivo world. The desktop heading now balances across its two lines. The desktop author capture preserves the compact flame and limited Fraunces byline.

At every width, **Browse all five skills** (`docs/index.html:924`) has the solid-white primary treatment; **View on GitHub** has the translucent secondary treatment. Real clicks on Browse navigated to `#skills`, with the section top within 0.4px of the viewport top. The adjacent installation-help link (`:947`) navigated to `#install`, exposing “Install a complete skill folder.” with the section top within 0.4px of the viewport top. These routes stayed on the local document.

## Keyboard and fixed issues

Actual Tab/Enter input exposed the skip link and moved focus to `main-content` at all five widths. Continuing native Tab traversal reached the explicit terminal `<pre tabindex="0" role="region">` (`docs/index.html:1069`) after 19 Tabs from the main entry. It retained its descriptive accessible name and a **3px solid gold focus outline**, `rgb(240, 177, 62)`, offset inward by `-3px` at every width.

At 320px, the terminal's 280px viewport contains 327px of content; ArrowRight moved its horizontal scroll position from 0 to 39px while preserving gold focus. At wider widths it has no horizontal overflow, and ArrowRight correctly leaves scroll position at zero. The earlier missing-explicit-focusability scanner finding is resolved in this rendered version.

Two more Tabs from the terminal reached the native scorecard region through its source link. The region remains `tabindex="0"`, `role="region"`, named, and described by the **visible** `scorecard-scroll-help` cue (`:1089`): “Scroll within the table for more rows; scroll sideways on narrow screens for all columns.” The region shows its 3px inward steel focus outline. ArrowRight moves the phone/tablet table horizontally; PageDown scrolls rows vertically.

All six table headers compute to `position: sticky; top: 0px` (`:695`). After 500px of internal vertical scrolling at 390/768/1024/1440, their top edges remained at the region's top while body cells moved behind them. A separate native PageDown confirmation at 320 likewise scrolled 500px with all six headers staying at the region top. Phone and desktop focus/scroll captures show the cue, sticky header, and visible focus ring. Contained scorecard overflow does not expand the document.

## Accessibility scanner

Ran the default **axe-core 4.14.0** browser rules from the official npm package at 320px and 1440px after successful scorecard loading:

- **320px: 0 violations**, 49 passed rule groups, 41 inapplicable groups.
- **1440px: 0 violations**, 49 passed rule groups, 41 inapplicable groups.
- Both runs still mark eight symbol-only spans for manual color-contrast review: seven checks and one cross. The scanner says their content contains only non-text characters. Their computed green/red colors on the flat terminal background retain calculated ratios of 8.81:1 and 7.48:1. This is not a blanket WCAG conformance finding.

## Evidence and cleanup

Thirteen private PNG captures were retained for the separate file-only finish reviewer: five top viewports, two phone-card focus views, two terminal focus views, three scrolled scorecard focus views, and the desktop author. Exact temporary paths were handed to the parent separately and are intentionally absent from this committed report. Private measurement and scanner-result JSON were also retained for that handoff.

The assessor's browser session is closed. Temporary automation scripts and downloaded scanner files were removed. The parent-owned local static server remains running. No source edits, Git/GitHub actions, review requests, implementation mocks, user-visible overlays, or changes to other reports were made.

Limits: headless Chrome with CSS viewport emulation; no physical-device, Safari, assistive-technology, audible-announcement, external-link, or deployed Pages acceptance. Loading/failure announcements were exercised in the earlier Assessment B; this targeted run checked the final success state rather than claiming to repeat those transitions.
