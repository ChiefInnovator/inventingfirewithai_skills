# Interface, Contract, and Dependency Inversion Skills Research

**Prepared for:** Rich Crane  
**Prepared on:** May 02, 2026, 12:01 PM EST  
**Focus:** Agent skills and engineering guidance for interface based development, contracts, dependency inversion, test seams, adapters, public API boundaries, and maintainable abstractions.  
**Platforms:** Claude Code, Codex, GitHub Copilot style skills, .NET, TypeScript, React, Python, API services, Azure applications, and agent systems.

## Scope

This research focuses on reusable skills and durable engineering principles.

Excluded by design:

1. Hexagonal Architecture material.
2. Symfony material.
3. One off framework or product specific examples.
4. Advice that encourages creating interfaces everywhere by default.

## Executive Summary

Interface based development is valuable when it creates a real design boundary.

The central rule:

```text
Use interfaces to protect meaningful seams, not to decorate every class.
```

A good interface should do at least one of the following:

1. Protect business logic from infrastructure.
2. Define a stable contract between layers.
3. Enable dependency inversion.
4. Allow safe test doubles without hitting external systems.
5. Support more than one implementation.
6. Make external providers replaceable.
7. Enable parallel development by separating contract from implementation.
8. Make failure behavior explicit.
9. Reduce coupling across modules.
10. Clarify public behavior.

The mandatory guardrail:

```text
Do not create interfaces for simple data classes, DTOs, pure internal helpers, private implementation details, classes with only one stable use and no likely replacement, or code where the interface simply duplicates the class.
```

## Best Skills and References

## 1. Matt Pocock Interface Design Skill

**Best for:** Exploring multiple contract options before choosing an interface.

This skill uses a "Design It Twice" approach. The agent creates multiple interface options, compares them, and selects the best one instead of accepting the first abstraction.

**Features to borrow:**

1. Generate more than one interface option.
2. Use parallel agents for important interface decisions.
3. Compare contract shapes before implementation.
4. Focus on module seams, adapters, leverage, and public contract quality.
5. Document why the chosen interface wins.

**Why it matters:**

Most weak abstractions happen because the agent picks the first obvious interface. This skill forces design pressure before code is created.

**Reference:**

https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/INTERFACE-DESIGN.md

## 2. Matt Pocock Improve Codebase Architecture Skill

**Best for:** Deciding whether an abstraction earns its keep.

This skill includes several useful architecture heuristics. The most relevant ideas are that the interface is the test surface, one adapter is a hypothetical seam, and two adapters prove a real seam.

**Features to borrow:**

1. Treat the public interface as the test surface.
2. Use the deletion test: would deleting the abstraction simplify the system or spread complexity across callers?
3. Treat one adapter as a weak signal.
4. Treat two or more adapters as a stronger signal that the seam is real.
5. Avoid pass through modules that only rename another API.

**Why it matters:**

It helps agents decide whether an interface is a real boundary or just extra ceremony.

**Reference:**

https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md

## 3. Matt Pocock TDD Skill

**Best for:** Testing behavior through public interfaces.

This skill is not only about tests. It helps validate whether an interface is useful because good public contracts should be easy to test through behavior.

**Features to borrow:**

1. Add tests while writing behavior.
2. Test public behavior, not private implementation.
3. Add positive and negative tests.
4. Use small vertical slices.
5. Let test friction reveal poor contract design.

**Why it matters:**

An interface that is hard to test is often the wrong interface.

**Reference:**

https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md

## 4. Matt Pocock Interface Design for Testability Guidance

**Best for:** Making dependencies explicit.

This guidance connects interface design to testability. The most important rule is: accept dependencies, do not create them inside business logic.

**Features to borrow:**

1. Accept dependencies from the outside.
2. Avoid hidden construction of external dependencies.
3. Prefer return values where practical.
4. Reduce unnecessary side effects.
5. Use tests to reveal awkward contracts.

**Why it matters:**

Hidden dependency creation makes code harder to test and harder to replace.

**Reference:**

https://github.com/mattpocock/skills/blob/main/tdd/interface-design.md

## 5. Clean Architecture Dependency Inversion Skill

**Best for:** Refactoring concrete dependencies into meaningful abstractions.

This skill triggers when business logic imports concrete repositories, SDKs, ORMs, infrastructure services, frameworks, or classes that construct their own collaborators.

**Features to borrow:**

1. Detect dependency direction violations.
2. Extract interfaces at real boundaries.
3. Move concrete implementations toward infrastructure or adapter code.
4. Use constructor injection.
5. Wire concrete implementations in the composition root.

**Why it matters:**

Dependency inversion prevents business logic from being coupled to external tools, databases, SDKs, and frameworks.

**Reference:**

https://github.com/PanGan21/clean-architecture-claude-skills/blob/master/skills/clean-architecture-dependency-inversion/SKILL.md

## 6. GitHub Awesome Copilot .NET Best Practices Skill

**Best for:** .NET service interfaces, dependency injection, and interface segregation.

This skill gives practical .NET guidance around service interfaces, constructor injection, dependency injection, and interface segregation.

**Features to borrow:**

1. Use constructor injection.
2. Use small role based interfaces.
3. Keep services focused.
4. Register implementations in the composition root.
5. Avoid large interfaces that force unused methods on consumers.

**Why it matters:**

It aligns interface usage with common .NET production patterns.

**Reference:**

https://github.com/github/awesome-copilot/blob/main/plugins/csharp-dotnet-development/skills/dotnet-best-practices/SKILL.md

## 7. GitHub Awesome Copilot .NET Design Pattern Review Skill

**Best for:** Reviewing whether interface usage improves design.

This skill reviews abstractions, provider patterns, repository abstractions, SOLID violations, dependency inversion, testability, maintainability, and dependency injection.

**Features to borrow:**

1. Review whether each interface has a real reason to exist.
2. Check dependency direction.
3. Check whether the pattern reduces coupling or adds ceremony.
4. Check testability.
5. Remove abstractions that do not carry design weight.

**Why it matters:**

This should be used after code generation to catch over abstracted code.

**Reference:**

https://github.com/github/awesome-copilot/blob/main/skills/dotnet-design-pattern-review/SKILL.md

## 8. GitHub Awesome Copilot C Sharp Expert Agent

**Best for:** Avoiding unnecessary abstractions.

This is one of the strongest references for your stated preference. It warns not to add interfaces or abstractions unless they are needed for external dependencies or testing, and not to wrap existing abstractions.

**Features to borrow:**

1. Do not add interfaces by default.
2. Do not wrap an abstraction in another abstraction without a strong reason.
3. Use least exposure for types and members.
4. Do not add unused methods or parameters.
5. Prefer simple concrete code when no seam exists.

**Why it matters:**

This prevents the common AI failure mode of creating `IFoo` for every `Foo`.

**Reference:**

https://github.com/github/awesome-copilot/blob/main/agents/CSharpExpert.agent.md

## 9. GitHub Awesome Copilot Object Oriented Design Patterns Instructions

**Best for:** General interface segregation and dependency inversion review.

This instruction set covers object oriented design principles, including Interface Segregation and Dependency Inversion.

**Features to borrow:**

1. Prefer role specific interfaces.
2. Do not force clients to depend on methods they do not use.
3. High level modules should depend on abstractions when there is a real boundary.
4. Details should depend on abstractions.
5. Use patterns only when they solve real problems.

**Why it matters:**

It is a useful cross language design review layer.

**Reference:**

https://github.com/github/awesome-copilot/blob/main/instructions/oop-design-patterns.instructions.md

## 10. GitHub Awesome Copilot .NET Architecture Good Practices Instructions

**Best for:** Architecture level review of SOLID, dependency direction, and maintainability.

This instruction file includes SOLID principles, dependency inversion, interface segregation, and maintainability guidance.

**Features to borrow:**

1. Keep interfaces consumer focused.
2. Avoid forcing unused members on consumers.
3. Keep architecture simple until a real seam appears.
4. Watch for too many constructor dependencies.
5. Use abstractions to reduce real coupling, not to satisfy a pattern checklist.

**Why it matters:**

It provides a practical architecture checklist for .NET and enterprise systems.

**Reference:**

https://github.com/github/awesome-copilot/blob/main/instructions/dotnet-architecture-good-practices.instructions.md

## 11. SOLID Skills

**Best for:** Broad object oriented design quality.

SOLID skills are useful because they cover Interface Segregation and Dependency Inversion directly. They must be paired with a strong anti over abstraction rule.

**Features to borrow:**

1. Interface Segregation.
2. Dependency Inversion.
3. Single Responsibility.
4. Refactoring guidance.
5. Design review language.

**Why it matters:**

SOLID is useful as a review lens but dangerous as a boilerplate generator.

**Reference:**

https://github.com/ramziddin/solid-skills

## 12. Microsoft .NET Design Guidelines: Abstractions

**Best for:** Official Microsoft guidance on interfaces and abstract types.

Microsoft describes abstractions as contracts and advises not to provide abstractions unless they are tested by concrete implementations and APIs consuming the abstractions.

**Features to borrow:**

1. Treat interfaces as contracts.
2. Avoid premature abstractions.
3. Test abstractions with real implementations.
4. Test abstractions with APIs that consume them.
5. Choose abstractions only when they support extensibility, testability, or replaceability.

**Why it matters:**

This directly supports the rule that interfaces should not exist just because a class exists.

**Reference:**

https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/abstractions-abstract-types-and-interfaces

## 13. Microsoft .NET Dependency Injection Guidelines

**Best for:** Constructor injection and avoiding hidden concrete dependencies.

Microsoft's DI guidance says to avoid direct instantiation of dependent classes within services because it couples code to a particular implementation. It also recommends small, well factored, easily tested services.

**Features to borrow:**

1. Avoid direct instantiation of dependent classes inside services.
2. Use constructor injection for dependencies.
3. Keep services small and well factored.
4. Make services easy to test.
5. Keep dependency lifetimes intentional.

**Why it matters:**

Dependency injection is the practical mechanism that makes interface based development useful in .NET.

**Reference:**

https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection/guidelines

## 14. Microsoft ASP.NET Core Dependency Injection Guidance

**Best for:** Production ASP.NET Core service design.

This guidance reinforces the same design rule: avoid direct instantiation of dependencies inside services, because it couples the code to specific implementations.

**Features to borrow:**

1. Use DI for service dependencies.
2. Avoid direct construction of dependencies.
3. Use constructor injection.
4. Keep services small.
5. Keep services easy to test.

**Reference:**

https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection

## 15. Microsoft .NET Architecture Principles

**Best for:** Official architecture rationale for dependency inversion.

Microsoft's modern web application architecture guidance lists dependency inversion as an architectural principle that helps build modular, testable, maintainable applications.

**Features to borrow:**

1. Higher level modules should depend on abstractions.
2. Lower level implementations should be swappable.
3. Use architecture boundaries to improve maintainability.
4. Use dependency inversion to support testing.
5. Use dependency inversion to isolate infrastructure.

**Reference:**

https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles

## 16. TypeScript Handbook: Interfaces

**Best for:** TypeScript structural contracts.

The TypeScript Handbook describes interfaces as a way to name structural types and define contracts inside your code and with code outside your project.

**Features to borrow:**

1. Use interfaces to describe object shapes and contracts.
2. Use structural typing intentionally.
3. Prefer interface or type aliases where they clarify public contracts.
4. Avoid exporting internal implementation details.
5. Use interfaces for public contracts, not every object.

**Why it matters:**

In TypeScript, the distinction between class and interface is different from C Sharp. Interfaces are often contract shapes, not runtime artifacts.

**Reference:**

https://www.typescriptlang.org/docs/handbook/interfaces.html

## 17. Python Protocols and Structural Subtyping

**Best for:** Python interface like contracts without rigid inheritance.

Python Protocols support structural subtyping. A class can satisfy a protocol by shape rather than explicit inheritance.

**Features to borrow:**

1. Use protocols for dependency contracts.
2. Prefer structural typing when explicit inheritance adds ceremony.
3. Use protocols for test doubles and replaceable dependencies.
4. Keep protocols small.
5. Avoid protocols for trivial data carriers.

**Why it matters:**

Python often benefits from Protocols over heavy abstract base classes when the goal is testability and flexible contracts.

**References:**

https://typing.python.org/en/latest/reference/protocols.html

https://peps.python.org/pep-0544/

## Feature Comparison Matrix

| Source | Best Feature | Prevents Over Abstraction | Supports Tests | Supports Dependency Inversion | Best Platform |
|---|---|---:|---:|---:|---|
| Matt Pocock Interface Design | Multiple interface options | Medium | Medium | Medium | General |
| Matt Pocock Architecture | Interface as test surface, deletion test | High | High | Medium | General |
| Matt Pocock TDD | Public behavior tests | Medium | High | Medium | General |
| Interface Design for Testability | Accept dependencies | Medium | High | High | General |
| Clean Architecture Dependency Inversion | Move concrete dependencies to edges | Medium | High | High | General |
| .NET Best Practices | DI and interface segregation | Medium | High | High | .NET |
| .NET Design Pattern Review | Review abstractions after implementation | High | High | High | .NET |
| C Sharp Expert Agent | Avoid pointless abstractions | Very High | Medium | Medium | .NET |
| OOP Design Patterns Instructions | ISP and DIP review | Medium | Medium | High | General |
| .NET Architecture Instructions | Architecture review | Medium | Medium | High | .NET |
| SOLID Skills | Design principles | Low without guardrails | Medium | High | General |
| Microsoft Abstractions Guidance | Official abstraction discipline | Very High | High | High | .NET |
| Microsoft DI Guidelines | Constructor injection | Medium | High | High | .NET |
| TypeScript Interfaces | Structural contracts | Medium | Medium | Medium | TypeScript |
| Python Protocols | Structural contracts | Medium | High | Medium | Python |

## Clear Reasons for Interface Based Development

## 1. Decoupling

Interfaces decouple high level business logic from low level implementation details.

Good example boundaries:

1. Database clients.
2. External APIs.
3. Payment gateways.
4. Email providers.
5. AI model providers.
6. Message buses.
7. File systems.
8. Clocks and ID generators.
9. Search providers.
10. Feature flag systems.

## 2. Testability

Interfaces make it possible to replace slow, expensive, nondeterministic, or unsafe dependencies during tests.

Examples:

1. Replace live payment provider with fake payment gateway.
2. Replace system clock with test clock.
3. Replace network client with stub client.
4. Replace AI model provider with deterministic test provider.
5. Replace database with in memory repository only when the repository itself is not what is under test.

## 3. Replaceable Implementations

Interfaces allow a system to change providers without rewriting the core workflow.

Examples:

1. SQL to Cosmos DB.
2. Azure OpenAI to OpenAI or another model provider.
3. SendGrid to Microsoft Graph email.
4. Local file system to Azure Blob Storage.
5. In memory cache to Redis.
6. Direct HTTP call to message queue.

## 4. Clear Public Contracts

Interfaces define what a module promises to callers.

A good contract should clarify:

1. Inputs.
2. Outputs.
3. Failure modes.
4. Idempotency behavior.
5. Security assumptions.
6. Side effects.
7. Ownership of resources.
8. Error handling expectations.

## 5. Parallel Development

A contract lets one agent implement the core logic while another agent implements the adapter.

Example:

1. Agent A defines `IPaymentGateway`.
2. Agent B implements Stripe adapter.
3. Agent C writes tests using fake payment gateway.
4. Lead agent wires the composition root.

## 6. Lower Regression Risk

When callers depend on stable contracts, implementations can change without breaking the rest of the system.

## 7. Better Agent Behavior

Interfaces give agents a controlled seam. They reduce context pollution and make implementation assignments cleaner.

## When To Create an Interface

Create an interface when at least one of these is true:

1. The dependency talks to an external system.
2. The dependency is slow, expensive, nondeterministic, or unsafe in tests.
3. Multiple implementations already exist.
4. Multiple implementations are very likely.
5. The dependency crosses a layer boundary.
6. The module is a plugin point.
7. The core application should not know the provider.
8. The contract lets agents or teams work in parallel.
9. The interface expresses business capability better than implementation details.
10. The abstraction reduces coupling more than it adds complexity.

## When Not To Create an Interface

Do not create an interface for:

1. Simple data classes.
2. DTOs.
3. Pure internal helpers.
4. Private implementation details.
5. Classes with only one stable use and no likely replacement.
6. Code where the interface simply duplicates the class.
7. Value objects.
8. Records whose purpose is data transfer.
9. Local algorithms with no external dependency.
10. Small functions that are already easy to test.
11. Concrete classes already hidden behind a higher level interface.
12. Framework types already abstracted by the framework.
13. Anything created only because "every service needs an interface."

## Good Interface Candidates

Use interfaces for:

1. Repositories when persistence must be isolated.
2. Gateways to external systems.
3. AI model providers.
4. Payment providers.
5. Email and notification senders.
6. Storage providers.
7. Message publishers.
8. Clocks and time providers.
9. ID generators.
10. Authorization policies.
11. Feature flag providers.
12. Search providers.
13. Cache providers.
14. Workflow executors.
15. API client wrappers when the API is external or unstable.
16. Agent tool interfaces.
17. Plugin systems.
18. Environment and configuration providers when tests need control.

## Bad Interface Candidates

Avoid interfaces for:

1. `CustomerDto`.
2. `CreateOrderRequest`.
3. `OrderResponse`.
4. `Money` value object.
5. `Address` value object.
6. `StringFormatter` used once internally.
7. `DateParser` used only by one private method.
8. `IUserService` that exactly duplicates `UserService` with no alternate implementation.
9. `IThing` created only because `Thing` exists.
10. Wrapper around a framework abstraction that already solves the same problem.

## Interface Quality Checklist

Before creating an interface, answer:

1. What concrete dependency does this remove?
2. What layer boundary does this protect?
3. What test becomes easier or safer?
4. What second implementation exists or is likely?
5. What provider may change?
6. What business capability does the interface express?
7. Does the interface expose implementation details?
8. Does the interface force consumers to depend on unused members?
9. Could this be a simple function instead?
10. Would deleting this interface make the system simpler with no downside?

If the answers are weak, do not create the interface.

## Interface Design Rules

## 1. Consumer Owned

The interface should usually be owned by the layer that consumes it.

Bad:

```text
Infrastructure defines what the domain must call.
```

Good:

```text
Application or domain defines what it needs. Infrastructure implements it.
```

## 2. Small and Role Based

Prefer:

```text
IEmailSender
IClock
IOrderRepository
IPaymentGateway
IModelProvider
```

Avoid:

```text
IUtilityService
IManager
IRepositoryWithEverything
ICommonService
IThingService
```

## 3. No Infrastructure Leakage

Do not leak infrastructure types into core contracts.

Bad:

```csharp
Task<SqlDataReader> GetOrdersAsync();
```

Good:

```csharp
Task<IReadOnlyList<Order>> GetOrdersAsync(CustomerId customerId);
```

## 4. Explicit Failure Modes

Contracts should make expected failure clear.

Examples:

1. Return a result type.
2. Throw documented domain exceptions.
3. Return nullable only when absence is normal.
4. Use status objects for expected external failures.
5. Do not swallow errors silently.

## 5. Composition Root Wiring

The application composition root should bind interfaces to implementations.

Examples:

1. .NET service registration.
2. Python dependency provider.
3. TypeScript composition module.
4. React provider at app boundary when appropriate.

## 6. Test Through the Contract

If the interface matters, tests should verify behavior through that contract.

## Agent Instructions for Claude Code and Codex

Add this to `CLAUDE.md` and `AGENTS.md`.

```markdown
# Interface and Abstraction Policy

Use interfaces only when they create a meaningful boundary.

Create an interface when it protects business logic from infrastructure, enables dependency inversion, supports test doubles, allows replaceable implementations, defines a stable public contract, or enables parallel development.

Do not create interfaces for simple data classes, DTOs, pure internal helpers, private implementation details, classes with only one stable use and no likely replacement, or code where the interface simply duplicates the class.

Before creating an interface, explain the reason in one sentence.

Every new interface must identify:
1. The concrete dependency it removes.
2. The boundary it protects.
3. The test or replacement scenario it enables.
4. The composition root where it is wired.
5. Whether more than one implementation exists or is likely.

If no strong reason exists, use the concrete class directly.
```

# Ready To Use Skill: Contract Based Interface Development

Save this as:

```text
contract-based-interface-development/SKILL.md
```

```markdown
---
name: contract-based-interface-development
description: Use when designing or refactoring interfaces, contracts, dependency inversion, adapter boundaries, test seams, provider abstractions, public module boundaries, or replaceable implementations. Prevents pointless interfaces and requires a clear reason for each abstraction.
---

# Contract Based Interface Development Skill

## Purpose

Use this skill to design useful interfaces and avoid pointless abstractions.

The agent must create interfaces only when they define a meaningful contract, protect a boundary, improve testability, enable replacement, or reduce real coupling.

## Core Principle

Use interfaces to protect meaningful seams, not to decorate every class.

Do not create interfaces by default.

## Mandatory Exclusion Rule

Do not create interfaces for:

1. Simple data classes.
2. DTOs.
3. Pure internal helpers.
4. Private implementation details.
5. Classes with only one stable use and no likely replacement.
6. Code where the interface simply duplicates the class.
7. Value objects.
8. Records used only to carry data.
9. Local algorithms that are already easy to test.
10. Any abstraction created only because the concrete class exists.

## Use Interfaces When

Create an interface when at least one of these is true:

1. Business logic depends on infrastructure.
2. Code depends on a database, SDK, HTTP client, queue, cache, file system, clock, ID generator, AI model provider, payment provider, or external service.
3. A dependency must be mocked, stubbed, or faked in tests.
4. Multiple implementations exist.
5. Multiple implementations are likely.
6. A provider may change.
7. A module boundary needs a stable contract.
8. Parallel agents or teams need to split contract and implementation work.
9. A plugin or strategy point is needed.
10. The interface expresses a business capability better than implementation details.

## Interface Decision Workflow

Before creating an interface:

1. Identify the concrete dependency.
2. Identify the boundary being protected.
3. Identify the consuming layer.
4. Identify the test seam.
5. Identify likely alternate implementations.
6. Check whether the interface would only duplicate the class.
7. Check whether a simple function would be enough.
8. Choose the smallest role based contract.
9. Place the interface near the consumer.
10. Wire the implementation in the composition root.

## Design It Twice Rule

For important public contracts:

1. Generate two or three interface options.
2. Compare each by simplicity, clarity, testability, future replacement, and implementation cost.
3. Select the best option.
4. Document rejected alternatives briefly.

## Quality Rules

1. Interfaces should express business capability.
2. Interfaces should not expose infrastructure details.
3. Interfaces should be small and role based.
4. Interfaces should avoid unused members.
5. Interfaces should make failure behavior explicit.
6. Interfaces should not mirror one class without reason.
7. Interfaces should be tested through public behavior.
8. Interfaces should support dependency injection.
9. Implementations should live at the infrastructure edge.
10. The composition root should own binding.

## Naming Rules

Prefer names that express capability:

```text
IPaymentGateway
IEmailSender
IClock
IIdGenerator
IOrderRepository
IModelProvider
ISearchProvider
IAuthorizationPolicy
```

Avoid vague names:

```text
IManager
IHelper
IUtility
ICommonService
IThingService
IDataService
```

## Final Report Format

When creating or changing interfaces, report:

```markdown
## Interface Decisions

| Interface | Reason | Boundary Protected | Implementation | Test Seam |
|---|---|---|---|---|
| `<name>` | `<reason>` | `<boundary>` | `<class>` | `<test scenario>` |

## Interfaces Not Created

| Candidate | Reason Rejected |
|---|---|
| `<name>` | Simple data class, DTO, internal helper, one stable implementation, or duplicate of class |

## Composition Root Changes

1. `<registration or provider>`

## Tests

1. `<test name or command>`
```

## Review Checklist

Before completing, verify:

1. No DTO has a pointless interface.
2. No simple data class has a pointless interface.
3. No private helper has a pointless interface.
4. No interface merely duplicates one class.
5. Every interface has a stated reason.
6. Every interface protects a boundary or test seam.
7. Every interface is small and role based.
8. Implementations are wired at the composition root.
9. Tests verify behavior through the public contract.
10. The code is simpler with the interface than without it.

## Operating Mantra

Find the seam.  
Define the contract.  
Invert the dependency.  
Implement the adapter.  
Wire the composition root.  
Test the public behavior.  
Reject pointless interfaces.
```

## Recommended Skill Pairings

Use this skill with:

1. TDD Skill for public behavior tests.
2. Security API Preconditions Skill for endpoint contracts.
3. Performance as a Feature Skill for nonfunctional contract requirements.
4. Autonomous Execution Skill for research before asking.
5. Parallel Agent Orchestration Skill for splitting contract, implementation, and tests.
6. .NET Best Practices Skill for C Sharp and ASP.NET Core projects.
7. TypeScript contract guidance for React and Node projects.
8. Python Protocol guidance for Python services.

## Recommended Claude Code Setup

```text
CLAUDE.md
.claude/
  skills/
    contract-based-interface-development/
      SKILL.md
  agents/
    interface-reviewer.md
    contract-designer.md
    abstraction-skeptic.md
```

## Claude Agent: Interface Reviewer

```markdown
---
name: interface-reviewer
description: Reviews interfaces and abstractions for real boundaries, test seams, dependency inversion, and over abstraction.
tools: Read, Glob, Grep, Bash
model: sonnet
effort: medium
---

You are an interface reviewer.

Review each interface and abstraction.

Reject interfaces for simple data classes, DTOs, pure internal helpers, private implementation details, one stable implementation, or duplicate class shapes.

Return:
1. Interfaces that should remain.
2. Interfaces that should be removed.
3. Interfaces that should be split.
4. Concrete dependencies that should be inverted.
5. Tests that should verify the contract.
```

## Claude Agent: Contract Designer

```markdown
---
name: contract-designer
description: Designs small public contracts for real seams and compares multiple interface options before selecting one.
tools: Read, Glob, Grep
model: sonnet
effort: medium
---

You are a contract designer.

Generate two or three interface options for important seams. Compare simplicity, testability, implementation cost, failure behavior, and future replacement value.

Choose the best contract and explain why.
```

## Claude Agent: Abstraction Skeptic

```markdown
---
name: abstraction-skeptic
description: Challenges unnecessary interfaces, pass through abstractions, and duplicate contracts.
tools: Read, Glob, Grep
model: haiku
effort: low
---

You are an abstraction skeptic.

Your job is to find pointless abstractions.

Flag interfaces that duplicate one class, protect no boundary, enable no test seam, or have no likely replacement.

Prefer concrete code when abstraction adds ceremony without leverage.
```

## Recommended Codex Setup

```text
AGENTS.md
.codex/
  agents/
    interface_reviewer.toml
    contract_designer.toml
    abstraction_skeptic.toml
skills/
  contract-based-interface-development/
    SKILL.md
```

## Codex Agent: Interface Reviewer

```toml
name = "interface_reviewer"
description = "Reviews interfaces for real boundaries, test seams, dependency inversion, and over abstraction."
model_reasoning_effort = "medium"
sandbox_mode = "read-only"

developer_instructions = '''
Review each interface and abstraction.
Reject interfaces for simple data classes, DTOs, pure internal helpers, private implementation details, one stable implementation, or duplicate class shapes.
Return interfaces that should remain, be removed, be split, or be replaced by concrete code.
'''
```

## Codex Agent: Contract Designer

```toml
name = "contract_designer"
description = "Designs small public contracts for real seams and compares multiple options before selecting one."
model_reasoning_effort = "medium"
sandbox_mode = "read-only"

developer_instructions = '''
Generate two or three interface options for important seams.
Compare simplicity, testability, implementation cost, failure behavior, and replacement value.
Choose the best contract and explain why.
'''
```

## Codex Agent: Abstraction Skeptic

```toml
name = "abstraction_skeptic"
description = "Challenges unnecessary interfaces, pass through abstractions, and duplicate contracts."
model_reasoning_effort = "low"
sandbox_mode = "read-only"

developer_instructions = '''
Find pointless abstractions.
Flag interfaces that duplicate one class, protect no boundary, enable no test seam, or have no likely replacement.
Prefer concrete code when abstraction adds ceremony without leverage.
'''
```

## Practical Examples

## Good Interface Example: Payment Gateway

Reason:

1. External dependency.
2. Expensive and unsafe to call in tests.
3. Provider may change.
4. Failure behavior matters.

```csharp
public interface IPaymentGateway
{
    Task<PaymentResult> ChargeAsync(PaymentRequest request, CancellationToken cancellationToken);
}
```

## Good Interface Example: Clock

Reason:

1. System time is nondeterministic.
2. Tests need control over time.
3. Implementation is trivial but seam is valuable.

```csharp
public interface IClock
{
    DateTimeOffset UtcNow { get; }
}
```

## Good Interface Example: AI Model Provider

Reason:

1. External model provider.
2. Provider may change.
3. Tests need deterministic responses.
4. Cost and latency matter.

```csharp
public interface IModelProvider
{
    Task<ModelResponse> GenerateAsync(ModelRequest request, CancellationToken cancellationToken);
}
```

## Bad Interface Example: DTO

Do not do this:

```csharp
public interface ICreateCustomerRequest
{
    string Name { get; }
    string Email { get; }
}
```

Use a concrete DTO or record instead:

```csharp
public sealed record CreateCustomerRequest(string Name, string Email);
```

## Bad Interface Example: One Stable Class

Do not do this unless there is a real seam:

```csharp
public interface IUserDisplayNameFormatter
{
    string Format(User user);
}

public sealed class UserDisplayNameFormatter : IUserDisplayNameFormatter
{
    public string Format(User user) => $"{user.FirstName} {user.LastName}";
}
```

A simple function or concrete class is enough.

## Bad Interface Example: Duplicate Class Shape

Do not create this:

```csharp
public interface IOrderService
{
    Task<Order> GetOrderAsync(Guid id);
    Task SaveOrderAsync(Order order);
}
```

If it only mirrors `OrderService` and has no second implementation, no external boundary, no test need, and no replacement scenario, it is ceremony.

## Recommended Workflow for Agents

For any new service or module:

1. Start concrete.
2. Identify external dependencies.
3. Identify test pain.
4. Identify provider change risk.
5. Add interfaces only at meaningful seams.
6. Keep interfaces small.
7. Inject dependencies.
8. Wire implementations in the composition root.
9. Test through public behavior.
10. Remove interfaces that do not carry weight.

## Final Recommendation

Install one custom skill:

```text
contract-based-interface-development
```

Pair it with:

1. TDD.
2. Dependency inversion.
3. Security API Preconditions.
4. Parallel Agent Orchestration.
5. Abstraction Skeptic review agent.

The most important instruction for Claude and Codex is:

```text
Every interface must justify its existence. If it protects no boundary, enables no test seam, supports no replacement, and only duplicates one class, remove it.
```

## References

### Skills and Agent References

1. Matt Pocock Interface Design  
   https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/INTERFACE-DESIGN.md

2. Matt Pocock Improve Codebase Architecture  
   https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md

3. Matt Pocock TDD Skill  
   https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md

4. Matt Pocock Interface Design for Testability  
   https://github.com/mattpocock/skills/blob/main/tdd/interface-design.md

5. Clean Architecture Dependency Inversion Skill  
   https://github.com/PanGan21/clean-architecture-claude-skills/blob/master/skills/clean-architecture-dependency-inversion/SKILL.md

6. GitHub Awesome Copilot .NET Best Practices  
   https://github.com/github/awesome-copilot/blob/main/plugins/csharp-dotnet-development/skills/dotnet-best-practices/SKILL.md

7. GitHub Awesome Copilot .NET Design Pattern Review  
   https://github.com/github/awesome-copilot/blob/main/skills/dotnet-design-pattern-review/SKILL.md

8. GitHub Awesome Copilot C Sharp Expert Agent  
   https://github.com/github/awesome-copilot/blob/main/agents/CSharpExpert.agent.md

9. GitHub Awesome Copilot Object Oriented Design Patterns Instructions  
   https://github.com/github/awesome-copilot/blob/main/instructions/oop-design-patterns.instructions.md

10. GitHub Awesome Copilot .NET Architecture Good Practices Instructions  
    https://github.com/github/awesome-copilot/blob/main/instructions/dotnet-architecture-good-practices.instructions.md

11. SOLID Skills  
    https://github.com/ramziddin/solid-skills

### Official Engineering References

1. Microsoft .NET Design Guidelines: Abstractions, Abstract Types, and Interfaces  
   https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/abstractions-abstract-types-and-interfaces

2. Microsoft .NET Dependency Injection Guidelines  
   https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection/guidelines

3. Microsoft ASP.NET Core Dependency Injection  
   https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection

4. Microsoft .NET Architecture Principles  
   https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles

5. TypeScript Handbook: Interfaces  
   https://www.typescriptlang.org/docs/handbook/interfaces.html

6. Python Typing: Protocols and Structural Subtyping  
   https://typing.python.org/en/latest/reference/protocols.html

7. Python PEP 544: Protocols  
   https://peps.python.org/pep-0544/
