## Phase 4 — Ensure a PR exists

```bash
gh pr view --json number,state,url,isDraft,mergeable,baseRefName 2>/dev/null
```

**If no PR exists**, create one against `$BASE`:

```bash
gh pr create --base "$BASE" --head "$BRANCH" \
  --title "<conventional-commit-style title>" --body "<body>"
```

Body should cover: what changed and why, how it was verified, and anything the reviewer should look at closely. PR bodies, unlike commits, may carry the Claude Code attribution footer — follow whatever the repo's recent PRs already do.

**If a PR exists** but targets something other than `$BASE`, stop and ask — retargeting changes the review surface.

**If the PR is a draft**, ask before marking it ready.

Capture the PR number once, alongside `$BRANCH` and `$BASE`:

```bash
PR=$(gh pr view --json number -q .number)
```

---
