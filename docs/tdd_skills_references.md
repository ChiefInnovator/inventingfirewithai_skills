# TDD Skill References

Generated: May 2, 2026

## Purpose

This file collects practical references for coding agent skills that support test driven development. The focus is on writing tests as part of code creation, using positive and negative tests, following Red, Green, Refactor, and avoiding code changes that are not verified by tests.

## Recommended Base Skill

### 1. Matt Pocock: TDD Skill

Link: https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md

Why it matters:

1. Clear and lightweight.
2. Focuses on Red, Green, Refactor.
3. Encourages testing through public interfaces.
4. Avoids writing all tests upfront.
5. Good base for a simple reusable coding agent skill.

Supporting files:

1. Deep modules: https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/deep-modules.md
2. Tests guidance: https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/tests.md
3. Interface design: https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/interface-design.md

## Strong General Purpose Skills

### 2. Addy Osmani: Test Driven Development Skill

Link: https://github.com/addyosmani/agent-skills/blob/main/skills/test-driven-development/SKILL.md

Why it matters:

1. Strong production coding agent guidance.
2. Triggers when implementing logic, fixing bugs, or changing behavior.
3. Treats tests as proof that code works.
4. Good for teams using AI coding agents.
5. Useful companion to code review and quality gates.

Related repository:

https://github.com/addyosmani/agent-skills

Getting started guide:

https://github.com/addyosmani/agent-skills/blob/main/docs/getting-started.md

### 3. Obra Superpowers: Test Driven Development Skill

Link: https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md

Why it matters:

1. Strict test first discipline.
2. Requires watching the test fail before implementation.
3. Good for enforcing TDD with less ambiguity.
4. Strong fit when you want the agent to avoid skipping tests.
5. Useful for teams that want hard guardrails.

Related repository:

https://github.com/obra/superpowers

Related issue on automatic TDD enforcement:

https://github.com/obra/superpowers/issues/384

## Best Skill For Positive And Negative Test Coverage

### 4. Alireza Rezvani: TDD Guide Skill

Link: https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/tdd-guide/SKILL.md

Why it matters:

1. Explicitly calls for happy path, error cases, and edge cases.
2. Covers test generation and coverage analysis.
3. Supports TypeScript, JavaScript, Python, and Java.
4. Mentions common frameworks such as Jest, Pytest, JUnit, and Vitest.
5. Good source for positive and negative test language.

Related repository:

https://github.com/alirezarezvani/claude-skills

Alternate generated skill reference:

https://github.com/alirezarezvani/claude-code-skill-factory/blob/dev/generated-skills/tdd-guide/SKILL.md

README reference:

https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/tdd-guide/README.md

## Additional Practical References

### 5. mfranzon: TDD Skill For Claude Code

Link: https://github.com/mfranzon/tdd

Why it matters:

1. Simple command style workflow.
2. Useful model for slash command based TDD.
3. Walks through Red, Green, Refactor.
4. Supports multiple implementation stacks.
5. Good inspiration for lightweight developer workflow design.

### 6. morodomi: TDD Skills

Link: https://github.com/morodomi/tdd-skills

Why it matters:

1. More advanced than a simple skill.
2. Useful if you want strict workflow enforcement.
3. Includes setup and quality gate ideas.
4. Helpful reference for plugin style TDD systems.
5. Better as inspiration than as the first implementation.

## Recommended Skill Design Pattern

Use this structure for a simple internal TDD skill:

```markdown
# Test Driven Development

Use this skill whenever implementing logic, fixing a bug, changing behavior, or adding a feature.

## Core Rule

Write the test first. Watch it fail. Then write the smallest amount of code needed to pass.

## Required Test Coverage

Every meaningful change must include:

1. At least one positive test for expected behavior.
2. At least one negative test for invalid input, failure mode, permission issue, boundary case, or error condition.
3. At least one regression test when fixing a bug.
4. A full test run before the work is considered complete.

## Workflow

1. Identify the smallest behavior slice.
2. Write a failing test for that behavior.
3. Run the test and confirm it fails for the right reason.
4. Implement the smallest safe change.
5. Run the test and confirm it passes.
6. Add negative or edge case tests.
7. Refactor only after tests pass.
8. Run the relevant test suite.
9. Summarize what was tested and what remains untested.

## Guardrails

1. Do not write production code before a failing test unless the project has no test harness.
2. Do not generate a large test suite blindly.
3. Do not test implementation details unless there is no better public interface.
4. Do not call the work done until positive and negative tests pass.
5. Do not skip tests because the change appears small.
```

## Best Combination

For a simple, effective skill:

1. Start with Matt Pocock for simplicity.
2. Add Addy Osmani for agent quality gates.
3. Add Alireza Rezvani for explicit positive and negative test coverage.
4. Add Obra Superpowers if strict enforcement is needed.

## Final Recommendation

Use Matt Pocock as the base and merge in the positive and negative test language from Alireza Rezvani. Add the strict failing test requirement from Obra Superpowers. This gives you a simple, enforceable, high signal TDD skill without making the workflow too heavy.
