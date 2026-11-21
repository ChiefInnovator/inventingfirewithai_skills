# Impeccable in the build prompt

Impeccable is the owner's installed design skill for user interfaces. It sets a visual direction, writes `PRODUCT.md` and `DESIGN.md`, and reviews and refines rendered screens. Read this when the product has a user interface, and write the result into the prompt's `## Design` section.

## When the prompt uses it

Use it for every surface a person looks at and operates: web pages and apps, landing and store pages, dashboards, forms, settings, onboarding, empty states, native iOS and Android screens, and a game's menus, HUD, and overlays.

Leave the section out for a product with no interface (a library, a command-line tool, a service, a trading engine with no screen). Impeccable does not cover game-world art, character graphics, character animation, or motion graphics; those still go to `codex`.

## Where it goes in the build

Pick only the rows this product needs. Write them into `## Design` as a table of command, target surface, milestone, and result, and name the same steps in the milestone they belong to in `## Implementation Plan`.

|Milestone|Command|Use it for|
|---|---|---|
|1, before any interface code|`init`|`PRODUCT.md`, written from the prompt's product brief|
|1, before any interface code|a plain request to design the primary surface|The visual direction and `DESIGN.md`|
|2|`onboard <target>`|First-run flow and empty states, when the quality bar has them|
|2|`harden <target>`|Error states, long text, edge cases|
|2|`adapt <target>`|Other screen sizes, when the product ships on more than one|
|2|`animate <target>` or `delight <target>`|Motion or personality, only when a quality bar requirement names it|
|2, last|`critique <target>`, then `audit <target>`|Design and technical review of each main surface; the builder fixes what is correct|
|3 or 4|a plain request to design the landing or store page|The page that sells the product, when the primary channel needs one|
|4, before final verification|`polish <target>`|The last pass over every surface|

Keep these out of every prompt, because each one stops for a person: `shape` (an interview), `live` and `generate` (a person picks in a browser), and Impeccable with no command (it only shows a menu).

For an existing product that already has a `DESIGN.md`, the design is settled: drop the `init` and direction rows and use only the refinement and review rows, unless the idea asks for a redesign.

## Wording for the prompt

Put this in `## Design`, in these words or close to them, above the table:

```text
Design work uses the Impeccable skill. Invoke it as `/impeccable <command>
<target>` (Claude Code, GitHub Copilot) or `$impeccable <command> <target>`
(Codex), always with a command or a specific design request from the table
below.

Nobody is available to answer Impeccable. The owner has answered every
question it would ask in advance, and the answer is always "use your
recommendation". Treat that as an answer already received:

- Do not call a question tool, and do not open or wait on Impeccable's
  decision page. Where its instructions say to ask and wait, apply its
  recommendation and continue.
- Product questions are answered by the product brief and the decisions in
  this prompt. Write PRODUCT.md from them and label anything you inferred.
- Stack and platform are settled in "Decisions already made".
- Build path: take the path Impeccable names for the surface (comp-first for
  a landing page or showcase when image generation is available, code-first
  for an app screen or document). Do not store it as a default.
- Direction: build the direction Impeccable leads with, at full commitment.
  Do not re-roll for taste and do not take the conventional alternative.
- Review: at most two critique-and-fix rounds per surface. Then record what
  is still open and move on.

The art direction in "Decisions already made" is the brief. Impeccable
honors what it pins and decides what it leaves open.

Record each choice Impeccable made in one line in the progress log, and list
them in the final report under what no person verified.

Workers do not run Impeccable. You run it, and you put DESIGN.md and the
tokens a task needs into the brief of every worker that writes interface
code.

If Impeccable is not installed, or its launcher fails, do not stop. Build to
the art direction in this prompt and record that Impeccable did not run.
```
