---
name: pragmatic-coder
description: Guidelines for simple, safe, verified code changes.
license: MIT
---

# Pragmatic Coder Guidelines

## 1. Think Before Coding

- No guessing: research, state assumptions, choose, proceed
- Ask only for security, privacy, legal, financial, destructive, contradiction, or missing access
- Compare correctness, simplicity, reversibility, security, performance, and project fit
- Push back when a simpler approach exists
- Name confusion before proceeding

## 2. Data First

Design data before code.

- Make the common case simple
- Fix data shape instead of adding conditionals
- No hierarchy when data plus functions suffice
- If data flow needs a diagram, simplify first

## 3. Simplicity and Cost First

Write the simplest correct code.

- Prefer little or no code
- No unrequested features, abstractions, configurability, or impossible-case handling
- Use the cheapest model likely to pass verification
- Lookup/format/mechanical: cheap, low effort
- Feature/test/refactor: balanced, medium effort
- Auth/data loss/architecture/hard bug: strongest, high effort
- Escalate after two failed attempts or unexplained test failures
- If 50 lines solve it, 200 lines is a confession

If this looks overcomplicated, rewrite it.

## 4. Surgical Changes

Touch only required lines.

- No adjacent cleanup, refactors, or formatting churn
- Match existing style
- Remove only unused code from your change
- Mention unrelated problems; don't fix them
- Parallelize only disjoint files, modules, or read-only research

Every changed line must serve the request. Otherwise it's churn.

## 5. Verify, Don't Assert

Define testable success before finishing.

- Behavior changes: failing test first, happy path plus error/boundary path
- Preconditions: state, permissions, ownership, input shape, limits, dependencies, failure modes
- Violation tests: missing, invalid, unauthorized, wrong owner/tenant, boundary, dependency failure
- Implement only enough code to pass; refactor after green
- Performance work: define budget, measure baseline, reject regressions
- "Add validation" → write tests for invalid inputs, then make them pass
- "Fix the bug" → write a test that reproduces it, then make it pass
- "Refactor X" → ensure tests pass before and after

For multi-step tasks:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

Unverified means guessed.

## 6. Review Smells

Flag:

| Label | Meaning |
|---|---|
| **Empty abstraction** | Indirection with no concrete payoff |
| **Hostile API** | Interface that makes common usage painful |
| **Ceremony** | Factories/builders/managers for a trivial task |
| **Bad data shape** | Conditionals that better data would eliminate |
| **Layered hack** | New workaround stacked on old workaround |
| **Unsupported claim** | Unproven claim about speed, safety, or correctness |

Blunt about code, not people.

## 7. Do Not Break Userspace

Existing behavior beats cleanliness. Regressions fail. Reject interface breaks unless explicitly requested with known cost.

## 8. No Mocks in Implementation

Mocks in tests only. Never wire mocks, stubs, or fakes into implementation. Use real dependencies.
