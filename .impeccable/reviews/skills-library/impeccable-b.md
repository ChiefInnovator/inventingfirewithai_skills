# Assessment B — detector and rendered-browser evidence

Target: `docs/index.html` (`docs-index-html`). Assessor: independent Assessment B; no Assessment A report or findings read. Context was already loaded by the parent and was not rerun. Review date: November 2, 2026.

## Detector

Ran the bundled `impeccable detect --json docs/index.html` from the project root. Exit **0**: **0 primary findings, 10 advisory findings**. Actual result objects are saved in `detector.json`; only absolute file prefixes were normalized to repository-relative paths. No scan result was removed or rewritten.

| Rule | Count | Source locations | Contextual assessment |
| --- | ---: | --- | --- |
| `design-system-color` | 6 | `docs/index.html:717`, `:738`, `:739`, `:749`, `:760`, and reported line `0` | Five existing terminal/author colors are missing from normative palette metadata, though their component roles are described in DESIGN.md. The line-0 black `Video Downloader` underline is a static-analysis false positive: rendered `border-bottom-color` is `rgb(255, 179, 71)`, the documented brand accent, through `currentColor`. |
| `design-system-font-size` | 4 | `docs/index.html:360`, `:379`, `:587`, `:680` | Existing 14px navigation/table text, the 18px fluid endpoint, 34px statistics, and 12px table labels do not all appear in the frontmatter ramp. These are documentation/token completeness advisories, not evidence of illegible rendered text. |

The project has no `.impeccable/critique/ignore.md`. Detector config has no ignored rules/files and one sanctioned `overused-font` value ignore for Fraunces in `docs/index.html`. Browser inspection confirmed Chivo on body text and Fraunces on exactly one element, the author H2. Preserve this approved exception.

## Browser method and visualization

The parent recorded failed native-browser-host and Chrome-pipe attempts. Assessment B used the working fallback: a fresh named Playwright CLI session, headless Chrome 156, an isolated temporary profile, and the existing local static server. No user browser/profile/tab was reused. No implementation or source state was edited.

Mutable injection was genuinely preflighted: a temporary document title and appended script executed in B's page. A temporary Impeccable live server then served `detect.js`; script injection succeeded and the page title was labeled `[Human]`. The detector logged **8 runtime observations**: 1 `unbalanced-heading`, 3 `straggler`, and 4 `line-length`. The observed text included the trailing words “escalating.”, “evaluation.”, and “consent.”; reported long measures were approximately 92–98 characters. These are layout/typography signals, not automatic accessibility failures. The desktop hero screenshot independently shows “Skills” alone on its second heading line. The CLI JSON is the authoritative saved static scan; these runtime observations are additional browser evidence.

**No reliable user-visible overlay is available:** injection and execution succeeded in the private headless session, which has no user-visible presentation. Do not tell the user an overlay is open in their browser. The temporary Impeccable live server was stopped with `stop --keep-inject`; the source HTML was not injected. Reload removed the private page overlay before other measurements.

## Responsive and visual verification

Rendered measurements used a 900px viewport height at all requested widths. The compact mark was loaded, displayed, **36×36 CSS px**, and in the first viewport at every width. No document-level horizontal overflow occurred (`documentElement.scrollWidth === innerWidth` and body scroll width matched). All **15 package links** measured at least **48.5625×44 CSS px**. Cards and links wrapped inside their container.

| Widths checked | Skill columns | Principles/statistics columns | Section vertical padding |
| --- | ---: | ---: | --- |
| 320, 390, 600 | 1 | 1 | 48px |
| 601, 768, 860 | 1 | 1 | 86px |
| 861, 1024, 1100 | 2 | 3 | 86px |
| 1101, 1440 | 3 | 3 | 86px |

At 600/601, section padding changes as designed; at 860/861 the cards and navigation change as designed; at 1100/1101 the skill grid changes from two to three columns. The wrapper maintains 20px phone gutters, skill cards retain 26px internal side padding, and the phone hero uses 28px top / 44px bottom padding. The 1440px wrapper is 1120px wide with 160px outer gutters. The browse action remains visible in the first viewport at 320 and 390.

Top-of-page captures were inspected at 320, 390, 768, 1024, and 1440; phone cards and phone/desktop scorecard focus were also visually inspected. A transient resized-screen capture artifact at 768 was checked against a fresh navigation and DOM inventory: the verified page has one static navigation. Element-cropped screenshots also showed stale fixed-layer pixels; viewport captures and current DOM state were used instead. Neither capture artifact is reported as a product defect.

## Keyboard and scorecard

At 320, 390, 768, 1024, and 1440, real Tab/Enter interaction revealed the skip link, with a visible 3px steel outline, and moved focus to `#main-content`. Continuing with Tab reached `#scorecard-table`, with `:focus-visible` true and a **3px solid `rgb(35, 100, 119)` inward outline (`-3px`)**. Phone and desktop captures confirmed the ring remains visible inside the clipped panel. Arrow keys scrolled the focused region horizontally where necessary and vertically at all five widths.

At 320 the scorecard region is 278px wide with an 860px scrollable table; at 390 it is 348px wide. This is contained table overflow, not page overflow. The success table had 137 body rows and six column headers. Table headers have native column scopes and the table has a caption.

The scorecard asset request was genuinely delayed and then aborted in B's page; the original application handlers ran unchanged. A document-start observer recorded these actual status transitions:

| Real request condition | Live-region text | Busy state / result |
| --- | --- | --- |
| Delayed original request | `Loading skill scorecard.` | `aria-busy="true"`; crawlable local scorecard fallback present |
| Original response succeeds | `Skill scorecard loaded.` | `aria-busy="false"`; 137 rows rendered |
| Request fails | `Scorecard preview could not load. The markdown source link remains available.` | `aria-busy="false"`; visible failure explanation and actual “Open markdown” source link retained |

The status element consistently exposed `role="status"`, `aria-live="polite"`, and `aria-atomic="true"`. Routes were removed and the normal success page restored. This proves real DOM updates and live-region semantics; no screen reader or audible announcement was tested.

The local server returned byte-identical `index.html` and scorecard-data assets compared with current repository files (SHA-256 checked). Homepage SHA-256: `3744d2cd6e11a30127857489252aebe75c9dde22dabda91dd4d41555bea1eee6`; data SHA-256: `845fe8cb865a6c377a418cbd5b562fc8ef75ec0b032821903cbe5b2c7689e0a4`. This establishes local served-source parity, not GitHub Pages deployment acceptance.

## Accessibility scanner and material follow-up

Ran **axe-core 4.14.0**, fetched from the official npm `axe-core` package, with the default browser rules at 320 and 1440 after successful scorecard loading. The package was used only in private browser instrumentation; no dependency or implementation code changed.

- **320px: 1 violation**, `scrollable-region-focusable`, serious scanner impact, on the terminal `<pre>` at `docs/index.html:1043` (overflow styling `:730`). Its content box is 280px wide and scroll width is 327px. It has no tabindex or focusable child. Axe explicitly identifies keyboard access in Safari as the concern. **1440px: 0 violations.**
- The current Chrome automatically includes this overflowing `<pre>` in the tab order; a real Tab reached it and ArrowRight changed its scroll position from 0 to 37px. Therefore, this is a concrete missing explicit keyboard affordance and a cross-browser risk, **not a reproduced Chrome failure**. Safari was not exercised. A small explicit focusability/focus-ring change for the code region would avoid depending on Chrome's auto-focus behavior; recommended synthesis severity P2, not an invented P1 outage.
- Both default runs had eight `color-contrast` items needing review, all seven check-mark spans and the one cross span. Axe's reason was “Element content contains only non-text characters.” The computed glyph colors against the flat terminal background have calculated contrast ratios **8.81:1** (green) and **7.48:1** (red); these incomplete automated checks do not establish low contrast.
- Each run recorded 48 passed rule groups and 42 inapplicable groups. Do not describe the whole surface as accessibility-clean.

Other bounded observations: the desktop heading's lone final word is a minor typography refinement (P3); the 10 static advisories mostly concern design-record completeness (P3), including one verified false positive. The runtime line-length warnings warrant judgment against the Read-mode layout, not wholesale redesign or removing the approved byline font. A local `favicon.ico` request returned 404; this is not evidence that deployed Pages assets are broken.

## Scope and cleanup

Only this report and `detector.json` were written in the repository. No source fixes, Git/GitHub mutations, model calls, external messages, new frameworks, or other review reports were used. The pre-existing local static server remains owned by the parent and was left running. B's temporary detector server was stopped and B's browser session was closed. Temporary scripts, downloaded scanner files, and private browser captures/logs were removed after report preparation. Persisted evidence consists of this self-contained report and the actual normalized detector JSON.

Limits: one desktop browser engine in headless mode; CSS viewport emulation rather than physical devices; no Safari, assistive technology, live GitHub Pages, external destination acceptance, or user-visible overlay acceptance. Assessment A remained isolated from detector findings; the parent must release B only after A has finished.
