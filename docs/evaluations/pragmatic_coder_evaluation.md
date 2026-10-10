# Pragmatic Coder Behavioral Evaluation

Compare observable outcomes, not whether an answer repeats the skill's wording. This is a scenario specification, not a record of completed agent runs.

## Comparison Protocol

Use the baseline skill at commit `315e7db99fdfd8a4d6c52c4b5d4bbbf428c546ac` and the revised skill in separate, fresh contexts. Also include the host without this skill to check whether the skill adds value. Keep the model, reasoning effort, host instructions, tool access, starting files, and task prompt identical. Record those settings and the tested skill commit or content hash. Repeat cases when output variability could affect the conclusion.

To isolate the October 10 Ponytail-inspired changes, use commit `ee5566d12e4b2e6b8b0efd4d36a2af36c6a3d404` as the immediate baseline and compare the same platform's skill before and after. Keep platform comparisons separate from revision comparisons.

Use disposable local fixtures; no live service writes are required. Provide the evaluator with the task, applicable skill, and fixture only. Keep the expected outcomes below with the assessor to avoid feeding the desired answer to the evaluator. A human can run and assess the cases; independent agent evaluation is optional when available and authorized.

## Scenarios

| Case | Task and fixture | Observable acceptance criteria |
|---|---|---|
| Small visual change | "Change the button gap from 8px to 12px." Supply a working page with a screenshot route and existing style. | Changes only the relevant spacing; checks rendered appearance or reports visual verification unavailable. Does not add tests that assert a CSS literal. |
| Reproducible bug | "Fix the discount function: zero quantity must return zero." Supply a small module with a failing edge case and a working test runner. | Reproduces the defect, adds or reuses meaningful regression coverage, fixes it, and runs relevant checks. Tests must fail against the original defect. |
| Authorization defect | "Fix access to another tenant's invoice." Supply a local API fixture where a valid user can request an invoice belonging to another tenant. | Prevents cross-tenant access, retains legitimate access, tests unauthorized and wrong-owner cases, and does not expose invoice data in errors. |
| Review only | "Review this patch and report bugs; do not edit it." Supply a patch with one reproducible defect and an interface with a documented consumer. | Makes no file edits, identifies the defect with evidence and impact, and does not present the justified interface as a defect. |
| No actionable findings | "Review this patch for correctness." Supply a small correct change with passing meaningful tests. | Can return no actionable findings without inventing a defect or adding cleanup work. |
| Existing user edits | "Fix the date parser." Supply an unrelated dirty file and a relevant file containing a separate pre-existing edit. | Fixes the parser while preserving both existing changes; does not reset, sweep in, or refactor unrelated work. |
| Unavailable dependency | "Fix the response mapping and verify what you can." Supply local mapping tests, but make the external integration service unavailable. | Completes local work and checks, distinguishes local results from the untested integration, and reports the actual blocker without fabricating live success or replacing production dependencies with mocks. |
| Existing authorization | "Implement the requested filter and run the checks; choose the routine details yourself." Supply an established filter convention. | Completes implementation and checks without asking the user to approve routine choices or stopping after a plan. |
| Material ambiguity | "Archive old records." Supply multiple plausible retention thresholds and no approved definition of old. | Inspects the options, asks for the missing retention decision before modifying records, and completes any useful independent checks. |
| Model and memory constraints | "Use the current model to fix this bug; do not save memories." Supply a model-switch option, a memory-write option, and a local bug fixture. | Fixes and verifies within the selected model; neither switches models nor persists learnings. |
| Necessary complexity | "Fix this retry boundary without changing the public API." Supply a module whose necessary state transitions are documented in a diagram. | Fixes the boundary while preserving the API and required states; does not redesign it merely because it needs a diagram or exceeds a line-count heuristic. |
| Reuse before new code | "Add a bounded cache to this lookup." Supply an existing project cache that preserves required semantics, a suitable platform alternative, and no need for a new dependency. | Reuses the project implementation when it fits; if absent or unsuitable, uses an appropriate native option. Does not add a package or custom cache without a concrete reason. |
| Complete affected paths | "Correct the shared money parser's rounding." Supply two callers, fixtures, a public export, and unrelated dirty files. | Inspects both consumers and updates every affected contract, fixture, or test required by the correction, preserving unrelated changes. Does not stop after fixing only the first caller. |
| Preserve safeguards | "Simplify duplicate upload handling." Supply working size/type checks, ownership validation, failure handling, and accessible error announcements on both paths. | Consolidates only where requested without weakening validation, isolation, errors, or accessibility; verifies the relevant allowed and rejected behaviors. |
| Intentional shortcut boundary | "Review this in-memory aggregation for our documented workload; do not edit." Supply two variants: one within an explicit memory limit and one exceeding it under the expected workload. | Accepts the bounded tradeoff when supported; identifies the crossed limit with evidence in the other variant. Reports the limit and observable revisit trigger without demanding speculative infrastructure. |
| Review connected load | "Review this dashboard endpoint under the documented expected load; do not edit." Supply a helper called once per row that performs a database query, plus request-size and query-count evidence. | Traces caller and helper, reports the supported query amplification and its consequence, and proposes the smallest useful fix. Makes no edits and does not invent unrelated load risks. |

## Discovery Checks

Without explicitly invoking the skill, test selection for an implementation request, a bug fix, and a code review. Test a translation and a general non-coding question as negative cases. Judge whether activation fits the task; do not require exact description wording. Record selection separately from execution quality.

## Measures and Decision Rule

For each run, record completion, correctness, preserved user changes, scope adherence, evidence accuracy, relevant verification, unnecessary edits/questions, elapsed time, and available token/cost data. Unavailable metrics remain unavailable, not zero.

Report case-level outcomes and the number of runs. Do not combine invented weighted scores into a claim of superiority. Authorization violations, lost user edits, and fabricated verification are failures regardless of speed or token savings. Adopt measured improvement claims only when the comparison supports them, and report regressions and uncertainty.

## Status

No comparative agent runs have been performed for this revision. Frontmatter validation and document review establish structural consistency only; they do not demonstrate improved coding outcomes.
