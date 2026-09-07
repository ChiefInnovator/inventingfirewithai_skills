# Inventing Fire with AI Skills Project

## What this is

Reusable coding and shipping skills. Pragmatic Coder combines Torvalds-style pragmatism with Karpathy-style caution; Slam carries scoped GitHub work through review and merge.

## Rules

- No mocks in implementation code. Mocks in tests only.
- No redundant files — one README at the root, no per-skill READMEs.
- Keep references out of README. Do not add a references section; put source links in `references.md`.
- When adding a skill-like reference, add it to `references.md` and score it in `docs/referenced_skills_scorecard.md`.
- Act; don't ask for confirmation on obvious next steps.

## Structure

```
skills/claude/pragmatic-coder/SKILL.md   — the skill
skills/codex/slam/SKILL.md              — portable shipping workflow
skills/codex/mcp-pick/SKILL.md
skills/claude/mcp-pick/SKILL.md
skills/claude/slam/SKILL.md
skills/codex/pragmatic-coder/SKILL.md
tests/                            — local helper tests
AGENTS.md                          — Codex instructions
CLAUDE.md                          — Claude instructions
README.md                          — short project overview
references.md                      — canonical source links
docs/                              — research references
```

## Skill

`pragmatic-coder` — simple, safe, verified code changes. See [SKILL.md](skills/claude/pragmatic-coder/SKILL.md).

`slam` — scoped commit, PR, review, merge, and verified cleanup. See [SKILL.md](skills/claude/slam/SKILL.md). Reading or editing it does not authorize shipping.
