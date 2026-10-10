## Phase 7 — Clean up the branch

Delete the feature branch once the work is genuinely landed. **Every one of these must hold — if any fails, stop and leave the branch alone:**

```bash
# $BRANCH is the value captured in Phase 1. Do NOT reassign it here and do NOT
# re-derive it — Phase 6 has already checked out $BASE, so any fresh
# `git branch --show-current` now yields the base branch, not the branch to delete.

# 0. NEVER a protected branch, and never an empty name. Check this FIRST —
#    an unset $BRANCH would otherwise expand to nothing and corrupt the
#    delete commands below.
is_protected "$BRANCH" && { echo "REFUSE: '$BRANCH' is protected or invalid"; exit 1; }

# 1. GitHub reports the PR merged — state MERGED *and* a real timestamp
read -r state merged_at <<<"$(gh pr view "$PR" --json state,mergedAt -q '"\(.state) \(.mergedAt)"')"
[ "$state" = "MERGED" ] && [ -n "$merged_at" ] && [ "$merged_at" != "null" ] \
  || { echo "REFUSE: PR $PR is not merged (state=$state mergedAt=$merged_at)"; exit 1; }

# 2. You are NOT standing on the branch you're deleting
[ "$(git branch --show-current)" = "$BASE" ] \
  || { echo "REFUSE: not on $BASE — Phase 6 should have checked it out"; exit 1; }

# 3. The branch is an ancestor of the base — its commits really are in.
#    Re-fetch IMMEDIATELY BEFORE the check. Phase R's fetch is minutes old by
#    now and Phase 6's pull refreshed only $BASE. If anyone pushed to the
#    feature branch during this run, a stale origin/$BRANCH points at an older
#    commit that IS contained in the base — the gate would pass and the delete
#    would take the newer commits with it.
git fetch origin --prune --quiet \
  || { echo "REFUSE: git fetch failed — cannot judge containment on stale refs"; exit 1; }
remote_ref=$(git ls-remote --heads origin "refs/heads/$BRANCH") \
  || { echo "REFUSE: remote lookup failed"; exit 1; }
if [ -n "$remote_ref" ]; then
  remote_head=$(printf '%s' "$remote_ref" | cut -f1)
  git merge-base --is-ancestor "$remote_head" "origin/$BASE" \
    || { echo "REFUSE: remote feature is NOT contained in origin/$BASE"; exit 1; }
fi
# A missing remote feature is already clean, not a merge failure.
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git merge-base --is-ancestor "refs/heads/$BRANCH" "origin/$BASE" \
    || { echo "REFUSE: local feature is NOT contained in origin/$BASE"; exit 1; }
fi
```

Every check above **exits non-zero on failure** rather than printing a verdict for you to read past. That is deliberate: a gate that only narrates is not a gate. In particular, note that `--is-ancestor ... && echo ok || echo "NOT CONTAINED"` would *swallow* the non-zero exit and let the deletion proceed — never write the containment check that way.

Only with all four satisfied, perform local cleanup. Retain the remote feature by default: a live-ref check followed by an ordinary delete is not atomic. Remote deletion requires repository-supported exclusive control preventing updates between the check and deletion. Never infer exclusivity from a quiet branch or use force/force-with-lease to bypass the no-force rule; report retention when exclusive control is unavailable.

```bash
# Retain the remote feature unless exclusive control has been established.
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git branch -d "$BRANCH"           # local — -d, never -D
fi
```

Use `git branch -d`, never `-D`. `-d` refuses to delete a branch whose commits aren't reachable from the current HEAD, which is a free second opinion on check 3. **If `-d` refuses, that is a real signal** — the commits are not in the base. Stop and investigate rather than reaching for `-D`.

Note this ordering matters if the merge was ever done as a squash: squashed commits are not literally ancestors of the base, so checks 3 and `-d` will both correctly refuse. That is the desired behavior — report it rather than forcing.

**Skip deletion entirely** (and say so) if the merge did not happen, if the user asked to keep the branch, or if the branch has commits that never made it into the PR.

---
