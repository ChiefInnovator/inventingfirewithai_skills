# Capture and identity

## Preconditions

Discover the current runner's Figma tools and their schemas. Follow any installed provider prerequisite such as `figma-design-to-code` before design-context calls, and `figma-use` before document scripting. Use the provider's supported connection and authentication flow; an enabled connector is not proof of access to the selected file. Do not install a second connection or change global settings when an existing one works.

Use the repository's Flutter SDK pin and dependency lockfiles. Record the actual SDK and rendering platform; do not upgrade shared tooling as a side effect of conversion. Native checks need the corresponding SDK and simulator/device. Resolve LFS pointers to real asset bytes before rendering. Keep missing authentication or tooling distinct from a design mismatch.

## Resolve the requested source

Run the bundled read-only URL resolver from the skill folder:

```sh
python3 scripts/input_url.py 'https://www.figma.com/design/ExampleFile/Example?node-id=1-2' --ledger /path/to/project/design/ledger.json
```

Omit `--ledger` for a new collection. Examples use synthetic identifiers. The resolver supports design, legacy file, prototype, branch, and nested-instance links. A file-wide link needs frame selection; inspect actual pages instead of guessing a page ID. A nested component does not become a full screen unless the request and metadata support that scope.

Match `(effective fileKey, nodeId)`, preserving parent-file and branch URLs. Same node IDs in different files are different sources. Names are labels; a rename must not change identity or erase another file's entries.

## Capture enough to reproduce the frame

1. Read design context for the exact frame using the available tool's Flutter/Dart options. Obtain its full-frame screenshot and variable definitions. Tool-generated web code is evidence about layout, not production Flutter.
2. Compare context coverage with metadata and the screenshot. Read omitted or truncated visible subtrees. Save actual tool results with call/file/node/time provenance; never manufacture a complete snapshot from inferred values.
3. Where supported, capture read-only node geometry and properties: local and absolute bounds, transforms, constraints, Auto Layout, padding, stroke placement, masks, clipping, paint order, typography, styled runs, and resolved variables. Load required tool-specific guidance first. If the provider cannot expose a needed property, record the missing evidence.
4. Download the exact provided image/vector bytes. Preserve asset references and local paths; temporary URLs are not durable Flutter assets. Do not substitute unrelated stock images or font glyphs for icons.
5. Verify screenshot dimensions against frame and render bounds. External shadows can exceed frame bounds. Obtain an unscaled export when the tool clamps large screenshots. A crop must follow recorded frame bounds and scale, not a visually chosen region that hides differences.
6. Save complete captures into a new capture-ID directory. Use a staging directory and finalize only after required files and provenance are present. Never overwrite a previous capture or attach a fresh timestamp to old pixels.

Record supplied URL, effective file/node, original names, capture time, dimensions/scale, source mode, required fonts, asset mapping, and missing fields. Hash saved evidence before comparison. Store credentials only through the runner's supported authentication mechanism, never in captures.

For Codex, save the actual current tool-result blocks and downloaded resources. For Claude Code, use the current client's documented result mechanism. Do not search another client's transcripts or assume a transcript format. If outputs truncate, use supported result retrieval or smaller node scopes; report incomplete capture if it cannot be recovered.

Respect provider rate limits and retry guidance. Serial calls are a safe default. Do not launch multiple capture agents merely to bypass a shared account limit.
