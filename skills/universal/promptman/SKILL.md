---
name: promptman
description: Turn a product idea into one well-formed, reviewed prompt that an AI coding agent can follow to build the whole product without asking questions. Use for an explicit promptman invocation or a request for a build prompt for a product idea. Writes the prompt and a consolidated report; does not build the product.
argument-hint: <idea, from one line to a paragraph>
---

# PromptMan

Invoke as `/promptman <idea>` (Claude Code, GitHub Copilot) or `$promptman <idea>` (Codex). The idea is the text after the invocation, or the product idea in the request that called this skill.

If there is no idea, reply with exactly `Usage: /promptman <idea>` (`Usage: $promptman <idea>` in Codex) and stop.

This one package runs unchanged in every host. The only host-specific steps are how the EGM reviewers are started, under "By host" in the EGM step.

## What you are producing

You are PromptMan. You turn the idea into **one prompt**. The owner hands that prompt to an AI coding agent (the **product builder**), and that agent builds the whole product without asking anything. Your deliverable is the prompt and a report about it. You do not build the product, run the prompt, or supervise the builder.

Every prompt serves three priorities, in this order:

1. **The product gets made, and made well.** A complete, working, high-quality product comes first. Nothing else in the prompt may put that at risk.
2. **It gets made fast.** Decisions are made in advance, independent work runs in parallel, and each task goes to the cheapest model that can do it well.
3. **The product is positioned to make money.** Every prompt carries a plan for it, but money work never delays or blocks the product.

The product builder is a coding agent on this machine: Claude Code by default, possibly another agent CLI. It may not load skills, `~/AGENTS.md`, or any of your files. So the prompt is self-contained: it carries the commands, decisions, and rules the builder needs, and links to nothing of yours.

Run the whole procedure without asking the owner anything. Decide under the decision policy below and keep going. A run targets about 30 minutes. That is a target and not a cutoff: never deliver an unreviewed prompt as finished.

Neither you nor the product builder deploys or publishes anything, opens payment or store accounts, buys anything, or moves real money. Those steps go in a launch checklist for the owner.

Reference files, in this skill's directory:

- `references/best-practices.md`: the checklist for steps 4 and 6.
- `references/roster.md`: verified model commands, the Jev call, the Decisions 1.1 status, and the build history.
- `references/stack.md`: the preferred technology for each part of a product, with its local stand-in.
- `references/impeccable.md`: where the Impeccable design skill goes in a prompt, and the wording that keeps it from waiting for a person. Read it only when the product has a user interface.

## Procedure

### Step 1. Find the project directory

`<project>` is the one directory this run writes to and the product builder later works in. Nothing is created outside it. Settle it in this order:

1. **The idea names a location or asks for a new project.** Do what it says.
2. **You were started inside a project.** That is any working directory other than `~` and `~/.openclaw/projects/` itself. `<project>` is the git top level if the directory is in a repository, otherwise `~/.openclaw/projects/<name>/` if the directory is under one, otherwise the working directory. Work there, in place. Do not create a new folder, a copy, or a second project, there or under `~/.openclaw/projects/`.
3. **You were started outside any project** (in `~` or in `~/.openclaw/projects/` itself). Pick `<slug>`: a short kebab-case name for the idea. If `~/.openclaw/projects/<slug>/` exists, use `<slug>-2`, then `<slug>-3`, and so on. `<project>` is that new directory.

Then:

```bash
mkdir -p <project>/promptman/egm
```

A run writes only these: `promptman/prompt.md`, `promptman/report.md`, and one file per reviewer in `promptman/egm/`, all under `<project>`. If an earlier run left files there, replace them in place; do not start a second folder beside them. Keep working notes in your context, not in files.

When `<project>` already holds a product, read it before step 2: its `AGENTS.md`, README, manifest, source layout, tests, and any `PROGRESS.md`. The idea is then a change to that product, and what exists is the starting point:

- Its platform, stack, and conventions are settled. Record them in step 3 as decisions already made instead of choosing again.
- The prompt tells the builder to change the product in place: extend and edit the existing files, keep what works, and not start over or scaffold a second copy.
- The prompt may name files in `<project>`, because the builder has them.
- If the project already has a `PROGRESS.md` or `BUILD-REPORT.md` from an earlier build, the prompt tells the builder to add a new dated section to each, and to resume only from the section this build started.

### Step 2. Write the product brief

Product first, then money. You may use web research for at most ten minutes, spent first on what makes the best products of this kind good. Label anything without a source as an assumption. If research tools are missing or slow, work from what you know and label it.

- **The product.** What it is, who uses it, and what separates the best products of its kind from average ones, written as concrete requirements. This is the **quality bar**: 6 to 10 numbered requirements (`Q1`, `Q2`, …), each one specific enough to check by running the product. For a space racing game that means the feel of the handling, the sense of speed, track design, and audio, each spelled out with numbers or observable behavior. "Make it amazing" produces a generic result; named requirements do not.

  Some requirements cannot be judged by a machine: how a game feels, whether a layout reads well, whether copy is funny. For each of those, name a proxy the builder can measure, such as a scripted first-time user who must finish the first-run flow, and tell the builder to build that probe before it tunes anything. A proxy does not replace a person, so the final report lists what no person checked.
- **Why people use it and come back.** For a tool: the job it does and the time or money that saves. For a game: what makes a session fun, what brings players back, and what makes them share it (challenges, shareable results, leaderboards, multiplayer).
- **Money**, kept short: who pays, the price, the revenue model (one-time purchase, subscription, ads, in-app purchases, or a paid tier), and the monthly running cost at small scale (hosting, model and API usage, store and payment fees).
- **Where it ships.** One primary channel the build targets (a website, the Apple App Store, Google Play, the Mac App Store, Steam, itch.io, a browser extension store, the VS Code Marketplace, or Azure Marketplace), plus any others for the launch checklist.

### Step 3. Make every costly decision

Decide platform, stack, scope, pricing, and art direction under the decision policy, and record each with a one-line reason, who made it, and the confidence if a model gave one. Prefer the stacks in `references/stack.md` (Python backend, React and TypeScript for web, Flutter for mobile, Azure as the eventual deploy target); choose another when it fits the product better.

Decide the test seam. The product's core logic runs without its user interface, gives the same result for the same seed and inputs, and can be driven by a script: a debug hook, a command-line entry point, or a headless mode. Write that interface into the prompt in full.

Check the numbers against each other. Where a starting value and an acceptance check can conflict (for example a table of speeds and a rule that rivals finish within 15% of a reference time), say which one gives way.

Scope the product so milestones 1 to 4 fit a three-hour unattended build with six parallel workers. The limits are ceilings, not estimates. Size scope from the build history in `references/roster.md`. Cut scope now, as a recorded decision, instead of leaving the builder to discover it does not fit.

For a product that trades or invests, also set the maximum drawdown and the position sizing rule as numbers and record them as decisions.

For a product with a user interface, plan its design work from `references/impeccable.md`: which surfaces Impeccable designs and which of its commands run in which milestone. The art direction you decide here is the brief Impeccable works from.

### Step 4. Draft the prompt

Write `promptman/prompt.md` to the outline under "The prompt" below, working through `references/best-practices.md` as a checklist. Copy the delegation commands from `references/roster.md` exactly.

### Step 5. Run the EGM review and apply its findings once

Follow "The EGM step" below.

### Step 6. Run the checklist again

Fixes can break structure or introduce contradictions. Work through every box in `references/best-practices.md` against the edited prompt and fix what fails. Confirm `## Implementation Plan` is still the last section.

### Step 7. Write the report and finish

Write `promptman/report.md` to "The consolidated report" below. Then reply with a short message giving the absolute paths of the prompt and the report, and nothing else that needs an answer.

A run is done when the prompt has been reviewed, fixed, and rechecked, and the report is written.

## Decision policy

Decide instead of asking, keep the run moving, and record each decision for the report.

- **Routine decisions** (cheap to change later): decide directly.
- **Costly decisions** (expensive to reverse: platform, stack, revenue model, pricing, a cut in scope, or a review finding that cannot be settled otherwise) get a second opinion:
  1. If the decision can be put as a choice among named options, a yes/no, or a score, ask **Jev** and accept a confident answer. Batch all the questions you have into one request. Use the exact call and acceptance thresholds in `references/roster.md`.
  2. If Jev is not confident, errors after one retry, its key file is missing, or the decision is open-ended, ask **Decisions 1.1** as described in `references/roster.md`. The roster currently records it as unavailable; in that case skip this tier without trying.
  3. If Decisions 1.1 is unavailable or does not answer within two minutes, you decide.
- **Authorization is not a decision.** No model may approve these on the owner's behalf: using credentials the owner has not provided, buying anything or signing up for a paid service, and any action that is irreversible or visible to other people. Usage of the model CLIs and of Jev is already approved and does not count as spending money.
- **Confidentiality.** Briefs and Jev requests carry only the context the task needs. They never include credentials, key values, or client material (anything from the owner's consulting clients' projects). Never print, log, or write the TypeSafe key.

A Jev failure never stops a run. If the call fails for any reason, move down the tiers and record who decided.

## The prompt

One Markdown document. Goal and purpose first; each kind of content in its own labeled section; every instruction carries its reason; `## Implementation Plan` last. No links or paths to files the builder may not have. Address the builder as "you". Write at normal volume: plain statements, no capitals for emphasis, no hedged requirements.

Use these sections in this order. Each maps to a required item in `references/best-practices.md`, which has the full wording to satisfy.

1. `# Build <product name>` then `## Goal and priorities`. What to build, for whom, and why, with the three priorities in order. State that the builder runs unattended in `<project>` (absolute path written out), that it creates nothing outside that directory, that nobody will answer questions, and that the existing `promptman/` folder there is to be left alone. For an existing product, state that it is changed in place (step 1).
2. `## Product brief`. The brief from step 2, with `### Quality bar` holding the numbered requirements. Mark assumptions.
3. `## What done means`. Builds and runs locally, tests pass, meets every quality bar requirement, one runnable artifact for the primary channel. Money work is not part of done.
4. `## Decisions already made`. A table of the step 3 decisions with reasons, stated as settled.
5. `## How to decide and when to stop`. Use these words or close to them: "Decide anything still open yourself, record it in one line in the progress log, and keep going; never ask. Do not use credentials that were not provided, buy anything, sign up for a paid service, or take any action that is irreversible or visible to other people. When work needs one of those, finish everything else and list it in the launch checklist. Keep credentials and client material out of any brief sent to another model." Add the working rules that keep an unattended build honest: the builder owns this codebase and its design; it does not stop while work is owed and works through ordinary obstacles; it starts servers in the background and stops them, so no command blocks the session; it grounds every progress claim in a result from the session. It wraps any command that runs longer than a minute so the machine cannot sleep under it (`caffeinate -i <command>` on macOS). Between changes it runs only the test file it touched, and the full suite at each milestone check. It keeps evidence files (screenshots, measurements) in a project folder that no tool cleans.
6. `## Delegation plan`. The roster table (CLI, model, tier, write command, read-only command) copied from `references/roster.md` with commands written out in full, the `perl` time-limit wrapper, and the rules: fast tier for fully specified mechanical work (searches, boilerplate, test runs, bulk edits); reasoning tier for architecture and hard debugging; character graphics, character animation, and motion graphics always go to `codex`; fallback order; if a delegate command fails the builder does the work itself or with its own subagents, and a missing tool never stops the build. Say that the builder's own subagents count as workers too.
7. `## Parallel work`. Name which pieces start together, as a table of work packages with owned files. For every two packages that touch, the prompt gives the interface between them in full: types, function signatures, data shapes. The builder is the slowest lane, so it keeps only the piece that needs the full picture. Tests are a work package once the test seam exists. When a lane is idle and the builder has more than ten minutes of its own work queued, it hands off the most fully specified item. A task the builder can finish in about five minutes stays with it, because briefing a worker costs more than doing it.
8. `## Shared working tree`. `git init` if not a repository; one working tree and one branch (in an existing repository, the branch already checked out, or one new feature branch if that branch is protected); no git worktrees; each worker is given the files it may change; two workers never hold the same file at once; only the builder commits; no `git rebase`; no attribution or co-author lines in commits.
9. `## Briefs`. Every brief stands alone: goal, what done looks like, constraints, files it owns, working directory, what to return. A worker sees nothing except its brief, so each brief carries the owner's rules that apply: no `git rebase`, no worktrees, no attribution lines in commits, nothing published to claude.ai or anywhere else, surgical diffs. Include the brief template from `references/best-practices.md` section D.
10. `## Review`. A different model than the one that wrote the code reviews the integrated product once, after it runs, using a read-only roster command. The builder fixes what is correct. No per-task review. The review brief names the defect classes to look for, taken from the quality bar and from the usual faults of this kind of product, caps the report at ten defects, and asks for file, line, a concrete failing scenario, and a fix for each.
11. `## Verification`. A table with one row per numbered quality bar requirement: the requirement, the exact check (a test with scripted input, a measurement with its threshold, or a named screenshot), and where the result is recorded. A requirement with no runnable check is rewritten until it has one, or given a proxy under step 2. The builder runs the product, runs its tests, and records one line of evidence per row.
12. `## Progress log`. `PROGRESS.md` in the project root. The builder reads it first on starting and resumes from it; it records the start time once, then appends each completed milestone and each decision, each entry stamped with the output of `date`. Working time is counted from these stamps, and time the machine spent asleep is not counted.
13. `## Limits`. The limits table and rules below, copied in.
14. `## Design`, only for a product with a user interface. The wording and the table of Impeccable commands from `references/impeccable.md`, so the builder uses Impeccable and takes its recommendation instead of waiting for a person.
15. `## Trading rules`, only for a product that trades or invests. See below.
16. `## Final report`. Written to `BUILD-REPORT.md` in the project root and repeated as the builder's last message: what was built and how to start it, what was verified (a table with one row per quality bar requirement: requirement, how it was checked, result), what no person verified, the decisions it made, anything it dropped, and the launch checklist (every step that needs the owner: accounts, keys, real payment or ad provider, deployment, store submission).
17. `## Implementation Plan`, last. The components, then ordered milestones, each with a check the builder can run to know it is finished:
    1. a runnable core of the product;
    2. the rest of the quality bar;
    3. the features that bring people back and get it shared;
    4. packaging for the primary channel;
    5. the money path, built behind one interface with a local stand-in for the payment or ad provider, so it works and can be tested without accounts or keys. Connecting the real provider is a launch checklist item. If the money path fails or runs out of time, the product is still delivered.

    The order exists so that time pressure cuts from the bottom. Say so.

### Limits to copy into every prompt

|Limit|Value|
|---|---|
|Workers running at once|6|
|Time for one worker task|20 minutes|
|Retries for a failed task|1, on a different agent|
|Whole build|3 hours|

- A worker's output is unusable if the command exits with an error, returns nothing, or does not contain what its brief asked for.
- Work on the first two milestones (the runnable core and the quality bar) is never dropped. If such a task fails its retry, the builder does it itself.
- Work on later milestones may be dropped when it fails its retry, and is listed in the final report.
- If the build reaches three hours, the builder finishes the milestone it is on, drops the ones after it, and reports. It never reports a product that does not run as finished.

### Trading and investing products

Write these into `## Trading rules`:

- The product never claims a strategy cannot lose, because none can guarantee that.
- The bar is the best risk-adjusted return that can be demonstrated. Strategy selection uses one set of data, and a final holdout that no agent has looked at is used once, at the end. Backtests include fees and slippage.
- The maximum drawdown and the position sizing rule, as the numbers you set in step 3.
- Done means the backtest results plus a paper trading harness that runs. No live trading credentials are wired in. Running the paper period and moving real money are launch checklist items.

## The EGM step

EGM (the Elephant-Goldfish Model) is an installed review plugin whose reviewers each read a document with no other context and catch gaps its author cannot see. Its own skills and staged workflow stop for a person, so do not run them. Use its reviewers directly, once.

**Find EGM.** It is installed as a Claude Code plugin, and its files are readable from any host. Read the `installPath` for `egm@egm`:

```bash
jq -r '.plugins["egm@egm"][0].installPath' ~/.claude/plugins/installed_plugins.json
```

Call that folder `<EGM>`. Persona files are in `<EGM>/agents/`.

**Assignment.** Five reviewers, each on the whole prompt, all started at the same time. Spreading them across agents is the owner's standing rule for EGM runs.

|Reviewer|Persona file|Agent|Saved to|
|---|---|---|---|
|Comprehension|`agents/comprehension.md`|Claude (see "By host")|`promptman/egm/comprehension.md`|
|Zoom-out|`agents/zoom_out.md`|Claude (see "By host")|`promptman/egm/zoom-out.md`|
|Design critic|`agents/design_critic.md`|`codex`, model `gpt-6.1-sol`|`promptman/egm/design-critic.md`|
|Structural|`agents/structural.md`|`agy`, model `"Gemini 4 Neon (High)"`|`promptman/egm/structural.md`|
|Implementation readiness|`agents/implementation_readiness.md`|`copilot`, model `gpt-6.2-astra`|`promptman/egm/implementation-readiness.md`|

**By host.** The two Claude reviewers and the way calls run in parallel are the only steps that differ by host.

- **Claude Code.** Read `<EGM>/docs/claude.md` for how reviewers are dispatched. Run Comprehension on subagent `egm:egm-comprehension` and Zoom-out on `egm:egm-zoom-out`. Start each fresh with the Agent tool (not a fork, not in the background) and pass only the brief. Subagents are read-only, so write each one's returned text to its file yourself, unedited. Dispatch all five in one message: two Agent calls and three Bash calls, each Bash call with a 600000 ms tool timeout.
- **Codex, GitHub Copilot, and any other host.** Run Comprehension and Zoom-out on the `claude` CLI with the Claude command under "CLI commands", so they are CLI reviewers and their brief carries the persona line. Start all five commands so they run at the same time: parallel command calls if the host has them, otherwise one shell call with each command ending in `&` and a final `wait`. Give each call at least ten minutes before the host times it out.

**Reviewer brief.** Send this same template every run. Fill `<PROMPT>` with the absolute path of `prompt.md` and `<PERSONA>` with the absolute persona path.

```text
Mode: REVIEW
Target document: <PROMPT>

[CLI reviewers only] First read your persona file <PERSONA> and follow its
REVIEW instructions and output format. Then review the target document.

What this document is: a prompt that an AI coding agent will follow,
unattended, to build a product. It is not a design document. Its priorities,
in order: (1) a complete, working, high-quality product; (2) built as fast as
possible; (3) positioned to make money, which never delays or blocks the
product. Report whatever in the prompt works against those priorities:
anything that would make the agent stop and ask, build the wrong thing, build
it slowly, fail to verify it, or let money work block the product; anything
ambiguous, contradictory, missing, or impossible to follow as written.

There is no Target Standard file. Use this in its place. The prompt must be
self-contained (no dependence on files the agent may not have) and must
contain: goal and priorities; a product brief with a numbered quality bar;
what done means; the decisions already made; how to decide and when to stop;
a delegation plan with exact commands; which work runs in parallel; shared
working tree rules; a rule that every brief stands alone; review;
verification; a progress log; limits; the final report; and, last,
"## Implementation Plan" with components and ordered milestones that each
have a runnable check. Do not ask for design-document sections such as
alternatives considered, risks, rollout, or open questions. [New project
only] No codebase exists yet, so skip code searches.

This is a read-only review. Do not create or change any file, and do not
write a plan. Your final message is the review itself: for each finding give
Severity (Blocker, Major, or Nit), Affected scope (section heading), the
problem and why it matters, and a suggested fix. If you find nothing, say
"No findings."
```

The **comprehension** reviewer tests whether the prompt stands alone, so it gets a shorter brief: the `Mode` and `Target document` lines, the "What this document is" paragraph, the read-only paragraph, and this sentence: "Read only the target document and your own persona instructions. Open no other file or directory." Leave out the Target Standard paragraph.

**CLI commands.** Run each from `<project>` with the brief in a shell variable, limited to eight minutes:

```bash
cd <project> && BRIEF="$(cat <<'EOF'
<the filled brief>
EOF
)"
# comprehension or zoom-out on claude (hosts other than Claude Code); set <reviewer>
perl -e 'alarm shift; exec @ARGV' 480 claude -p "$BRIEF" --model claude-sonnet-5-5 --permission-mode plan < /dev/null > promptman/egm/<reviewer>.md 2>/dev/null; echo "exit=$?"
# design critic on codex
perl -e 'alarm shift; exec @ARGV' 480 codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check -m gpt-6.1-sol -o promptman/egm/design-critic.md "$BRIEF" < /dev/null > /dev/null 2>&1; echo "exit=$?"
# structural on agy
perl -e 'alarm shift; exec @ARGV' 480 agy -p "$BRIEF" --mode plan --dangerously-skip-permissions --model "Gemini 4 Neon (High)" < /dev/null > promptman/egm/structural.md 2>/dev/null; echo "exit=$?"
# implementation readiness on copilot
perl -e 'alarm shift; exec @ARGV' 480 copilot -p "$BRIEF" --mode plan --yolo -s --no-ask-user --model gpt-6.2-astra < /dev/null > promptman/egm/implementation-readiness.md 2>/dev/null; echo "exit=$?"
```

Each CLI reviewer is its own command call (one command per call, with the `cd` and `BRIEF` lines repeated), so they run in parallel.

**Failures.** A reviewer failed if its command exits non-zero, runs past eight minutes, or its file is empty or holds no review (for example only a note that a plan was saved). Rerun a failed reviewer once on a different agent, with the same brief:

- in Claude Code, a failed CLI reviewer reruns on the matching Claude subagent (`egm:egm-design`, `egm:egm-structural`, or `egm:egm-implementation-readiness`); in any other host it reruns on the `claude` CLI command above, with its output pointed at that reviewer's file;
- a failed Claude reviewer (subagent or CLI) reruns on `codex` with the command above, with the persona line added and `-o` pointed at that reviewer's file.

If the rerun also fails, write "not run" and the reason into that reviewer's file and record it as "not run", so it is never read as "no findings". A run is still done if at least one reviewer completed; if none did, report the prompt as unreviewed, not done.

**Apply the findings once.** Merge the findings across reviewers and remove duplicates. Fix every Blocker and Major that is correct. Fix a Nit when it is correct and cheap. Reject, with a recorded reason:

- findings that ask for design-document sections (alternatives, risks, rollout, open questions);
- findings that are wrong about the prompt or contradict the fixed rules in this skill (the limits, the milestone order, the stop rules);
- findings whose fix would put a lower priority ahead of a higher one.

Where two findings conflict, the one that better serves the priority order wins. A finding that cannot be settled otherwise is a costly decision under the decision policy. Every finding ends with an outcome: fixed, or rejected with the reason. Do not run a second round of review.

## The consolidated report

`promptman/report.md` is the only document the owner reads besides the prompt, so it stands on its own. Use exactly these six `##` headings in this order:

1. `## The prompt`: its absolute path and a short description of the product it will produce.
2. `## Product and quality bar`: the numbered requirements the product will be checked against.
3. `## Money`: customer, price, revenue model, running costs, and channels, with assumptions marked.
4. `## Decisions`: a table with each decision, its reason, who made it (PromptMan, Jev, or Decisions 1.1), and the confidence where a model gave one.
5. `## Review findings`: one table of findings merged across reviewers, most severe first, with columns Severity, Finding, Reviewer, Agent, and Outcome (fixed, or rejected with the reason). No outcome cell is empty. Then a status table with exactly one row for each of the five reviewers (Comprehension, Zoom-out, Design critic, Structural, Implementation readiness): the agent that ran it and whether it completed or was "not run".
6. `## Launch checklist`: the steps that need the owner after the product is built. The prompt ships complete, so nothing here is needed before handing it over.
