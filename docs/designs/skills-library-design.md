---
title: Skills library verification and website design
description: Design for complete local checks, reproducible site data, clear installation, and accessible browsing while preserving the existing skill library and brand.
---

# Skills library verification and website design

- Author: ChiefInnovator
- Status: Implemented baseline; homepage scorecard presentation superseded
- Date: 2026-11-02
- Baseline: repository revision `8af960bb310f514f27bf08a63dbeb54dd371af34`

## Current scope update

On November 2, 2026, the owner directed removal of the research scorecard from the
homepage. Its panel, navigation link, installation CTA, table styles, and loader
are removed; the research document and supporting artifact checks remain.
The scorecard presentation and loading steps below record the superseded baseline
and are no longer homepage requirements. Current implementation details live in
the repository's `DESIGN.md` and site visibility guidance.

## Overview

Keep the existing five-skill library, three client packages, static GitHub Pages
site, and Inventing Fire with AI branding. Make the published evidence easier to
trust and the packages easier to install. Close gaps in which existing executable
tests run in CI, keep the scorecard preview tied to the deployed site, and improve
the existing browsing and installation experience on phones and intermediate widths.

The owner confirmed this scope and authorized drafting, independent reviews,
documentation, and implementation without intermediate approval pauses. This is
an improvement to the incumbent system, not a new product or visual identity.

## The Problem

The root test command omits executable tests bundled with Figma-to-Flutter and
the Codex and Copilot MCP Picker packages. A green root run therefore does not
mean all existing Python suites passed. Installation guidance names the matching
client directory without giving Codex and Claude users a concrete destination.
The homepage fetches its scorecard from moving GitHub `main` content rather than
the deployed snapshot. Its package links and phone spacing need rendered review.

Product and visual decisions exist in code and conversation, but there is no
root PRODUCT.md, DESIGN.md, or Impeccable design sidecar. Future edits can repeat
past branding and accessibility mistakes unless those decisions are recorded.

## Goals

1. Provide one documented local/CI command that runs all six existing Python
   unittest suites in isolated processes and reports failures without hiding skipped
   suites. Standalone Flutter SDK acceptance remains separate.
2. Serve scorecard preview data from the same deployed artifact as the page,
   with a check that rejects stale generated data.
3. Give a first-time user an explicit complete-folder installation destination,
   invocation syntax, and discovery check for each supported client.
4. Preserve the compact fire mark, current fonts and colors, factual copy,
   canonical metadata, structured data, and native semantic accessibility.
5. Record product truth, incumbent design tokens, surface constraints, independent
   review findings, and their dispositions in the repository.
6. Demonstrate the new required `feature-only` check on the next genuine feature
   PR; keep main restricted to same-repository develop PRs and the repository's
   cloud Copilot rule restricted to develop, including drafts and new pushes.

## Non-Goals

- No framework migration, new service, login, analytics, theme switch, new skill,
  automatic private-profile store, or booking implementation.
- No change to the five families or intentional client-specific entrypoints.
- No invented user testimonials, model benchmarks, privacy certification, search
  rankings, AI citations, or claim that structural tests prove live host behavior.
- No manual review requests, fake pushes, direct protected-branch changes, or
  changes to unrelated account-wide Copilot preferences.
- No changes to Phoenix adapters or the completed personal Slam consolidation.

## Critical User Journeys

### Choose and install a package

Given a visitor knows their coding client, when they browse a skill and follow
installation guidance, then they can copy the complete folder to the stated
supported location and check discovery without guessing paths or losing resources.

### Assess evidence

Given a visitor opens the scorecard or tests section, when the preview loads or
fails, then its data belongs to the deployed site, loading/result/error states
remain accessible, and source links remain usable without JavaScript.

### Contribute safely

Given a same-repository work branch, when its real PR targets develop, then the
required source guard and all package/site suites run. Main accepts only develop.
Copilot review completion is reported separately from an enabled rule or CI result.

## Technical Plan

Retain the current static HTML/CSS/JavaScript and GitHub Pages/Jekyll deployment.
Keep the source scorecard in its existing Markdown document. A small standard-library
sync utility prefixes its exact bytes with a fixed non-YAML provenance line in a
public text asset, preventing Jekyll from treating its front matter as a page.
The homepage fetches
that relative asset and retains its existing escaped table renderer and fallback.
A check mode detects missing or stale output without modifying it. The asset's
contract is the fixed prefix followed by the canonical Markdown bytes, not equality
between the whole asset and Markdown file. CI builds with the official Jekyll
Pages action and compares the built asset against this contract.

Add a standard-library check runner with an explicit suite list. It invokes each
unittest discovery command in a separate Python process from the repository root,
using the same interpreter and pinned test dependencies as CI. The existing Codex
MCP suite also requires the real Codex CLI for isolated local metadata/configuration
tests; it does not create model threads or call providers. This avoids module
name collisions between the three Figma packages. Run every suite and return a
nonzero status if any suite fails or is missing. This does not invoke agents,
provider APIs, real bookings, or review assignments.

```text
canonical scorecard -> sync utility -> deployed text asset -> existing preview
                          |
                    --check in CI

root + three Figma suites + two MCP suites -> check runner -> local / GitHub CI

feature PR -> develop [feature-only + cloud review] -> main [develop-only] -> Pages
```

Preserve the existing homepage composition. Improve only confirmed usability
issues: package-link targets of at least 44×44 CSS pixels, narrower phone section spacing,
an intermediate two-column skill grid, and
an inward scorecard focus outline if the existing ring clips. These changes must
retain first-viewport branding and keyboard entry. No decorative asset generation
is needed; reuse the checked-in fire imagery and fonts.

Create PRODUCT.md from the confirmed brief and repository facts. Extract DESIGN.md
and `.impeccable/design.json` from the actual implementation, retaining the existing
Fraunces author-panel exception. Record homepage Read mode and its specific constraints
through Impeccable's surface-brief tool. Keep development-only direction and review
metadata outside browser-delivered assets.

Keep raw stage/persona reports and development direction in `.impeccable/` at the
repository root, outside Pages' `docs/` source. Publish only this design and a
curated evidence/disposition page at `docs/evaluations/skills_library_review.md`.
Development-only means excluded from the site build, not private: this is a public
repository, so these records must never contain credentials, personal information,
or machine-specific paths.

## Alternatives Considered

- Keep root-only CI: least work, but leaves already-maintained executable suites
  outside the green result. Rejected because coverage can improve without a new framework.
- Run every suite in one interpreter: fewer processes, but duplicate Figma test
  and helper module names can contaminate imports. Rejected in favor of isolated runs.
- Fetch the scorecard from raw GitHub: avoids a generated copy, but preview content
  can differ from the deployed page. Rejected in favor of byte-checked local data.
- Replace the site or centralize all client packages into a new compiler: would
  expand the architecture and risk host-specific behavior. Outside the confirmed scope.

## Non-Functional Requirements

Preserve package-local references, whole-folder distribution, existing host hooks,
and the private-state exclusion rules. Pin Pillow 13.0.0, whose official package
metadata supports Python 3.11 and newer, for the existing image-test imports; keep
the existing PyYAML pin and add the Codex MCP helper's existing `tomlkit==0.15.2`
dependency. CI installs Node.js 24 and Codex CLI 0.166.0 explicitly.
Local verification requires Codex CLI 0.153.4 or newer; installing 0.166.0 reproduces
the CI environment. No new production runtime dependency is introduced.

Use semantic HTML, valid ARIA, visible focus, and accessible loading announcements.
Verify 320/390/768/1024/1440px layouts and keyboard use. Preserve factual SEO/GEO/AEO
metadata and discovery links; these checks establish eligibility, not indexing.

Test runners must use argument arrays, fixed suite paths, bounded subprocesses,
and no shell interpolation. Generated scorecard output is public editorial material,
never private profile or trip state. It must remain a literal copy, not an executable.

## Evidence and Limits

The baseline has 138 passing root tests. Existing travel fixtures and package checks
are separate from real Claude/Copilot host acceptance, connected private stores,
assistive technology, live bookings, and search indexing. Record exact commands,
revision, viewport, and browser for new evidence. Do not turn an unrun check into
a pass. At the design baseline, the `feature-only` rule's first genuine PR execution
was unobserved. It subsequently passed on draft PR #17 at candidate
`24fe7bacdfa566893fdabd7e276f89fa839ff0d9`; cloud Copilot also completed an automatic
review of that draft. Account-wide personal automatic-review preferences are separate
from repository rules and will not be changed by this work.

## Detailed Implementation Plan

### Installation contract

Use the same facts in the README and homepage. These are vendor-supported
destination templates, not references to files on a maintainer's computer.
Copy the entire named directory, preserving its resources. A discovery check
does not invoke the skill or authorize Slam to ship anything.

| Client | Source | Destination | Invocation | Discovery and observable success |
|---|---|---|---|---|
| Codex, personal | `skills/codex/<skill-name>/` | `~/.agents/skills/<skill-name>/` | `$<skill-name>` | Start a fresh Codex session; open the `$` skill picker and confirm the skill name is listed. Exit the picker without submitting. |
| Claude Code, personal | `skills/claude/<skill-name>/` | `~/.claude/skills/<skill-name>/` | `/<skill-name>` | Start a fresh Claude Code session; open the `/` command picker and confirm the skill name is listed. Exit without invoking it. |
| Copilot CLI, repository | `skills/copilot/<skill-name>/` | `.github/skills/<skill-name>/` in the target repository | `/<skill-name>` | From that repository run `/skills reload`, then `/skills info <skill-name>`; verify the reported skill points to the copied folder and is enabled. |

For example, the complete `skills/codex/pragmatic-coder/` folder becomes
`~/.agents/skills/pragmatic-coder/`, including SKILL.md and supporting resources.
Do not create a second Codex personal copy in a legacy skills root. Do not replace
intentional project adapters. Other Copilot hosts may expose different discovery
controls; the procedure above makes a specific claim for Copilot CLI.

### File changes

1. **Design and review artifacts:** maintain this document, then store the five
   stage reports, raw persona reports, a consolidated review, and a finding-to-fix
   matrix in `.impeccable/reviews/skills-library/`. Use fresh, history-free Goldfish
   reviewers; parent synthesis must preserve disagreements and unresolved limits.
2. **Impeccable artifacts:** create `PRODUCT.md`, `DESIGN.md`, and
   `.impeccable/design.json`; create the homepage surface brief using
   `impeccable surface-brief write docs/index.html`. Record actual colors,
   typography, spacing, and components in DESIGN.md; record breakpoints, shadows,
   transitions, full component snippets, and narrative in the sidecar.
   Treat these as development documents rather than page content.
3. **Test runner (new `scripts/check_repository.py`):** run root discovery and
   discoveries in `skills/{codex,claude,copilot}/figma-to-flutter/scripts`,
   `skills/codex/mcp-pick/tests`, and `skills/copilot/mcp-pick/tests`. Resolve paths
   from the runner location; refuse missing suites, run all six, collect exit
   codes, and exit nonzero on any failure. Check the Codex version before its MCP
   suite and report a missing/incompatible CLI as that suite's failure while
   continuing the others. The maintainer runner supports macOS/Linux; refuse other
   operating systems clearly rather than claim unverified process cleanup. Start
   each suite in a new POSIX session/process group. On its 180-second timeout,
   send SIGTERM to the group, allow up to five seconds, send SIGKILL to any
   remaining group members, and reap the direct child before continuing. Group
   cleanup covers the existing helpers' normally inherited descendants; explicitly
   detached processes are outside this contract. Test a disposable descendant
   that ignores SIGTERM. Print an explicit failed/timed-out suite name. Do not claim live Flutter acceptance
   from tests that use disposable fixtures.
4. **Dependencies and CI:** add Pillow 13.0.0 and the existing helper dependency
   `tomlkit==0.15.2` to `tests/requirements.txt`.
   Change `.github/workflows/skills-checks.yml` to install Node.js 24 with a
   commit-pinned setup-node action, install `@openai/codex@0.166.0`, and call the
   unified runner with Python 3.14. Keep read-only permissions, branch/event coverage, and the existing
   check name. Add a separate `Pages artifact check` job using the commit-pinned
   official `actions/jekyll-build-pages` action with `source: docs` and
   `destination: _site`. Install Python there and run
   `python scripts/sync_site_data.py --check --built-dir _site` after the real
   Jekyll build. Keep that job's timeout at 10 minutes. Set the package job
   timeout to 25 minutes to cover six 180-second suite
   limits, five-second cleanup grace periods, and dependency setup. Record normal
   measured duration separately; this is a failure-handling ceiling, not a target.
5. **Site data (new `scripts/sync_site_data.py` and
   `docs/assets/data/referenced-skills-scorecard.txt`):** copy
   `docs/evaluations/referenced_skills_scorecard.md` unchanged after the fixed UTF-8
   prefix `Generated scorecard snapshot. Source: docs/evaluations/referenced_skills_scorecard.md`
   and two newline bytes. This prevents front-matter/Liquid processing while the
   existing table parser ignores the non-table line. Default mode writes;
   `--check` compares the expected prefix-plus-source bytes and exits nonzero for
   a missing/different asset. `--built-dir` is allowed only with `--check` and
   compares `<built-dir>/assets/data/referenced-skills-scorecard.txt` too.
   The unified runner checks freshness before tests and still reports test results
   if data is stale. Regenerate after source catalog/scorecard edits.
6. **Homepage `docs/index.html`:** replace only the raw-GitHub fetch URL with the
   relative text asset. Keep the existing renderer, escape function, announcements,
   and failure/source-link behavior. Add at least 44px package-link targets,
   48px phone section spacing at 600px and below, an inward scorecard focus ring,
   and a two-column skill grid between 861 and 1100px using equal fractional columns.
   Retain one column at 860px and below and the existing three-column layout above
   1100px. Baseline Chromium at 1024px gives secondary cards about 271px width and
   wraps the Figma heading to two lines; the selected middle layout provides room
   for the package-link row. Check 600/601, 860/861, and 1100/1101px boundaries.
   Show complete-folder Codex/Claude personal paths and Copilot project paths in
   the existing installation section; preserve current branding and factual claims.
7. **Documentation and catalog:** update `README.md` with the unified check
   command, Codex CLI prerequisite/reproduction command, and concise installation destinations; update
   `docs/evaluations/site_visibility.md` and
   `docs/evaluations/travel_like_a_local_evaluation.md` to describe actual check
   coverage. Add Google EGM and Impeccable source references to `references.md`
   and `docs/evaluations/referenced_skills_scorecard.md`, marking assessments as
   editorial rather than benchmark results. Update `docs/sitemap.xml` and
   `docs/llms.txt` for the new public design/review index, without changing host-root
   crawler policy. Keep raw review transcripts out of the discovery index.
8. **Regression tests:** add `tests/test_repository_checks.py` for subprocess
   isolation, missing/failing/timed-out suite reporting, descendant termination,
   and data-check aggregation,
   using disposable fixtures. Extend `tests/test_pages_visibility.py` for the
   deployed local data asset and exact prefix-plus-source parity. Cover a source
   fixture with YAML front matter and Liquid syntax, stale/missing built output,
   and the invariant that generated data cannot begin with YAML front matter. Extend
   `tests/test_pages_accessibility.py` only where structural assertions are useful;
   verify touch sizing and focus visibility in the browser rather than claiming
   static tests establish them. Do not modify distributed skill implementation.
9. **Independent Impeccable review:** after the reviewed design and required docs
   exist, use two isolated assessments of the same local homepage: visual design,
   and Impeccable's anti-pattern detector supplemented by rendered browser checks.
   Capture their reports and the synthesized verdict
   in `.impeccable/reviews/skills-library/impeccable-review.md`. Publish curated
   findings, evidence, and limits in `docs/evaluations/skills_library_review.md`. Apply all valid
   in-scope findings, document exclusions, and recheck the changed behaviors.
10. **Delivery:** leave the EGM design-only workflow before production edits.
    Commit on the feature branch, open a PR into develop, observe `feature-only`,
    CI, and the automatic Copilot review on its exact head, resolve valid findings,
    and merge without bypassing protections. Promote develop to main by a separate
    PR when publishing the website changes; verify Pages build and deployed assets.
    Use merge commits, synchronize local branches, and safely remove only merged
    feature branches. Never manually request a review or manufacture a push.

## Verification and Rollback

### Stable delivery phases

The numbered file list above is not a sequence of independently shippable states.
Use these atomic phases and their verification gates:

1. **Design records:** finish the EGM reports, PRODUCT.md, DESIGN.md, sidecar, and
   surface brief together. Run `git diff --check` and the existing visibility
   tests with pinned requirements. Expected: no whitespace errors or broken public
   document links. No production workflow or homepage changes in this phase.
2. **Verification infrastructure:** land the check runner, Python requirements,
   Node/Codex CI setup, data sync utility, initial text asset, runner regressions,
   and CI invocation/build verification as one change set. With Git/Bash, Node.js 24 and Codex CLI
   0.166.0 available, run `uv run --no-project --python 3.14 --with-requirements
   tests/requirements.txt python scripts/check_repository.py`. Expected: fresh
   data and all six isolated unittest suites pass, including descendant-timeout fixtures;
   missing prerequisites fail explicitly instead of silently skipping suites.
3. **Website and documentation:** apply the scoped homepage fixes, installation
   contract, source catalog and editorial scorecard additions, public evidence page,
   sitemap and reading index together. Run `python scripts/sync_site_data.py`,
   then `python scripts/sync_site_data.py --check`, root visibility/accessibility
   tests with pinned requirements, and rendered checks at the specified widths
   and breakpoint edges. Expected: exact prefix-plus-source parity, preserved metadata and
   five-skill inventory, no horizontal overflow, 44px package-link targets, and
   visible scorecard focus. Package code is unchanged in this phase.
4. **Review and release:** complete isolated Impeccable assessments, implement
   accepted fixes, refresh the design record to the final code, run affected
   checks and the complete command, and observe required checks plus automatic
   Copilot review on the final PR head. Promote only the verified develop branch
   to main. Expected: both PR merges are verified, Pages succeeds, and deployed
   artifacts match the approved source. Record real host/assistive-technology
   acceptance and indexing as unverified unless separately exercised.

Run the complete local command with pinned dependencies, then CI. Compare source
and ZIP parity, verify the scorecard asset byte for byte, and inspect desktop/phone
screens plus keyboard loading, success, and failure states. Check all added public
document URLs, canonical metadata, and deployed asset bytes after publishing.

Changes are additive or localized. A revert PR can restore the old check command,
data source, and CSS without changing skill content. Do not weaken the branch
rules or enable direct pushes to roll back. Retain private backups of personal
skill installations if they need changes; none are planned here.

## Sources

- [Repository overview](https://github.com/ChiefInnovator/inventingfirewithai_skills/blob/develop/README.md)
- [Repository instructions](https://github.com/ChiefInnovator/inventingfirewithai_skills/blob/develop/AGENTS.md)
- [Google EGM](https://github.com/google/elephant-goldfish-model)
- [Impeccable](https://github.com/pbakaus/impeccable)
- [Pillow package metadata](https://pypi.org/project/Pillow/13.0.0/)
- [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Copilot CLI skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
