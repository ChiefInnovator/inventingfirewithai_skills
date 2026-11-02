# Portable draft compiler

`scripts/convert.py` is an independent Python implementation that turns enriched Figma node JSON into a scratch Flutter widget. It does not invoke Figma, parse arbitrary React/Tailwind as node JSON, or import an application's private theme. Apply [mapping.md](mapping.md) during reviewed canonical adoption.

From this skill's directory:

```sh
python3 scripts/convert.py /tmp/frame.json \
  --repo-root /path/to/project --file-key ExampleFile --node-id 1:2 \
  --assets /tmp/assets.json --variables /tmp/variables.json \
  --class-name ExampleDraft --output /tmp/example-draft
```

Use a fresh output directory outside the target repository. The explicit `--repo-root` works for both repository-local and globally installed skill folders; it is never inferred from the skill's parent directories. Existing nonempty output is refused.

Inputs:

- A single node, a `document` wrapper, or a REST `nodes` response. `--node-id` is required for the last form.
- Optional asset map: `{"1:3": "assets/icon.svg", "example-image-ref": "assets/photo.png"}`. Values identify local bundled assets; the compiler references but does not download or copy them.
- Optional variable map: `{"VariableID:example": "Palette/Accent"}`. This preserves variable names in review warnings; it does not silently bind application tokens.

Outputs are `draft.dart`, `normalized.json`, and `report.json`. The report retains source identity, node trace, asset map, required font families/weights/styles, warnings, and unchecked visual approval. Literal draft tokens preserve captured color values without an application dependency. Resolve them to verified project tokens during adoption.

Implemented mechanics include fixed/hug/fill sizing, bounded flex, wrapping, flow plus absolute positioning, transforms, constraints, visibility, clipping, gradients, borders, rich text, and local image/SVG references. Multiple paints, masks, custom vectors/effects, certain text features, and incomplete metadata can remain approximations. Read the warnings; successful emission is not proof of complete or correct rendering.

The compiler preserves background/foreground overlay order and bounded flow alignment, counts included stroke padding once, paints borders in front, converts layer/background blur radius to Gaussian sigma, and reviews centered hugging text with trailing spaces. Interleaved flow overlays, dashed paths, and unresolved Material line heights retain explicit warnings. Project component mappings and richer provider export envelopes require reviewed adapters; none are inferred from a previous application.

Install Pillow from `requirements.txt` in an isolated environment to use visual checks. Compiler and URL tests require only Python's standard library. Run the bundled regression suite from this skill's directory:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/test_flutter.py --flutter flutter
```

The optional Flutter smoke test creates an isolated temporary package, resolves its Flutter dependencies, analyzes generated widgets, and runs layout checks. It needs an installed compatible Flutter SDK and package access. It uses synthetic geometry and default fonts, so it does not prove source-font or real-screen fidelity. It leaves the target application untouched.

The standard-library [run metrics helper](performance.md#whole-run-timing) is also bundled. Font acquisition/preflight integration, live capture scheduling, render caching, hosted browser checks, and explorer generation remain target-project workflows, not preinstalled adapters. Run tests with the same dependency-compatible Python environment used for image checks.

## Public conversion reference

The community [Figma to Code plugin](https://www.figma.com/community/plugin/842128343887142055) and its [official repository](https://github.com/bernaferrari/FigmaToCode) are useful references for read/normalize/layout/generate architecture and target limitations. The repository catalog also links a comparison explaining why this skill adds project integration and acceptance checks. This package does not vendor the plugin's implementation or require its installation.

For an upstream review, inspect an exact public revision and relevant source/tests. Record the revision, findings, affected rules, and regression evidence in the project's chosen maintenance record. Do not carry another project's reviewed SHA, private decisions, scheduled job, or acceptance results into a new installation. A fetched commit is not a completed review.
