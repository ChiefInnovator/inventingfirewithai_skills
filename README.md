# pragmatic-coder

Use for simple, safe, verified implementation, review, and refactor work.

Part of **[Inventing Fire with AI](https://inventingfirewith.ai)** by **[Richard Crane](https://mvp.microsoft.com/en-US/MVP/profile/10ce0bc0-7536-43f6-b28c-e9601a4a0d0d)** — Microsoft MVP and founder of **[MILL5](https://www.mill5.com)**.

**Landing page:** [chiefinnovator.github.io/inventingfirewithai_skills](https://chiefinnovator.github.io/inventingfirewithai_skills/)

## What it does

`pragmatic-coder` makes coding agents behave like pragmatic senior engineers by default: no guessing, little or no code, data-first design, surgical edits, verified changes, security and precondition checks, performance discipline, contract restraint, parallel-work boundaries, and cost-aware model use.

## Why this exists

Agent skill libraries grow fast. Too many overlapping skills add context bloat, conflicting advice, and slow decision-making.

`pragmatic-coder` distills the coding behaviors we want most into one compact default skill. It replaces a pile of overlapping coding guidance with a streamlined, high-signal operating standard.

## When to use

Implementation, review, or refactor tasks.

## Influences

Karpathy-style caution plus Torvalds-style pragmatism around data, simplicity, and regressions. Adds autonomy, TDD, preconditions, security, performance, parallel-agent, cost, and contract rules.

## Rules

1. **Think Before Coding** — Research first; no guessing; ask only for blockers
2. **Data First** — Design data before code; use interfaces only for real seams
3. **Simplicity and Cost First** — Little or no code; cheapest model likely to verify
4. **Surgical Changes** — Touch required lines; avoid overlapping parallel edits
5. **Verify, Don't Assert** — One public-interface failing test at a time; test preconditions, security, and performance
6. **Review Smells** — Flag empty abstractions, pointless interfaces, hostile APIs, ceremony, bad data shapes, unexplained mechanisms, layered workarounds, and unsupported claims
7. **Constraints** — Don't break existing behavior; mocks in tests only

## License

MIT

## Credits

Created by **Richard Crane**, Microsoft MVP and founder of **MILL5**.

- **MILL5:** [mill5.com](https://www.mill5.com)
- **Microsoft MVP profile:** [Richard Crane](https://mvp.microsoft.com/en-US/MVP/profile/10ce0bc0-7536-43f6-b28c-e9601a4a0d0d)
- **Podcast:** [Inventing Fire with AI](https://inventingfirewith.ai)
- **GitHub:** [@ChiefInnovator](https://github.com/ChiefInnovator)

## References

- Andrej Karpathy Skills: https://github.com/forrestchang/andrej-karpathy-skills
- Linus Torvalds Skills: https://github.com/leopiney/linus-torvalds-skills
- Referenced Skills Scorecard: `docs/referenced_skills_scorecard.md`
- Referenced Skills Audit: `docs/referenced_skills_audit.md`
- TDD Skills References: `docs/tdd_skills_references.md`
- Matt Pocock TDD Skill: https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md
- Matt Pocock TDD Tests Guidance: https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/tests.md
- Matt Pocock TDD Interface Design: https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/interface-design.md
- Addy Osmani Agent Skills TDD: https://github.com/addyosmani/agent-skills/blob/main/skills/test-driven-development/SKILL.md
- Obra Superpowers TDD: https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md
- Alireza Rezvani TDD Guide: https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/tdd-guide/SKILL.md
- mfranzon TDD: https://github.com/mfranzon/tdd
- morodomi TDD Skills: https://github.com/morodomi/tdd-skills
- Performance Skills References: `docs/performance_skills_references.md`
- Addy Osmani Performance Optimization Skill: https://github.com/addyosmani/agent-skills/blob/main/skills/performance-optimization/SKILL.md
- Addy Osmani Web Quality Skills: https://github.com/addyosmani/web-quality-skills
- Vercel React Best Practices Skill: https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md
- Callstack React Native Best Practices Skill: https://github.com/callstackincubator/agent-skills/blob/main/skills/react-native-best-practices/SKILL.md
- perf lighthouse Skill: https://github.com/christophacham/agent-skills-library/blob/main/skills/web-dev/perf-lighthouse/SKILL.md
- OpenRequirementsAI Performance Engineering Skill: https://github.com/AgenticTesting/OpenRequirementsAI/blob/main/.claude/skills/performanceengineering/SKILL.md
- WordPress wp performance Skill: https://github.com/WordPress/agent-skills/blob/trunk/skills/wp-performance/SKILL.md
- RTK Performance Skill: https://github.com/rtk-ai/rtk/blob/master/.claude/skills/performance/SKILL.md
- Autonomous Execution Skills Research: `docs/autonomous_execution_skills_research.md`
- Loki Mode: https://github.com/asklokesh/loki-mode
- Loki Mode Skill: https://github.com/asklokesh/loki-mode/blob/main/SKILL.md
- AWS Code Agent Skill: https://github.com/aws-samples/sample-strands-agent-with-agentcore/blob/main/chatbot-app/agentcore/skills/code-agent/SKILL.md
- consult-llm Debate VS Skill: https://github.com/raine/consult-llm/blob/main/skills/debate-vs/SKILL.md
- consult-llm Collab Skill: https://github.com/raine/consult-llm/blob/main/skills/collab/SKILL.md
- consult-llm Debate Skill: https://github.com/raine/consult-llm/blob/main/skills/debate/SKILL.md
- Autonomous Skill: https://github.com/allanninal/claude-code-skills/blob/main/skills/autonomous-skill/SKILL.md
- Concise Planning Skill: https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/productivity/concise-planning/SKILL.md
- Deep Research Autonomy Verification: https://github.com/199-biotechnologies/claude-deep-research-skill/blob/main/AUTONOMY_VERIFICATION.md
- LLM Coding Workflow Skill: https://github.com/ericporres/llm-coding-workflow-skill
- Parallel Agent Coding Skills Research: `docs/parallel_agent_coding_skills_research.md`
- Claude Code Subagents: https://code.claude.com/docs/en/sub-agents
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Agent Teams: https://code.claude.com/docs/en/agent-teams
- OpenAI Codex Subagents: https://developers.openai.com/codex/subagents
- OpenAI Codex Skills: https://developers.openai.com/codex/skills
- OpenAI Codex AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- OpenAI Codex Agents SDK Workflows: https://developers.openai.com/codex/guides/agents-sdk
- Travis Neuman Agent Teams Skill: https://github.com/travisjneuman/.claude/blob/master/skills/agent-teams/SKILL.md
- Zoran Spirkovski Creating Agent Teams: https://github.com/ZoranSpirkovski/creating-agent-teams
- ShakaCode File By File Review Command: https://github.com/shakacode/claude-code-commands-skills-agents/blob/main/commands/file-by-file-review.md
- Model Selection Cost Minimization Skills: `docs/model_selection_cost_minimization_skills.md`
- OpenClaw Model Router Skill: https://github.com/openclaw/skills/blob/main/skills/digitaladaption/model-router/SKILL.md
- Cost Aware LLM Pipeline Skill: https://github.com/affaan-m/everything-claude-code/blob/main/skills/cost-aware-llm-pipeline/SKILL.md
- LLM Cost Optimizer Skill: https://github.com/alirezarezvani/claude-skills/blob/main/engineering/llm-cost-optimizer/SKILL.md
- Claude Code Cost Optimization Skill: https://github.com/markus41/claude/blob/main/plugins/claude-code-expert/skills/cost-optimization/SKILL.md
- GitHub Copilot Model Recommendation Skill: https://github.com/github/awesome-copilot/blob/main/skills/model-recommendation/SKILL.md
- Research Lookup Skill: https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/scientific/research-lookup/SKILL.md
- Claude Code Model Config: https://code.claude.com/docs/en/model-config
- Security API Preconditions Skills Research: `docs/security_api_preconditions_skills_research.md`
- Addy Osmani Security and Hardening Skill: https://github.com/addyosmani/agent-skills/blob/main/skills/security-and-hardening/SKILL.md
- API Security Best Practices Skill: https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/security/api-security-best-practices/SKILL.md
- Senior Security Skill: https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/senior-security/SKILL.md
- Security Pen Testing Skill: https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/security-pen-testing/SKILL.md
- OWASP Security Skill for Claude Code: https://github.com/agamm/claude-code-owasp
- Adversarial Code Reviewer Skill: https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/adversarial-reviewer/SKILL.md
- Agent OWASP ASI Compliance Skill: https://github.com/github/awesome-copilot/blob/main/skills/agent-owasp-compliance/SKILL.md
- Invariant Analyzer Skill: https://github.com/majiayu000/claude-skill-registry/blob/main/skills/other/other/invariant-analyzer/SKILL.md
- Contract Oriented Docstring Skill: https://github.com/honnibal/claude-skills
- Tiger Style Skill: https://github.com/M64GitHub/tiger-style
- API Design Skill: https://github.com/affaan-m/everything-claude-code/blob/main/skills/api-design/SKILL.md
- API Designer Skill: https://github.com/Jeffallan/claude-skills/blob/main/skills/api-designer/SKILL.md
- OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x00-header/
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- OWASP REST Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
- OWASP Input Validation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- Interface Contract Dependency Inversion Skills Research: `docs/interface_contract_dependency_inversion_skills_research.md`
- Matt Pocock Interface Design Guidance: https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/INTERFACE-DESIGN.md
- Matt Pocock Improve Codebase Architecture Skill: https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md
- Clean Architecture Dependency Inversion Skill: https://github.com/PanGan21/clean-architecture-claude-skills/blob/master/skills/clean-architecture-dependency-inversion/SKILL.md
- GitHub Copilot .NET Best Practices Skill: https://github.com/github/awesome-copilot/blob/main/plugins/csharp-dotnet-development/skills/dotnet-best-practices/SKILL.md
- GitHub Copilot .NET Design Pattern Review Skill: https://github.com/github/awesome-copilot/blob/main/skills/dotnet-design-pattern-review/SKILL.md
- GitHub Copilot C Sharp Expert Agent: https://github.com/github/awesome-copilot/blob/main/agents/CSharpExpert.agent.md
- GitHub Copilot OOP Design Pattern Instructions: https://github.com/github/awesome-copilot/blob/main/instructions/oop-design-patterns.instructions.md
- GitHub Copilot .NET Architecture Instructions: https://github.com/github/awesome-copilot/blob/main/instructions/dotnet-architecture-good-practices.instructions.md
- SOLID Skills: https://github.com/ramziddin/solid-skills
- Microsoft .NET Abstractions Guidance: https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/abstractions-abstract-types-and-interfaces
- Microsoft .NET Dependency Injection Guidelines: https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection/guidelines
- ASP.NET Core Dependency Injection Guidance: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection
- Microsoft .NET Architecture Principles: https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles
- TypeScript Interfaces: https://www.typescriptlang.org/docs/handbook/interfaces.html
- Python Protocols: https://typing.python.org/en/latest/reference/protocols.html
- PEP 544 Protocols: https://peps.python.org/pep-0544/
