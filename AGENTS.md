# Inventing Fire with AI Skills

Reusable coding, shipping, Figma-to-Flutter, and travel skills for Codex, Claude Code, and GitHub Copilot. This is the shared repository instruction file; Claude can read `AGENTS.md` directly.

## Rules

- Keep `README.md` short; no per-skill READMEs or redundant docs. Put source links in `references.md`, research under `docs/`, and operational rules here.
- Keep Pragmatic Coder compact; add capability only when it earns its token cost.
- Do not reference local files outside this repo.
- No mocks in implementation code; mocks stay in tests.
- Add skill-like references to `references.md` and `docs/evaluations/referenced_skills_scorecard.md`.
- Act on obvious next steps; ask only for real blockers.
- Reading, editing, or installing Slam does not authorize shipping.
- All check-ins use a feature branch and a pull request into `main`; never commit or push directly to `main`.
- Wait for GitHub Copilot review on the current PR head; address valid findings and pass required checks before merging. Do not bypass repository rules.
- Keep automatic Copilot review enabled for every target branch, including drafts and new pushes, without path exclusions.

## Layout and use

- `skills/{codex,claude,copilot}/<name>/`: downloadable client packages, not skills installed for this repository.
- Names: `pragmatic-coder`, `slam`, `mcp-pick`, `travel-like-a-local`, `figma-to-flutter`.
- Install entire folders, including resources. Invoke `$<name>` in Codex or `/<name>` in Claude Code and Copilot.
- `tests/`: helper checks; `docs/{designs,research,evaluations,migrations}/`: supporting documents.
