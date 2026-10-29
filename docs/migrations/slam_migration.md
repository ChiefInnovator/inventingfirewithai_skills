# Slam Migration to Codex

Adapted on September 5, 2026 from the user's 560-line Claude `slam` skill, source SHA-256 `52832e6d0b627dcac1c2ed9167520ca453c956a37a7c4fdba8823486a5516475`. The maintained packages are [Codex](../../skills/codex/slam/SKILL.md), [Claude](../../skills/claude/slam/SKILL.md), and [Copilot](../../skills/copilot/slam/SKILL.md); the Claude package has since been updated rather than kept as a frozen original. All three now bundle the review reference and Python cleanup guard. Codex retains OpenAI UI metadata; Claude retains its native Stop hook; Copilot uses its host's supported task capabilities.

## Preserved Workflow

Preflight, scoped commit and push, develop/main/default base selection, PR creation/reuse, AI review triage and replies, CI gates, merge-commit preference, and verified feature-branch cleanup. No rebasing, force-pushing, admin bypass, protected-branch deletion, or AI commit attribution. Explicit user/project choices take precedence over defaults.

## Platform Adaptations

- Standard skill frontmatter replaces Claude-only invocation/argument fields. `$slam` accepts ordinary request text; no `$ARGUMENTS` substitution is required.
- `agents/openai.yaml` provides a display name, description, and invocation prompt. Automatic discovery remains at the host default, with an explicit distinction between shipping requests and skill inspection/migration.
- Goal tools are optional and used only when the user explicitly requests a goal. Completion and blocked states follow the host's actual tool semantics; Claude Stop-hook and `/goal clear` instructions are removed.
- Runtime requirements are a local checkout, Git, authenticated GitHub CLI or equivalent GitHub tools, and Python 3 for the read-only cleanup guard. There is no OpenAI API key dependency.
- The same package can be used by a compatible OpenAI host with filesystem and repository tool access. Copying it locally does not install it into a remote account, grant access to repositories, or guarantee background execution.

## Correctness Adjustments

- Handle a missing origin before fetching; never treat failed remote/API access as absence of data or policy.
- Preserve local commits on a protected branch by branching from them; leave its ref intact instead of requiring a rewind to ship.
- Make GitHub repository/host, PR, branch, base, and head explicit. Do not rely on mutable checkout state or environment defaults.
- Monitor automatic reviews only; never manually request or re-request through assignments, APIs, comments, or delegates, and never manufacture a push as a review trigger. Paginate all feedback, verify completed review on the captured head, and distinguish quota/refusal messages from actual review.
- Honor an explicit user instruction not to wait for optional AI review, without bypassing mandatory GitHub approvals, required checks, or protections. A missing review is recorded as absent, never approved.
- Resolve routine divergence/conflicts with merge commits while preserving both branches' intended behavior. Ask only for real product/scope decisions or an explicit project approval requirement.
- Match the PR head at merge time; wait for actual merged state after queueing. Capture the verified full merge commit as `SLAM_MERGE_SHA` in persistent task state before cleanup, restoring it across tool calls. Use fast-forward-only local base synchronization.
- Check both local and live remote feature heads, worktrees, clean base state, and ancestry before cleanup. The guard performs no deletion and supplements, rather than replaces, GitHub policy and PR identity checks.
- Keep squash-merge cleanup conservative, retain branches on uncertainty, and disclose the guard's point-in-time concurrency limitation.

## Validation

Validate the Codex frontmatter with the skill validator and the native Claude frontmatter with a YAML parser. The cleanup tests run against all three packages using real disposable Git repositories; Stop-hook tests execute the actual registered shell command with temporary gates and disposable command-line fixtures, including a real sleeping process for timeout coverage:

```bash
python3 -m unittest discover -s tests -p 'test*slam*.py' -v
```

The original 16 cleanup tests passed on September 5, 2026; all three packages now run those same scenarios. They cover merged containment, protected/invalid targets, dirty/wrong checkouts, newer local/remote work, stale bases, worktrees, squash merges, missing refs, remote failure, and CLI behavior. Hook tests cover PR states, malformed gate/input data, session isolation, real process timeouts, recursive stop events, and safe failure. Recursive hook events allow stopping while retaining unfinished evidence; gate deletion is best-effort and cannot trap the session. They do not perform an end-to-end live GitHub shipping run or prove reviewer availability. No real project is committed, pushed, merged, or deleted merely to validate a skill update; Git mutations occur only in disposable fixtures.

## Sources

- [OpenAI skill format and discovery](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI long-running work](https://learn.chatgpt.com/docs/long-running-work)
- [GitHub automatic review configuration](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review)
- [GitHub CLI merge gates and queues](https://cli.github.com/manual/gh_pr_merge)
- [GitHub Copilot review and re-review behavior](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review)
- [Claude Code skill metadata](https://code.claude.com/docs/en/skills)
- [Claude Code Stop hooks](https://code.claude.com/docs/en/hooks)
