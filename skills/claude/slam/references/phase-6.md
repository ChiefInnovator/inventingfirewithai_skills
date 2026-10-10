## Phase 6 — Merge

**Check mergeability and CI first:**

```bash
gh pr view "$PR" --json mergeable,mergeStateStatus,statusCheckRollup \
  -q '{mergeable, mergeStateStatus, checks: [.statusCheckRollup[]? | {name, conclusion}]}'
```

**Merge gates — resolve or wait before merging:**

| Condition | Action |
| --- | --- |
| Any required check failing or still running | Wait for running checks. Inspect failures, fix in-scope causes, verify, push, and recheck the new head. Stop only if no authorized remedy remains. Never merge red. |
| `mergeable: CONFLICTING` | Report the conflict and obtain user approval before resolving it. Diverged branches also require approval. Never rebase; after authorized resolution, verify, push, and recheck. |
| A human reviewer requested changes | Address actionable in-scope requests, verify, push, and request re-review. Never dismiss the human's block; if reviewer action is all that remains, report the dependency and wait or stop according to host capabilities. |
| Unresolved review comments you couldn't triage | Stop and ask. |

A repo with no CI configured returns an empty check list. That is "nothing to wait for", not "checks passed" — report it as such.

**Merge with a merge commit:**

```bash
gh pr merge "$PR" --merge
```

Do **not** pass `--rebase`. Do **not** pass `--admin` to bypass protections. Do **not** pass `--delete-branch` here either — deletion is Phase 7, gated on verifying the merge actually happened.

**Verify it actually merged**, then sync the local base branch. If fast-forward synchronization fails, retain the local branch and report the blocker; do not rebase, reset, or force-update it:

```bash
gh pr view "$PR" --json state,mergedAt,mergeCommit
git fetch origin --prune && git checkout "$BASE" && git merge --ff-only "origin/$BASE"
```

---
