## Phase R — Resolve the repo's shape

Everything downstream depends on three facts. Establish them once, here, and carry them through the whole run: **`$BASE`, `$BRANCH`, `$REPO`.** Re-deriving any of them mid-run is how a later phase acts on the wrong branch.

### The base branch: `develop` if it exists, else `main`

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  || { echo "REFUSE: not a git repository"; exit 1; }

git fetch origin --quiet \
  || { echo "REFUSE: git fetch failed — every check below would run on stale refs"; exit 1; }

if   git show-ref --verify --quiet refs/remotes/origin/develop; then BASE=develop
elif git show-ref --verify --quiet refs/remotes/origin/main;    then BASE=main
else BASE=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null)
fi
[ -n "$BASE" ] || { echo "REFUSE: cannot determine a base branch"; exit 1; }
git show-ref --verify --quiet "refs/remotes/origin/$BASE" \
  || { echo "REFUSE: origin/$BASE does not exist"; exit 1; }
echo "base: $BASE"
```

`develop` wins whenever it exists — a repo with both is running a develop→main promotion flow, and feature work targets `develop`. The `gh` fallback catches repos on `master` or another custom default.

**Never hardcode `develop` or `main` anywhere below.** Use `$BASE`.

### The protected set

`$BASE` is protected, and so are `main`, `master`, and `develop` **even when they are not the base** — a repo with a develop flow still must not have `main` deleted or reset by this skill. Use this test everywhere a branch name is about to be deleted, reset, or committed to:

```bash
is_protected() {
  case "$1" in
    ""|main|master|develop|"$BASE"|origin/*) return 0;;
    *) return 1;;
  esac
}
```

The empty string is in that list deliberately: an unset variable expands to nothing, and `git push origin --delete ""` must never be one typo away from running.

---
