# Prompt checklist

Work through this when drafting the prompt (step 4) and again after the review fixes (step 6). Every box must be true of `prompt.md`. It condenses `~/.openclaw/projects/promptman/docs/anthropic-prompting-best-practices.md` and `openai-prompting-best-practices.md`; read those only when an item needs more detail.

## A. Format

- [ ] One Markdown document. The goal and its purpose come first.
- [ ] Each kind of content sits in its own labeled `##` section (brief, decisions, rules, delegation, limits, and so on). Nothing is repeated in two sections with different wording.
- [ ] The last section is `## Implementation Plan`, spelled exactly so, and nothing follows it.
- [ ] No link or path to a file the product builder may not have: no PromptMan files, no `~/AGENTS.md`, no skills. Everything it needs is written in the prompt. Commands are written out in full. The one skill a prompt may name is Impeccable, and only with the instruction for what to do when it is not installed.
- [ ] No questions to the reader, no "TBD", no "choose between". Every open point has been decided.

## B. Required contents

One box per item. Each must be present and findable by its heading.

- [ ] **Goal and priorities.** What to build and why, with the order: (1) a complete, working, high-quality product; (2) built as fast as possible; (3) positioned to make money, which never delays or blocks the product.
- [ ] **Product brief.** What it is, who uses it, why people use it and come back, money (who pays, price, revenue model, monthly running cost), where it ships (one primary channel; others for the launch checklist). Unsourced claims are labeled as assumptions.
- [ ] **Quality bar.** Named, numbered, concrete requirements that separate the best products of this kind from average ones. Each is checkable by running the product. "Make it amazing" does not appear.
- [ ] **What done means.** The product builds and runs locally, its tests pass, it meets the quality bar, and there is one runnable artifact for the primary channel. Money work is not part of done.
- [ ] **Product decisions.** Platform, stack, scope, pricing, art direction, each with a one-line reason, stated as settled so the builder does not reopen them.
- [ ] **Test seam.** Core logic runs without the user interface, is deterministic for a given seed and inputs, and has a scriptable entry point whose interface is in the prompt.
- [ ] **How to decide and when to stop.** In these words or close to them: decide anything still open yourself, record it in one line, and keep going; never ask. Do not use credentials that were not provided, buy anything, sign up for a paid service, or take any action that is irreversible or visible to other people. When work needs one of those, finish everything else and list it in the launch checklist. Keep credentials and client material out of any brief sent to another model.
- [ ] **Delegation plan.** Copied from `roster.md` with exact commands, including the `perl` time-limit wrapper. Fast tier for fully specified, mechanical work (searches, boilerplate, test runs, bulk edits); reasoning tier for architecture and hard debugging; character graphics, character animation, and motion graphics always to `codex`. If a delegate command fails, the builder does the work itself or with its own subagents; a missing tool never stops the build.
- [ ] **Parallel work.** Which pieces start together, as a table of work packages with owned files. The builder is the slowest lane, so it keeps only the piece that needs the full picture. Tests are a work package once the test seam exists. When a lane is idle and the builder has more than ten minutes of its own work queued, it hands off the most fully specified item. A task the builder can finish in about five minutes stays with it, because briefing a worker costs more than doing it.
- [ ] **Interfaces between packages.** Every two work packages that touch have their shared types, signatures, and data shapes written out in the prompt.
- [ ] **Shared working tree rules.** `git init` if the directory is not a repository. One working tree, one branch (in an existing repository, the branch already checked out, or one new feature branch if that branch is protected), no git worktrees. Each worker is given the files it may change; two workers never hold the same file at once; only the product builder commits.
- [ ] **Every brief stands alone.** Goal, what done looks like, constraints, files it owns, working directory, what to return. Each brief carries the owner's rules that apply: no `git rebase`, no worktrees, no attribution or co-author lines in commits, nothing published to claude.ai, surgical diffs. The brief template below is included in the prompt.
- [ ] **Review.** A different model than the one that wrote the code reviews the integrated product once, after it runs. No per-task review.
- [ ] **Verification.** A table with one row per numbered quality bar requirement: the requirement, the exact runnable check (a test with scripted input, a measurement with its threshold, or a named screenshot), and where the result is recorded. No requirement is left without a runnable check; one a machine cannot judge is checked through its proxy. The builder runs the product, runs its tests, and records one line of evidence per row.
- [ ] **Progress log.** A named log file in the project. The builder reads it first on starting and appends each completed milestone and each decision, so an interrupted build resumes instead of starting over. Every entry is stamped with the output of `date`; working time is counted from the stamps, and time the machine spent asleep is not counted.
- [ ] **Limits.** 6 workers at once; 20 minutes per worker task; 1 retry on a different agent; 3 hours for the whole build. What counts as unusable output. Milestones 1 and 2 are never dropped (the builder does a twice-failed task itself). Later milestones may be dropped after a failed retry and are reported. At three hours: finish the current milestone, drop the rest, report. Never report a product that does not run as finished.
- [ ] **Final report.** What was built and how to start it, what was verified (per quality bar requirement), decisions made, anything dropped, and the launch checklist.
- [ ] **Design**, only for a product with a user interface: the wording from `impeccable.md` and a table of Impeccable commands by surface and milestone. Every question Impeccable would ask is answered in advance with "use your recommendation"; no step waits for a person; `shape`, `live`, `generate`, and Impeccable with no command do not appear; workers get `DESIGN.md` in their briefs; a missing Impeccable does not stop the build.
- [ ] **Trading rules**, only for a product that trades or invests: never claims a strategy cannot lose; bar is the best demonstrable risk-adjusted return; selection data separate from a final holdout no agent has seen, used once at the end; backtests include fees and slippage; maximum drawdown and position sizing rule given as numbers; done means backtest results plus a paper trading harness that runs; no live trading credentials; the paper period and real money are launch checklist items.
- [ ] **`## Implementation Plan`**, last: the components, then ordered milestones, each with a check the builder can run. Order: (1) runnable core; (2) rest of the quality bar; (3) features that bring people back and get it shared; (4) packaging for the primary channel; (5) the money path behind one interface with a local stand-in for the payment or ad provider, so it works without accounts or keys. Connecting the real provider is a launch checklist item. If the money path fails or runs out of time, the product is still delivered.

## C. Writing quality (from the Anthropic and OpenAI guidance)

- [ ] The prompt gives audience, purpose, and quality bar, and each constraint carries its reason. A reason lets the builder generalize.
- [ ] It states the larger purpose: who the product is for and what the owner will do with it.
- [ ] Instructions are at normal volume: no capitals for emphasis, no "CRITICAL". Requirements are not hedged ("try to", "if possible").
- [ ] Instructions say what to do, in preference to what not to do.
- [ ] It asks for action: build, do not suggest.
- [ ] Goals and constraints, not step-by-step micromanagement. The builder plans its own steps inside each milestone.
- [ ] Approval rules name the exact actions they cover (credentials, purchases, paid signups, irreversible or publicly visible actions).
- [ ] It tells the builder it owns this codebase and its design.
- [ ] It tells the builder not to stop while work is owed, and to work through ordinary obstacles (errors, timeouts, missing tools).
- [ ] It tells the builder to ground every progress claim in a result from the session and to report failures plainly.
- [ ] It tells the builder to test real behavior for all valid inputs, not to satisfy the tests.
- [ ] No line tries to control thinking depth, sets a token budget, or asks for reasoning to be written out.
- [ ] Examples are absent, or varied and clearly marked as examples.
- [ ] Frontend or visual products name imagery, typography, palette, and visual style.
- [ ] It defines completion as an observable result and requires a final completeness check before the report.
- [ ] Numbers are consistent everywhere they appear (prices, limits, counts, file names, commands). No section contradicts another.
- [ ] The prompt names one project directory by absolute path and says nothing is created outside it. For an existing product it says to change the product in place, not to start over or build a copy.
- [ ] Where two numeric requirements can conflict, the prompt says which gives way.
- [ ] Every requirement a machine cannot judge has a named, measurable proxy, and the final report must list what no person verified.
- [ ] Long commands are wrapped against machine sleep, evidence goes in a folder no tool cleans, and the full test suite runs at milestone checks only.

## D. Brief template

The prompt includes this template for the builder's own briefs to workers (adapted from the reusable task template in the OpenAI guidance):

```text
# Goal
[Concrete result, and what it is part of.]

# Working directory
[Absolute path. Work only here.]

# Files you own
[Exact paths this task may create or change. Change nothing else.]

# Inputs
[Interfaces, types, data, and decisions this task depends on, written out.]

# Constraints
[Stack and conventions. Rules: no git commits, no git rebase, no git
worktrees or new branches, no attribution or co-author lines, nothing
published or deployed, no purchases, no credentials. Keep the diff to the
files you own.]

# Done
[Observable acceptance criteria and the command that checks them.]

# Return
[What to reply with: files changed, check output, anything unresolved.]
```
