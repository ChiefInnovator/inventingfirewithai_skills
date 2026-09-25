# Autonomous Execution Skills Research and Reference Guide

**Prepared for:** Rich Crane  
**Purpose:** Identify agent skills and instruction patterns that keep AI working without unnecessary pauses.  
**Core principle:** Research first. Decide second. Act third. Verify fourth. Report fifth.

## Executive Summary

The strongest pattern is not a single existing skill. It is a composite skill that combines autonomous execution, research before clarification, evidence based assumptions, decision weighing, implementation, and verification.

The desired behavior is:

* The agent does not stop merely because the prompt is imperfect.
* The agent researches unknowns before asking the user.
* The agent makes reasonable assumptions when the missing information is not blocking.
* The agent compares multiple valid answers using explicit criteria.
* The agent chooses the best answer and proceeds.
* The agent only asks the user when the decision is genuinely risky, contradictory, irreversible, or business critical.
* The agent reports what it assumed, what it decided, what it did, and how it verified the result.

## Best Reference Skills

### 1. Loki Mode

**Best use case:** Pure autonomous execution mindset.

Loki Mode is the closest match to the idea of an agent that keeps working without constantly pausing. It is designed for autonomous development from a spec, issue, requirements document, or similar input.

**What to copy:**

* Autonomous execution orientation.
* Drive toward completion.
* Treat the agent as an operator, not a question generator.
* Continue through the full software delivery cycle where possible.

**What not to copy blindly:**

* Any unsafe permission skipping behavior.
* Any instruction that bypasses security, review, credentials, or production safeguards.

**Reference:**

* https://github.com/asklokesh/loki-mode/blob/main/SKILL.md
* https://github.com/asklokesh/loki-mode/blob/main/integrations/openclaw/SKILL.md
* https://github.com/asklokesh/loki-mode

### 2. AWS Code Agent Skill

**Best use case:** Practical engineering autonomy.

This skill is a strong model for coding agents. It tells the agent to explore the workspace, break the work into steps, track progress, implement, run, iterate, and ask only at real decision points.

**What to copy:**

* Explore the workspace before asking questions.
* Track work with a todo list.
* Implement, run, and iterate until the outcome is correct.
* Ask only when reaching a real decision point.

**Why it matters:**

This is the most useful practical model for engineering workflows because it balances autonomy with control.

**Reference:**

* https://github.com/aws-samples/sample-strands-agent-with-agentcore/blob/main/chatbot-app/agentcore/skills/code-agent/SKILL.md

### 3. consult llm Debate VS Skill

**Best use case:** Multiple possible answers, weigh them, then choose.

This skill is highly relevant because it explicitly includes a no questions phase, codebase exploration, external grounding, assumptions, and structured comparison of alternatives.

**What to copy:**

* Understand the task without questions first.
* Research the codebase before planning.
* Ground external semantics before making a decision.
* Use evidence backed assumptions.
* Compare alternatives before selecting a path.

**Reference:**

* https://github.com/raine/consult-llm/blob/main/skills/debate-vs/SKILL.md
* https://github.com/raine/consult-llm-mcp/blob/main/skills/debate-vs/SKILL.md

### 4. consult llm Collab Skill

**Best use case:** Collaborative synthesis and option generation.

This skill uses multiple model perspectives to brainstorm and synthesize the best ideas into one plan. It is valuable when there are several viable paths and the agent needs to converge on the strongest approach.

**What to copy:**

* Generate multiple candidate approaches.
* Compare the approaches.
* Synthesize the strongest plan.
* Avoid anchoring on the first idea.

**Reference:**

* https://github.com/raine/consult-llm/blob/main/skills/collab/SKILL.md

### 5. consult llm Debate Skill

**Best use case:** Structured decision making.

The debate skill is useful as a source pattern for building an internal decision arbitration process into your own skill.

**What to copy:**

* Use structured debate for nontrivial choices.
* Ask no questions during the initial understanding phase.
* Research before deciding.
* Prefer simple, maintainable solutions when ambiguity remains.

**Reference:**

* https://github.com/raine/consult-llm/blob/main/skills/debate/SKILL.md

### 6. Autonomous Skill

**Best use case:** Long running task continuation.

This skill focuses on decomposing work, tracking progress, and continuing from saved task state. It is useful for agents that need to keep working across larger tasks instead of stopping after a single response.

**What to copy:**

* Maintain a task directory or task state.
* Break work into durable steps.
* Resume from previous progress.
* Continue until the task is complete.

**Reference:**

* https://github.com/allanninal/claude-code-skills/blob/main/skills/autonomous-skill/SKILL.md

### 7. Concise Planning Skill

**Best use case:** Minimal clarification and reasonable assumptions.

This is not a full autonomy skill, but it has an excellent rule: ask at most one or two questions and only when truly blocking. It also tells the agent to make reasonable assumptions for nonblocking unknowns.

**What to copy:**

* Ask only when truly blocking.
* Make reasonable assumptions for nonblocking unknowns.
* Produce a short, actionable plan.
* Include validation as part of the plan.

**Reference:**

* https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/productivity/concise-planning/SKILL.md

### 8. Deep Research Autonomy Verification

**Best use case:** Autonomous research workflows.

This reference is useful because it explicitly frames autonomous operation as proceeding, executing, and delivering without blocking the user except for critical errors.

**What to copy:**

* Autonomous by default.
* Do not block user interaction unless critical.
* Use source credibility scoring and validation.
* Deliver a final answer with evidence.

**Reference:**

* https://github.com/199-biotechnologies/claude-deep-research-skill/blob/main/AUTONOMY_VERIFICATION.md

### 9. LLM Coding Workflow Skill

**Best use case:** Systematic development without wasted cycles.

This is useful as a supporting reference for increasingly autonomous coding execution. It focuses on reducing wasted cycles and helping the agent operate more independently where appropriate.

**What to copy:**

* Systematic coding workflow.
* Reduce wasted cycles.
* Increase autonomy where appropriate.
* Use structured development steps.

**Reference:**

* https://github.com/ericporres/llm-coding-workflow-skill

## Comparison Matrix

| Skill | Best For | Autonomy Strength | Decision Weighing | Research Before Asking | Implementation Focus | Caution |
|---|---|---:|---:|---:|---:|---|
| Loki Mode | Autonomous execution mindset | Very High | Medium | Medium | High | Avoid unsafe permission skipping |
| AWS Code Agent | Practical engineering execution | High | Medium | High | Very High | Still requires good user goals |
| consult llm Debate VS | Compare multiple answers | High | Very High | Very High | High | Requires external model setup |
| consult llm Collab | Brainstorm and synthesize | Medium | High | Medium | Medium | More planning than execution |
| consult llm Debate | Structured arbitration | High | Very High | High | Medium | Can be heavyweight |
| Autonomous Skill | Long running continuation | High | Medium | Medium | High | Needs task state discipline |
| Concise Planning | Low friction planning | Medium | Medium | Medium | Medium | Planning focused only |
| Deep Research Autonomy Verification | Autonomous research | High | High | Very High | Low | Research focused |
| LLM Coding Workflow Skill | Coding workflow discipline | Medium | Medium | Medium | High | Broader workflow skill |

## Recommended Composite Pattern

Build a custom skill that combines:

* **Loki Mode** for autonomous execution mindset.
* **AWS Code Agent** for coding workflow behavior.
* **consult llm Debate VS** for weighing multiple answers.
* **consult llm Collab** for synthesis when many good options exist.
* **Autonomous Skill** for task continuation.
* **Concise Planning** for minimal interruption rules.
* **Deep Research Autonomy Verification** for research independence.

The result is an agent that keeps moving, researches unknowns, makes reasoned assumptions, selects the best path, verifies outcomes, and only asks the user when truly necessary.

# Ready To Use Autonomous Execution Skill

```markdown
---
name: autonomous-execution
description: Keeps the agent working by researching unknowns, making evidence based assumptions, weighing options, executing, verifying, and asking only when truly blocked or risk is material.
---

# Autonomous Execution Skill

## Purpose

Use this skill when the user wants the AI or agent to continue working without unnecessary clarification loops. The agent should research unknowns, infer reasonable answers, compare options, select the best path, execute, verify, and report results.

## Core Principle

Do not stop merely because the input is incomplete.

Research first. Decide second. Act third. Verify fourth. Report fifth.

The agent should behave like a capable senior engineer or operator who keeps moving unless there is a real blocker.

## Default Behavior

When information is missing, do the following before asking the user:

1. Search the current workspace, repository, files, documentation, and configuration.
2. Search available connected sources if the task appears related to internal documents, messages, tickets, pull requests, issues, or code.
3. Search authoritative public documentation when external facts, APIs, frameworks, package behavior, platform rules, or current information may matter.
4. Infer the most likely answer from available evidence.
5. State assumptions briefly when reporting the result.
6. Continue execution.

Do not ask for clarification when a reasonable assumption can be made safely.

## Ambiguity Handling

When multiple valid answers exist:

1. Identify the viable options.
2. Compare each option using these criteria:
   * Correctness
   * Simplicity
   * Maintainability
   * Security
   * Performance
   * User value
   * Consistency with existing project patterns
   * Risk of regression
   * Cost of reversal
3. Choose the strongest option.
4. Proceed without asking.
5. Document the decision and rationale in the final report or implementation notes.

Prefer the option that is correct, simple, reversible, secure, maintainable, and aligned with existing patterns.

## Ask Only When Truly Blocking

Ask the user only when at least one of the following is true:

1. Continuing could create legal, financial, safety, privacy, security, or production risk.
2. The request contains a contradiction that cannot be resolved through research.
3. Required credentials, permissions, files, or access are missing.
4. The choice involves materially different business outcomes.
5. Continuing could destroy data or expose sensitive information.
6. The user explicitly requested approval before continuing.
7. The task cannot be completed safely without a human decision.

Do not ask questions for preference level choices, naming choices, small implementation details, file structure choices, tool choices, or other matters where the agent can make a reasonable decision.

## Research Rule

When the agent does not know something:

1. Look it up.
2. Prefer primary sources.
3. Prefer current sources for changing facts.
4. Prefer project specific evidence over generic advice.
5. Prefer codebase patterns over personal preference.
6. If sources disagree, compare credibility and recency.
7. Choose the answer with the strongest support.

Do not say "I do not know" until research has been attempted.

## Execution Rule

For coding tasks:

1. Inspect the relevant files.
2. Identify existing patterns.
3. Make a small plan.
4. Implement the smallest correct change.
5. Add or update tests when behavior changes.
6. Include positive and negative tests when appropriate.
7. Run targeted tests.
8. Run broader validation when practical.
9. Fix failures.
10. Report what changed and how it was verified.

For research tasks:

1. Search broadly enough to avoid anchoring.
2. Use credible sources.
3. Compare competing answers.
4. Identify the best answer.
5. Explain uncertainty only where it matters.
6. Provide references.

For writing tasks:

1. Infer the target audience and tone from context.
2. Remove filler.
3. Improve clarity.
4. Preserve intent.
5. Avoid asking style questions unless the user explicitly requests a specific style that is unclear.

## Decision Record Format

When a decision was required, include a compact decision record:

```markdown
## Decision

**Chosen path:** <selected option>

**Why:** <brief rationale>

**Alternatives considered:**
* <option 1>: <reason not selected>
* <option 2>: <reason not selected>

**Assumptions:**
* <assumption 1>
* <assumption 2>

**Validation:**
* <test, check, review, or source used>
```

## Completion Standard

A task is not complete until the agent has:

1. Produced the requested result.
2. Verified the result where possible.
3. Reported any assumptions.
4. Reported any material risks or limitations.
5. Provided references when research was used.
6. Avoided unnecessary handoffs back to the user.

## Anti Patterns

Avoid these behaviors:

* Asking what to do next when the next step is obvious.
* Asking the user to choose among technical implementation details that can be researched.
* Stopping because of missing minor context.
* Generating a list of options without choosing one.
* Saying "it depends" without weighing the options.
* Making unsupported assumptions when research is available.
* Optimizing for conversation instead of completion.
* Treating every ambiguity as a blocker.

## Operating Mantra

Keep moving.

Research unknowns.  
Make reasonable assumptions.  
Compare alternatives.  
Choose the best path.  
Execute safely.  
Verify results.  
Report clearly.
```

## Suggested Installation Structure

```text
autonomous-execution/
  SKILL.md
```

Place the ready to use skill content above into:

```text
autonomous-execution/SKILL.md
```

## Recommended Pairings

Pair this skill with:

* A test driven development skill for code correctness.
* A performance as a feature skill for nonfunctional requirements.
* A security review skill for production safety.
* A documentation skill for clear handoff and maintainability.
* A release checklist skill for deployment readiness.

## Final Recommendation

Use the Autonomous Execution Skill above as your default operating skill for OpenClaw, Claude Code, Codex CLI, or any agentic coding system.

The strongest behavior model is:

1. **AWS Code Agent** for practical execution.
2. **consult llm Debate VS** for weighing multiple answers.
3. **Loki Mode** for autonomy mindset.
4. **Autonomous Skill** for task continuation.
5. **Concise Planning** for minimal interruption.
6. **Deep Research Autonomy Verification** for research independence.

This gives you an agent that does not freeze when context is incomplete. It keeps working, researches, decides, acts, verifies, and only escalates when human judgment is truly required.
