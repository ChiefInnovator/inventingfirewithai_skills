# Impeccable synthesized review — skills library

Reviewed November 2, 2026, against candidate `24fe7bacdfa566893fdabd7e276f89fa839ff0d9`.
Assessment A completed its independent design critique before Assessment B released
its independent detector/browser evidence. Both used fresh agent contexts and
isolated headless Chrome sessions; neither read the other assessment.

## Combined verdict and priorities

The incumbent Read-mode identity is coherent. Retain branding, static architecture,
factual copy, five families, and all fifteen package destinations. Assessment A
scored **29/40** across ten applicable Nielsen heuristics. No P0 or P1 was found.
The score describes the reviewed candidate; later fixes do not imply a rescore.

| ID | Priority | Finding | Authorized disposition |
| --- | --- | --- | --- |
| I1 | P2 | Package choices lack adjacent installation guidance | Add a local install route at the library decision point. |
| I2 | P2 | Long scorecard loses column context | Sticky column headings and an explicit horizontal-scroll cue; keep native scrolling. Do not pin a wide name column over the phone reading area. |
| I3 | P2 | Hero primary emphasis sends readers to source before browsing | Exchange existing button emphasis, retaining text and destinations. |
| I4 | P2 | Overflowing terminal depends on Chrome automatic focus behavior | Explicit named keyboard region with inward visible focus; verify native scrolling. |
| I5 | P3 | Existing palette/type values missing from normative metadata | Record actual semantic colors and type steps; preserve the approved visual system. |
| I6 | P3 | Desktop heading has a lonely final word | Apply scoped heading balancing if it preserves responsive hierarchy. |
| I7 | False positive | Static detector reports a black Video Downloader underline | Actual rendered underline is documented amber through currentColor. Persist only this file/value exception. |

## Independent detector and runtime evidence

Assessment B recorded zero primary static findings and ten advisories: six color
and four font-size metadata mismatches. Five colors and four type steps need
documentation; the black underline is a verified false positive. The existing
Fraunces author-byline exception remains sanctioned and unchanged. Raw results are
in `detector.json`, with repository-relative paths. Eight live-detector minor
typographic observations were assessed contextually, without replacing the brand.

Rendered checks covered 320, 390, 600, 601, 768, 860, 861, 1024, 1100, 1101, and
1440 CSS px. No page overflow occurred; the flame was 36px in the first viewport;
all fifteen package targets were at least 44px tall. Real keyboard interaction
verified skip-link entry and two-axis scorecard scrolling. Actual delayed,
successful, and failed asset requests exercised the unchanged application handlers
and their live-region/busy/fallback states. This verifies DOM semantics, not
audible assistive-technology announcements.

Axe-core 4.14.0 reported one violation at 320px, the terminal focusability finding
I4, and none at 1440px. Chrome already tabs to this overflowing pre automatically;
Safari was not run. Eight contrast checks were incomplete for symbolic glyphs;
computed green/red contrast was 8.81:1 and 7.48:1, respectively. These were not
reported as contrast failures or a complete WCAG audit.

Local served HTML and scorecard bytes matched source. No deployed Pages, physical
device, Safari, screen-reader, search-indexing, AI-citation, or live host-install
acceptance is established by these checks. Both assessment browser sessions and
the temporary detector server were closed; no user browser/profile was accessed.
No user-visible detector overlay was claimed.

## Full independent design assessment

# Assessment A — skills library design review

Method: isolated design-review sub-agent (`impeccable_assessment_a`).
Target: `docs/index.html`. Mode: Read. Assessment date: 2026-11-02.

This assessment was completed without detector output, Assessment B, or previous review reports. The incumbent fire identity, Chivo typography, static HTML/Jekyll architecture, factual copy, and dark author panel are the governing constraints.

## Design specificity verdict

The page feels like an authored developer library. The compact layered flame, charcoal surfaces, blunt Chivo headings, cool paper canvas, restrained ember emphasis, and warmer author panel form a coherent workshop identity. The concrete skill names, three client packages per family, discovery checks, and careful evidence limits give the content considerably more specificity than the otherwise familiar hero-and-card structure.

The card and statistics composition is conventional, but that is appropriate for a Read surface. Replacing it with a more expressive concept would increase effort without improving the task. The best opportunity is to make the existing browse → choose client → install route more continuous.

## Overall impression

Readable, credible, and unusually careful about what its evidence establishes. The principal weakness is the distance between selecting a package and seeing how to install it. The scorecard is accessible to keyboard entry, but its long two-axis scroll loses reading context.

## Nielsen heuristic scores

Scores describe this static reading and installation-discovery surface, not a stateful application. No heuristic needed an applicability exemption.

| # | Heuristic | Score | Evidence and limitation |
|---|---|---:|---|
| 1 | Visibility of system status | 3/4 | Scorecard announces loading and completion; loaded DOM has `aria-busy="false"`. Native anchors expose location in the URL. No active navigation indication on the long page. |
| 2 | Match between system and real world | 3/4 | Familiar client names, useful skill descriptions, and explicit copy-to destinations. Some terms such as MCP assume the intended developer audience. |
| 3 | User control and freedom | 3/4 | Native links and browser Back work; no modal or forced onboarding. The scrollable scorecard can be entered and left without a keyboard trap. |
| 4 | Consistency and standards | 3/4 | Repeated package-link groups, native underlined links, coherent typography and spacing. The primary hero emphasis favors repository browsing over the declared browse/select task. |
| 5 | Error prevention | 3/4 | Whole-folder instructions, host-specific destinations, and explicit non-invoking discovery checks prevent meaningful mistakes. Installation guidance is distant from package choice. |
| 6 | Recognition rather than recall | 2/4 | Names and clients are visible in cards, but the user must carry the selected family/client from the cards or GitHub into generic installation instructions farther down the page. |
| 7 | Flexibility and efficiency of use | 3/4 | Direct section anchors, direct package-folder links, a working skip link, and keyboard activation offer useful shortcuts. The local installation route is absent at the card decision point. Application keyboard shortcuts would not be warranted here. |
| 8 | Aesthetic and minimalist design | 3/4 | Strong hierarchy, restrained accents, readable cards, and no competing decoration. The inline reference table adds substantial density before installation. |
| 9 | Recognize, diagnose, and recover from errors | 3/4 | Source inspection shows a plain-language failed-preview message, preserved markdown link, and live failure announcement. That failure path was not induced in this assessment, so rendered failure acceptance is unverified. |
| 10 | Help and documentation | 3/4 | Useful installation instructions, FAQ, evidence links, and bounded claims. Help is comprehensive but not sufficiently contextual at the package-selection moment. |
| **Total** | | **29/40** | **Good. Ten applicable heuristics; no N/A scores.** |

## What's working

1. **Identity stays compact and legible.** At 390×844, the flame and brand name remain in the first viewport, both hero actions remain visible, and the text is comfortably readable. At 1024×900 and 1440×1000, the restrained dark/light rhythm and readable line lengths retain that clarity. The author panel adds a distinct, credible ending without spreading its serif style through the interface.
2. **Package choice is concrete.** Each family has a purpose and the same three underlined client links. The phone layout keeps the first package choices together; measured first-card links were 44px high and approximately 49px, 97px, and 55px wide. The sampled Codex link reached the correct public GitHub package folder, and browser Back returned to the skills section.
3. **Verification limits are part of the reading experience.** Editorial scores are distinguished from behavioral benchmarks, offline tests from live acceptance, and discovery from execution. The warning against invoking Slam just to test installation gives reassurance at the point where an accidental action would matter.

## Priority issues

No P0 or P1 issue was observed. These three P2 refinements have concrete user value; they do not require a replacement concept, service, framework, or new factual claim.

### 1. [P2] Installation guidance is separated from package selection

- **Evidence:** `docs/index.html:934` begins the first package group; the five groups lead directly to GitHub. Installation starts at `docs/index.html:1071`. At 390×844, the skills section begins around page y=1432 and installation around y=6769. At 1440×1000 they begin around y=1037 and y=4386 respectively. The intervening standard and scorecard sections are useful reading, but they are not installation steps. The top navigation does provide a working Install shortcut, although it is no longer visible while reading the cards.
- **Why it matters:** A visitor can choose a family and client, leave for its source folder, and only later discover the destination path and discovery check. That creates an avoidable memory bridge in the primary task. This is friction, not a broken package link or proof that installation fails.
- **Scoped fix:** Place a clearly named in-page link to `#install` at the library/package decision point, or bring the existing installation summary alongside that decision. Keep every host-specific path, full-folder requirement, discovery check, and source destination intact.
- **Suggested command:** `$impeccable onboard`, followed by `$impeccable polish`.

### 2. [P2] The scorecard loses column context during scrolling

- **Evidence:** `docs/index.html:653` defines the bounded scroll region; `docs/index.html:662` defines the table with an 860px minimum width. At 390×844 the region was 348px wide, its content 860px wide, and it held 137 rows with approximately 10,422px of scroll content. Its height was 506px. Keyboard ArrowRight and PageDown worked; after one PageDown the table had scrolled 466px and all column headings were out of view. Horizontal movement also clips the skill names. The inward 3px steel focus ring remained clearly visible.
- **Why it matters:** Reading a reason or numeric value requires remembering an offscreen heading and sometimes the associated skill name. Two-axis scrolling makes that harder on a phone, especially when the enclosing document also scrolls. The existing markdown alternative is a useful escape, so this is not a blocking accessibility finding.
- **Scoped fix:** Keep column headings visible while the table scrolls and make horizontal overflow discoverable with a concise visible cue. Evaluate retaining row-name context without consuming the phone's usable reading width. Preserve the bounded region, native keyboard scrolling, inward focus ring, live status, and source fallback.
- **Suggested command:** `$impeccable adapt`, followed by `$impeccable polish`.

### 3. [P2] Hero emphasis sends the strongest signal to GitHub

- **Evidence:** `docs/index.html:898` gives “View on GitHub” the solid primary button; “Browse all five skills” uses the quieter secondary treatment at `docs/index.html:899`. This hierarchy is visible at all three inspected widths. Both links work and both remain visible on the phone.
- **Why it matters:** The surface contract makes selecting a skill/client the primary next action. The strongest visual action instead sends the visitor away before that choice. Developers intentionally seeking source still need the GitHub route, but it need not outrank the library itself.
- **Scoped fix:** Exchange the two button emphasis roles while preserving their wording, destinations, order if required, wrapping, and focus treatment.
- **Suggested command:** `$impeccable layout`, followed by `$impeccable polish`.

## Cognitive load

**Two checklist failures: moderate cognitive load.** The load is concentrated in navigation choice and the installation memory bridge, not general visual clutter.

| Checklist | Result | Observation |
|---|---|---|
| Single focus | Pass | The hero has two actions and the card area has one understandable selection task. |
| Chunking | Pass with caveat | Each card groups a purpose with three client choices. Five families are a small, fixed inventory; the six principle cards are supporting reading, not six required workflow steps. |
| Grouping | Pass | Borders, proximity, and consistent package groups clearly associate each client choice with its skill. |
| Visual hierarchy | Pass | Headings, descriptions, and links are readily distinguished. Hero emphasis is a local priority mismatch, not a collapse of hierarchy. |
| One thing at a time | Pass | A visitor can read a family before choosing its client; there is no simultaneous form or setup demand. |
| Minimal choices | **Fail** | Eight top navigation links exceed four visible options. On desktop there are five family choices; the 15 package links are meaningfully grouped as three per family and should not be treated as 15 unrelated choices. The author panel also has six peripheral links. |
| Working memory | **Fail** | The chosen skill/client is not carried into the distant generic installation instructions. The scrolled scorecard also asks readers to retain column context. |
| Progressive disclosure | Pass with caveat | Reading is divided into sections and the full scorecard is height-bounded with a source alternative. It remains a large inline evidence block before installation; no new accordion or hidden content is necessary to fix the identified friction. |

The intrinsic load is real: five skills, three clients, and different destination/discovery rules. The repeated client pattern and explicit copy/check instructions support learning. Reduce the avoidable cross-section recall and table orientation cost without hiding the product inventory or adding a client-selection application.

## Emotional journey

- **Entry:** Clear branding, practical language, and visible browse/source routes create confidence. The phone's 190px navigation is substantial, but the entire hero action group still appears within the first viewport.
- **Choice:** Concrete purpose statements and predictable client groups make selection feel manageable. The featured coding standard supplies a useful default without concealing the other families.
- **Valley:** Leaving for a GitHub folder before seeing installation guidance interrupts momentum. Reading the long scorecard creates a second, optional valley as its headings disappear during nested scrolling.
- **Reassurance and ending:** Whole-folder requirements, non-invoking checks, and evidence limits reduce the risk of overconfidence. The warm author panel closes with recognizable attribution and useful links. No fabricated completion state is needed for a static page that cannot observe installation.

## Persona red flags

- **Jordan, first-time skill user:** The package links are easy to recognize, but there is no adjacent “how to install” route when choosing one. The generic `<skill-name>` installation examples require carrying the family/client choice across sections or back from GitHub.
- **Sam, keyboard/low-vision reader:** The skip link and desktop Browse action were visibly focusable and keyboard activated successfully; the scorecard accepted ArrowRight and PageDown. The observed red flag is loss of column context within that focused table, not absent keyboard access. Screen-reader behavior and assistive-technology announcements were not tested.
- **Casey, distracted phone reader:** At 390×844 the card stack is approximately 1909px high, and installation begins substantially farther down the document. An interruption after selecting a package can make the next step harder to recover. Touch target size in the sampled package group is a strength.

## Minor observations

- Pragmatic Coder's tag-row spacing places its title lower than adjacent titles at desktop/intermediate widths. Its package links remain aligned with neighbors. This is minor rhythm polish, not a reason to remove its useful category/client tags or alter the grid.
- The eight-link navigation occupies two rows beneath the brand at phone width. It is readable and usable; its 190px height is an efficiency tradeoff, not a first-viewport failure. Avoid adding a menu solely to satisfy an arbitrary option count.
- Repeated “Available” tags carry little differentiation while all five families share that state. Preserve factual copy in this scope; any later removal should be an explicit editorial choice.

## Improvement direction

First connect the library decision point to the existing installation guidance. Then preserve orientation inside the scorecard and align hero emphasis with browsing. Retain the current five-family inventory, card layout, brand assets, fonts, source links, factual descriptions, and bounded evidence claims. Finish with rendered and keyboard checks after the selected refinements.

Questions skipped: owner authorized uninterrupted implementation.

## Evidence and limits

- Read `AGENTS.md`, `PRODUCT.md`, `DESIGN.md`, `.impeccable/surfaces/docs-index-html.md`, the installed Impeccable instructions, and the critique reference's design-review, cognitive-load, heuristic, and persona guidance. No critique ignore file was present. No detector output or other assessment/review report was read.
- Inspected the rendered local homepage at **390×844**, **1024×900**, and **1440×1000** in a fresh, isolated headless Chrome session named `impeccable-a`, using the approved Playwright CLI fallback. No persistent user profile or user browser/account was accessed. The parent reported that browser-host and native Chrome-pipe entry points had already failed; this assessment did not repeat them.
- Inspected first viewports, skills, phone installation, scorecard entry and scrolled state, intermediate card layout, and desktop author ending. DOM measurements showed document width equal to viewport width at the three sampled widths. This is not coverage of every required breakpoint or 320px/768px edge; Assessment A makes no claim about those untested sizes.
- Exercised the phone skip link (focus moved to `main-content`), desktop skip → Browse keyboard route (gold 3px focus; Enter reached `#skills`), phone scorecard keyboard entry/scrolling (steel 3px inward focus), and one public Codex package-folder link plus browser Back. No package was installed, no skill was invoked, and no shipping or account mutation was performed.
- Scorecard success loaded in the browser. Failure recovery was inspected in source only. Assistive technology, real touch input, slow networks, search indexing, deployed Pages parity, full outbound-link coverage, and live host installation acceptance were not verified here.
- Private captures were kept outside the repository with `impeccable-a-` filenames, including desktop/phone first viewport, all three card layouts, phone installation, phone scorecard before/after keyboard scrolling, keyboard focus, and desktop author ending. They are evidence for this run, not new shipping assets. Source and browser artifacts were not modified to install a detector overlay.
- The shared preview server was owned by the parent; this agent did not start or stop it. Only the agent's own browser session was closed. No source files or Git state were changed; this report is the sole repository write.

## Follow-through gate

Implement I1–I6, preserve the narrow I7 exception, then perform a targeted rendered
finish review and the complete six-suite repository check. Retain the independent
reports as historical evidence and record final outcomes separately.

Questions skipped: owner authorized uninterrupted implementation.

## Final disposition

I1–I6 are implemented; I7 is narrowly preserved as a verified false-positive
exception. Final configured detector returned zero findings. Targeted real browser
checks and axe scans passed at the recorded widths; the separate file-only finish
reviewer returned **ship**, with all seven findings resolved and no visible
regression. No new heuristic score or full accessibility certification is claimed.
Final unified verification passed 487 tests, zero skips/failures. See the separate
browser and finish reports for exact evidence and limits.
