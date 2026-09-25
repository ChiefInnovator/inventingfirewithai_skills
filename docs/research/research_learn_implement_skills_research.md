# Research, Learning, and Implementation Skills for AI Agents

**Prepared for:** Rich Crane  
**Prepared on:** May 02, 2026, 01:02 PM EST  
**Focus:** Skills that help AI agents respond to unknowns by researching, learning, implementing, testing, and preserving what they learned.  
**Primary platforms:** Claude Code and OpenAI Codex  
**Core goal:** Do not stop when the agent does not know something. Research first, learn the relevant context, implement the best answer, verify the result, and capture the learning.

## Executive Summary

The best solution is a skill stack, not a single skill.

Agents need five capabilities when they do not know something:

1. Research unknowns before asking the user.
2. Learn the relevant domain, codebase, API, or standard.
3. Compare possible answers and choose the best one.
4. Implement and verify the solution.
5. Save durable learnings so the agent does not repeat the same gap.

The strongest pattern is:

```text
Unknown detected
Research sources
Extract learning
Choose approach
Implement
Test or evaluate
Record durable learning
Promote repeated learning into instructions or skills
```

## Recommended Skill Stack

Use this stack:

1. **Research Learn Implement Skill** from this document.
2. **Anthropic Skill Creator** for researching and writing reusable skills.
3. **AutoResearch Skill** for experiment and evaluate loops.
4. **Self Improving Agent Skill** for LEARNINGS, ERRORS, and feature request logs.
5. **Reflect Learn Skill** for extracting learnings from sessions and proposing new rules or skills.
6. **Lamarck** for analyzing skill performance across sessions and improving SKILL.md files.
7. **LLM Wiki Skill** for persistent structured knowledge.
8. **Standards Researcher Skill** for architecture and standards research.
9. **Research Engineer Skill** for rigorous tool and literature review before implementation.
10. **Autonomous Execution Skill** for “do not ask unless truly blocked” behavior.

## Best Skills and References

## 1. Agent Skills Standard

**Best for:** Understanding how skills are packaged and loaded.

Agent Skills are a lightweight open format. A skill is a folder with a `SKILL.md` file that contains metadata and instructions. Skills can also bundle scripts, references, templates, and assets.

The most relevant detail is progressive disclosure:

1. Discovery loads skill name and description.
2. Activation loads the full `SKILL.md`.
3. Execution follows the instructions and optionally uses scripts or references.

**Why it matters:** Learning skills should be written as reusable workflows that load when the agent faces unknowns, research needs, or repeated implementation patterns.

**Reference:**  
https://agentskills.io/home

## 2. OpenAI Codex Skills

**Best for:** Codex reusable workflows.

Codex skills package instructions, resources, and optional scripts so Codex can follow a workflow reliably. Codex starts with each skill name, description, and path, then loads the full skill only when it decides to use it.

**Why it matters:** For Codex, the skill should have a strong description so it activates when the task includes unknown APIs, unfamiliar frameworks, missing context, or research before implementation.

**Reference:**  
https://developers.openai.com/codex/skills

## 3. Codex AGENTS.md

**Best for:** Mandatory always on behavior.

Codex reads `AGENTS.md` before doing work. For “research when you do not know,” put the mandatory rule in `AGENTS.md` and keep the detailed workflow in a skill.

**Reference:**  
https://developers.openai.com/codex/guides/agents-md

## 4. Claude Code Skills

**Best for:** Claude Code reusable learning workflows.

Claude Code supports custom file system skills. Claude discovers and uses them automatically when relevant.

**Why it matters:** The learning skill should be installed under `.claude/skills/` or `~/.claude/skills/`, and its description should explicitly say to use it when the agent lacks knowledge, needs research, must inspect unfamiliar code, or must learn a new API before implementing.

**Reference:**  
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

## 5. Claude Skill Authoring Best Practices

**Best for:** Writing skills that actually trigger and work.

Anthropic’s best practices say skills should be concise, structured, and tested with real usage.

**Reference:**  
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## 6. Anthropic Skill Creator Skill

**Best for:** Creating new skills after research.

The official Skill Creator skill instructs the agent to interview, research, check available MCPs, search docs, find similar skills, look up best practices, and research in parallel with subagents when available.

**Strong ideas to borrow:**

1. Research before writing the skill.
2. Check available tools and MCPs.
3. Search similar skills.
4. Use parallel subagents when useful.
5. Reduce user burden by coming prepared with context.
6. Include tests when outputs are objectively verifiable.

**Reference:**  
https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md

## 7. AutoResearch Skill

**Best for:** Experiment, evaluate, iterate loops.

AutoResearch is an autonomous research loop skill for LLM agents. It turns natural language research goals into experiment, evaluate, and iterate loops. It works with Claude Code, Codex CLI, and Gemini CLI.

**Strong ideas to borrow:**

1. Define the goal in a research file.
2. Generate hypotheses.
3. Try implementations or experiments.
4. Evaluate using a metric.
5. Keep winners and revert losers.
6. Iterate until the metric improves or the budget is exhausted.

**Reference:**  
https://github.com/wjgoarxiv/autoresearch-skill

## 8. Auto Claude Code Research Pipeline

**Best for:** Long research pipelines with stages.

This skill organizes research into stages such as idea discovery, implementation, deployment, and auto review. It includes an auto proceed option after an initial human checkpoint.

**Strong ideas to borrow:**

1. Stage the work.
2. Auto select top ideas when configured.
3. Implement after research.
4. Review results.
5. Track budget.
6. Fail gracefully instead of forcing bad progress.

**Reference:**  
https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/main/skills/research-pipeline/SKILL.md

## 9. Self Improving Agent Skill

**Best for:** Capturing durable learning files.

This skill creates structured learning files such as `LEARNINGS.md`, `ERRORS.md`, and `FEATURE_REQUESTS.md`. It also describes promotion targets for broadly useful learnings, such as `AGENTS.md`, tool notes, memory files, and behavioral guidelines.

**Strong ideas to borrow:**

1. Log corrections.
2. Log knowledge gaps.
3. Log command failures.
4. Log tool gotchas.
5. Promote repeated learnings into agent instructions.
6. Keep low confidence learning separate from high confidence rules.

**Reference:**  
https://github.com/openclaw/skills/blob/main/skills/pskoett/self-improving-agent/SKILL.md

## 10. Reflect Learn Skill

**Best for:** Turning session experience into rules and new skills.

Reflect Learn extracts signals from a session, proposes new skills, checks whether they are reusable and non trivial, checks for duplication, and writes learnings to project or global locations.

**Strong ideas to borrow:**

1. Extract learnings from completed work.
2. Separate low, medium, and high confidence signals.
3. Propose new skills when a pattern repeats.
4. Check for duplication before creating skills.
5. Route learning to the right file, such as memory, rules, or skills.

**Reference:**  
https://github.com/openclaw/skills/blob/main/skills/stevengonsalvez/reflect-learn/SKILL.md

## 11. Claude Starter Kit Learning Pattern

**Best for:** Persistent project learning.

This starter kit uses `LEARNINGS.md` files, session notes, project knowledge, and a reflect loop. It describes a flow where the agent notices corrections, writes them to knowledge files, and avoids repeating the mistake in later sessions.

**Reference:**  
https://github.com/mp-web3/claude-starter-kit

## 12. Lamarck

**Best for:** Analyzing whether skills are working.

Lamarck analyzes Claude Code sessions and extracts high signal learnings into memory files. It can analyze a skill across real conversations, find gaps, produce reports, and generate an improved `SKILL.md`.

**Reference:**  
https://github.com/johnlindquist/lamarck

## 13. LLM Wiki Skill Pattern

**Best for:** Persistent structured knowledge.

The LLM Wiki pattern builds and maintains a structured markdown knowledge base that gets richer with each source added and each question asked. This is useful when the agent repeatedly learns about a codebase, domain, customer, or platform.

**References:**  
https://github.com/kfchou/wiki-skills  
https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## 14. Research Engineer Skill

**Best for:** Rigorous research before implementation.

This skill focuses on theoretical correctness, tool selection, and implementation rigor. It requires literature or tool review before selecting an implementation path.

**Strong ideas to borrow:**

1. Do not invent libraries or APIs.
2. Review tools before choosing implementation.
3. Define exact constraints.
4. Critique flawed premises.
5. Implement only after selecting an appropriate tool.

**Reference:**  
https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/ai-research/research-engineer/SKILL.md

## 15. Loki Mode

**Best for:** Autonomous execution mindset.

Loki Mode is aggressive about not stopping or asking questions. Use the autonomy principle, not unsafe permission skipping. Pair it with safety gates, tests, and escalation rules.

**Reference:**  
https://github.com/asklokesh/loki-mode/blob/main/SKILL.md

## 16. Standards Researcher Skill

**Best for:** Researching standards and architectural patterns.

This skill researches industry standards and architectural patterns. It is useful when the agent does not know the correct standard, compliance expectation, or architecture pattern.

**Reference:**  
https://raw.githubusercontent.com/NeverSight/skills_feed/refs/heads/main/data/skills-md/levnikolaevich/claude-code-skills/ln-001-standards-researcher/SKILL.md

## Skill Comparison Matrix

| Skill or Pattern | Best Use | Research | Learn | Implement | Verify | Persist Learning |
|---|---|---:|---:|---:|---:|---:|
| Agent Skills Standard | Skill format | Medium | Medium | Medium | Low | Medium |
| Codex Skills | Codex reusable workflows | Medium | Medium | High | Medium | Medium |
| Codex AGENTS.md | Always on behavior | Low | Medium | High | Medium | Medium |
| Claude Code Skills | Claude reusable workflows | Medium | Medium | High | Medium | Medium |
| Skill Creator | Create new skills | High | High | Medium | Medium | Medium |
| AutoResearch | Experiment loops | High | High | High | High | Medium |
| Research Pipeline | Long staged research | High | High | High | High | Medium |
| Self Improving Agent | Learning files | Medium | High | Medium | Medium | High |
| Reflect Learn | Session learning extraction | Medium | High | Medium | Medium | High |
| Starter Kit Learning Pattern | Persistent project memory | Medium | High | Medium | Medium | High |
| Lamarck | Skill improvement from sessions | High | High | Medium | High | High |
| LLM Wiki | Durable knowledge base | High | High | Low | Medium | High |
| Research Engineer | Rigorous research to implementation | High | High | High | Medium | Low |
| Loki Mode | Keep moving | Medium | Medium | High | Medium | Low |
| Standards Researcher | Standards and architecture patterns | High | High | Medium | Medium | Medium |

## Recommended Operating Model

Use this decision tree:

```text
Does the agent know enough to implement safely?

Yes:
  Implement, test, and report.

No:
  Is the missing information likely discoverable?
    Yes:
      Research codebase, docs, standards, and sources.
      Compare findings.
      Choose best path.
      Implement.
      Test.
      Record learning.
    No:
      Make the safest reasonable assumption if reversible.
      Ask only if the decision is high risk or irreversible.
```

## Recommended Default Policy for Claude Code

Add this to `CLAUDE.md`.

```markdown
# Research Learn Implement Policy

When you do not know something, do not stop by default.

First:
1. Search the repository.
2. Read relevant docs.
3. Search official or authoritative sources.
4. Review similar code.
5. Compare viable answers.
6. Choose the safest and most maintainable answer.
7. Implement the solution.
8. Add or update tests.
9. Record durable learnings in LEARNINGS.md when the knowledge will matter again.

Ask the user only when:
1. The decision has legal, security, financial, production, or privacy risk.
2. Required credentials or private information are missing.
3. The request is contradictory.
4. Continuing could destroy data or create irreversible harm.
5. The user explicitly requested approval before proceeding.
```

## Recommended Default Policy for Codex

Add this to `AGENTS.md`.

```markdown
# Research Learn Implement Policy

When information is missing, research before asking.

Use this order:
1. Inspect the repository.
2. Search local docs.
3. Search official docs.
4. Search credible external references.
5. Review existing tests and patterns.
6. Pick the best supported answer.
7. Implement.
8. Verify.
9. Record the learning if it is reusable.

Do not ask clarification questions for minor missing context when a safe assumption can be made.

Escalate to the user only for material risk, contradictory requirements, missing credentials, irreversible operations, or business decisions.
```

# Ready To Use Skill: Research Learn Implement

Save this as:

```text
research-learn-implement/SKILL.md
```

```markdown
---
name: research-learn-implement
description: Use when the agent does not know something, lacks API or framework knowledge, needs to inspect unfamiliar code, must compare multiple possible answers, or must learn before implementing. Research first, learn the relevant context, choose the best supported approach, implement, verify, and record durable learnings.
---

# Research Learn Implement Skill

## Purpose

Use this skill when the agent encounters unknowns.

The agent should not stop simply because it lacks knowledge. It should research, learn, implement, verify, and preserve the learning.

## Core Principle

Do not guess when research is available.

Do not ask when the answer can be discovered safely.

Research first. Learn second. Implement third. Verify fourth. Record fifth.

## Trigger Conditions

Use this skill when:

1. The agent does not know an API.
2. The agent does not know a framework.
3. The agent does not understand a codebase area.
4. The task references a standard, package, tool, or service that may have changed.
5. Multiple implementation approaches are possible.
6. The agent needs to compare libraries or patterns.
7. The agent is about to modify unfamiliar code.
8. Tests fail and the cause is unclear.
9. The agent sees a recurring error.
10. The agent receives a correction that should be remembered.

## Research Order

Use this order:

1. Search the repository.
2. Read relevant source files.
3. Read project documentation.
4. Read tests.
5. Search official documentation.
6. Search authoritative references.
7. Search similar skills or examples.
8. Compare findings.
9. Identify the best supported answer.

Prefer project specific evidence over generic advice.

Prefer official documentation over blog posts.

Prefer current sources for facts that may have changed.

## Learning Extraction

After research, extract:

1. What was unknown.
2. What was learned.
3. Which source proved it.
4. Which decision it changes.
5. Whether the learning is one time or reusable.
6. Whether it should become a rule, memory, test, or skill.

## Decision Workflow

When multiple answers exist:

1. List viable options.
2. Compare correctness.
3. Compare maintainability.
4. Compare security risk.
5. Compare performance risk.
6. Compare project fit.
7. Compare implementation cost.
8. Select the best supported option.
9. Document the reason briefly.

## Implementation Workflow

After choosing an answer:

1. Make the smallest correct change.
2. Follow existing project patterns.
3. Add or update tests.
4. Include positive and negative tests when behavior changes.
5. Run targeted verification.
6. Fix failures.
7. Run broader checks when practical.
8. Report final result.

## Learning Persistence

Record durable learning when:

1. The same mistake could happen again.
2. The project has a non obvious convention.
3. A tool has a gotcha.
4. A command failed and the fix is reusable.
5. A user correction should affect future work.
6. A new workflow should become a skill.
7. A source settled an uncertain technical choice.

Suggested files:

```text
LEARNINGS.md
ERRORS.md
TOOLS.md
AGENTS.md
CLAUDE.md
MEMORY.md
.claude/reflections/
.codex/notes/
```

## Learning Entry Format

Use this format:

```markdown
## Learning

**Date:** YYYY-MM-DD

**Unknown:** What the agent did not know.

**Research:** Sources or files checked.

**Conclusion:** What was learned.

**Implementation impact:** What changed.

**Verification:** Tests, commands, or checks run.

**Promotion target:** None, LEARNINGS.md, AGENTS.md, CLAUDE.md, skill, test, docs, or memory.

**Confidence:** Low, medium, or high.
```

## Ask Only When Truly Blocked

Ask the user only when:

1. The decision has legal, security, financial, production, or privacy risk.
2. Required credentials or access are missing.
3. The request is contradictory.
4. Continuing could destroy data.
5. The choice has materially different business consequences.
6. The user explicitly requested approval before proceeding.

Do not ask because of ordinary uncertainty. Research first.

## Verification Rules

Before completion:

1. Cite or list sources used.
2. State assumptions.
3. Run relevant tests when coding.
4. Confirm the implementation follows the learned facts.
5. Record durable learning when appropriate.

## Final Report Format

```markdown
## Result

<summary>

## Research Performed

1. <source or file>
2. <source or file>

## Key Learning

<what was learned>

## Decision

<chosen approach and reason>

## Implementation

<what changed>

## Verification

<tests or checks>

## Durable Learning

<where it was recorded or why not recorded>
```

## Anti Patterns

Avoid:

1. Asking before searching.
2. Guessing library APIs.
3. Inventing packages or methods.
4. Implementing from memory when facts may have changed.
5. Ignoring project conventions.
6. Choosing the first answer without comparing alternatives.
7. Failing to test the learned implementation.
8. Relearning the same thing repeatedly without recording it.
9. Promoting low confidence notes into mandatory rules.
10. Continuing through high risk decisions without human approval.

## Operating Mantra

Unknowns are work, not blockers.

Research.  
Learn.  
Decide.  
Implement.  
Verify.  
Remember.
```

## Recommended Supporting Agents

## Researcher Agent

```markdown
---
name: researcher
description: Researches unknown APIs, standards, codebase areas, libraries, and implementation options before coding.
tools: Read, Glob, Grep, Bash, WebSearch, WebFetch
model: sonnet
effort: medium
---

Research the unknown.

Return:
1. What was searched.
2. Sources checked.
3. Findings.
4. Options.
5. Recommended answer.
6. Confidence level.
```

## Learning Recorder Agent

```markdown
---
name: learning-recorder
description: Extracts durable learnings from completed work and writes concise learning entries.
tools: Read, Write, Edit, Glob, Grep
model: haiku
effort: low
---

Extract reusable learning.

Do not promote weak or one time observations into mandatory rules.

Return:
1. Learning summary.
2. Confidence.
3. Suggested target file.
4. Exact entry text.
```

## Implementation Agent

```markdown
---
name: research-backed-implementer
description: Implements only after research has identified the best supported approach.
tools: Read, Glob, Grep, Bash, Edit, Write
model: sonnet
effort: medium
---

Implement based on research findings.

Follow existing project patterns.

Add or update tests.

Report:
1. Files changed.
2. Research used.
3. Tests run.
4. Remaining risks.
```

## Best Practical Recommendation

Install this skill and supporting agents, then add the mandatory policy to both `CLAUDE.md` and `AGENTS.md`.

The most important rule is:

```text
When the agent does not know something, it should not pause by default. It should research, learn, implement, verify, and record durable learning.
```

## Reference List

1. Agent Skills Overview  
   https://agentskills.io/home

2. OpenAI Codex Skills  
   https://developers.openai.com/codex/skills

3. OpenAI Codex AGENTS.md  
   https://developers.openai.com/codex/guides/agents-md

4. Claude Agent Skills Overview  
   https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

5. Claude Skill Authoring Best Practices  
   https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

6. Anthropic Skill Creator  
   https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md

7. AutoResearch Skill  
   https://github.com/wjgoarxiv/autoresearch-skill

8. Auto Claude Code Research Pipeline  
   https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/main/skills/research-pipeline/SKILL.md

9. Self Improving Agent Skill  
   https://github.com/openclaw/skills/blob/main/skills/pskoett/self-improving-agent/SKILL.md

10. Reflect Learn Skill  
    https://github.com/openclaw/skills/blob/main/skills/stevengonsalvez/reflect-learn/SKILL.md

11. Claude Starter Kit  
    https://github.com/mp-web3/claude-starter-kit

12. Lamarck  
    https://github.com/johnlindquist/lamarck

13. Wiki Skills  
    https://github.com/kfchou/wiki-skills

14. Karpathy LLM Wiki Pattern  
    https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

15. Research Engineer Skill  
    https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/ai-research/research-engineer/SKILL.md

16. Loki Mode  
    https://github.com/asklokesh/loki-mode/blob/main/SKILL.md

17. Standards Researcher Skill  
    https://raw.githubusercontent.com/NeverSight/skills_feed/refs/heads/main/data/skills-md/levnikolaevich/claude-code-skills/ln-001-standards-researcher/SKILL.md
