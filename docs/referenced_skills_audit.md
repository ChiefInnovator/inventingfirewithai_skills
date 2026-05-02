# Referenced Skills Audit

This audit checks each referenced skill for ideas worth adding to `skills/pragmatic-coder/SKILL.md`. The goal is to keep the skill compact while preserving capability.

## Decisions

| Skill | Useful idea | Decision | Result |
|---|---|---|---|
| pragmatic-coder | Baseline compact coding standard | Keep | No action |
| Karpathy Guidelines | Read before changing, avoid guessing, keep edits small | Add | Strengthened "No guessing" with code/docs/tests |
| Torvalds Doctrine | Data shape beats control-flow complexity | Covered | Data First already captures it |
| Matt Pocock TDD | Test public behavior, not implementation details | Covered | Public-interface TDD already included |
| Addy Osmani TDD | Agent quality gates and scoped verification | Covered | Verification and targeted checks already included |
| Obra Superpowers TDD | Strict red/green/refactor loop | Covered | Behavior-change rule already captures it |
| Alireza TDD Guide | Positive/negative/boundary coverage | Covered | Happy/error/boundary paths already included |
| mfranzon TDD | Lightweight command-style TDD | Reject | Too tool-specific for a general skill |
| morodomi TDD Skills | Multi-skill TDD orchestration | Reject | Too large for one compact skill |
| Addy Performance Optimization | Budget, baseline, measure, reject regressions | Covered | Performance work rule already captures it |
| Vercel React Best Practices | React/Next-specific optimization | Reject | Framework-specific; README reference is enough |
| Callstack React Native Best Practices | Mobile/RN performance patterns | Reject | Framework-specific; README reference is enough |
| perf lighthouse | Lighthouse budgets and audits | Covered | General budget/baseline/check rule covers it |
| OpenRequirementsAI Performance Engineering | NFR/SLA framing | Covered | Performance budget captures the useful part |
| WordPress wp-performance | WordPress-specific performance checks | Reject | Platform-specific |
| RTK Performance | CLI-driven performance targets | Reject | Tool-specific; general rule already present |
| Loki Mode | Autonomous execution and persistence | Covered | Ask-only-for-blockers and targeted reporting cover it |
| AWS Code Agent | Explore, plan, implement, verify | Covered | Sections 1, 4, and 5 cover it |
| consult-llm Debate VS | Compare alternatives before choosing | Covered | Decision comparison already included |
| consult-llm Collab | Synthesize multiple views | Covered | Parallel-work synthesis already included |
| consult-llm Debate | Structured arbitration | Reject | Too process-heavy for routine coding |
| Autonomous Skill | Continue until blocked; preserve task state | Covered | Ask-only-for-blockers covers the useful part |
| Concise Planning | Minimal questions and compact plans | Covered | Ask-only-for-blockers already included |
| Travis Agent Teams | Assign disjoint ownership in parallel work | Covered | Parallel-work rule already captures it |
| OpenClaw Model Router | Model selection and escalation | Covered | Model-cost rule already included |
| Cost Aware LLM Pipeline | Use cost discipline without reducing success | Covered | Cheapest-likely-to-verify rule already included |
| LLM Cost Optimizer | Escalate when cheaper model fails | Covered | Two-failure escalation already included |
| Claude Code Cost Optimization | Model tier mapping | Covered | Current model-cost rule is platform-neutral |
| GitHub Model Recommendation | Match model strength to task risk | Covered | Model-cost rule names simple, coding, and high-risk work |
| Research Lookup | Use narrow research before answering | Covered | No guessing rule covers it |
| Addy Security and Hardening | Secrets, dependencies, injection, leaks | Covered | Security work rule already captures it |
| API Security Best Practices | API auth, ownership, input, rate, error checks | Covered | Preconditions and API boundary rules cover it |
| Senior Security | Threat modeling mindset | Covered | Security and precondition checks cover useful parts |
| Security Pen Testing | Abuse-case testing | Covered | Test abuse and data exposure already included |
| Adversarial Code Reviewer | Skeptical review against claims | Covered | Unsupported claim smell and verification rules cover it |
| Agent OWASP ASI Compliance | Agent/tool abuse and data exposure | Covered | API boundary and abuse checks cover it |
| Invariant Analyzer | Preconditions and invariants | Add | Added invariant/owner contract language |
| API Design | Contracts for input, output, errors, ownership | Add | Added contract language |
| API Designer | REST/GraphQL contract structure | Covered | General contract rule captures useful part |
| Matt Pocock Architecture | Use interfaces only for real seams | Covered | Interface rule already included |
| Clean Architecture Dependency Inversion | Composition root and dependency direction | Covered | Interface/composition-root rule already included |
| GitHub .NET Best Practices | DI and interface restraint | Covered | Interface rule already included |
| GitHub .NET Design Pattern Review | Avoid pattern overuse | Covered | Review smells and simplicity rules cover it |
| CSharpExpert Agent | Practical guardrails, no overabstraction | Covered | Simplicity, Data First, and smells cover it |
| OOP Design Pattern Instructions | SOLID/pattern review | Covered | Useful parts covered without SOLID verbosity |
| GitHub .NET Architecture Instructions | Architecture principles and boundaries | Covered | Reversibility, contracts, and project fit cover useful parts |

## Skill Changes Made

- `No guessing` now explicitly starts from local code, docs, and tests.
- New seams/contracts now name inputs, outputs, errors, invariants, and owner.

## Rejected Categories

- Framework-specific rules belong in dedicated skills or README references.
- Tool-specific command recipes add token cost without general capability.
- Heavy debate/orchestration processes are useful sometimes, but too large for default activation.
