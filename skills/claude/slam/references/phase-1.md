## Phase 1 — Preflight

Run these and evaluate before touching anything:

```bash
# Capture the branch ONCE. Empty means detached HEAD — stop here rather than
# letting an empty $BRANCH flow into push/delete commands downstream.
BRANCH=$(git branch --show-current)
[ -n "$BRANCH" ] || { echo "REFUSE: detached HEAD — no branch to ship"; exit 1; }

# This skill ships FEATURE branches. Refuse a protected branch outright:
# committing straight to one is forbidden, and Phase 7 must never receive its name.
is_protected "$BRANCH" \
  && { echo "REFUSE: '$BRANCH' is protected — /slam ships feature branches"; exit 1; }
echo "branch: $BRANCH  ->  base: $BASE"

gh auth status >/dev/null || { echo "REFUSE: gh not authenticated — run 'gh auth login'"; exit 1; }
git remote get-url origin >/dev/null 2>&1 || { echo "NO_REMOTE"; }
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null)
```

**Every row in the table below is enforced by the block above, not left to your judgement.** A stop condition that is only described is a stop condition that does not fire.

**Record `$BRANCH` now and carry it through the whole run.** Phase 6 checks out `$BASE`, so from that point on `git branch --show-current` no longer names the feature branch — and Phase 7 deletes by name. Re-deriving it after the checkout is how you delete the wrong branch.

**Stop conditions:**

| Condition | Why it stops |
| --- | --- |
| Current branch is protected | This skill ships *feature branches*. Phase 0 should already have moved the work off; if you reach here still on one, that is a bug, so stop. |
| Detached HEAD | Nothing to push. |
| `gh` not authenticated | Cannot manage the PR. Tell the user to run `gh auth login`. |
| No `origin` remote | Handled below — offer to create one; don't silently ship nowhere. |

### No remote — create one

Every repo should have a remote. If `origin` is missing, the local history is a single disk failure from gone, and none of Phases 3–7 can run at all.

**Confirm with the user before creating it, and default to private.** Creating a repo publishes code — that is outward-facing and not reversible in the way a local commit is. Before you offer, **scan the tree for anything that must not leave the machine**:

```bash
git ls-files -z | xargs -0 grep -nEI \
  '(api[_-]?key|secret|password|client[_-]?secret|connection[_-]?string|BEGIN [A-Z ]*PRIVATE KEY|xox[bp]-|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})' \
  2>/dev/null | grep -viE '(process\.env|import\.meta\.env|placeholder|example|your-|\$\{)' | head -25
git ls-files | grep -iE '\.env$|\.pem$|\.pfx$|credential' || echo "no credential files tracked"
```

Report what you find — including tenant/subscription/account identifiers, which are not credentials but do name real infrastructure — then create it:

```bash
gh repo create "<owner>/<name>" --private --source=. --remote=origin --push
```

Only propose `--public` if the user asks for it, and only after the scan came back clean. Then re-run Phase R so `$BASE` and `$REPO` reflect the new remote.

### Branch-off-base check

Confirm the branch actually descends from `$BASE`:

```bash
git merge-base --is-ancestor "origin/$BASE" HEAD && echo "up to date with $BASE" \
  || echo "BEHIND: origin/$BASE has commits not in HEAD"
```

If it reports BEHIND, the branch is stale. **Merge the base in — never rebase:**

```bash
git merge "origin/$BASE"
```

If that conflicts, stop and hand the conflict list to the user. Do not attempt clever resolutions on someone else's code.

If `git merge-base "origin/$BASE" HEAD` is empty, the branch shares no history with the base — stop, something is wrong.

---
