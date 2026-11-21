# Model roster

Every command below returned output from a live call on 2026-11-20 (macOS, zsh). Re-verify with a trivial call before trusting a row after a CLI update.

## How to read the commands

- `<brief>` is the path of a brief file. Every command runs from the project directory, so workers write there.
- Read-only and write forms differ by a flag where the CLI has one, and by instruction where it does not. A read-only brief always says "do not create or change any file; reply with your result as your final message."
- `< /dev/null` stops a CLI from waiting on standard input.
- `agy` and `copilot` are shell functions in `~/.zshenv` that add `--dangerously-skip-permissions` and `--yolo`. The flags are written out here so the commands work from any shell. `command` skips the function.
- macOS has no `timeout`. Put this in front of any command to limit it:

```bash
perl -e 'alarm shift; exec @ARGV' <seconds> <command...>
```

  Example, a 20-minute build task: `perl -e 'alarm shift; exec @ARGV' 1200 codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check -m gpt-6.2-sol "$(cat <brief>)" < /dev/null`

## Roster

Cost and speed are relative: low, medium, high.

|CLI|Model ID|Tier|Cost|Speed|Review (read-only)|Build (may write files)|
|---|---|---|---|---|---|---|
|`claude`|`claude-haiku-5-5`|fast|low|high|`claude -p "$(cat <brief>)" --model claude-haiku-5-5 --permission-mode plan < /dev/null`|`claude -p "$(cat <brief>)" --model claude-haiku-5-5 --dangerously-skip-permissions < /dev/null`|
|`claude`|`claude-sonnet-5-5`|fast|medium|medium|`claude -p "$(cat <brief>)" --model claude-sonnet-5-5 --permission-mode plan < /dev/null`|`claude -p "$(cat <brief>)" --model claude-sonnet-5-5 --dangerously-skip-permissions < /dev/null`|
|`claude`|`claude-opus-5-5`|reasoning|high|medium|`claude -p "$(cat <brief>)" --model claude-opus-5-5 --permission-mode plan < /dev/null`|`claude -p "$(cat <brief>)" --model claude-opus-5-5 --dangerously-skip-permissions < /dev/null`|
|`claude`|`claude-fable-5-2`|reasoning (**strongest reasoner**)|high|low|`claude -p "$(cat <brief>)" --model claude-fable-5-2 --permission-mode plan < /dev/null`|`claude -p "$(cat <brief>)" --model claude-fable-5-2 --dangerously-skip-permissions < /dev/null`|
|`codex`|`gpt-6.2-sol`|fast|low|high|`codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check -m gpt-6.2-sol -o <out-file> "$(cat <brief>)" < /dev/null`|`codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check -m gpt-6.2-sol "$(cat <brief>)" < /dev/null`|
|`codex`|`gpt-6.1-sol`|reasoning|medium|medium|`codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check -m gpt-6.1-sol -o <out-file> "$(cat <brief>)" < /dev/null`|`codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check -m gpt-6.1-sol "$(cat <brief>)" < /dev/null`|
|`codex`|`gpt-6.2-astra`|reasoning|high|low|`codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check -m gpt-6.2-astra -o <out-file> "$(cat <brief>)" < /dev/null`|`codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check -m gpt-6.2-astra "$(cat <brief>)" < /dev/null`|
|`agy`|`"Gemini 3.8 Flash (Low)"`|fast|low|high|`command agy -p "$(cat <brief>)" --mode plan --dangerously-skip-permissions --model "Gemini 3.8 Flash (Low)" < /dev/null`|`command agy -p "$(cat <brief>)" --dangerously-skip-permissions --model "Gemini 3.8 Flash (Low)" < /dev/null`|
|`agy`|`"Gemini 4 Neon (High)"`|reasoning|medium|medium|`command agy -p "$(cat <brief>)" --mode plan --dangerously-skip-permissions --model "Gemini 4 Neon (High)" < /dev/null`|`command agy -p "$(cat <brief>)" --dangerously-skip-permissions --model "Gemini 4 Neon (High)" < /dev/null`|
|`copilot`|`claude-sonnet-5.5`|fast|medium|medium|`command copilot -p "$(cat <brief>)" --mode plan --yolo -s --no-ask-user --model claude-sonnet-5.5 < /dev/null`|`command copilot -p "$(cat <brief>)" --yolo -s --no-ask-user --model claude-sonnet-5.5 < /dev/null`|
|`copilot`|`gpt-6.2-astra`|reasoning|high|low|`command copilot -p "$(cat <brief>)" --mode plan --yolo -s --no-ask-user --model gpt-6.2-astra < /dev/null`|`command copilot -p "$(cat <brief>)" --yolo -s --no-ask-user --model gpt-6.2-astra < /dev/null`|

Notes on the verified forms:

- `codex exec` prints a long log. `-o <out-file>` saves only the final message; use it whenever the reply is the deliverable. Codex has no plan flag in the form `~/AGENTS.md` prescribes, so its read-only form is read-only by instruction.
- `agy --model` takes the display name in quotes. An unknown name prints the full list, as does `command agy models`.
- `copilot` uses dots in Claude model IDs (`claude-sonnet-5.5`); `claude` uses hyphens (`claude-sonnet-5-5`). `-s` prints only the reply.
- `agy` occasionally fails with "backend returned an empty conversation id". That is transient; it counts as a failed call under the retry rule.

## Standing rules

- **Character graphics, character animation, and motion graphics always go to `codex`** (owner's standing rule). Use `gpt-6.1-sol` unless the task is trivial.
- **Fast tier** takes work that is fully specified and mechanical: searches, boilerplate, test runs, bulk edits.
- **Reasoning tier** takes architecture and hard debugging.
- **Strongest reasoner:** `claude-fable-5-2`. Use it for the hardest single problem in a build, not as a default.
- **Fallback order** when a command fails: the same tier on the next CLI in the order `claude` → `codex` → `agy` → `copilot`. If every CLI fails, the agent does the work itself or with its own subagents. A missing tool never stops a build.

## Dropped (failed a live call)

|What|Result|Restore|
|---|---|---|
|`grok` (xAI), all models|`Error: Not signed in` on `grok -p`|Run `grok login`, then verify `grok -p "<brief>" --permission-mode plan` (read-only) and `grok -p "<brief>" --always-approve` (write); `grok models` lists `grok-4.6` (default) and `grok-4.5`|
|`agy --mode auto`|Listed by `agy --help`, but prints `warning: --mode auto is not available for this account; continuing in the default mode.`|Not needed: the build form already runs in the default mode. Leave `--mode` out of write commands|
|`copilot --model gpt-6.2-sol` for review|In `--mode plan` it saves a plan instead of replying|Usable for build work only; not listed|
|`copilot --model` with `claude-sonnet-5-5`, `claude-haiku-5-5`, `claude-opus-5-5`, `claude-fable-5-2`, `gpt-5.6-sol`, `gemini-3.8-flash`|`Model "<name>" is not available`|Use the dotted IDs in the roster|

## Build history

One row per finished build. Add a row after each build, so this table stays current. Step 3 sizes scope from it: the limits are ceilings, and these are what builds have actually taken.

|Date|Product|Kind|Milestones done|Worker tasks|Working time|
|---|---|---|---|---|---|
|2026-11-20|bin-there-done-that|Browser game|5 of 5|9 plus 1 review|54 minutes|

## Jev (TypeSafe classifier)

Jev returns typed answers with a confidence and generates no text. Each question is specific and carries its own options. Context goes in `state`; several questions can share one request. Run the whole block in one shell call (shell state does not carry between calls) and build the JSON with `jq` so quotes in the context cannot break it.

```bash
source "${PROMPTMAN_TYPESAFE_ENV:-$HOME/.config/typesafe/env}"   # sets TYPESAFE_API_KEY; never print, log, or commit it
jq -n --arg state "$CONTEXT" '{model:"jev-latest", state:$state, questions:{
  stack:{type:"choice", instructions:"Which stack fits best?",
         criteria:{web:"TypeScript web game", native:"Native desktop app"}},
  needs_backend:{type:"noul", instructions:"Does this product need a server?"},
  scope_fit:{type:"score", instructions:"How well does this scope fit a three-hour build?",
             criteria:["Far too large","Somewhat too large","Fits"]}}}' |
curl -sS -m 20 https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" -d @-
```

Verified response shape: `{"model":"jev-1.14.0","answers":{"stack":{"type":"choice","choice":"web","confidence":1.0,...},"needs_backend":{"type":"noul","noul":0.15},"scope_fit":{"type":"score","score":2.0,"confidence":1.0,...}},"usage":{...}}`

|Type|Read|Accept when|
|---|---|---|
|`choice`|`answers.<key>.choice`, `.confidence`|confidence is 0.7 or higher|
|`noul` (yes/no)|`answers.<key>.noul`, the probability of yes|0.7 or higher is yes; 0.3 or lower is no|
|`score`|`answers.<key>.score` (index into `criteria`, from 0), `.confidence`|confidence is 0.7 or higher|

Anything outside those ranges is not confident. On a timeout or HTTP error, retry once, then move to Decisions 1.1. If the key file is missing (`source` fails), move to Decisions 1.1 straight away without calling the API. Reference: https://docs.typesafe.ai/llms.txt

## Decisions 1.1

**Status: unavailable.** Copilot has no command that lists models, and on 2026-11-20 `copilot --model` rejected every name tried: `decisions-1.1`, `decisions-1-1`, `Decisions 1.1`, `Decisions-1.1`, `decisions1.1`, `decisions-1.1-preview`, `decisions` (all "Model ... is not available") and `microsoft/decisions-1.1` ("Provider model ... is not registered").

The decision policy therefore skips this tier: when Jev is not confident, errors, or the decision is open-ended, PromptMan decides and records "PromptMan (Decisions 1.1 unavailable)" as who made it.

If a working model ID is found later, this is the command shape (verified with another Copilot model), limited to two minutes:

```bash
perl -e 'alarm shift; exec @ARGV' 120 command copilot -p "$(cat <decision-brief>)" \
  --mode plan --yolo -s --no-ask-user --model <decisions-model-id> < /dev/null
```

The decision brief gives the context, the options considered, and what the decision affects, and ends with: "Pick one option. Reply as `PICK: <option> — <one-line reason>` and write nothing else."
