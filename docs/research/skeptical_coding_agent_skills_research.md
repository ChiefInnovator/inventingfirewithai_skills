# Skeptical Coding Agent Skills Research

**Prepared for:** Rich Crane  
**Prepared on:** May 02, 2026, 01:04 PM EST  
**Focus:** Coding agent skills that force agents to second guess themselves, trust but verify, play devil's advocate, and avoid guessing.  
**Primary platforms:** Claude Code, OpenAI Codex, GitHub Copilot style agents, and general Agent Skills compatible coding tools.

## Executive Summary

The best solution is a skill stack, not one skill.

The behavior you want has four parts:

1. **Always second guess:** The agent must challenge its own plan, code, and assumptions before calling work complete.
2. **Trust but verify:** The agent must run tests, builds, linters, grep checks, or runtime checks before claiming success.
3. **Play devil's advocate:** The agent must intentionally argue against its own implementation and look for hidden failure modes.
4. **No guessing:** The agent must research APIs, read code, inspect actual files, and cite evidence instead of inventing details.

Recommended skill stack:

1. Adversarial Code Reviewer.
2. Verification Before Completion.
3. Quality Playbook.
4. Devil's Advocate Review.
5. Evidence Based Code Review.
6. Doublecheck.
7. Research Engineer.
8. Research Learn Implement.
9. Security API Preconditions for endpoint work.
10. TDD for proof through tests.

## Best Existing Skills and References

## 1. Adversarial Code Reviewer

**Best for:** Always second guess and play devil's advocate.

This skill forces genuine perspective shifts through hostile reviewer personas. The personas include a production breaker, a maintainability critic, and a security auditor. Each persona must find at least one issue, which prevents empty "looks good" reviews.

**Behavior covered:**

1. Always second guess.
2. Devil's advocate.
3. Security skepticism.
4. Maintainability skepticism.
5. Merge blocking review.

**Why it matters:**

AI generated code often receives weak self review because the reviewer shares the same mental model as the author. This skill deliberately breaks that pattern.

**Reference:**

https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/adversarial-reviewer/SKILL.md

## 2. Devil's Advocate Code Review

**Best for:** Pre pull request code challenge.

This Claude Code slash command simulates a multi round review between an Author and a Reviewer. It reviews the current branch diff against `master`, then works through correctness, error handling, performance, security, maintainability, and testing gaps.

**Behavior covered:**

1. Play devil's advocate.
2. Always second guess.
3. Pre pull request review.
4. Concrete action items.
5. Prioritized review topics.

**Why it matters:**

This is useful when the agent has already implemented a change and needs to debate whether it is actually ready.

**Reference:**

https://github.com/richiethomas/claude-devils-advocate

Direct command file:

https://github.com/richiethomas/claude-devils-advocate/blob/main/devils-advocate.md

## 3. Devil's Advocate Plugin

**Best for:** Adversarial self critique before shipping.

This Claude Code plugin adds adversarial self critique to every task. It scores work across multiple dimensions, identifies weaknesses, and proposes improvements before shipping.

**Behavior covered:**

1. Always second guess.
2. Devil's advocate.
3. Self critique.
4. Improvement before completion.
5. Risk scoring.

**Reference:**

https://github.com/brandonsimpson/devils-advocate

## 4. Adversarial Code Review with Claude and Codex

**Best for:** External reviewer pattern.

This skill orchestrates Claude and Codex interaction where Claude is the executor and Codex is the external reviewer. The important pattern is that the executor should not be the only reviewer.

**Behavior covered:**

1. Trust but verify.
2. External review.
3. Second model review.
4. Cross agent skepticism.
5. Reduced same model blind spots.

**Why it matters:**

The strongest review often comes from a different model or agent role. This avoids self validation by the same context that wrote the code.

**Reference:**

https://github.com/dementev-dev/adversarial-review/blob/master/SKILL.md

## 5. Devs Advocate Skill Collection

**Best for:** General hidden risk discovery.

This skill challenges AI generated plans, code, and decisions. It uses pre mortem analysis, inversion thinking, Socratic questioning, engineering blind spot categories, and AI specific failure patterns.

**Behavior covered:**

1. Always second guess.
2. Devil's advocate.
3. Hidden assumption discovery.
4. Pre mortem analysis.
5. Blind spot detection.

**Reference:**

https://github.com/notmanas/claude-code-skills

## 6. Contrarian Agent

**Best for:** Architecture and plan stress testing.

This is a devil's advocate analyst agent for Claude Code. It stress tests proposals by challenging assumptions. It is focused on strategy, approach, hidden risks, pre mortem analysis, architecture reviews, and decision validation.

**Behavior covered:**

1. Always second guess.
2. Devil's advocate.
3. Architecture skepticism.
4. Decision validation.
5. Hidden risk analysis.

**Reference:**

https://github.com/aaddrick/contrarian

## 7. Code Review Skill with Verification Gates

**Best for:** Evidence based code review and completion claims.

This code review skill emphasizes technical rigor over performative agreement, systematic review through a code reviewer subagent, and verification gates requiring evidence before status claims.

**Behavior covered:**

1. Trust but verify.
2. No empty agreement.
3. Evidence before completion.
4. Review before proceeding.
5. Technical rigor.

**Why it matters:**

This is directly aligned with "trust but verify." The agent cannot just accept review feedback or declare completion. It must technically evaluate and verify.

**Reference:**

https://github.com/congdon1207/agents.md/blob/main/.claude/skills/code-review/SKILL.md

## 8. Verification Before Completion

**Best for:** Trust but verify.

This skill enforces the rule that the agent cannot claim work is complete, fixed, or passing without fresh verification evidence. It requires running verification commands and confirming actual output before success claims.

**Behavior covered:**

1. Trust but verify.
2. Evidence before claims.
3. No premature completion.
4. Builds and tests before completion.
5. Red green verification for fixes.

**Why it matters:**

This is the strongest "do not lie about success" skill. It prevents false confidence.

**Reference:**

https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md

Related marketplace description:

https://mcpmarket.com/tools/skills/verification-before-completion-1777161173961

## 9. Quality Playbook

**Best for:** No hallucinated code review findings.

This GitHub Awesome Copilot skill includes review guardrails that prevent hallucinated findings. It emphasizes line numbers, grep before claiming, and reading actual code bodies before making review assertions.

**Behavior covered:**

1. No guessing.
2. Evidence based review.
3. Trust but verify.
4. Code review with guardrails.
5. Integration test protocol.

**Why it matters:**

A common AI review failure is making plausible claims about code that was not actually inspected. This skill directly addresses that.

**Reference:**

https://github.com/github/awesome-copilot/blob/main/skills/quality-playbook/SKILL.md

## 10. Doublecheck Skill

**Best for:** External evidence for claims.

This skill extracts claims and searches for external evidence so users can independently verify the claims.

**Behavior covered:**

1. Trust but verify.
2. No guessing.
3. Claim extraction.
4. Source verification.
5. Independent evidence.

**Why it matters:**

This is more research focused than coding focused, but the claim extraction pattern is very useful for code review reports, architecture recommendations, and technical claims.

**Reference:**

https://github.com/github/awesome-copilot/blob/main/skills/doublecheck/SKILL.md

## 11. Generic Code Review Instructions

**Best for:** Broad review checklist.

This GitHub Awesome Copilot instruction set provides structured code review guidance covering code quality, security, testing, and architecture.

**Behavior covered:**

1. Trust but verify.
2. Review discipline.
3. Security and testing checks.
4. Architecture checks.
5. Reusable review process.

**Reference:**

https://github.com/github/awesome-copilot/blob/main/instructions/code-review-generic.instructions.md

## 12. Verify Skill Pattern

**Best for:** Runtime observation.

This skill pattern defines verification as runtime observation. The agent builds the app, runs it, drives it to where changed code executes, and captures evidence.

**Behavior covered:**

1. Trust but verify.
2. Runtime proof.
3. Manual validation.
4. No assertion without observation.
5. Change specific verification.

**Why it matters:**

Unit tests are not always enough. For UI, integration, or workflow changes, direct runtime observation can be the only reliable proof.

**Reference:**

https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/system-prompts/skill-verify-skill.md

## 13. Research Engineer Skill

**Best for:** No guessing before implementation.

This skill focuses on rigorous research, tool selection, and implementation discipline. It is useful when the agent does not know a library, package, standard, or correct implementation approach.

**Behavior covered:**

1. No guessing.
2. Research before coding.
3. Tool review.
4. Implementation discipline.
5. Correctness over speed.

**Reference:**

https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/ai-research/research-engineer/SKILL.md

## 14. Anthropic Skill Creator

**Best for:** Research before creating skills.

The official Skill Creator skill includes research before writing a skill. It checks similar skills, researches best practices, and uses parallel subagents when available.

**Behavior covered:**

1. No guessing.
2. Research before authoring.
3. Compare existing examples.
4. Use references.
5. Build skills with evidence.

**Reference:**

https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md

## 15. OpenAI Codex Skills and AGENTS.md

**Best for:** Making the behavior reusable and mandatory.

Codex skills package instructions, resources, and optional scripts so Codex can follow workflows reliably. Codex also reads `AGENTS.md` before doing work, making `AGENTS.md` the right place for mandatory rules like "no guessing" and "verify before claiming done."

**Behavior covered:**

1. Reusable skill.
2. Always on project policy.
3. No guessing rules.
4. Verification rules.
5. Consistent coding expectations.

**References:**

https://developers.openai.com/codex/skills

https://developers.openai.com/codex/guides/agents-md

## 16. Claude Code Skills and Best Practices

**Best for:** Skill authoring and Claude Code behavior.

Claude Code skills are reusable workflows that can be triggered when relevant. Claude Code best practices also emphasize effective agentic workflows across real codebases.

**Behavior covered:**

1. Skill based repeatability.
2. Claude specific workflow.
3. Reusable verification patterns.
4. Agent coding practices.
5. Better task reliability.

**References:**

https://code.claude.com/docs/en/best-practices

https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## Behavior Mapping

| Behavior | Best Skills |
|---|---|
| Always second guess | Adversarial Code Reviewer, Devil's Advocate Code Review, Contrarian Agent, Devs Advocate |
| Trust but verify | Verification Before Completion, Code Review Skill with Verification Gates, Verify Skill Pattern, Quality Playbook |
| Play devil's advocate | Devil's Advocate Code Review, Devil's Advocate Plugin, Contrarian Agent, Adversarial Code Reviewer |
| No guessing | Quality Playbook, Research Engineer, Doublecheck, Skill Creator, Research Learn Implement |
| Evidence before claims | Verification Before Completion, Code Review Skill with Verification Gates, Doublecheck, Verify Skill Pattern |
| External reviewer | Adversarial Code Review with Claude and Codex |
| Security skepticism | Adversarial Code Reviewer, Generic Code Review Instructions, Security API Preconditions |
| Runtime proof | Verify Skill Pattern, Quality Playbook, Verification Before Completion |
| Anti hallucination | Quality Playbook, Doublecheck, Verification Before Completion |
| Plan stress test | Contrarian Agent, Devs Advocate, Devil's Advocate Plugin |

## Recommended Skill Stack

Use these together.

### Core Stack

1. **verification-before-completion**
2. **adversarial-reviewer**
3. **quality-playbook**
4. **devils-advocate**
5. **research-engineer**

### Stronger Coding Stack

1. **TDD**
2. **security-api-preconditions**
3. **performance-as-a-feature**
4. **parallel-agent-orchestration**
5. **research-learn-implement**
6. **verification-before-completion**
7. **adversarial-reviewer**

### High Risk Change Stack

Use this for auth, payments, data deletion, migrations, security, production changes, or API boundary changes.

1. Research Engineer.
2. TDD.
3. Security API Preconditions.
4. Adversarial Code Reviewer.
5. Verification Before Completion.
6. External reviewer, ideally another model or subagent.
7. Final human approval if the change is irreversible or high risk.

## Recommended Mandatory Policy for AGENTS.md and CLAUDE.md

Use this policy in both Codex and Claude Code projects.

```markdown
# Skeptical Coding Policy

Do not guess.

When facts are missing:
1. Inspect the repository.
2. Search actual files.
3. Read function bodies before making claims.
4. Use grep, tests, builds, linters, or runtime checks as evidence.
5. Search official documentation when APIs, SDKs, frameworks, or current behavior matter.
6. State assumptions explicitly only when research cannot resolve them.

Always second guess:
1. Challenge the implementation before calling it done.
2. Look for hidden failure modes.
3. Look for missing negative tests.
4. Look for security, performance, maintainability, and edge case risks.
5. Ask what would break in production.

Trust but verify:
1. Do not claim work is complete without fresh verification evidence.
2. Run the relevant tests, build, type checks, linters, or runtime validation.
3. Report exact commands and results.
4. If verification cannot be run, say so clearly and do not claim it passed.

Play devil's advocate:
1. Argue against the chosen approach.
2. Identify the strongest objection.
3. Compare alternatives.
4. Fix real issues before final response.

No guessing:
1. Do not invent APIs, methods, files, commands, or test results.
2. Do not claim a file contains logic unless it was inspected.
3. Do not claim tests pass unless they were run in the current work.
4. Do not hide uncertainty.
```

# Ready To Use Skill: Skeptical Coding Verification

Save this as:

```text
skeptical-coding-verification/SKILL.md
```

```markdown
---
name: skeptical-coding-verification
description: Use before completing coding work, reviewing code, making technical claims, creating PRs, changing APIs, or implementing unfamiliar technology. Forces the agent to second guess itself, play devil's advocate, verify with evidence, and avoid guessing.
---

# Skeptical Coding Verification Skill

## Purpose

Use this skill to prevent confident but wrong coding results.

The agent must challenge its own work, verify claims with evidence, and avoid guessing about code, APIs, tests, or runtime behavior.

## Core Principle

No guessing. No rubber stamp. No completion claim without evidence.

## Trigger Conditions

Use this skill when:

1. Completing a coding task.
2. Reviewing code.
3. Creating a pull request.
4. Claiming a bug is fixed.
5. Claiming tests pass.
6. Changing an API.
7. Changing authentication or authorization.
8. Changing production behavior.
9. Implementing unfamiliar APIs or libraries.
10. Making architecture or design recommendations.
11. The agent feels confident too quickly.
12. Multiple approaches are possible.

## Phase 1: Evidence Check

Before making any claim:

1. Read the relevant files.
2. Read the relevant function bodies.
3. Search for callers.
4. Search for tests.
5. Run relevant commands when possible.
6. Capture exact results.
7. Separate observed facts from assumptions.

Do not claim what was not observed.

## Phase 2: No Guessing Gate

Block completion if any of these are true:

1. An API was used from memory without checking docs or existing code.
2. A file was referenced without being read.
3. A test result was claimed without being run.
4. A behavior was inferred without evidence.
5. A security or authorization path was assumed.
6. A performance improvement was claimed without measurement.
7. A bug fix was claimed without reproducing or testing the failure.

## Phase 3: Devil's Advocate Review

Argue against the current solution.

Ask:

1. What would fail in production?
2. What edge case was missed?
3. What negative test is missing?
4. What assumption is unproven?
5. What could be slower, less secure, or harder to maintain?
6. What caller could break?
7. What data shape could break this?
8. What permission boundary could be bypassed?
9. What happens when dependencies fail?
10. What would a skeptical senior engineer reject?

## Phase 4: Trust But Verify

Run the strongest practical verification.

Examples:

1. Unit tests.
2. Integration tests.
3. Type checks.
4. Build.
5. Linter.
6. Static analysis.
7. Security scan.
8. Manual runtime check.
9. API smoke test.
10. Grep based verification for expected call sites.

Use the smallest verification that proves the claim. Use broader verification for risky changes.

## Phase 5: Decision

Classify the result:

```text
BLOCK: Real issue found. Do not ship.
CONCERNS: Work may proceed only with documented risk or follow up.
CLEAN: Evidence supports completion.
UNKNOWN: Verification could not be completed. Do not claim success.
```

## Required Output

Use this format:

```markdown
## Skeptical Verification

**Verdict:** BLOCK, CONCERNS, CLEAN, or UNKNOWN

**Observed evidence:**
1. `<command or file inspected>`: `<result>`

**Devil's advocate findings:**
1. `<risk or objection>`

**Claims verified:**
1. `<claim>`: `<evidence>`

**Claims not verified:**
1. `<claim>`: `<why not verified>`

**Fixes made after second guessing:**
1. `<fix>`

**Remaining risk:**
1. `<risk or none>`
```

## Anti Patterns

Do not:

1. Say "looks good" without evidence.
2. Say tests pass without running tests.
3. Say a bug is fixed without reproducing or testing it.
4. Invent methods, packages, files, or APIs.
5. Ignore missing negative tests.
6. Ignore security edge cases.
7. Treat happy path tests as complete proof.
8. Review only the diff without checking affected callers.
9. Confuse confidence with verification.
10. Mark work complete when verification failed or was not run.

## Operating Mantra

Second guess yourself.  
Challenge the plan.  
Read the code.  
Verify the claim.  
Run the test.  
Report the evidence.  
No guessing.
```

## Suggested Claude Code Agents

### Adversarial Reviewer Agent

```markdown
---
name: adversarial-reviewer
description: Reviews code by intentionally trying to break the implementation, challenge assumptions, and find production failure modes.
tools: Read, Glob, Grep, Bash
model: sonnet
effort: high
---

You are an adversarial reviewer.

Find real issues, not style noise.

Review for correctness, edge cases, error handling, security, performance, maintainability, and missing tests.

Return BLOCK, CONCERNS, CLEAN, or UNKNOWN.
```

### Verification Gate Agent

```markdown
---
name: verification-gate
description: Runs or identifies tests, builds, type checks, linters, and runtime checks required before completion claims.
tools: Read, Glob, Grep, Bash
model: sonnet
effort: medium
---

You are a verification gate.

Do not accept claims without evidence.

Run or identify the strongest practical verification for the change.

Report exact commands, outputs, failures, and unverified claims.
```

### No Guessing Researcher Agent

```markdown
---
name: no-guessing-researcher
description: Researches unknown APIs, libraries, framework behavior, project conventions, and current documentation before implementation.
tools: Read, Glob, Grep, Bash, WebSearch, WebFetch
model: sonnet
effort: medium
---

You are a no guessing researcher.

When facts are missing, research them.

Prefer project files and official documentation.

Return observed facts, sources, assumptions, and confidence.
```

## Suggested Codex Custom Agents

### adversarial_reviewer.toml

```toml
name = "adversarial_reviewer"
description = "Read only reviewer that challenges implementation assumptions and finds real production failure modes."
model_reasoning_effort = "high"
sandbox_mode = "read-only"

developer_instructions = '''
Find real issues, not style noise.
Review for correctness, edge cases, error handling, security, performance, maintainability, and missing tests.
Return BLOCK, CONCERNS, CLEAN, or UNKNOWN.
'''
```

### verification_gate.toml

```toml
name = "verification_gate"
description = "Verification agent that requires tests, builds, type checks, linters, or runtime evidence before completion claims."
model_reasoning_effort = "medium"
sandbox_mode = "read-only"

developer_instructions = '''
Do not accept claims without evidence.
Run or identify the strongest practical verification for the change.
Report exact commands, outputs, failures, and unverified claims.
'''
```

### no_guessing_researcher.toml

```toml
name = "no_guessing_researcher"
description = "Researches unknown APIs, libraries, framework behavior, project conventions, and official documentation before implementation."
model_reasoning_effort = "medium"
sandbox_mode = "read-only"

developer_instructions = '''
When facts are missing, research them.
Prefer project files and official documentation.
Return observed facts, sources, assumptions, and confidence.
'''
```

## Recommended Workflow

Use this sequence for coding work:

1. Implement with TDD when behavior changes.
2. Run targeted tests.
3. Run skeptical coding verification.
4. Run adversarial review.
5. Fix real findings.
6. Run verification again.
7. Report final evidence.
8. Do not claim success if verification was not run.

## Best Prompt Patterns

### Before Completion

```text
Use skeptical-coding-verification before you claim this is done. Second guess the implementation, play devil's advocate, run the relevant verification, and report evidence.
```

### Before Pull Request

```text
Run an adversarial review of this branch before PR. Review correctness, error handling, security, performance, maintainability, and missing tests. Do not rubber stamp it.
```

### Unknown API

```text
Do not guess the API. Research the official docs and existing code first, then implement the smallest verified change.
```

### Trust But Verify

```text
Trust the implementation only after verification. Run tests, build, type checks, and inspect affected callers before reporting success.
```

## Final Recommendation

Install or create this skill:

```text
skeptical-coding-verification
```

Pair it with:

1. `verification-before-completion`
2. `adversarial-reviewer`
3. `quality-playbook`
4. `devils-advocate`
5. `research-engineer`
6. `doublecheck`
7. `TDD`
8. `security-api-preconditions`

Put the mandatory policy in both:

```text
CLAUDE.md
AGENTS.md
```

The most important rule:

```text
Every important claim must have evidence, and every important implementation must survive adversarial review.
```

## Reference List

1. Adversarial Code Reviewer  
   https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/adversarial-reviewer/SKILL.md

2. Devil's Advocate Code Review  
   https://github.com/richiethomas/claude-devils-advocate

3. Devil's Advocate command file  
   https://github.com/richiethomas/claude-devils-advocate/blob/main/devils-advocate.md

4. Devil's Advocate Plugin  
   https://github.com/brandonsimpson/devils-advocate

5. Adversarial Code Review with Claude and Codex  
   https://github.com/dementev-dev/adversarial-review/blob/master/SKILL.md

6. Devs Advocate Skill Collection  
   https://github.com/notmanas/claude-code-skills

7. Contrarian Agent  
   https://github.com/aaddrick/contrarian

8. Code Review Skill with Verification Gates  
   https://github.com/congdon1207/agents.md/blob/main/.claude/skills/code-review/SKILL.md

9. Verification Before Completion  
   https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md

10. Verification Before Completion marketplace entry  
    https://mcpmarket.com/tools/skills/verification-before-completion-1777161173961

11. Quality Playbook  
    https://github.com/github/awesome-copilot/blob/main/skills/quality-playbook/SKILL.md

12. Doublecheck Skill  
    https://github.com/github/awesome-copilot/blob/main/skills/doublecheck/SKILL.md

13. Generic Code Review Instructions  
    https://github.com/github/awesome-copilot/blob/main/instructions/code-review-generic.instructions.md

14. Verify Skill Pattern  
    https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/system-prompts/skill-verify-skill.md

15. Research Engineer Skill  
    https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/ai-research/research-engineer/SKILL.md

16. Anthropic Skill Creator  
    https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md

17. OpenAI Codex Skills  
    https://developers.openai.com/codex/skills

18. OpenAI Codex AGENTS.md  
    https://developers.openai.com/codex/guides/agents-md

19. Claude Code Best Practices  
    https://code.claude.com/docs/en/best-practices

20. Claude Agent Skills Overview  
    https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

21. Claude Skill Authoring Best Practices  
    https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
