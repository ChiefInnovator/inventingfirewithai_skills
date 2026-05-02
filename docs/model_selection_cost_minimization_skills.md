# Model Selection and Cost Minimization Skills for Claude Code and Codex

**Prepared for:** Rich Crane  
**Prepared on:** May 02, 2026, 10:55 AM EST  
**Primary platforms:** Claude Code and OpenAI Codex  
**Purpose:** Define skills and instruction patterns that automatically select the right model for the task while minimizing cost.

## Executive Summary

The best solution is a **cost aware model routing skill** supported by platform specific configuration.

The agent should not default to the most expensive model. It should classify the task, choose the cheapest model that can reliably complete it, escalate only when needed, and use stronger models for planning, security, architecture, hard debugging, and final arbitration.

The recommended pattern is:

```text
Classify task.
Choose the lowest sufficient model.
Use cheap models for exploration, summaries, formatting, and simple edits.
Use balanced coding models for normal implementation.
Use strongest models only for architecture, security, ambiguous bugs, and final arbitration.
Escalate only when confidence is low, tests fail repeatedly, or risk is high.
Track why escalation happened.
```

## Best Existing Skills and References

### 1. Model Router Skill

**Best use case:** General model routing across multiple providers.

This is the closest existing skill to the requested behavior. It is designed to automatically select the optimal model based on task type, complexity, cost, provider preference, and confidence scoring.

**What it does well:**

1. Classifies tasks by type.
2. Routes work to the best configured provider.
3. Uses cheaper models for simple tasks.
4. Provides recommendations with confidence and reasoning.
5. Supports multiple providers, including Anthropic, OpenAI, Gemini, Moonshot, Z.ai, and GLM.

**Reference:**

https://github.com/openclaw/skills/blob/main/skills/digitaladaption/model-router/SKILL.md

### 2. Cost Aware LLM Pipeline Skill

**Best use case:** Building a repeatable cost control pipeline.

This skill is useful because it combines model routing, budget tracking, retry logic, and prompt caching. It is broader than coding agents and works well for systems that call LLM APIs repeatedly.

**What it does well:**

1. Routes by task complexity.
2. Uses cheaper models for simple tasks.
3. Reserves expensive models for complex work.
4. Adds retry logic.
5. Adds prompt caching.
6. Adds budget tracking.

**Reference:**

https://github.com/affaan-m/everything-claude-code/blob/main/skills/cost-aware-llm-pipeline/SKILL.md

### 3. LLM Cost Optimizer Skill

**Best use case:** Cost engineering discipline.

This skill frames LLM cost as an engineering cost. It focuses on cutting API cost while preserving quality through routing, caching, prompt compression, and observability.

**What it does well:**

1. Treats LLM cost like database query cost.
2. Measures before optimizing.
3. Uses routing, caching, compression, and monitoring.
4. Focuses on user facing quality, not just lower spend.

**Reference:**

https://github.com/alirezarezvani/claude-skills/blob/main/engineering/llm-cost-optimizer/SKILL.md

### 4. Claude Code Cost Optimization Skill

**Best use case:** Claude specific model tier mapping.

This skill maps Claude model tiers to practical task types. It is useful as a direct reference for Haiku, Sonnet, and Opus routing.

**What it does well:**

1. Uses Haiku for quick lookups and simple tasks.
2. Uses Sonnet for general development and implementation.
3. Uses Opus for architecture and complex decisions.
4. Gives concrete switching examples.

**Reference:**

https://github.com/markus41/claude/blob/main/plugins/claude-code-expert/skills/cost-optimization/SKILL.md

### 5. GitHub Awesome Copilot Model Recommendation Skill

**Best use case:** Model recommendation policy.

This is not Claude or Codex specific, but it is useful because it analyzes agent and prompt files, then recommends suitable models based on required capability, cost efficiency, and performance tradeoffs.

**What it does well:**

1. Recommends a model based on task complexity.
2. Considers subscription tiers and premium usage.
3. Explains rationale for model choice.
4. Helps standardize model assignment across prompts and agents.

**Reference:**

https://github.com/github/awesome-copilot/blob/main/skills/model-recommendation/SKILL.md

### 6. Research Lookup Skill with Automatic Model Choice

**Best use case:** Narrow example of automatic model selection.

This skill selects between a faster search model and a stronger reasoning model based on query complexity. It is useful as a focused design example.

**What it does well:**

1. Chooses efficient lookup for simple research.
2. Chooses stronger reasoning for deep analysis.
3. Adds citation focused output.
4. Demonstrates task specific model routing.

**Reference:**

https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/scientific/research-lookup/SKILL.md

## Official Claude Code Capabilities

Claude Code supports model configuration at several layers.

### Claude Code Model Aliases

Claude Code supports model aliases:

```text
haiku   = fast and efficient model for simple tasks
sonnet  = daily coding tasks
opus    = complex reasoning tasks
best    = most capable available model
opusplan = Opus during plan mode, then Sonnet for execution
```

**Reference:**

https://code.claude.com/docs/en/model-config

### Claude Code Skill Model Field

Claude Code skills can include a `model` field and an `effort` field in frontmatter. The model override applies for the current turn when the skill is active.

Example:

```markdown
---
name: cost-aware-model-router
description: Chooses the lowest sufficient model for a task and escalates only when needed.
model: sonnet
effort: medium
---
```

**Reference:**

https://code.claude.com/docs/en/skills

### Claude Code Subagent Model Field

Claude Code subagents can include a `model` field. Valid values include `haiku`, `sonnet`, `opus`, a full model ID, or `inherit`.

Example:

```markdown
---
name: cheap-codebase-explorer
description: Fast read only codebase explorer for simple investigation and file discovery.
tools: Read, Glob, Grep, Bash
model: haiku
effort: low
---
```

**Reference:**

https://code.claude.com/docs/en/sub-agents

### Claude Code Cost Control Pattern

Use model routing by role:

```text
Explore agent     = haiku
Formatter agent   = haiku
Docs lookup agent = haiku or sonnet
Implementer       = sonnet
Test validator    = sonnet
Security reviewer = opus or sonnet high effort
Architect         = opus
Final arbitrator  = opus only when needed
```

## Official Codex Capabilities

Codex supports model and reasoning effort through custom agents and configuration.

### Codex Skills

Codex skills package reusable workflows. Codex initially sees the skill name, description, and path, then loads the full `SKILL.md` only when it decides to use the skill. This keeps large skill instructions out of the main context until needed.

**Reference:**

https://developers.openai.com/codex/skills

### Codex AGENTS.md

Codex reads `AGENTS.md` before doing work. Use it for mandatory model routing behavior, because a skill may not always be selected automatically.

**Reference:**

https://developers.openai.com/codex/guides/agents-md

### Codex Custom Agents

Codex custom agents live in:

```text
~/.codex/agents/
.codex/agents/
```

Each custom agent can specify:

```text
name
description
developer_instructions
model
model_reasoning_effort
sandbox_mode
skills.config
```

**Reference:**

https://developers.openai.com/codex/subagents

### Codex Model Reasoning Effort

Use reasoning effort as a cost and quality control dial:

```text
low     = lookup, formatting, simple edits, simple reviews
medium  = normal coding, implementation, test updates
high    = security, architecture, hard bugs, final review
```

### Codex Cost Control Pattern

Use custom agents by role:

```text
explorer        = cheaper fast model, medium reasoning, read only
docs_researcher = cheaper mini model, medium reasoning, read only
worker          = balanced coding model, medium reasoning
reviewer        = strongest needed model, high reasoning, read only
final_arbitrator = strongest model only when competing answers remain
```

## Recommended Architecture

### Directory Layout for Claude Code

```text
CLAUDE.md
.claude/
  skills/
    cost-aware-model-routing/
      SKILL.md
  agents/
    cheap-codebase-explorer.md
    balanced-implementer.md
    cost-aware-test-validator.md
    high-confidence-reviewer.md
    final-arbitrator.md
```

### Directory Layout for Codex

```text
AGENTS.md
.codex/
  config.toml
  agents/
    explorer.toml
    implementer.toml
    test_validator.toml
    reviewer.toml
    final_arbitrator.toml
skills/
  cost-aware-model-routing/
    SKILL.md
```

## Mandatory Instruction for CLAUDE.md

Add this to `CLAUDE.md`:

```markdown
# Cost Aware Model Routing

Use the lowest cost model that can reliably complete the task.

Default routing:
1. Use Haiku for simple lookup, summarization, formatting, file discovery, and mechanical edits.
2. Use Sonnet for normal coding, test writing, refactoring, and implementation.
3. Use Opus for architecture, security critical work, complex debugging, ambiguous requirements, and final arbitration.
4. Use OpusPlan when planning quality matters but execution can be done by Sonnet.
5. Do not use Opus by default.
6. Escalate only when the cheaper model fails, confidence is low, tests repeatedly fail, or risk is material.
7. Prefer read only cheap agents for exploration.
8. Prefer Sonnet for implementation.
9. Prefer Opus only for decisions that would be expensive to reverse.
10. Report any escalation and why it happened.
```

## Mandatory Instruction for AGENTS.md

Add this to `AGENTS.md`:

```markdown
# Cost Aware Model Routing

Use the cheapest model and reasoning effort that can reliably complete the task.

Default routing:
1. Use low reasoning for lookup, formatting, file discovery, summarization, and simple edits.
2. Use medium reasoning for normal coding, tests, implementation, and refactoring.
3. Use high reasoning for security, architecture, hard debugging, complex logic, and final review.
4. Use cheaper or mini models for read only exploration and documentation checks.
5. Use stronger models only for implementation risk, final arbitration, or repeated failure.
6. Do not fan out high reasoning subagents unless the task requires it.
7. Keep reviewer and explorer agents read only by default.
8. Track why a stronger model or higher reasoning effort was used.
9. If a cheaper agent returns low confidence or conflicting results, escalate one tier and retry once.
10. Prefer one strong final arbitrator over many expensive workers.
```

# Ready To Use Skill: Cost Aware Model Routing

Save this as:

```text
cost-aware-model-routing/SKILL.md
```

```markdown
---
name: cost-aware-model-routing
description: Automatically selects the lowest cost model or agent configuration that can reliably complete the task. Use when choosing Claude or Codex models, assigning subagents, minimizing API spend, controlling reasoning effort, or deciding whether to escalate to a stronger model.
---

# Cost Aware Model Routing Skill

## Purpose

Use this skill to select the right model for a task while minimizing cost.

The goal is not to use the cheapest model at all times. The goal is to use the cheapest model that can reliably complete the task with acceptable quality, risk, and verification.

## Core Principle

Use the lowest sufficient model.

Escalate only when evidence shows the current model is not sufficient.

## Routing Workflow

1. Classify the task.
2. Estimate complexity.
3. Estimate risk.
4. Estimate reversibility.
5. Select the lowest sufficient model.
6. Set reasoning effort.
7. Execute the task.
8. Verify the result.
9. Escalate only if needed.
10. Report the final model decision.

## Task Classification

Classify the task into one of these categories:

1. Simple lookup.
2. Formatting or rewriting.
3. Codebase exploration.
4. Documentation lookup.
5. Small mechanical edit.
6. Normal implementation.
7. Test writing.
8. Refactoring.
9. Performance analysis.
10. Security review.
11. Architecture.
12. Hard debugging.
13. Final arbitration.
14. Production risk review.

## Complexity Levels

### Level 1: Simple

Examples:

1. Rename a symbol.
2. Summarize a file.
3. Format a document.
4. Search for a string.
5. Explain a small function.
6. Generate boilerplate.

Use cheapest fast model.

### Level 2: Standard

Examples:

1. Implement a normal feature.
2. Add tests.
3. Fix a clear bug.
4. Refactor a small module.
5. Update API handling.
6. Modify UI behavior.

Use balanced coding model.

### Level 3: Complex

Examples:

1. Architecture decision.
2. Ambiguous bug.
3. Cross service behavior.
4. Security sensitive change.
5. Performance regression.
6. Complex concurrency.
7. Data migration.
8. Final decision among conflicting results.

Use strongest necessary model.

## Risk Levels

### Low Risk

Use cheap or balanced model.

Examples:

1. Read only exploration.
2. Formatting.
3. Documentation.
4. Non production code.
5. Test only changes.

### Medium Risk

Use balanced model.

Examples:

1. Normal implementation.
2. Moderate refactoring.
3. User facing behavior.
4. API changes with tests.

### High Risk

Use strongest model or high reasoning.

Examples:

1. Authentication.
2. Authorization.
3. Payments.
4. Healthcare or legal workflows.
5. Data deletion.
6. Production deployment.
7. Security boundaries.
8. Irreversible migrations.

## Claude Code Routing

Use this mapping:

```text
haiku
Use for:
1. Simple lookup.
2. File discovery.
3. Summaries.
4. Formatting.
5. Mechanical edits.
6. Read only exploration.

sonnet
Use for:
1. Default coding.
2. Implementation.
3. Test writing.
4. Refactoring.
5. Debugging with clear failure.
6. Review of normal changes.

opus
Use for:
1. Architecture.
2. Security critical work.
3. Hard debugging.
4. Complex reasoning.
5. Final arbitration.
6. High risk production decisions.

opusplan
Use for:
1. Expensive planning with cheaper execution.
2. Large feature design.
3. Cross module refactors.
4. High confidence plan before Sonnet implementation.
```

## Codex Routing

Use this mapping:

```text
low reasoning
Use for:
1. Lookup.
2. Formatting.
3. Simple edits.
4. Read only exploration.
5. Summaries.

medium reasoning
Use for:
1. Default implementation.
2. Test writing.
3. Refactoring.
4. Documentation updates.
5. Standard PR review.

high reasoning
Use for:
1. Security review.
2. Architecture.
3. Hard debugging.
4. Complex logic.
5. Final arbitration.
6. High risk changes.
```

## Subagent Cost Rules

When using subagents:

1. Use cheap read only agents for exploration.
2. Use balanced agents for implementation.
3. Use stronger agents only for review, architecture, security, or arbitration.
4. Do not spawn many high cost agents.
5. Prefer one strong arbitrator after several cheap agents.
6. Keep exploratory agents read only.
7. Keep documentation agents read only.
8. Limit recursive delegation.
9. Run high cost agents only after cheaper agents provide focused context.
10. Stop escalation after one failed retry unless the task is high value.

## Escalation Rules

Escalate one tier when:

1. The model reports low confidence.
2. The output conflicts with tests or source evidence.
3. The task fails twice.
4. The model misses obvious project patterns.
5. The task involves security, data loss, or production risk.
6. Multiple agents disagree and the decision matters.
7. The implementation becomes broader than expected.

Do not escalate when:

1. The work is stylistic.
2. The issue is minor.
3. A test failure clearly identifies the fix.
4. The current model can solve the issue with more context.
5. The user asked to minimize cost aggressively.

## De Escalation Rules

De escalate when:

1. The task becomes mechanical.
2. The plan is already approved.
3. The strong model has produced the architecture.
4. Remaining work is file edits or test updates.
5. The agent is only formatting or summarizing.
6. The subagent is read only.

## Decision Criteria

Use these criteria when choosing a model:

1. Correctness need.
2. Risk level.
3. Reversibility.
4. Scope.
5. Ambiguity.
6. Security sensitivity.
7. Performance sensitivity.
8. Test coverage.
9. Cost.
10. Time.
11. Context length.
12. Tool usage required.

## Final Report Format

At the end, report model routing briefly:

```markdown
## Model Routing

**Selected route:** <model or effort level>

**Reason:** <why this was sufficient>

**Escalation:** <none or reason>

**Cost controls used:**
1. <control>
2. <control>

**Validation:**
1. <test or check>
```

## Anti Patterns

Avoid these behaviors:

1. Using the strongest model by default.
2. Spawning many expensive agents.
3. Escalating before reading the code.
4. Using high reasoning for formatting.
5. Using expensive models for raw search.
6. Repeating the same failed approach.
7. Optimizing cost so aggressively that quality drops.
8. Ignoring security or production risk to save tokens.
9. Using long context models when targeted file reads are enough.
10. Running high cost final review when tests and risk are low.

## Operating Mantra

Cheap for search.  
Balanced for build.  
Strong for risk.  
Escalate with evidence.  
Verify before done.
```

## Recommended Claude Code Subagents

### Cheap Codebase Explorer

Save as:

```text
.claude/agents/cheap-codebase-explorer.md
```

```markdown
---
name: cheap-codebase-explorer
description: Fast read only codebase explorer for file discovery, symbol lookup, and simple codebase mapping. Use before expensive reasoning.
tools: Read, Glob, Grep, Bash
model: haiku
effort: low
---

You are a read only codebase explorer.

Do not edit files.

Find the smallest relevant set of files, symbols, tests, and commands.

Return:
1. Relevant files.
2. Key symbols.
3. Likely execution path.
4. Suggested next step.
5. Confidence level.
```

### Balanced Implementer

Save as:

```text
.claude/agents/balanced-implementer.md
```

```markdown
---
name: balanced-implementer
description: Default implementation agent for scoped coding tasks with tests.
tools: Read, Glob, Grep, Bash, Edit, Write
model: sonnet
effort: medium
---

You are an implementation agent.

Implement only the assigned scope.

Follow existing project patterns. Add or update tests when behavior changes. Run targeted validation.

Return:
1. Files changed.
2. Behavior changed.
3. Tests added or updated.
4. Commands run.
5. Remaining risks.
```

### Final Arbitrator

Save as:

```text
.claude/agents/final-arbitrator.md
```

```markdown
---
name: final-arbitrator
description: High confidence reviewer for conflicting agent results, architecture decisions, security sensitive work, and final risk review.
tools: Read, Glob, Grep, Bash
model: opus
effort: high
---

You are a final arbitrator.

Use this agent only when the decision is high risk, ambiguous, security sensitive, or expensive to reverse.

Review evidence from other agents. Do not redo cheap exploration unless necessary.

Return:
1. Best decision.
2. Rationale.
3. Alternatives rejected.
4. Risks.
5. Required validation.
```

## Recommended Codex Custom Agents

### Explorer

Save as:

```text
.codex/agents/explorer.toml
```

```toml
name = "explorer"
description = "Low cost read only codebase explorer for file discovery, symbol lookup, and simple mapping."
model = "gpt-5.4-mini"
model_reasoning_effort = "low"
sandbox_mode = "read-only"

developer_instructions = '''
Stay in exploration mode.
Do not edit files.
Use targeted search and file reads.
Return relevant files, symbols, execution path, and confidence.
'''
```

### Implementer

Save as:

```text
.codex/agents/implementer.toml
```

```toml
name = "implementer"
description = "Balanced coding agent for scoped implementation and tests."
model = "gpt-5.4"
model_reasoning_effort = "medium"

developer_instructions = '''
Implement only the assigned scope.
Follow existing project patterns.
Add or update tests when behavior changes.
Run targeted validation.
Report files changed, commands run, and remaining risks.
'''
```

### Reviewer

Save as:

```text
.codex/agents/reviewer.toml
```

```toml
name = "reviewer"
description = "High confidence reviewer for correctness, security, performance, and missing tests."
model = "gpt-5.4"
model_reasoning_effort = "high"
sandbox_mode = "read-only"

developer_instructions = '''
Review like an owner.
Prioritize correctness, security, behavior regressions, performance risk, and missing tests.
Avoid style only comments unless they hide a real bug.
Return concrete findings with severity and file references.
'''
```

### Final Arbitrator

Save as:

```text
.codex/agents/final_arbitrator.toml
```

```toml
name = "final_arbitrator"
description = "Strong final decision agent for conflicting results, high risk decisions, architecture, and security critical work."
model = "gpt-5.4"
model_reasoning_effort = "high"
sandbox_mode = "read-only"

developer_instructions = '''
Use only when the decision is high risk, ambiguous, security sensitive, or expensive to reverse.
Review evidence from other agents.
Choose the best path.
Explain rejected alternatives.
Define required validation.
'''
```

## Practical Routing Examples

### Example 1: Simple Rename

```text
Task: Rename a CSS class.
Claude: Haiku
Codex: low reasoning
Why: Mechanical, low risk, easy to verify.
```

### Example 2: Normal Feature

```text
Task: Add a settings page with tests.
Claude: Sonnet
Codex: medium reasoning
Why: Normal implementation with test coverage.
```

### Example 3: Security Review

```text
Task: Review authentication changes.
Claude: Opus or Sonnet with high effort
Codex: high reasoning reviewer
Why: Security and production risk justify stronger reasoning.
```

### Example 4: Large Feature Plan

```text
Task: Plan a cross module refactor.
Claude: OpusPlan
Codex: high reasoning planner, then medium reasoning implementer
Why: Strong planning matters, but execution can be cheaper.
```

### Example 5: Parallel Subagents

```text
Task: Review a large PR.
Route:
1. Explorer on cheap model.
2. Docs researcher on cheap or mini model.
3. Test reviewer on balanced model.
4. Security reviewer on strong model only if risk exists.
5. Final arbitrator only if agents disagree.
```

## Recommended Default Policy

Use this policy across both Claude Code and Codex:

1. Never default to the most expensive model.
2. Use cheap models for search, summaries, formatting, and exploration.
3. Use balanced models for implementation and tests.
4. Use strong models for security, architecture, hard debugging, and final arbitration.
5. Escalate only with evidence.
6. De escalate after planning.
7. Keep reviewers and explorers read only when possible.
8. Avoid recursive or uncontrolled subagent fan out.
9. Track model choice in the final summary.
10. Prefer a strong final decision maker over many strong workers.

## References

### Official Claude Code References

1. Claude Code model configuration  
   https://code.claude.com/docs/en/model-config

2. Claude Code skills  
   https://code.claude.com/docs/en/skills

3. Claude Code subagents  
   https://code.claude.com/docs/en/sub-agents

### Official OpenAI Codex References

1. Codex skills  
   https://developers.openai.com/codex/skills

2. Codex AGENTS.md  
   https://developers.openai.com/codex/guides/agents-md

3. Codex subagents  
   https://developers.openai.com/codex/subagents

4. Codex subagent concepts  
   https://developers.openai.com/codex/concepts/subagents

5. Codex best practices  
   https://developers.openai.com/codex/learn/best-practices

### Skill References

1. Model Router Skill  
   https://github.com/openclaw/skills/blob/main/skills/digitaladaption/model-router/SKILL.md

2. Cost Aware LLM Pipeline Skill  
   https://github.com/affaan-m/everything-claude-code/blob/main/skills/cost-aware-llm-pipeline/SKILL.md

3. LLM Cost Optimizer Skill  
   https://github.com/alirezarezvani/claude-skills/blob/main/engineering/llm-cost-optimizer/SKILL.md

4. Claude Code Cost Optimization Skill  
   https://github.com/markus41/claude/blob/main/plugins/claude-code-expert/skills/cost-optimization/SKILL.md

5. GitHub Awesome Copilot Model Recommendation Skill  
   https://github.com/github/awesome-copilot/blob/main/skills/model-recommendation/SKILL.md

6. Research Lookup Skill  
   https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/scientific/research-lookup/SKILL.md

## Final Recommendation

Install the `cost-aware-model-routing` skill and add the mandatory routing instructions to both `CLAUDE.md` and `AGENTS.md`.

For Claude Code, rely on:

1. `model` and `effort` in skill frontmatter.
2. `model` and `effort` in subagent frontmatter.
3. `opusplan` for expensive planning with cheaper execution.
4. Haiku for cheap exploration.
5. Sonnet for default coding.
6. Opus for high risk decisions.

For Codex, rely on:

1. `AGENTS.md` for mandatory policy.
2. Custom agents in `.codex/agents/`.
3. `model` and `model_reasoning_effort` per custom agent.
4. Read only explorer and reviewer agents.
5. Strong final arbitration only when needed.

The best cost saving strategy is not simply choosing cheaper models. It is **using stronger models at the decision points and cheaper models for the work around those decisions**.
