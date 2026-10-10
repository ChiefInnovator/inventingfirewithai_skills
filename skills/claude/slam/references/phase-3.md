## Phase 3 — Push

```bash
git push -u origin "$BRANCH"
```

If rejected as non-fast-forward, fetch `origin` and inspect both histories. If the local feature branch is strictly behind its remote, use `git merge --ff-only "origin/$BRANCH"`, verify, and retry the push. If histories diverge or conflicts require resolution, stop and ask for approval. Never pull, rebase, or force-push.

Confirm it landed:

```bash
git log origin/"$BRANCH"..HEAD --oneline   # expect empty
```

---
