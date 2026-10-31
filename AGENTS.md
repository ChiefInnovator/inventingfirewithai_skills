# Inventing Fire with AI Skills

Reusable coding, shipping, Figma-to-Flutter, and travel skills for Codex, Claude Code, and GitHub Copilot. This is the shared repository instruction file; Claude can read `AGENTS.md` directly.

## Rules

- Keep `README.md` short; no per-skill READMEs or redundant docs. Put source links in `references.md`, research under `docs/`, and operational rules here.
- Keep docs and GitHub Pages optimized for SEO, GEO, and AEO: crawlable factual HTML, clear answers, canonical/social metadata, accurate structured data, and working discovery links. Run visibility regression checks and verify the deployed output; respect host-root crawler-policy scope and never promise rankings or AI citations.
- Keep Pages accessible: use semantic HTML, appropriate ARIA names/states/live announcements, descriptive links and image alternatives, visible keyboard focus, and a working skip link. Run accessibility regression checks and verify keyboard use at desktop and phone widths; do not add redundant or invalid ARIA.
- Keep Pragmatic Coder compact; add capability only when it earns its token cost.
- Do not reference local files outside this repo.
- No mocks in implementation code; mocks stay in tests.
- Add skill-like references to `references.md` and `docs/evaluations/referenced_skills_scorecard.md`.
- Act on obvious next steps; ask only for real blockers.
- Reading, editing, or installing Slam does not authorize shipping.
- Feature branches merge into `develop` by pull request; only `develop` merges into `main`, also by pull request. Never commit or push directly to `develop` or `main`.
- Monitor automatic Copilot review and address valid findings. Honor an explicit user instruction not to wait for Copilot; required GitHub checks, approvals, and branch protections still apply.
- Keep automatic Copilot review enabled for every target branch, including drafts and new pushes, without path exclusions.
- Keep shared Slam references and helpers identical across the three client packages; preserve host-specific entrypoints and Claude hooks. Synchronize authorized installed copies when shipping skill maintenance.

## Layout and use

- `skills/{codex,claude,copilot}/<name>/`: downloadable client packages, not skills installed for this repository.
- Names: `pragmatic-coder`, `slam`, `mcp-pick`, `travel-like-a-local`, `figma-to-flutter`.
- Install entire folders, including resources. Invoke `$<name>` in Codex or `/<name>` in Claude Code and Copilot.
- `tests/`: helper checks; `docs/{designs,research,evaluations,migrations}/`: supporting documents.
