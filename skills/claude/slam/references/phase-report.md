## Final report

Summarize concretely:

- Repo and the detected `$BASE`, and why (`develop` present, or fell back to `main`/default)
- Commit SHA(s) and subject(s)
- PR number and URL, and whether you created it or reused an existing one
- Whether an AI review actually ran — and if not, why (no ruleset, no subscription, over the 300-file cap). Never let silence read as approval.
- Every AI comment: what it said, and whether you fixed it or declined (with the reason)
- CI status at merge time, or "no checks configured"
- Merge commit SHA, and confirmation the local base branch is synced
- Whether the feature branch was deleted (local + remote), or why it was kept
- **Anything you skipped or that remains open** — state it plainly rather than implying a clean sweep

If you stopped early, report the phase, attempted remedies, remaining obstacle, and what would enable resumption. Distinguish completed, blocked, and explicitly abandoned outcomes; abandonment records who decided and why. A blocked or abandoned run is not shipped.

**Put the literal facts in the text** — PR number, `state=MERGED`, the merge commit SHA, and the deleted branch name or verified retention reason. For an unfinished run, report the named stop condition and its blocker separately; they are not completion evidence. If the user set their own `/goal`, the same facts are what its evaluator needs.

**Release the ship gate last:** `rm -f` this session's gate file (path in SKILL.md), whether the run completed, halted, or was abandoned.
