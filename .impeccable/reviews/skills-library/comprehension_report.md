## What this proposes

The design preserves the existing skill library, client packages, static website, and branding while improving verification, installation guidance, and responsive browsing. A unified runner will execute all six existing Python suites in separate processes, and a byte-checked local scorecard asset will keep previews consistent with the deployed website. Product and design documents, independent reviews, browser checks, and protected PR delivery will record and validate the changes.

## How the existing system works, per this document

The repository distributes five skill families across Codex, Claude, and Copilot packages and publishes a static GitHub Pages/Jekyll website. Root test discovery currently omits several package suites, while the homepage fetches scorecard content from moving GitHub `main`. Installation destinations and recorded product/design decisions are incomplete. Feature work targets develop before promotion to main; repository Copilot review is configured for develop, and the first genuine execution of the `feature-only` check remains unobserved.

## Read receipt

- Upstream persona, read from the installed Google EGM plugin: `agents/comprehension.md` — complete.
- Target: `docs/designs/skills-library-design.md:1–248` — complete.
- Feature scope: lines 1–162; detailed scope: lines 163–248.
- No additional referenced files, other review reports, or private memory read.

## Findings

### C1 — Major: Public versus development-only review artifacts is unclear

**Affected scope:** Technical Plan, Detailed Implementation Plan items 1 and 7; lines 119–123, 165–168, and 207–209.

**Evidence:** The plan requires development-only “direction and review metadata” to remain outside browser-delivered assets, then places stage reports, raw persona reports, and review synthesis under `docs/designs/skills-library-review/`. It also introduces a public design/review index while excluding raw transcripts only from the discovery index.

**Rationale:** A fresh reader cannot determine which review artifacts are intended for public delivery. Excluding transcripts from discovery does not establish that they are excluded from the deployed artifact. Define the public versus development-only boundary and explain how the raw reports satisfy it.

## Limitations

This review assesses document self-containment and clarity. It does not validate implementation, external links, package behavior, browser rendering, repository rules, or deployment. No writes, tests, builds, or Git/GitHub mutations were performed.
