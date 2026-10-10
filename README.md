<p align="center">
  <img src="assets/branding/primary%20square%20for%20white%20bg.png" alt="Inventing Fire with AI" width="280">
</p>

# Inventing Fire with AI Skills

Reusable skills for software development, shipping, and personalized travel planning.

Part of **[Inventing Fire with AI](https://inventingfirewith.ai)** by **[Richard Crane](https://mvp.microsoft.com/en-US/MVP/profile/10ce0bc0-7536-43f6-b28c-e9601a4a0d0d)** — Microsoft MVP and founder of **[MILL5](https://www.mill5.com)**.

**Landing page:** [chiefinnovator.github.io/inventingfirewithai_skills](https://chiefinnovator.github.io/inventingfirewithai_skills/)

## What it does

| Skill | Codex | Claude Code | GitHub Copilot | Purpose |
|---|---|---|---|---|
| figma-to-flutter | [Skill](skills/codex/figma-to-flutter/SKILL.md) | [Skill](skills/claude/figma-to-flutter/SKILL.md) | [Skill](skills/copilot/figma-to-flutter/SKILL.md) | Capture, convert, and check Flutter against Figma. |
| pragmatic-coder | [Skill](skills/codex/pragmatic-coder/SKILL.md) | [Skill](skills/claude/pragmatic-coder/SKILL.md) | [Skill](skills/copilot/pragmatic-coder/SKILL.md) | Make focused changes with proportionate verification. |
| slam | [Skill](skills/codex/slam/SKILL.md) | [Skill](skills/claude/slam/SKILL.md) | [Skill](skills/copilot/slam/SKILL.md) | Ship through review, CI, merge, and verified cleanup. |
| mcp-pick | [Skill](skills/codex/mcp-pick/SKILL.md) | [Skill](skills/claude/mcp-pick/SKILL.md) | [Skill](skills/copilot/mcp-pick/SKILL.md) | Select project-relevant MCP servers. |
| travel-like-a-local | [Skill](skills/codex/travel-like-a-local/SKILL.md) | [Skill](skills/claude/travel-like-a-local/SKILL.md) | [Skill](skills/copilot/travel-like-a-local/SKILL.md) | Plan local experiences, property stays, and trip logistics. |

`pragmatic-coder` guides coding agents to finish authorized work with minimal changes, proportionate verification, clear evidence, and respect for user choices. It favors simple data, maintainable solutions, relevant security checks, and measured performance work.

Install an entire skill folder, including its resources: use `skills/codex/` or `skills/claude/` for those clients. Download a Copilot folder from `skills/copilot/` and copy the entire folder into your target repository's `.github/skills/`. Invoke `$<skill-name>` in Codex or `/<skill-name>` in Claude Code and GitHub Copilot. In Copilot CLI, reload with `/skills reload` and check `/skills info <skill-name>`. MCP Picker's supported scope depends on the Copilot host; it reports prepared commands separately from applied settings.

For ChatGPT on the web, see the [travel skill export and setup status](docs/migrations/travel_chatgpt_web.md).

Use `$figma-to-flutter` in Codex or `/figma-to-flutter` in Claude Code. See [what it adds to community code generation](docs/research/figma_to_flutter_comparison.md).

Browse [designs, research, evaluations, and migration notes](references.md#local-documents).

## Why this exists

Agent skill libraries grow fast. Too many overlapping skills add context bloat, conflicting advice, and slow decision-making.

`pragmatic-coder` distills the coding behaviors we want most into one compact default skill. It replaces a pile of overlapping coding guidance with a streamlined, high-signal operating standard.

## When to use

Use `pragmatic-coder` for implementation, review, and refactoring. Invoke `$slam` when ready to ship the scoped work. Slam requires repository tools and authenticated GitHub access; inspecting or installing it does not run the shipping workflow.

## Influences

Karpathy-style caution plus Torvalds-style pragmatism around data, simplicity, and regressions. Adds autonomy, TDD, preconditions, security, performance, parallel-agent, cost, contract, research-learning, and skeptical-verification rules.

## Pragmatic Coder Rules

1. **Think Before Coding** — Inspect evidence, preserve scope, and reuse existing authorization
2. **Data First** — Simplify data within compatibility constraints; document meaningful boundaries
3. **Simplicity and Cost First** — Favor maintainability, respect model choices, and reassess failed approaches
4. **Surgical Changes** — Preserve user edits and existing behavior; keep changes tied to the request
5. **Verify, Don't Assert** — Use proportionate checks, finish the requested work, and distinguish evidence from assumptions
6. **Review Smells** — Report concrete consequences and evidence; separate defects from optional improvements

## License

MIT

## Credits

Created by **Richard Crane**, Microsoft MVP and founder of **MILL5**.

- **MILL5:** [mill5.com](https://www.mill5.com)
- **Microsoft MVP:** [Richard Crane](https://mvp.microsoft.com/en-US/MVP/profile/10ce0bc0-7536-43f6-b28c-e9601a4a0d0d)
- **Podcast:** [Inventing Fire with AI](https://inventingfirewith.ai)
- **GitHub:** [@ChiefInnovator](https://github.com/ChiefInnovator)
