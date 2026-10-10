## Phase 2 — Inspect and commit

```bash
git status
git diff --stat
git diff --cached --stat
```

If the tree is clean **and** there are no unpushed commits, skip to Phase 4 — there may still be an open PR needing attention. Say so rather than reporting "nothing to do".

**Before staging, look at what you're committing.** Read the actual diff, not just the stat. Specifically check for:

- **Secrets / credentials** — keys, tokens, connection strings, passwords, `.env` files. A secret in a diff is a stop condition, in any repo.
- **Encrypted paths committed as plaintext.** If the repo uses git-crypt, a file that should be ciphertext but got staged as plaintext is a hard stop — once pushed, removing it means rewriting history, which this skill will not do. This check auto-detects and no-ops in repos without git-crypt:
  ```bash
  viol=0
  while IFS= read -r f; do
    [ "$(git check-attr filter -- "$f" | sed 's/.*: //')" = "git-crypt" ] || continue
    hdr=$(git cat-file blob ":$f" 2>/dev/null | head -c 10 | xxd -p)
    case "$hdr" in
      00474954435259505400) : ;;   # \0GITCRYPT\0 — correctly encrypted
      *) echo "HARD STOP: $f is git-crypt-managed but staged as PLAINTEXT"; viol=1;;
    esac
  done < <(git diff --cached --name-only)
  [ "$viol" -eq 0 ] || exit 1
  ```
- **Large or generated files that belong in `.gitignore`** — build output, local databases (`*.sqlite3`), `node_modules`, editor state. Mention them; don't silently sweep them in with `git add -A`.
- **Files referencing deleted paths** — e.g. a `docker-compose.yml` service whose build context was removed in the same change. Grep for the removed path across the repo.
- **Debug leftovers** — stray `print`/`console.log`, commented-out blocks, `.orig`/`.rej` files.

Stage with `git add -A` unless the diff contains unrelated work; if it does, ask which changes belong in this commit rather than lumping them together.

**Commit message** — conventional commits (`type(scope): subject`), matched to the repo's own history (`git log --oneline -20` shows the house style):

- Subject in the imperative, no trailing period, ~72 chars.
- A body that explains **why**, not a restatement of the diff. Wrap at ~76.
- Multiple logical changes in one commit: lead with the dominant one, cover the rest in the body.
- No AI attribution, no `Co-Authored-By`.

Use a heredoc so the body survives intact:

```bash
git commit -F - <<'EOF'
type(scope): subject

Body.
EOF
```

---
