# Parallel Agent Coding Skills for Claude Code and Codex

**Purpose:** Identify and define the best coding skills and instruction patterns for breaking work into independent units and running them in parallel with agents or subagents.

**Primary platforms:** Claude Code and OpenAI Codex

**Recommended outcome:** Use a reusable orchestration skill plus specialized reviewer, researcher, implementer, test, and synthesis agents.

## Executive Summary

The best pattern is not one skill. It is a coordinated skill system.

Use one lead skill to decide when work should be split, then use specialized agents or subagents for execution. The lead owns task decomposition, agent assignment, conflict prevention, result synthesis, and final verification.

The core rule is simple:

```text
Break work into independent, file separated, or concern separated tasks.
Run independent work in parallel.
Prevent overlapping file edits.
Wait for all agents.
Synthesize results.
Run final tests.
Report decisions, changes, risks, and verification.
```

## Best Platform Capabilities

### Claude Code

Claude Code has three relevant mechanisms:

1. **Subagents**

   Claude Code subagents are specialized assistants that run in their own context window and return results to the main conversation. They are best for focused work such as codebase exploration, test review, security review, performance review, and isolated analysis.

2. **Skills**

   Claude Code skills are reusable procedures stored as `SKILL.md` files. Claude can invoke them when relevant or the user can invoke them directly. Skills can also run in a forked subagent context.

3. **Agent Teams**

   Claude Code Agent Teams coordinate multiple Claude Code sessions with a team lead, separate teammates, shared task list, and direct inter agent messaging. Agent Teams are better than normal subagents when workers need to coordinate, challenge each other, or divide larger feature work.

### Codex

Codex has three relevant mechanisms:

1. **Subagents**

   Codex can spawn specialized agents in parallel, wait for all requested results, and return a consolidated response. Codex only spawns subagents when explicitly asked.

2. **Custom Agents**

   Codex supports custom agent definitions under `.codex/agents/` or `~/.codex/agents/`. These agents can define names, descriptions, developer instructions, model choices, reasoning effort, sandbox settings, and skill configuration.

3. **Skills and AGENTS.md**

   Codex skills are reusable workflows stored as `SKILL.md` files. Codex also reads `AGENTS.md` before work begins, so mandatory behavior should go there.

## Best Existing References

### 1. Claude Code Subagents Documentation

**Best for:** Understanding when to use subagents, how to define them, and how to run parallel research.

Key takeaways:

1. Use subagents for focused work that would otherwise pollute the main context.
2. Each subagent has its own context window.
3. Claude can delegate automatically based on the subagent description.
4. Parallel research works best when workstreams are independent.
5. Subagents return summarized findings to the main conversation.
6. Subagents should not edit the same files at the same time.

Reference:

https://code.claude.com/docs/en/sub-agents

### 2. Claude Code Skills Documentation

**Best for:** Creating reusable workflows and running skills in forked subagent contexts.

Key takeaways:

1. Skills should be used for reusable playbooks and repeated workflows.
2. A skill can run inline or in a forked subagent context.
3. `context: fork` runs the skill in isolation.
4. `agent: Explore`, `agent: Plan`, or `agent: general-purpose` controls the execution environment.
5. Skills can preload dynamic context and supporting files.

Reference:

https://code.claude.com/docs/en/skills

### 3. Claude Code Agent Teams Documentation

**Best for:** True parallel coding, review, and investigation across multiple Claude Code sessions.

Key takeaways:

1. Agent Teams are experimental and must be enabled.
2. They are best for parallel research, review, new feature modules, competing debug hypotheses, and cross layer work.
3. Use teams when workers need to communicate with each other.
4. Use normal subagents when workers only need to report results to the lead.
5. Start with three to five teammates.
6. Avoid file conflicts by assigning separate files, modules, layers, or concerns.
7. The lead should wait for teammates, synthesize results, and run final verification.

Reference:

https://code.claude.com/docs/en/agent-teams

### 4. OpenAI Codex Subagents Documentation

**Best for:** Codex parallel subagent workflows.

Key takeaways:

1. Codex can spawn specialized agents in parallel.
2. Codex waits for all agents and consolidates the response.
3. Codex only spawns subagents when explicitly asked.
4. Built in agents include `default`, `worker`, and `explorer`.
5. Custom agents live under `.codex/agents/` or `~/.codex/agents/`.
6. Custom agents are narrow and opinionated.
7. A strong Codex setup uses an explorer, reviewer, docs researcher, implementer, and test validator.

Reference:

https://developers.openai.com/codex/subagents

### 5. OpenAI Codex Skills Documentation

**Best for:** Codex reusable workflows.

Key takeaways:

1. A skill packages instructions, resources, scripts, and references.
2. Codex initially sees the skill name, description, and path.
3. Codex loads the full `SKILL.md` only when it chooses to use the skill.
4. Skills are available in Codex CLI, IDE extension, and Codex app.
5. Skills should be used for repeatable workflows.

Reference:

https://developers.openai.com/codex/skills

### 6. OpenAI Codex AGENTS.md Documentation

**Best for:** Mandatory always on behavior.

Key takeaways:

1. Codex reads `AGENTS.md` before doing work.
2. Global and project instructions can be layered.
3. For behavior that must always happen, use `AGENTS.md`, not only a skill.

Reference:

https://developers.openai.com/codex/guides/agents-md

### 7. OpenAI Codex Agents SDK Multi Agent Workflows

**Best for:** Programmatic orchestration beyond CLI prompting.

Key takeaways:

1. Codex CLI can be exposed as an MCP server.
2. The OpenAI Agents SDK can orchestrate multi agent workflows.
3. This is the right path when you want deterministic, traceable, repeatable software delivery pipelines.

Reference:

https://developers.openai.com/codex/guides/agents-sdk

### 8. Travis Neuman Agent Teams Composition Skill

**Best for:** A ready made Claude Code skill that knows when to suggest agent teams.

Key takeaways:

1. Suggest teams for comprehensive review, cross layer work, unclear bugs, competing approaches, and independent file separated workstreams.
2. Do not use teams for sequential work, same file edits, small tasks, or token constrained work.
3. Useful templates include full review, feature development, and debug squad.

Reference:

https://github.com/travisjneuman/.claude/blob/master/skills/agent-teams/SKILL.md

### 9. Zoran Spirkovski Creating Agent Teams Plugin

**Best for:** Claude Code plugin that decides between a single agent, parallel subagents, and coordinated agent teams.

Key takeaways:

1. Helps analyze tasks and choose the right execution model.
2. Selects model tier by role.
3. Chooses agent types.
4. Avoids token waste, scope creep, and coordination overhead.

Reference:

https://github.com/ZoranSpirkovski/creating-agent-teams

### 10. ShakaCode File By File Review Command

**Best for:** Concrete example of parallel subagent review.

Key takeaways:

1. Splits a large PR by changed file.
2. Launches parallel Task agents in batches.
3. Gives every worker one file and one clear verdict.
4. Checks for missing reviews.
5. Composes a final summary after all workers complete.

Reference:

https://github.com/shakacode/claude-code-commands-skills-agents/blob/main/commands/file-by-file-review.md

## Recommended Skill Set

### Skill 1: Parallel Work Orchestrator

**Purpose:** Decide whether the task should be handled by one agent, several subagents, or a full team.

Use when:

1. The task touches multiple files, modules, layers, or concerns.
2. The task has independent research paths.
3. The task is a large PR review.
4. The task has unclear root cause.
5. The task needs security, performance, tests, and architecture reviewed independently.
6. The feature can be split by frontend, backend, data, tests, documentation, or infrastructure.

Do not use when:

1. The task is small and targeted.
2. The work requires many edits to the same file.
3. The workflow is strictly sequential.
4. The cost of coordination exceeds the benefit.
5. The user explicitly asks for a single agent workflow.

### Skill 2: Codebase Explorer

**Purpose:** Map the code before implementation.

Use one or more explorers in parallel when different areas need investigation.

Common assignments:

1. Authentication flow.
2. Database schema.
3. API endpoints.
4. UI components.
5. Build and deployment.
6. Test harness.
7. Existing conventions.

### Skill 3: Feature Implementer

**Purpose:** Make isolated code changes.

Use only when file ownership is clear.

Rules:

1. Each implementer owns a defined file set.
2. No two implementers edit the same file.
3. Implementers must preserve existing patterns.
4. Implementers must report changed files and validation steps.
5. The lead merges and resolves conflicts.

### Skill 4: Test Writer and Validator

**Purpose:** Add or update tests in parallel with implementation.

Rules:

1. Add positive tests.
2. Add negative tests.
3. Add regression tests for bug fixes.
4. Run targeted tests.
5. Report failing tests with exact commands and failure summaries.

### Skill 5: Security Reviewer

**Purpose:** Review changes for security risk.

Common focus areas:

1. Authentication.
2. Authorization.
3. Secrets.
4. Input validation.
5. Injection risks.
6. Data exposure.
7. Permissions.
8. Dependency risk.

### Skill 6: Performance Reviewer

**Purpose:** Treat performance as a feature.

Common focus areas:

1. Response time.
2. Memory use.
3. Bundle size.
4. Query count.
5. N plus one queries.
6. Caching.
7. Rendering efficiency.
8. Scalability.

### Skill 7: Final Integrator

**Purpose:** Synthesize all agent results and produce the final answer or patch.

Rules:

1. Wait for all agents.
2. Compare results.
3. Resolve contradictions.
4. Merge only compatible changes.
5. Run final validation.
6. Produce a concise report.

## Ready To Use Skill: Parallel Agent Orchestration

Save this as:

```text
parallel-agent-orchestration/SKILL.md
```

```markdown
---
name: parallel-agent-orchestration
description: Breaks complex coding work into independent workstreams, assigns parallel agents or subagents, prevents file conflicts, waits for all results, synthesizes findings, and verifies the final result.
---

# Parallel Agent Orchestration Skill

## Purpose

Use this skill when a coding task can be split across independent workstreams and completed faster or better with specialized agents or subagents.

The goal is not to create agents for show. The goal is to improve correctness, speed, coverage, and confidence.

## Core Principle

Split only what can safely run independently.

Parallelize research, review, testing, and file separated implementation.

Do not parallelize tightly coupled edits to the same file or sequential work that depends on unfinished decisions.

## Default Execution Model

When a task is complex:

1. Inspect the request.
2. Identify independent workstreams.
3. Choose the minimum number of agents needed.
4. Assign each agent a narrow role.
5. Give each agent explicit scope, files, tools, and deliverables.
6. Prevent overlapping edits.
7. Run agents in parallel where safe.
8. Wait for all agents.
9. Synthesize results.
10. Resolve contradictions.
11. Run final validation.
12. Report changes, decisions, risks, and verification.

## Use Single Agent When

1. The task is small.
2. The change is localized.
3. The work requires edits to one file.
4. The work is sequential.
5. The user needs a quick answer.
6. Parallel coordination would cost more than it saves.

## Use Subagents When

1. The work is independent.
2. The output would pollute the main context.
3. Each worker can return a summary.
4. Workers do not need to talk to each other.
5. The task is research, review, testing, or isolated analysis.

Examples:

1. Explore three modules in parallel.
2. Review security, performance, and test coverage in parallel.
3. Run test suite analysis in a separate context.
4. Compare several implementation approaches.

## Use Agent Teams When

1. Workers need to coordinate with each other.
2. Workers need to challenge assumptions.
3. The task has competing hypotheses.
4. The feature spans frontend, backend, database, and tests.
5. Workers need a shared task list.
6. The work is large enough to justify coordination overhead.

Examples:

1. Parallel PR review with security, performance, and test reviewers.
2. Debugging with competing root cause hypotheses.
3. Feature development split by frontend, backend, and tests.
4. Architecture review where teammates debate tradeoffs.

## Workstream Types

Use these workstream patterns:

### Research Workstream

Goal: understand the codebase or external docs.

Output:

1. Relevant files.
2. Key symbols.
3. Execution path.
4. Risks.
5. Recommended next step.

### Implementation Workstream

Goal: make scoped code changes.

Output:

1. Files changed.
2. Behavior changed.
3. Tests added or updated.
4. Commands run.
5. Risks or follow up work.

### Test Workstream

Goal: add and run tests.

Output:

1. Positive tests.
2. Negative tests.
3. Regression tests.
4. Commands run.
5. Failing tests and likely cause.

### Review Workstream

Goal: evaluate code quality.

Output:

1. Findings ranked by severity.
2. File and symbol references.
3. Reproduction or reasoning.
4. Recommended fix.
5. Confidence level.

### Integration Workstream

Goal: merge results.

Output:

1. Final changes.
2. Conflicts resolved.
3. Final validation.
4. Final summary.

## Agent Assignment Rules

Each agent must receive:

1. Role.
2. Objective.
3. Scope.
4. Files or modules allowed.
5. Files or modules forbidden.
6. Expected deliverable.
7. Validation command.
8. Reporting format.

## File Conflict Rules

Never allow two agents to edit the same file unless one is explicitly assigned as the integrator.

If overlap is unavoidable:

1. Make one agent read only.
2. Make one agent the editor.
3. Have the lead merge the findings.
4. Run final tests after merge.

## Minimum Useful Team Patterns

### Three Agent Review Team

Use for PR reviews.

1. Security reviewer.
2. Performance reviewer.
3. Test coverage reviewer.

Lead synthesizes all findings.

### Three Agent Feature Team

Use for a medium feature.

1. Architect or explorer.
2. Implementer.
3. Test writer.

Architect researches first. Implementer and test writer proceed after scope is clear.

### Four Agent Cross Layer Team

Use for full stack work.

1. Frontend implementer.
2. Backend implementer.
3. Data or integration implementer.
4. Test validator.

Lead owns integration and final test run.

### Five Agent Debug Squad

Use when root cause is unclear.

1. Hypothesis A investigator.
2. Hypothesis B investigator.
3. Hypothesis C investigator.
4. Logs and telemetry investigator.
5. Regression and test investigator.

Each investigator must try to disprove its own theory and challenge other theories.

## Required Final Synthesis

After agents finish, the lead must produce:

1. What each agent did.
2. Findings by agent.
3. Conflicts or contradictions.
4. Decision made.
5. Files changed.
6. Tests run.
7. Final result.
8. Remaining risks.

## Do Not Stop Early

Do not return partial work merely because one agent finished.

Wait for all assigned agents unless:

1. A critical failure invalidates the plan.
2. A permission problem blocks execution.
3. A security or data loss risk appears.
4. The user interrupts or redirects.

## Quality Gates

Before completion:

1. Run targeted tests.
2. Run lint or type checks when available.
3. Run broader tests when practical.
4. Verify no two agents produced incompatible edits.
5. Verify implementation matches the request.
6. Verify tests cover positive and negative cases when behavior changed.

## Claude Code Guidance

For Claude Code:

1. Use normal subagents for isolated research, review, and test analysis.
2. Use `context: fork` skills when the skill itself is an executable task.
3. Use Agent Teams for sustained parallel work where teammates must communicate.
4. Prefer three to five teammates.
5. Avoid same file edits across teammates.
6. Ask the lead to wait for teammates before final synthesis.

Example prompt:

```text
Create an agent team for this feature. Split the work into frontend, backend, tests, and final integration. Each teammate owns separate files. Wait for all teammates, synthesize the results, run final tests, and report risks.
```

## Codex Guidance

For Codex:

1. Explicitly ask Codex to spawn subagents.
2. Use custom agents for explorer, reviewer, implementer, test validator, and docs researcher.
3. Keep agents narrow and opinionated.
4. Set read only sandbox mode for reviewers and explorers.
5. Use AGENTS.md for mandatory orchestration behavior.
6. Use skills for reusable workflows.

Example prompt:

```text
Spawn one Codex subagent per workstream: codebase explorer, implementation planner, test coverage reviewer, and security reviewer. Wait for all of them, consolidate the findings, choose the safest implementation path, make the changes, run tests, and summarize the final result.
```

## Reporting Format

Use this final format:

```markdown
## Result

<one paragraph summary>

## Agent Workstreams

| Agent | Scope | Result | Status |
|---|---|---|---|
| Explorer | <scope> | <summary> | Complete |
| Implementer | <scope> | <summary> | Complete |
| Test Validator | <scope> | <summary> | Complete |

## Decisions

1. <decision and rationale>

## Files Changed

1. `<file>`: <summary>

## Validation

1. `<command>`: <result>

## Risks

1. <risk or none>
```
```

## Recommended Claude Code Setup

### Directory Structure

```text
.claude/
  skills/
    parallel-agent-orchestration/
      SKILL.md
  agents/
    security-reviewer.md
    performance-reviewer.md
    test-validator.md
    codebase-explorer.md
    feature-implementer.md
```

### Example Claude Subagent: Security Reviewer

```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities, auth risks, input validation, secrets, permissions, and data exposure.
tools: Read, Glob, Grep, Bash
model: sonnet
---

You are a security reviewer.

Review only for real security risk. Prioritize authentication, authorization, secrets, input validation, injection, data exposure, dependency risk, and unsafe permissions.

Return findings with severity, file references, rationale, and recommended fixes.

Do not edit files unless explicitly instructed.
```

### Example Claude Subagent: Test Validator

```markdown
---
name: test-validator
description: Adds, reviews, and runs positive, negative, and regression tests for behavior changing code.
tools: Read, Glob, Grep, Bash, Edit, Write
model: sonnet
---

You are a test validator.

Focus on test coverage and behavior verification.

Add or update tests when behavior changes. Include positive tests, negative tests, and regression tests where appropriate.

Run targeted tests and report exact commands and results.
```

### Example Claude Skill Frontmatter for Forked Research

```markdown
---
name: deep-codebase-research
description: Researches a codebase area in an isolated subagent context and returns concise findings.
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly.

Return:
1. Relevant files.
2. Key symbols.
3. Execution path.
4. Risks.
5. Recommended next step.
```

## Recommended Codex Setup

### Directory Structure

```text
AGENTS.md
.codex/
  config.toml
  agents/
    explorer.toml
    reviewer.toml
    test_validator.toml
    implementer.toml
skills/
  parallel-agent-orchestration/
    SKILL.md
```

### AGENTS.md Core Instruction

```markdown
# Agent Orchestration

For complex coding tasks, break work into independent workstreams and use Codex subagents when the work can run safely in parallel.

Use subagents for:
1. Codebase exploration.
2. PR review.
3. Security review.
4. Performance review.
5. Test coverage review.
6. Independent implementation tasks with non overlapping file ownership.

Do not use subagents for:
1. Small single file edits.
2. Sequential tasks.
3. Same file edits by multiple workers.
4. Work where coordination overhead exceeds the value.

Always wait for all subagents, synthesize results, choose the best path, implement safely, run tests, and report final validation.
```

### Codex Config

```toml
[agents]
max_threads = 6
max_depth = 1
```

### Codex Custom Agent: Explorer

```toml
name = "explorer"
description = "Read only codebase explorer that maps files, symbols, dependencies, and execution paths before implementation."
model_reasoning_effort = "medium"
sandbox_mode = "read-only"

developer_instructions = """
Stay in exploration mode.
Do not edit files.
Trace the real execution path.
Cite files, symbols, and commands.
Return concise findings and recommended next steps.
"""
```

### Codex Custom Agent: Reviewer

```toml
name = "reviewer"
description = "Read only reviewer focused on correctness, security, performance, maintainability, and missing tests."
model_reasoning_effort = "high"
sandbox_mode = "read-only"

developer_instructions = """
Review like an owner.
Prioritize correctness, security, regressions, missing tests, and performance risk.
Avoid style only comments unless they hide a real bug.
Return concrete findings with severity and file references.
"""
```

### Codex Custom Agent: Test Validator

```toml
name = "test_validator"
description = "Test specialist that adds or reviews positive, negative, and regression tests and verifies behavior."
model_reasoning_effort = "medium"

developer_instructions = """
Focus on tests and behavior verification.
Add or update tests only within the assigned scope.
Include positive, negative, and regression tests when appropriate.
Run targeted tests and report exact commands and results.
"""
```

### Codex Custom Agent: Implementer

```toml
name = "implementer"
description = "Implementation focused worker for scoped file separated coding tasks."
model_reasoning_effort = "high"

developer_instructions = """
Implement only the assigned scope.
Follow existing code patterns.
Do not edit files outside the assigned scope.
Add or update tests when behavior changes.
Run validation and report changed files, commands, and results.
"""
```

## Best Prompt Patterns

### Claude Code Parallel Review

```text
Create an agent team to review this PR. Spawn three reviewers:
1. Security reviewer.
2. Performance reviewer.
3. Test coverage reviewer.

Each reviewer should work independently, report findings with severity and file references, then the lead should synthesize the results into one final review.
```

### Claude Code Parallel Feature Work

```text
Use agent teams for this feature. Split the work into frontend, backend, tests, and final integration. Each teammate owns separate files. Require plan approval before implementation. Wait for all teammates before final synthesis. Run final tests.
```

### Codex Parallel PR Review

```text
Review this branch against main. Spawn one subagent per review area:
1. Security.
2. Code quality.
3. Bugs.
4. Race conditions.
5. Test flakiness.
6. Maintainability.

Wait for all subagents and return a consolidated review with severity, file references, and recommended fixes.
```

### Codex Parallel Feature Planning

```text
Spawn subagents for architecture, codebase exploration, test strategy, and risk review. Have each return concise findings. Wait for all results, choose the best implementation path, then implement the smallest safe change and run tests.
```

## Practical Recommendations

### Best Default Setup

Use this default system:

1. `parallel-agent-orchestration` skill.
2. Codebase explorer agent.
3. Security reviewer agent.
4. Performance reviewer agent.
5. Test validator agent.
6. Implementer agent.
7. Final integrator behavior in the lead agent.

### Best Team Size

Start with three agents.

Scale to five when the task has truly independent workstreams.

Avoid more than five unless the work is batch oriented, such as one file per worker or one package per worker.

### Best First Use Cases

1. Large PR review.
2. Security review.
3. Performance review.
4. Test coverage review.
5. Codebase exploration.
6. Debugging with competing hypotheses.
7. Full stack feature split by layer.

### Avoid Parallel Agents For

1. Single file edits.
2. Highly coupled refactors.
3. Tasks requiring constant human judgment.
4. Small fixes.
5. Production changes with unclear rollback.
6. Anything likely to create merge conflicts.

## Final Recommendation

Create one reusable skill named:

```text
parallel-agent-orchestration
```

Then install supporting agents for:

1. Explorer.
2. Implementer.
3. Test validator.
4. Security reviewer.
5. Performance reviewer.
6. Final integrator.

For **Claude Code**, use subagents for isolated work and Agent Teams when agents need to coordinate.

For **Codex**, explicitly ask it to spawn subagents and define custom agents under `.codex/agents/`.

Put mandatory behavior in:

1. `CLAUDE.md` for Claude Code.
2. `AGENTS.md` for Codex.

Use skills for the reusable workflow.
