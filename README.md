<p align="center">
  <img src="assets/branding/primary%20square%20for%20white%20bg.png" alt="Inventing Fire with AI" width="280">
</p>

# Inventing Fire with AI Skills

Reusable skills for implementing, reviewing, and shipping software.

Part of **[Inventing Fire with AI](https://inventingfirewith.ai)** by **[Richard Crane](https://mvp.microsoft.com/en-US/MVP/profile/10ce0bc0-7536-43f6-b28c-e9601a4a0d0d)** — Microsoft MVP and founder of **[MILL5](https://www.mill5.com)**.

**Landing page:** [chiefinnovator.github.io/inventingfirewithai_skills](https://chiefinnovator.github.io/inventingfirewithai_skills/)

## What it does

| Skill | Purpose |
|---|---|
| [pragmatic-coder (Codex)](skills/codex/pragmatic-coder/SKILL.md) | Implement, debug, review, and refactor with minimal changes and proportionate verification. |
| [pragmatic-coder (Claude Code)](skills/claude/pragmatic-coder/SKILL.md) | The same coding guidance adapted to Claude Code. |
| [slam (Codex)](skills/codex/slam/SKILL.md) | Ship scoped GitHub work through commit, PR, AI review, CI, merge, and verified branch cleanup. |
| [slam (Claude Code)](skills/claude/slam/SKILL.md) | Native Claude shipping workflow with session goal guidance. |
| [mcp-pick (Codex)](skills/codex/mcp-pick/SKILL.md) | Choose MCP servers and installed app integrations per Codex project. |
| [mcp-pick (Claude Code)](skills/claude/mcp-pick/SKILL.md) | Choose which MCP servers stay enabled per Claude Code project. |

`pragmatic-coder` guides coding agents to finish authorized work with minimal changes, proportionate verification, clear evidence, and respect for user choices. It favors simple data, maintainable solutions, relevant security checks, and measured performance work.

Install a skill folder from `skills/codex/` or `skills/claude/` into the matching client's skills directory, including its bundled resources. Invoke `$pragmatic-coder` or `$mcp-pick` in Codex; use `/pragmatic-coder` or `/mcp-pick` in Claude Code.

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
