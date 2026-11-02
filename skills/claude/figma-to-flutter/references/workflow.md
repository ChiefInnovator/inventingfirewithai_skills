# State, updates, explorers, and maintenance

## Project state

Keep state in the target project's chosen design root, not inside this distributable skill. Reuse existing schemas when present. A minimal ledger records:

- Chosen source, canonical output, explorer, and decision paths; required platform/acceptance policy.
- Per screen: stable slug, file key, original node ID/name, supplied and resolved URLs, dimensions, capture history, latest capture, and capture used by Dart.
- Canonical files and source revision; analyzer, render, pixel, human-review, and platform results; evidence paths; node-specific TODOs and differences.
- Pending work, reasons, and per-run changes/checks/next actions.

Use `pending` for work not completed, `draft` for generated or unresolved output, and `accepted` only when every selected acceptance gate has evidence. Keep source freshness separate from acceptance: a once-approved widget becomes stale when its relevant inputs change. A removed source is a reportable state, not automatic permission to delete application code.

`status` reports existing state without changing it. `drift` compares the requested live scope with captures but does not save results or trigger conversions. `sync` preserves unrelated file/page entries and updates only changed source plus dependent subtrees. Unchanged passing output should not be regenerated. `continue` resumes pending/failing/stale items without discarding partial user work.

Keep the whole-run measurements in external state under [performance.md](performance.md), including report-only invocations. Before calling drift unchanged, reconcile expected file/node identities with successful reads; blocked or cut-off calls remain unknown.

For a proven color-only change, refresh the changed bindings/values and patch only matching widgets or semantic token references. Verify that geometry, text, fonts, assets, and other dependencies are unchanged. Avoid global literal replacement, which can alter unrelated unbound paints. Rerender affected screens and requested modes under the normal gates.

## Decisions

Store only current-project questions, requirements, answers, and evidence. Do not import historical decision IDs, people, or approvals from the source skill. A useful entry has an ID, type, affected nodes/screens, owner role, question or requirement, status, adopted rule, and answer provenance.

Reuse an existing answer when it applies. Explicit requirements are requirements, not open questions. Ask only when a missing decision blocks correct work. A reversible draft fallback may keep independent work moving, but must remain labeled and cannot weaken an acceptance requirement. Never fabricate a designer's or product owner's approval.

## Shared explorer

Use one Flutter project with shared screen widgets for the requested platforms. Reuse an existing explorer instead of creating parallel catalogs. Each entry should retain a friendly title alongside original source URLs, file/node identity, dimensions, capture/version, status, TODOs, and evidence. Search, thumbnails, open/copy-source links, and inspectable metadata make review practical.

Keep fixtures and bundled assets deterministic and local. Generated mirrors are disposable outputs of canonical source; fix canonical widgets and regenerate rather than patching the mirrors. Refresh the catalog after screen or fixture changes. Check removed/duplicate entries and missing assets.

Run the project's preparation, analysis, and widget tests. Build and launch each requested platform on an explicit target and inspect the actual screen. A browser at phone width does not establish mobile acceptance. If no explorer exists, establish its location and requested targets before creating one; do not assume unrelated production-app edits are authorized.

When the explorer is embedded in an authorized application or review portal, validate that hosted surface too. Begin each screen from a fresh page or navigate to a blank page before loading it; previous canvases and app state must not satisfy readiness. Wait for the selected screen and mode, verify loaded content/assets, and inspect the actual render. Use existing supported authentication without copying project-specific session stubs. Remote URLs require fresh validation; local report reuse needs matching source/build/mode/browser/checker inputs and output hashes. Keep standalone and hosted results separate.

This package provides the workflow, not a prebuilt application-specific explorer or Docker runner. Discover or implement the target project's adapter within scope. Do not reference absent helper commands as if they were bundled.

## Batches and interruption

Use parallel agents only when available and authorized, and when independent screen work benefits. Give each worker disjoint canonical files and a clear source/capture contract. Keep shared ledgers, decisions, catalog updates, and final evidence reconciliation with one coordinator. Serialize operations sharing rate limits, render state, or caches.

Do not hard-code worker counts, model choices, transcript locations, shared Docker volumes, or machine-wide locks. Preserve partial work after interruption, mark unfinished checks accurately, and resume from artifacts rather than a worker's self-reported completion count.

After each batch, compare the diff with each worker's assigned files and source nodes, preserving public widget APIs and trace comments. Shared ledger/explorer updates belong to the coordinator. Permit only new captures for assigned sources; an existing capture is immutable. Isolate or repair a stray edit without discarding pre-existing user work. A worker's reported count cannot replace verified capture/render artifacts or complete drift coverage.

## Repairs and upstream knowledge

Fold demonstrated reusable repairs into the relevant mapping, helper, and regression test when skill maintenance is authorized. Keep customer examples and private capture evidence in the target project; use synthetic fixtures for distributed regression tests. A correction to one measured box is not automatically a universal layout rule.

For `upstream-review`, inspect the public plugin's current exact source revision and relevant tests. Separate useful conversion mechanics from repository integration and acceptance requirements. Record adopt/adapt/no-change decisions with evidence. Do not install a scheduler, run upstream setup scripts, or advance a reviewed baseline just because a new commit exists. Implement authorized upgrades, then rerun affected checks.
