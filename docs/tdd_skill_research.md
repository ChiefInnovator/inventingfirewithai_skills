# Test Driven Development Skill Research

Created: May 2, 2026, 6:00 PM EST

## Purpose

This document identifies simple, practical skills that encourage test driven development when writing code. The focus is on adding tests as part of the coding workflow, including both positive tests and negative tests, before declaring the implementation complete.

## Best Overall Recommendation

### 1. Matt Pocock: TDD Skill

Link: https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md

This is the best simple model to copy. It is short, practical, and focused on the core behavior that matters most:

1. Write one test.
2. Make it fail.
3. Implement the smallest amount of code needed to make it pass.
4. Refactor.
5. Repeat.

Why it is strong:

1. It keeps the workflow simple.
2. It discourages bulk test generation.
3. It focuses on public behavior rather than implementation details.
4. It works well as an agent skill because it prevents the assistant from jumping straight into production code.

## Other Strong Skills To Review

### 2. Addy Osmani: Agent Skills TDD

Link: https://github.com/addyosmani/agent-skills/blob/main/skills/test-driven-development/SKILL.md

Best for a polished general purpose agent skill. It frames tests as evidence that code works and is useful when an assistant is implementing logic, fixing bugs, or changing behavior.

Why it is useful:

1. Clear agent behavior.
2. Practical implementation flow.
3. Strong fit for coding assistants.
4. Good balance between discipline and flexibility.

### 3. Obra: Superpowers TDD Skill

Link: https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md

Best for strict TDD discipline. This skill is useful when you want a hard rule that production code should not be written before a failing test exists.

Why it is useful:

1. Enforces the red, green, refactor cycle.
2. Reduces shortcut behavior.
3. Makes the test first rule explicit.
4. Good for teams that want strong engineering discipline.

### 4. Alireza Rezvani: TDD Guide Skill

Link: https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/tdd-guide/SKILL.md

Best for explicit positive and negative test coverage. This skill is useful because it calls out happy path tests, error cases, edge cases, coverage gaps, and common test frameworks.

Why it is useful:

1. Explicitly supports positive tests.
2. Explicitly supports negative tests.
3. Encourages edge case coverage.
4. Works across common test frameworks such as Jest, Pytest, JUnit, Vitest, and Mocha.

### 5. mfranzon: TDD Skill for Claude Code

Link: https://github.com/mfranzon/tdd

Best lightweight command style option. It supports a simple command pattern where the user describes the feature and the assistant walks through the TDD cycle.

Why it is useful:

1. Simple command based workflow.
2. Detects the project language and test framework.
3. Supports Python, TypeScript, and Go.
4. Useful if you want a direct developer workflow instead of a general instruction file.

### 6. morodomi: tdd skills

Link: https://github.com/morodomi/tdd-skills

Best advanced option. It is more complex than needed for a simple skill, but useful if you want workflow enforcement, setup automation, quality gates, and language specific plugins.

Why it is useful:

1. More complete engineering workflow.
2. Better for mature teams.
3. Includes stronger process controls.
4. Useful reference if the simple skill later evolves into a full toolset.

## Recommended Skill Design

Use Matt Pocock's TDD skill as the base. Add the most useful parts of Alireza Rezvani's TDD Guide so the skill requires both positive and negative tests.

The resulting skill should instruct the coding assistant to:

1. Understand the requested behavior before writing code.
2. Identify the smallest testable slice.
3. Write one failing positive test for the expected behavior.
4. Write one failing negative test for an invalid input, error case, rejected state, or boundary condition.
5. Run the tests and confirm they fail for the expected reason.
6. Write the minimum production code needed to pass.
7. Run the tests again.
8. Refactor only after the tests pass.
9. Repeat the cycle for the next behavior.
10. Run the full relevant test suite before the work is considered complete.

## Suggested Simple Skill Template

```markdown
# Test Driven Development Skill

Use this skill whenever writing new code, fixing a bug, or changing behavior.

## Core Rule

Do not write production code first. Write a failing test that describes the expected behavior, then implement the smallest amount of code needed to pass it.

## Workflow

1. Clarify the behavior being implemented.
2. Identify the smallest useful slice of work.
3. Add one positive test for the expected behavior.
4. Add one negative test for an invalid input, error condition, rejected state, or boundary case.
5. Run the tests and confirm they fail for the expected reason.
6. Implement the minimum code required to pass the tests.
7. Run the tests again.
8. Refactor only after the tests pass.
9. Repeat until the requested behavior is complete.
10. Run the full relevant test suite before finishing.

## Positive Tests

Positive tests confirm the expected happy path behavior.

Examples:

1. Valid input returns the correct result.
2. A successful workflow completes.
3. A valid object is created.
4. A supported command produces the expected output.

## Negative Tests

Negative tests confirm the code behaves correctly when something is wrong.

Examples:

1. Invalid input is rejected.
2. Missing data returns a clear error.
3. Unauthorized access is denied.
4. Boundary values are handled correctly.
5. Unexpected states do not cause silent failure.

## Completion Criteria

The task is not complete until:

1. Positive tests exist.
2. Negative tests exist.
3. The tests pass.
4. The implementation is minimal and readable.
5. The relevant test suite has been run.
```

## Final Recommendation

Start with a simple Markdown skill. Avoid building a complex plugin until the team proves the behavior is useful. The winning pattern is direct and enforceable:

1. Test first.
2. Include positive tests.
3. Include negative tests.
4. Implement only what passes the tests.
5. Run the suite before declaring success.
