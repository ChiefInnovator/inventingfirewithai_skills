# Goldfish Annotated Review Report

Target: `docs/designs/skills-library-design.md`, full file. The owner authorized
uninterrupted drafting, review, resolution, and implementation within the confirmed
scope. All listed findings retain their reviewers' original severities.

| ID | Severity | Category | Approved resolution | Execution evidence required |
|---|---|---|---|---|
| Z1 | Major | PROPOSE FIX | Pin CI Codex CLI and Node; document the local prerequisite and no-model scope | Six-suite run and CI |
| C1 | Major | PROPOSE FIX | Raw reports under root `.impeccable/`; curated public evidence only under `docs/` | Real Pages build excludes development records |
| F1 | Nit | PROPOSE FIX | Specify package targets at least 44×44 CSS pixels | Browser rectangles at shipping widths |
| IZ1 | Major | PROPOSE FIX | Include existing `tomlkit==0.15.2` helper dependency | Clean dependency environment runs MCP tests |
| R1 | Major | PROPOSE FIX | Exact client/source/destination/invocation/discovery table | Matching README and homepage guidance |
| R2 | Major | PROPOSE FIX | Two equal columns at 861–1100px, existing layouts outside | Browser checks at both sides of breakpoints |
| R3 | Major | PROPOSE FIX | Atomic design, verification, website, and release phases with gates | Each phase's commands and results |
| B1 | Major | PROPOSE FIX | Same action as R1; preserve separate finding ID | Same installation-contract evidence |
| B2 | Major | PROPOSE FIX | POSIX suite process groups, bounded TERM/KILL escalation and direct-child reaping | Disposable resistant-descendant timeout test |
| T1 | Nit | PROPOSE FIX | Name breakpoints, shadows, transitions, component snippets, and narrative | Design sidecar matches source |
| T2 | Nit | PROPOSE FIX | Name Impeccable's anti-pattern detector and rendered checks separately | Independent assessment reports |
| BR1 | Major | PROPOSE FIX | Static non-YAML prefix plus canonical Markdown payload; compare actual Jekyll output | Pages artifact check and deployed-byte check |

No finding was contested, escalated, or silently downgraded. All have been
resolved in the design. Implementation evidence is tracked in the public curated
review page and the final Impeccable report; this table alone is not a test pass.

## Execution evidence

- Z1 / IZ1: final unified command passed all six suites, 487 tests, zero skips or failures; pinned Node/Codex/Python helpers are active in CI.
- C1: development records are outside `docs/`; the Pages artifact build passed on PR #17.
- F1 / R2: independent rendered measurements covered eleven widths and changed breakpoint boundaries; all fifteen package targets were at least 44px high with no page overflow.
- R1 / B1: README and homepage share concrete client destinations and non-invoking discovery checks; package choice now links locally to installation.
- R3: staged design, verification, UI, independent critique, and delivery gates were executed in order. Remote release checks remain tied to the actual final PR head.
- B2: resistant-descendant timeout and SIGINT interruption regressions passed. Intentionally detached processes remain outside this contract.
- T1 / T2: source-derived design records and independent A/B reports are present; final configured static detector returned zero findings.
- BR1: the real Jekyll build verified unchanged static data bytes. Deployed-byte parity is a separate release acceptance check.

The evidence above records implementation outcomes, not an additional Goldfish
re-audit or an assertion of live host, screen-reader, indexing, or provider acceptance.
