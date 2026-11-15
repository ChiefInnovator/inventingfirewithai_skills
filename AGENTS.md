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
- Feature branches belong to this repository and use `feature/`, `feat/`, `fix/`, `bugfix/`, `hotfix/`, `improve/`, `chore/`, `docs/`, `test/`, `refactor/`, `perf/`, `build/`, `ci/`, or `style/` prefixes.
- Monitor automatic Copilot review and address valid findings. Honor an explicit user instruction not to wait for Copilot; required GitHub checks, approvals, and branch protections still apply.
- Keep cloud Copilot code review active only for `refs/heads/develop`, including drafts and new pushes, without path exclusions. Do not target `main` or use `~DEFAULT_BRANCH`.
- Each skill has one package that must work unchanged in Codex, Claude Code, and GitHub Copilot. Keep host-specific steps in a clearly labeled section or a per-host reference, never in a per-client copy. Preserve Slam's Claude Stop hook. Synchronize authorized installed copies when shipping skill maintenance.
- Keep entrypoints within the token budgets in `tests/test_skill_budgets.py`; raise a budget only with a stated reason.

## Layout and use

- `skills/universal/<name>/`: downloadable packages shared by all three clients, not skills installed for this repository.
- Names: `pragmatic-coder`, `slam`, `mcp-pick`, `travel-like-a-local`, `figma-to-flutter`.
- Install entire folders, including resources. Invoke `$<name>` in Codex or `/<name>` in Claude Code and Copilot.
- `tests/`: helper checks; `docs/{designs,research,evaluations,migrations}/`: supporting documents.
