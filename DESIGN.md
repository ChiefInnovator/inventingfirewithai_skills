---
name: Inventing Fire with AI Skills
description: Cool paper documentation, charcoal surfaces, and compact fire branding.
colors:
  ink: "#151515"
  muted: "#5a5f66"
  line: "#d9dde3"
  paper: "#f3f6f8"
  panel: "#ffffff"
  ember: "#d94f30"
  ember-text: "#b84227"
  gold: "#f0b13e"
  steel: "#236477"
  green: "#1d7a5f"
  code: "#20252b"
  brand-surface: "#120f0c"
  brand-ink: "#f2ece3"
  brand-muted: "#c9bfb0"
  brand-accent: "#ffb347"
  tag-surface: "#eef3f4"
  terminal-bar: "#15191e"
  terminal-ink: "#f4f4f4"
  code-success: "#77d6aa"
  code-error: "#ff9a80"
  author-border: "#514335"
  mark-border: "#8f4319"
  mark-surface: "#0b0907"
typography:
  display:
    fontFamily: 'Chivo, "Segoe UI", sans-serif'
    fontSize: "clamp(36px, 5.5vw, 72px)"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0"
  headline:
    fontFamily: 'Chivo, "Segoe UI", sans-serif'
    fontSize: "clamp(30px, 4vw, 52px)"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0"
  skill-title:
    fontFamily: 'Chivo, "Segoe UI", sans-serif'
    fontSize: "30px"
    fontWeight: 700
    lineHeight: 1.3
  card-title:
    fontFamily: 'Chivo, "Segoe UI", sans-serif'
    fontSize: "20px"
    fontWeight: 700
    lineHeight: 1.3
  body:
    fontFamily: 'Chivo, "Segoe UI", sans-serif'
    lineHeight: 1.5
  lede:
    fontFamily: 'Chivo, "Segoe UI", sans-serif'
    fontSize: "20px"
    fontWeight: 400
    lineHeight: 1.5
  tag:
    fontFamily: 'Chivo, "Segoe UI", sans-serif'
    fontSize: "13px"
    fontWeight: 700
    lineHeight: 1.5
  author-title:
    fontFamily: 'Fraunces, "Iowan Old Style", Palatino, serif'
    fontSize: "22px"
    fontWeight: 500
    lineHeight: 1.3
  navigation:
    fontFamily: 'Chivo, "Segoe UI", sans-serif'
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  table-label:
    fontFamily: 'Chivo, "Segoe UI", sans-serif'
    fontSize: "12px"
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: ".04em"
  hero-copy:
    fontFamily: 'Chivo, "Segoe UI", sans-serif'
    fontSize: "clamp(18px, 2vw, 22px)"
    fontWeight: 400
    lineHeight: 1.5
  scorecard-title:
    fontFamily: 'Chivo, "Segoe UI", sans-serif'
    fontSize: "18px"
    fontWeight: 700
    lineHeight: 1.5
  statistic:
    fontFamily: 'Chivo, "Segoe UI", sans-serif'
    fontSize: "34px"
    fontWeight: 700
    lineHeight: 1.3
  author-link:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: ".1em"
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "15px"
    lineHeight: 1.65
rounded:
  button: "6px"
  panel: "8px"
  author: "14px"
  pill: "999px"
spacing:
  tag-gap: "8px"
  action-gap: "12px"
  grid-gap: "18px"
  gutter: "20px"
  card-padding: "24px"
  skill-padding: "26px"
  group-gap: "32px"
  split-gap: "42px"
components:
  button-primary:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.ink}"
    rounded: "{rounded.button}"
    padding: "0 18px"
  button-secondary:
    backgroundColor: "rgba(255, 255, 255, .08)"
    textColor: "{colors.panel}"
    rounded: "{rounded.button}"
    padding: "0 18px"
  tag:
    backgroundColor: "{colors.tag-surface}"
    textColor: "{colors.steel}"
    typography: "{typography.tag}"
    rounded: "{rounded.pill}"
    padding: "0 10px"
  card:
    backgroundColor: "{colors.panel}"
    rounded: "{rounded.panel}"
    padding: "{spacing.card-padding}"
  skill-card:
    backgroundColor: "{colors.panel}"
    rounded: "{rounded.panel}"
    padding: "{spacing.skill-padding}"
  navigation:
    backgroundColor: "{colors.code}"
    textColor: "{colors.panel}"
    padding: "18px 0"
  terminal:
    backgroundColor: "{colors.code}"
    rounded: "{rounded.panel}"
  client-link:
    typography: "{typography.body}"
  installation-list:
    typography: "{typography.body}"
  scorecard-panel:
    backgroundColor: "{colors.panel}"
    rounded: "{rounded.panel}"
  author-panel:
    backgroundColor: "{colors.brand-surface}"
    textColor: "{colors.brand-ink}"
    rounded: "{rounded.author}"
    padding: "44px 40px"
---

# Design System: Inventing Fire with AI Skills

## Overview

**Creative North Star: "The Fire Workshop"**

The existing fire identity sits inside practical documentation: cool paper,
white content panels, and charcoal navigation, hero, and code surfaces. Compact
branding and direct typography keep the library's content and actions legible.
This describes the incumbent implementation rather than a replacement concept.

The checked-in layered flame and the dark author panel connect the library to
Inventing Fire with AI. Chivo carries the interface; the author byline alone
uses Fraunces, matching the owner-approved Video Downloader branding reference.

**Key Characteristics:**
- Cool paper and white panels separated by fine neutral borders.
- Charcoal anchors with restrained ember, gold, and steel accents.
- Chivo hierarchy, readable body leading, and a limited serif author byline.
- Compact flame branding, wrapping links, and bordered content cards.

Source: `docs/index.html` inline stylesheet and markup; brand constraints in
`PRODUCT.md`; the sanctioned font exception in `.impeccable/config.json`.
The sidecar's synthesized tonal strips are preview metadata, not additional
production colors or a palette authorized for new surfaces.

## Colors

Cool documentation surfaces carry warm fire accents; the author panel retains
its own warmer dark palette. Frontmatter contains the normative values.

### Primary
- **Ember:** terminal indicator and featured-card border emphasis.
- **Ember text:** the first scorecard row's emphasized name on white.
- **Gold:** statistics, code keys, and focus outlines on dark surfaces.

### Secondary
- **Steel:** tags, scorecard links, numbered rules, text selection, and focus on light surfaces.
- **Green:** the terminal's third indicator; it is not a general success-state system.
- **Code success / code error:** light green and warm red example markers inside
  the charcoal terminal; these differ from the darker toolbar indicator fills.

### Neutral
- **Ink / muted:** main text and supporting text on light backgrounds.
- **Paper / panel / line:** page canvas, white panels, and separators.
- **Code:** shared charcoal for navigation, hero, statistics, and terminal.
- **Tag surface:** pale cool fill for informational pills.
- **Terminal bar / ink:** the darker toolbar and near-white terminal text.
- **Author border / mark border / mark surface:** the author panel's brown
  one-pixel perimeter, orange-brown two-pixel avatar perimeter, and dark inset.

These named additions are literal incumbent CSS colors, not newly designed
shades. White navigation and hero copy also use source alpha values (.82 and
.86) over charcoal; secondary buttons use an (.08) white fill and (.28) white
border over their parent surface. Featured cards use (.45) ember borders and
(.2) ember inset strokes over white. Those rendered mixtures are composited
colors, not independent opaque palette primitives. Author paragraph link
underlines inherit amber through `currentColor`; there is no black underline
color token.
- **Brand surface / ink / muted / accent:** the author panel's brown-black,
  warm light text, quieter supporting text, and amber links.

**The Surface Contrast Rule.** Use steel focus outlines on light surfaces and
gold outlines on navigation, hero, author, and focused terminal code surfaces,
as implemented.

## Typography

**Display and Body Font:** Chivo, with Segoe UI and sans-serif fallbacks.
**Author Font:** Fraunces, with Iowan Old Style, Palatino, and serif fallbacks.
**Code Font:** the platform monospace stack specified in the frontmatter.

Both web fonts are self-hosted with `font-display: swap`; their OFL license files
live alongside the font assets. Body size inherits the browser default; there is
no explicit site-wide body-size token or geometric modular scale.

### Hierarchy
- **Display:** fluid hero heading, bounded by the display token; maximum width (820px).
- **Headline:** fluid section heading; the author heading has its own smaller role.
- **Skill title / card title:** stronger skill names and smaller principle-card headings.
- **Body / lede:** normal paragraphs and larger introductions; ledes stop at (780px).
- **Tag:** compact bold informational labels; they are not controls.
- **Navigation:** compact links; table body text shares its (14px) size.
- **Table label:** (12px) uppercase headings with tracked letters.
- **Hero copy:** fluid paragraph size from (18px) to (22px).
- **Scorecard title:** (18px) bold header within the evaluation panel.
- **Statistic:** (34px) gold figures with heading-like leading.
- **Author link:** (12px) uppercase monospace links with wider tracking.
- **Code:** installation examples with more generous leading and horizontal overflow.
- **Author title:** the byline only, preserving the sanctioned serif exception.

**The One Byline Rule.** Keep Fraunces confined to the author heading; Chivo
remains the site's primary family.

## Layout

The centered wrapper is `min(1120px, calc(100% - 40px))`, giving (20px) side
gutters. Sections have (86px) vertical padding, reducing to (48px) at
`max-width: 600px`. Grid and split gaps use the named spacing values; cards
keep their own internal padding.

Above (860px), principle cards and statistics use three equal columns; split
sections use `.9fr 1.1fr`. Skill cards use two equal `minmax(0, 1fr)` columns
from (861px) through (1100px), then `1.5fr 1fr 1fr` above (1100px). Card grids
begin (38px) below their introduction. Actions and link groups wrap naturally.

At `max-width: 860px`, those grids become one column; navigation stacks and the
author panel centers in one column with padding (32px 24px). Hero padding changes
from (56px 0 64px) to (28px 0 44px). The implementation has explicit media
boundaries at (600px), (860px), and (1100px).

The scorecard alone retains a minimum table width (860px) inside a scrollable
region whose height is `min(60vh, 36rem)`. Its table cells use (13px 16px) padding;
numeric columns use tabular figures. The FAQ is capped at (72ch).

## Elevation & Depth

Most content is flat, separated by background tone and a fine border. Shadows
are limited to the scorecard, terminal, and author avatar; the featured card's
inset stroke adds emphasis rather than floating it above the page.

### Shadow Vocabulary
- **Scorecard:** `0 16px 42px rgba(0, 0, 0, .08)`.
- **Terminal:** `0 18px 50px rgba(0, 0, 0, .16)`.
- **Author avatar:** `0 12px 30px rgba(0, 0, 0, .2)`.
- **Featured card stroke:** `inset 0 0 0 1px rgba(217, 79, 48, .2)`.

**The Bordered Panel Rule.** Ordinary content cards retain their neutral border
and flat fill; reserve the documented shadows for their existing component roles.

## Shapes

Buttons have gently curved corners; panels and cards share the slightly larger
panel radius. The author panel has a distinct softer corner. Tags are pills;
numbered rule markers, terminal indicators, and the author avatar are circles.
Use the frontmatter radius roles rather than treating every surface as a pill.

The flame is a checked-in raster asset, not a text glyph. It occupies (36px)
in navigation and (60px) within the author's (88px) circular frame. Keep its
intrinsic proportions. The full wordmark image serves social previews rather
than replacing the compact navigation mark. Existing raster sources and byte
checksums are recorded in
`.impeccable/reviews/skills-library/asset-provenance.json`; this work changes no
image bytes and makes no new rights claim.

## Components

### Buttons

Direct link actions use the primary white fill or translucent secondary fill
on charcoal, a one-pixel translucent white border, bold text, and minimum height
(48px). The primary hero action browses the skills; GitHub is the secondary action. Actions wrap with the action gap. Both variants keep visible keyboard
focus; the source defines no distinct button hover, active, or animated state.

### Tags

Informational labels pair the tag surface with steel text, a pill radius, and
minimum height (28px). They neither imply filtering nor expose control states.

### Cards / Containers

Principle cards use the card padding and minimum height (190px). Skill cards
use the skill padding, minimum height (260px), and a vertical flex layout with
(22px) between content and package links. The featured card uses a translucent
ember border and the inset stroke recorded above. Package links remain underlined,
with minimum width and height (44px), wrapping labels, and maximum width (100%).
The nearby installation-help link is bold, underlined, and at least (44px) tall;
it leads to the local installation section.

### Navigation

The compact flame and bold brand name sit beside wrapping (14px) navigation
links. Links have minimum height (44px); navigation becomes stacked below the
existing breakpoint. The skip link appears at keyboard focus, entering the
semantic main content. Dark-surface links retain gold focus outlines.

### Scorecard

A white bordered panel contains a paper header and a dark table header. The
scroll region remains keyboard focusable, with a visible scroll-direction cue
connected through `aria-describedby`. Table headings stick to the top of the
scroll region (`top: 0`, `z-index: 1`). The cue has padding (12px 20px) and a
neutral bottom border. Loading and completion/failure
messages use the existing live status. Keep fallback source links usable when
data cannot load. The scroll region retains the global (3px) steel focus outline
with an inward offset (-3px), keeping the ring inside the clipped panel.

### Installation List

Client-specific installation instructions use a semantic definition list capped
at (78ch), with margin (28px 0). Bold client terms precede descriptions whose
margin is (6px 0 24px). Paragraphs use (8px) bottom spacing; inline code permits
wrapping anywhere so destination paths remain usable at phone widths.

### Terminal

A charcoal panel with a darker toolbar and three small circular indicators
contains a keyboard-focusable, named region for horizontally scrollable code.
The code region uses a gold (3px) focus outline with inward offset (-3px).
Gold marks keys;
green and warm red code text retain their existing limited example roles.
These indicators do not substitute for textual status.

### Author Panel

The warm dark panel combines the circular flame frame, compact Fraunces byline,
muted supporting copy, and wrapping monospace attribution links. Those links
have minimum height (44px) and change to amber with an underline border on hover.
Preserve the byline and source links; do not infer new credentials or claims.

## Do's and Don'ts

### Do:
- **Do** preserve the checked-in flame, its proportions, and compact navigation placement.
- **Do** use Chivo for the interface and reserve Fraunces for the author byline.
- **Do** retain neutral borders, readable text leading, and visible contrasting focus.
- **Do** preserve wrapping actions, native link semantics, and scrollable code or tables.
- **Do** keep brand attribution and package descriptions grounded in repository content.

### Don't:
- **Don't** enlarge the full wordmark into a separate branding section that displaces the first viewport.
- **Don't** spread the author panel's serif or warm palette across ordinary documentation.
- **Don't** turn informational tags into controls without implementing their semantics and behavior.
- **Don't** use color or terminal indicators as the only way to communicate status.
- **Don't** shrink package-link targets below (44px) in either dimension or move the scorecard focus ring outside its clipped panel.
