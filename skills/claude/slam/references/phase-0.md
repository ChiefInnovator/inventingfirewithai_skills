## Phase 0 — Get the work onto a feature branch

Only runs when the current branch is protected. Otherwise skip straight to Phase 1.

The work is on a protected branch and cannot ship from there. **Move it — don't stop, and don't commit where it stands.** How you move it depends entirely on whether anything has been committed yet, so establish that first:

```bash
PROT=$(git branch --show-current)

# Anything uncommitted (staged, unstaged, or untracked)?
dirty=$(git status --porcelain)

# Local commits that origin does not have? These are the dangerous case.
ahead=$(git log --oneline "origin/$PROT..HEAD")

echo "dirty: $([ -n "$dirty" ] && echo yes || echo no)"
# grep -c exits 1 when it counts zero, which `set -e` would treat as failure —
# and "no local commits" is the normal case, not an error.
echo "local commits ahead of origin/$PROT: $(printf '%s' "$ahead" | grep -c . || true)"
[ -n "$dirty$ahead" ] || { echo "nothing to ship — clean tree, nothing ahead"; exit 0; }
```

**Name the branch** from the dominant change. Use the repo's existing prefix convention — check what's already there (`git branch -a --format='%(refname:short)'`) rather than assuming; `feature/` for new work and `fix/` for a repair are the common default. Derive it from the diff — don't ask. Creating a branch is cheap and reversible; that is not the part that needs confirmation.

### Case A — uncommitted only (`ahead` empty)

The easy case, and the common one. `git checkout -b` carries the working tree across untouched and leaves the protected branch exactly where it was:

```bash
git checkout -b "$NEW_BRANCH"   # dirty tree comes along; protected branch not modified
```

Nothing else to undo. Proceed to Phase 1, which will capture `$BRANCH` as the new branch.

### Case B — local commits on the protected branch (`ahead` non-empty)

Commits already exist where they must not. Moving them means pointing the protected branch back at its remote — **the one step in this skill that discards local state, so it is gated on the user.**

```bash
# The local branch must be strictly AHEAD of its remote — a fast-forward and
# nothing else. If origin/$PROT is not an ancestor of HEAD the branch has
# diverged, which means someone else's commits are tangled in and rewinding
# would take them too.
git merge-base --is-ancestor "origin/$PROT" HEAD \
  || { echo "REFUSE: $PROT has diverged from origin/$PROT — resolve by hand"; exit 1; }
```

Show the user the exact commits from `$ahead` and confirm before touching anything. Then:

```bash
git checkout -b "$NEW_BRANCH"          # commits + dirty tree now live here
git branch -f "$PROT" "origin/$PROT"   # rewind the protected branch to its remote
```

Use `git branch -f` while standing on the **new** branch, never `git reset --hard` while standing on the protected one — `-f` only moves the ref and cannot touch the working tree, so a mistake costs a ref update and not your uncommitted edits. `git reflog` still holds the old position either way.

**Stop conditions:**

| Condition | Why it stops |
| --- | --- |
| `git fetch` fails | Cannot tell a local commit from a pushed one; every decision below depends on it. |
| The protected branch has diverged from its remote | Rewinding would discard commits that aren't yours to move. Hand the user the divergence. |
| Case B and the user does not confirm | Discarding local history is never unattended. |
| Tree holds clearly unrelated bodies of work | Don't sweep them onto one branch — ask which belong, as Phase 2 requires. |

Never `git branch -f` or reset a protected branch to anything but its own remote ref, and never delete a protected branch as a way of "moving" work.

---
