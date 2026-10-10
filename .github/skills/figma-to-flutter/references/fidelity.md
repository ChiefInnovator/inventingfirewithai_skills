# Source-to-render fidelity

## Independent evidence

Keep Figma source captures immutable and render the actual Dart independently. Record source and render hashes, file/node/capture identity, frame and render bounds, crop/scale, SDK/version, target device/platform, fonts, and the implementation revision. A generated golden is only a render snapshot. Never copy or re-encode the source image as the implementation render.

Use real source fonts and weights, not fallback test fonts. Hash fonts, assets, canonical widgets, relevant shared dependencies, runner configuration, and lockfiles with the evidence. Changes to these inputs invalidate prior visual results. Capture date and render date are different facts.

## Compare

From the installed skill folder:

```sh
python3 scripts/visual_check.py /tmp/source.png /tmp/flutter.png --output /tmp/comparison
```

The default compares RGBA pixels exactly. It never stretches or aligns images and rejects geometry mismatch. It produces `pixels.json`, a difference image, and an overlay for equal-size frames. Exit 0 means pixel agreement under the declared manifest, 1 means mismatch, and 2 means invalid input. Human approval remains unchecked.

For critical controls, supply `--manifest /tmp/regions.json`:

```json
{
  "regions": [
    {"name": "primary-action", "rect": [20, 100, 180, 148]},
    {"name": "navigation", "rect": [0, 160, 200, 200]}
  ]
}
```

Rectangles are `[left, top, right, bottom]` in compared pixels; derive actual values from the source. Whole-frame averages must not conceal a missing small control. Source/render crops require a documented `cropReason` and measured frame bounds. No ignore masks.

Explicit `channelTolerance` or `maxChangedFraction` budgets require `budgetReason`. Adopt budgets only when the project's acceptance policy supports them, before judging the implementation. Report their values and never call a budgeted pass pixel-identical. Do not increase a budget to make a failing screen pass.

`--profile diagnostic` additionally classifies differences and looks for displacement, ink imbalance, and structural blobs. Its thresholds are illustrative, not calibrated to a new project. It does not change the manifest's pixel verdict or confer acceptance. A heuristic pass cannot dismiss a visible defect.

## Repair and acceptance

Inspect the full side-by-side source/render and difference image. Tie each meaningful mismatch to its source node; fix measured layout, font, paint, or asset causes. Rerender after each actual repair. Track changed-pixel fraction and remaining differences. Stop at the entrypoint's round limits or a real blocker; unresolved differences stay visible in the report.

Use an independent reviewer when the project's acceptance process requires it. Record the actual reviewer, reviewed artifacts, decision, and time; never invent approval. The comparison tool checks pixels, not render authenticity, semantic correctness, or user experience.

Track these separately:

- Analyzer and widget/layout tests.
- Source coverage and remaining TODOs.
- Pixel comparison under its recorded policy.
- Human visual review.
- Web, Android, and iOS build/launch/render results for the requested targets.
- Production integration and behavior/accessibility acceptance, when in scope.

A web render does not prove native fidelity. A native build does not prove a screen was opened. A reference widget does not prove production adoption. If a toolchain or reviewer is unavailable, record that layer as unchecked and finish the independent checks that can run.

The package supplies a pixel checker, not an automated project-wide promotion validator. Review all required evidence before updating a ledger to accepted; do not treat a JSON status field as proof.
