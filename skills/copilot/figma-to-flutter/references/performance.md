# Incremental work and run measurements

## Whole-run timing

From the installed skill folder, choose a worktree-specific state directory outside tracked source. The helper uses only Python's standard library and never infers a repository from its installation path:

```sh
FIGMA_STATE_DIR=/path/to/worktree-cache/figma-runs
python3 scripts/run_state.py --state-dir "$FIGMA_STATE_DIR" start --command 'sync selected page'
```

Keep the returned `run` as `FIGMA_RUN_ID` for every stage and authorized worker in this invocation. Start before prerequisites and planning. Resume an interrupted invocation with its existing ID, or finish it as interrupted and start a new timer for a new `continue`. Never reconstruct an unrecorded start time.

Register selected work before dispatch, then replace each item's outcome with its verified result. Collection names come from the target project; identical slugs in different collections remain distinct:

```sh
python3 scripts/run_state.py --state-dir "$FIGMA_STATE_DIR" progress --run "$FIGMA_RUN_ID" --collection app --outcome pending screen-a screen-b
python3 scripts/run_state.py --state-dir "$FIGMA_STATE_DIR" progress --run "$FIGMA_RUN_ID" --collection app --kind part --outcome pending header
python3 scripts/run_state.py --state-dir "$FIGMA_STATE_DIR" progress --run "$FIGMA_RUN_ID" --collection app --outcome completed screen-a
python3 scripts/run_state.py --state-dir "$FIGMA_STATE_DIR" report --run "$FIGMA_RUN_ID"
python3 scripts/run_state.py --state-dir "$FIGMA_STATE_DIR" finish --run "$FIGMA_RUN_ID" --status interrupted
```

- A completed screen has finished the requested workflow and required checks. A capture during conversion, a render, or a cache hit alone does not complete a screen or grant visual approval.
- Count each collection/slug once, regardless of repairs, workers, modes, or platforms. Record parts and flow cards with `--kind part` or `--kind flow-card`; they do not increase full-screen throughput. An item cannot change kind within a run.
- Unchanged or previously completed work is `skipped`. Keep `failed`, `blocked`, and `pending` separate. Report-only or skill-maintenance runs normally complete zero screens.
- Elapsed wall time includes planning, waits, AI work, retries, checks, and any authorized shipping. Throughput divides completed full screens by that time. With zero completed screens, rates are zero and `secondsPerScreen` is null.
- Finish immediately before handoff on every exit path: `completed`, `blocked`, `failed`, or `interrupted`. `completed` is refused while any registered work is pending, failed, or blocked. Finished outcomes and timestamps are frozen; reporting does not modify the file.
- A hard process kill can leave a running record. Recovery must finish it as interrupted or explicitly resume the original invocation, preserving its start.

Optional stage measurements help find costs without replacing wall time:

```sh
python3 scripts/run_state.py --state-dir "$FIGMA_STATE_DIR" measure --run "$FIGMA_RUN_ID" --stage capture --seconds 12.5 --cache-hits 2 --retries 1 --throttles 0
```

`totals.seconds` is accumulated stage work and may overlap between workers. It is never the throughput denominator. State files retain raw timestamps, items, and stages; `report` and command responses derive elapsed time, counts, and rates without persisting those summary fields. Atomic writes and file locks protect concurrent updates. Include the returned `metricsFile` in the handoff with elapsed time, unique completed screens, rates, remaining outcomes, and supporting parts. Synthetic regression timings are not live Figma speed benchmarks.

## Optional finished-run history

When durable history is requested, `start` accepts optional `--repo-root /path/to/project` and `--skill-root /path/to/installed/skill`. They capture the starting Git commit/dirty flag and a location-independent skill content hash. Unrequested provenance is omitted, never inferred later; requested provenance must be readable before the timer record is created. Explicit repository selection also refuses mutable state inside that repository. Keep the normal timer outside project source.

After `finish`, export one sanitized record to an explicitly chosen directory:

```sh
python3 scripts/run_history.py --state-dir "$FIGMA_STATE_DIR" --run "$FIGMA_RUN_ID" --history-dir /path/to/chosen/history
```

The version 1 record contains `schemaVersion`, a SHA-256 `run` identifier, final status, timestamps, elapsed time, outcome counts, screen rates, numeric stages/totals, and optional starting `provenance`. Commands, local paths, collection/screen identifiers, branch names and arbitrary metadata are omitted. Only the stage labels `planning`, `capture`, `convert`, `render`, `pixel`, `check` and `review` survive; other labels become `other`. The run ID is hashed, not retained as free text. This minimizes disclosure; timestamps, counts and optional revision hashes still describe the run, so review the record before sharing it.

History and mutable state must use disjoint directories. A complete record is published atomically through a same-directory hard link; unsupported filesystems fail without replacing evidence. Existing records, including symlinks, are refused rather than overwritten. Use a new run ID for a new invocation. Exporting is optional: it never changes ledgers or captures, runs Git mutations, publishes remotely, or grants pixel, human or production acceptance. A report-only invocation still cannot write project history without that separately authorized output.

## Source selection and capture scheduling

Reconcile the entire selected live inventory by file key and node ID, including parts. Compare the expected identities with the actual successful drift reads. Missing, truncated, blocked, or failed reads remain unknown; retry within the provider's bounds or report them blocked, never unchanged.

An incremental baseline must cover node structure, text, geometry, paints, bindings and resolved variable modes, styles, components, images, and vectors. Missing dependencies require capture. Qualify a new baseline with matching dependency reads before and after the actual full capture; if they differ, recapture. Do not silently upgrade historical evidence. An explicit full refresh captures the entire requested scope.

Keep unchanged captures' original identities and dates. Fingerprint equality selects work; it does not provide a fresh screenshot or renewed approval. Read-only drift may write external run metrics, but cannot write captures, project ledgers, or conversions.

When workers are authorized, coordinate actual requests through one provider/account rate-limit window, honoring Retry-After and bounded retries. Bound independent downloads separately and verify URL/content identity before reuse. Preserve exact bytes and original tool-result provenance when decoding multipart or compressed captures; partial saves must not look complete. Use the current host's supported records, without importing another client's transcript machinery.

## Native rendering, caches, and stopped attempts

Use the project's pinned SDK on its supported host and record SDK, engine, architecture, renderer, and fonts. Do not introduce Docker, an emulated architecture, SDK upgrades, or a host-specific cache layout as conversion prerequisites. Select a Python interpreter compatible with the package requirements and use that same environment for dependent helpers and project adapters.

Cache keys must include source bytes, actual transitive widget/import and asset dependencies, font files and registrations, renderer/SDK, harness and lockfiles, checker/rule versions, relevant decisions, and requested modes. Verify output bytes as well as matching keys. Capture timestamps alone do not require rerendering; source comparison and approval remain separate gates. Run the font checks before reuse.

Use one owner for a shared render workspace. Acquire its lock before reading cache state, preserve unchanged generated bytes/timestamps, and atomically publish only complete results. Refresh the explorer once per completed batch, preserving incremental build outputs and pruning only generated stale files. Explicit force bypasses result reuse while retaining all checks.

Remember stopped repair attempts by their full input signature and concrete reason. Unchanged inputs remain visibly blocked or failed rather than triggering repeated automatic sweeps. Changed inputs or an explicit retry make them eligible again; scheduling state never changes acceptance. Resolve a shared font/component blocker once before another batch.

Only run measurement and optional finished-run export are bundled here. Capture schedulers, fingerprint planners, stopped-attempt caches, native renderers, and explorer build caches need target-project adapters; do not invoke absent helpers as if they were installed.
