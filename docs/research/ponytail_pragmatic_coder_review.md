# Ponytail review: Pragmatic Coder improvements

Reviewed October 10, 2026. The appropriate target is **Pragmatic Coder**, across Codex, Claude Code, and GitHub Copilot. The five recommendations below were applied to all three platform versions on October 10, 2026.

## Applied recommendations

| Area | Recommended wording | What it adds |
|---|---|---|
| Think Before Coding | “Trace affected callers, tests, fixtures, configuration, and exports before editing; include every change required by the requested behavior.” | Makes impact analysis concrete while keeping unrelated cleanup out of scope. |
| Simplicity and Cost First | “Before adding code, check existing project code, standard library/platform features, then installed dependencies; choose the smallest readable solution that fits.” | Turns the existing simplicity principle into an actionable reuse order. |
| Surgical Changes | “When moving or simplifying code, preserve required validation, error handling, accessibility, and trust boundaries.” | Makes safeguards explicit during refactoring. |
| Simplicity and Cost First | “For a deliberate shortcut with a material limit, document the limit and the observable trigger for revisiting it.” | Makes an intentional tradeoff reviewable without requiring a debt document for every small task. |
| Review Smells | “Check connected data flow and expected load; explain the demonstrated failure or maintenance cost and the smallest useful fix.” | Grounds review in the affected execution path. |

The entrypoints incorporate these recommendations into existing bullets, adding only one bullet for material shortcut limits. Evaluation scenarios cover project/native reuse, shared caller changes, retained validation during simplification, shortcut limits, and review under expected load. Behavioral evaluation remains pending.

## What to retain

Keep the local skill's proportionate verification, evidence reporting, scope boundaries, and host permission rules. Avoid importing intensity modes, session hooks, code-length targets, or a blanket requirement to test every branch. A shorter implementation can still be worse code. This review does not propose changing Slam or the Figma workflow.

## Evidence and limits

[Ponytail's implementation skill](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md) provides an explicit reuse ladder, affected-path inspection, and conscious shortcut boundaries. [Its review skill](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-review/SKILL.md) emphasizes connected context and supported consequences. The changes are independently worded adaptations to the existing skill, not an import of Ponytail's package or hooks.

The [published benchmark](https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-10-07-agentic.md) is author-run with a particular model and constrained harness. Many tasks measure delivery or size without hidden quality checks. It does not establish that these changes improve this repository's skill, model costs, or completion rates. No local comparative behavior benchmark has been run.
