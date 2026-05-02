# Referenced Skills Scorecard

Scores compare each referenced skill against `pragmatic-coder` for compact, professional coding-agent behavior: simplicity, verification, TDD, security, performance, contracts, cost control, and parallel execution. Counts use `tiktoken` `cl100k_base` for the local skill and directly fetchable GitHub files on May 2, 2026. `N/A` means the reference is repo-only, multi-skill, unavailable, or not a single canonical file.

| Skill | Score | Why | Lines | Characters | Tokens |
|---|---:|---|---:|---:|---:|
| pragmatic-coder | 9.2 | Best broad coding standard; compact coverage across simplicity, TDD, security, contracts, performance, cost, and parallel work. | 56 | 2,881 | 608 |
| Karpathy Guidelines | 8.0 | Strong assumptions, simplicity, surgical edits, and verification; narrower. | 67 | 2,506 | 580 |
| Torvalds Doctrine | 7.6 | Strong data/userspace instincts; tone and size reduce reuse. | 141 | 5,574 | 1,288 |
| Matt Pocock TDD | 8.9 | Excellent TDD/public-interface discipline; focused scope. | 109 | 4,371 | 968 |
| Addy Osmani TDD | 8.4 | Good agent TDD workflow and quality gates. | 379 | 14,259 | 3,290 |
| Obra Superpowers TDD | 8.3 | Strict red/green discipline; narrower. | 371 | 9,857 | 2,420 |
| Alireza TDD Guide | 8.1 | Strong positive/negative coverage; more verbose. | 403 | 13,569 | 3,282 |
| mfranzon TDD | 7.4 | Lightweight command-style TDD when available. | 82 | 5,138 | 1,223 |
| morodomi TDD Skills | 7.2 | Workflow-oriented multi-skill set; less useful as one compact skill. | N/A | N/A | N/A |
| Addy Performance Optimization | 8.5 | Strong general performance optimization guidance. | 350 | 11,415 | 2,829 |
| Vercel React Best Practices | 8.2 | Strong React/Next patterns; framework-specific. | 149 | 7,251 | 1,756 |
| Callstack React Native Best Practices | 8.1 | Strong mobile/RN performance guidance. | 253 | 11,980 | 2,875 |
| perf lighthouse | 7.9 | Focused Lighthouse and budget verification. | 239 | 6,395 | 1,615 |
| OpenRequirementsAI Performance Engineering | 8.0 | Good NFR/SLA framing; planning-heavy. | 902 | 36,815 | 9,086 |
| WordPress wp-performance | 8.0 | Strong WordPress-specific performance checks. | 146 | 5,828 | 1,356 |
| RTK Performance | 7.8 | Concrete CLI/performance targets. | 435 | 11,982 | 3,369 |
| Loki Mode | 8.0 | Strong autonomous execution mindset; safety depends on usage. | 384 | 19,263 | 5,026 |
| AWS Code Agent | 8.2 | Practical explore-plan-implement-verify workflow. | 226 | 11,604 | 2,477 |
| consult-llm Debate VS | 8.0 | Strong alternative comparison and decision weighing. | 310 | 9,461 | 2,243 |
| consult-llm Collab | 7.8 | Good synthesis/brainstorming; less implementation-focused. | 156 | 6,296 | 1,411 |
| consult-llm Debate | 7.8 | Useful structured arbitration; can be heavy. | 259 | 9,395 | 2,161 |
| Autonomous Skill | 7.7 | Good continuation/task-state idea; narrower. | 264 | 7,323 | 1,913 |
| Concise Planning | 7.8 | Good low-friction planning and minimal questions. | 62 | 1,310 | 338 |
| Travis Agent Teams | 8.0 | Good team/subagent selection patterns. | 80 | 2,918 | 601 |
| OpenClaw Model Router | 7.8 | Strong model routing/cost tooling; less coding-standard focused. | N/A | N/A | N/A |
| Cost Aware LLM Pipeline | 7.8 | Good pipeline/cost strategy. | 183 | 5,706 | 1,343 |
| LLM Cost Optimizer | 7.9 | Good LLM cost discipline and observability. | 218 | 11,256 | 2,427 |
| Claude Code Cost Optimization | 7.6 | Useful Claude-tier mapping. | N/A | N/A | N/A |
| GitHub Model Recommendation | 7.7 | Good model selection policy framing. | 672 | 25,188 | 6,398 |
| Research Lookup | 7.5 | Good narrow research routing example. | 502 | 19,857 | 4,081 |
| Addy Security and Hardening | 8.8 | Strong broad security hardening; long and domain-specific. | 349 | 11,175 | 2,659 |
| API Security Best Practices | 8.3 | Strong API auth/input/rate/security testing guidance. | 907 | 23,363 | 5,903 |
| Senior Security | 8.2 | Good threat modeling/security review depth. | 444 | 15,378 | 3,509 |
| Security Pen Testing | 8.1 | Good active testing/scanning lens. | 306 | 13,865 | 3,185 |
| Adversarial Code Reviewer | 8.1 | Good skeptical review behavior. | 247 | 11,846 | 2,698 |
| Agent OWASP ASI Compliance | 8.0 | Good agentic security/compliance lens. | 323 | 11,878 | 2,754 |
| Invariant Analyzer | 7.8 | Good precondition/invariant analysis. | 72 | 1,633 | 414 |
| API Design | 7.8 | Good API contract/status/pagination/rate basics. | 523 | 13,082 | 3,309 |
| API Designer | 7.7 | Useful REST/GraphQL/OpenAPI contract design. | 219 | 7,816 | 1,835 |
| Matt Pocock Architecture | 8.5 | Strong abstraction/test-surface/deep-module guidance. | 71 | 5,096 | 1,151 |
| Clean Architecture Dependency Inversion | 8.2 | Strong dependency direction and boundary guidance. | 63 | 2,692 | 553 |
| GitHub .NET Best Practices | 8.1 | Strong .NET DI/interface/service guidance. | 85 | 3,230 | 602 |
| GitHub .NET Design Pattern Review | 8.0 | Good abstraction/SOLID review lens. | 42 | 3,284 | 599 |
| CSharpExpert Agent | 8.0 | Strong practical C# guardrails and anti-overabstraction. | 204 | 8,597 | 2,096 |
| OOP Design Pattern Instructions | 7.8 | Useful OOP/SOLID review guidance. | 99 | 13,689 | 2,513 |
| GitHub .NET Architecture Instructions | 7.8 | Good .NET architecture principles. | 279 | 11,884 | 2,320 |

## Notes

- `pragmatic-coder` scores highest because it merges the strongest behaviors from the references into 608 tokens.
- The closest high-value references are Matt Pocock TDD, Addy Security and Hardening, Matt Pocock Architecture, and Addy Performance Optimization.
- Larger skills often score well for depth but lower for activation cost, reuse, and token efficiency.
