"""Optional heuristic pixel diagnostics; never an acceptance gate.

Classifies flat, effect, text and image regions and reports displacement,
ink imbalance and connected differences. Thresholds are illustrative defaults,
not diagnostic to the current project. Shift search never aligns pass evidence.
"""

import collections
import re

from PIL import ImageChops, ImageFilter

PROFILES = {
    'diagnostic': {
        'version': 1,
        'reason': 'Illustrative heuristic thresholds; project calibration and review required. Diagnostic only.',
        'flatRange': 2,           # 5x5 local channel range up to this is "no structure"
        'edgeRange': 24,          # above this is a hard edge; between is soft (effect)
        'imageRadius': 12,        # box-blur radius of the density window (25x25)
        'imageDensity': 0.9,      # share of structured pixels in that window that makes it "image"
        # A pixel may differ by `channelTolerance` levels or by `relativeTolerance` of the local contrast,
        # whichever is larger; `maxChangedFraction` of the type's pixels may exceed that.
        'types': {
            'flat': {'channelTolerance': 1, 'relativeTolerance': 0, 'maxChangedFraction': 0.001},
            'effect': {'channelTolerance': 4, 'relativeTolerance': 0.4, 'maxChangedFraction': 0.01},
            'text': {'channelTolerance': 0, 'relativeTolerance': 0.4, 'maxChangedFraction': 0.05},
            'image': {'channelTolerance': 4, 'relativeTolerance': 0.4, 'maxChangedFraction': 0.01},
        },
        'noise': 16,              # a pixel above this seeds a difference group
        'groupDilate': 7,         # odd; merges the glyphs of a word into one group
        'groupMargin': 2,
        'shiftRadius': 3,
        'displacement': {'maxResidual': 0.6, 'minMass': 1000},
        'ink': {'maxHeavier': 0.30, 'maxLighter': 0.15, 'minDelta': 2500},
        'structural': {'threshold': 64, 'minArea': 64},
    },
}
KINDS = ('flat', 'effect', 'text', 'image')
CODE = {'flat': 0, 'effect': 1, 'text': 2, 'image': 3}


def max_difference(a, b):
    """Per-pixel maximum RGBA channel difference as an L image (same rule as visual_check.compare)."""
    channels = ImageChops.difference(a.convert('RGBA'), b.convert('RGBA')).split()
    diff = channels[0]
    for channel in channels[1:]:
        diff = ImageChops.lighter(diff, channel)
    return diff


def _local_range(image, size=5):
    """Largest per-channel max-min inside a size x size window."""
    result = None
    for channel in image.convert('RGB').split():
        spread = ImageChops.subtract(channel.filter(ImageFilter.MaxFilter(size)),
                                     channel.filter(ImageFilter.MinFilter(size)))
        result = spread if result is None else ImageChops.lighter(result, spread)
    return result


def classify(source, render, profile):
    """L image holding a CODE value per pixel, from the structure of both images."""
    spread = ImageChops.lighter(_local_range(source), _local_range(render))
    flat, edge = profile['flatRange'], profile['edgeRange']
    kinds = spread.point(lambda v: CODE['flat'] if v <= flat else (CODE['effect'] if v <= edge else CODE['text']))
    structured = spread.point(lambda v: 255 if v > flat else 0)
    dense = structured.filter(ImageFilter.BoxBlur(profile['imageRadius'])).point(lambda v: 255 if v >= profile['imageDensity'] * 255 else 0)
    image = ImageChops.darker(dense, structured)  # dense areas, structured pixels only (flat stays flat)
    return ImageChops.add(kinds, image.point(lambda v: CODE['image'] if v else 0)).point(
        lambda v: v if v <= CODE['text'] else CODE['image'])


def components(mask, width, height):
    """8-connected components of a 0/1 mask given as bytes: [(area, left, top, right, bottom)]."""
    parent = []

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    runs, previous = [], []
    pattern = re.compile(rb'\x01+')
    for y in range(height):
        current = []
        for match in pattern.finditer(mask[y * width:(y + 1) * width]):
            index = len(parent)
            parent.append(index)
            current.append((match.start(), match.end() - 1, index))
            runs.append((y, match.start(), match.end() - 1, index))
        for start, end, index in current:
            for prev_start, prev_end, prev_index in previous:
                if prev_end >= start - 1 and prev_start <= end + 1:
                    a, b = find(index), find(prev_index)
                    if a != b:
                        parent[a] = b
        previous = current
    found = {}
    for y, start, end, index in runs:
        root = find(index)
        area = end - start + 1
        box = found.get(root)
        if box is None:
            found[root] = [area, start, y, end, y]
        else:
            box[0] += area
            box[1], box[2] = min(box[1], start), min(box[2], y)
            box[3], box[4] = max(box[3], end), max(box[4], y)
    return [tuple(box) for box in found.values()]


def _mass(diff):
    return sum(i * n for i, n in enumerate(diff.histogram()))


def _shift_search(source, render, box, radius):
    """Mass of the difference inside box when the source is moved by each integer (dx, dy)."""
    width, height = source.size
    left, top, right, bottom = box
    target = render.crop(box)
    masses = {}
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            window = (left + dx, top + dy, right + dx, bottom + dy)
            if window[0] < 0 or window[1] < 0 or window[2] > width or window[3] > height:
                continue
            masses[(dx, dy)] = _mass(max_difference(source.crop(window), target))
    return masses


def _ink(source, render, box):
    """Ink of the window in each image: distance of every channel value from one shared reference colour.

    The reference is the colour that is most common over both windows, so a flat colour drift is not mistaken for
    missing ink and a window dominated by a glyph colour measures the same way in both images.
    """
    first, second = (image.crop(box).convert('RGB').tobytes() for image in (source, render))
    pixels = collections.Counter(zip(first[0::3], first[1::3], first[2::3]))
    pixels.update(zip(second[0::3], second[1::3], second[2::3]))
    reference = pixels.most_common(1)[0][0]
    return tuple(sum(abs(v - reference[c]) for c in range(3) for v in data[c::3]) for data in (first, second))


def _share(kinds, box, code):
    histogram = kinds.crop(box).histogram()
    return histogram[code] / max(1, sum(histogram))


def _groups(diff, profile):
    width, height = diff.size
    mask = diff.point(lambda v: 255 if v > profile['noise'] else 0)
    mask = mask.filter(ImageFilter.MaxFilter(profile['groupDilate'])).point(lambda v: 1 if v else 0)
    margin = profile['groupMargin']
    return [(max(0, left - margin), max(0, top - margin), min(width, right + 1 + margin), min(height, bottom + 1 + margin))
            for _, left, top, right, bottom in components(mask.tobytes(), width, height)]


def evaluate(source, render, profile='diagnostic', regions=None):
    """Apply a profile to two same-size images; returns a JSON-able diagnostic report."""
    spec = PROFILES[profile]
    if source.size != render.size:
        raise ValueError('Profile needs same-size images; nothing is resized')
    source, render = source.convert('RGBA'), render.convert('RGBA')
    diff = max_difference(source, render)
    kinds = classify(source, render, spec)
    for region in regions or []:
        kind = region.get('kind')
        if kind is None:
            continue
        if kind not in KINDS:
            raise ValueError('Region kind must be one of ' + ', '.join(KINDS))
        left, top, right, bottom = region['rect']
        kinds.paste(CODE[kind], (left, top, right, bottom))
    spread = ImageChops.lighter(_local_range(source), _local_range(render))
    failures, types = [], {}
    for kind in KINDS:
        mask = kinds.point(lambda v, c=CODE[kind]: 255 if v == c else 0)
        count = mask.histogram()[255]
        budget = spec['types'][kind]
        # A sub-pixel position change moves edge coverage, not colour, so the allowance scales with the
        # local contrast: low-contrast and high-contrast text are held to the same relative error.
        limit = spread.point(lambda v, b=budget: max(b['channelTolerance'], int(v * b['relativeTolerance'])))
        changed = ImageChops.darker(ImageChops.subtract(diff, limit).point(lambda v: 255 if v else 0), mask).histogram()[255]
        tolerance = f'{budget["channelTolerance"]} levels or {budget["relativeTolerance"]:.0%} of the local contrast'
        fraction = changed / count if count else 0.0
        status = 'pass' if fraction <= budget['maxChangedFraction'] else 'fail'
        types[kind] = {'pixels': count, 'changedPixels': changed, 'changedFraction': fraction, **budget, 'status': status}
        if status == 'fail':
            failures.append(f'{kind}: {changed} of {count} px differ by more than {tolerance} '
                            f'({fraction:.4f} > {budget["maxChangedFraction"]})')
    displaced, imbalanced = [], []
    displacement, ink = spec['displacement'], spec['ink']
    boxes = _groups(diff, spec)
    for box in boxes:
        masses = _shift_search(source, render, box, spec['shiftRadius'])
        unshifted = masses[(0, 0)]
        best = min(masses, key=lambda s: (masses[s], abs(s[0]) + abs(s[1])))
        if best != (0, 0) and unshifted >= displacement['minMass'] and masses[best] <= displacement['maxResidual'] * unshifted:
            displaced.append({'rect': list(box), 'shift': list(best), 'residual': round(masses[best] / unshifted, 3)})
            failures.append(f'displaced {list(box)}: the source matches the render when moved by {best} '
                            f'(residual {masses[best] / unshifted:.2f} of the difference)')
            continue
        if _share(kinds, box, CODE['image']) > 0.5:
            continue  # photos have no single background colour to measure ink against
        ink_source, ink_render = _ink(source, render, box)
        delta = abs(ink_source - ink_render)
        signed = (ink_render - ink_source) / max(ink_source, ink_render, 1)  # +: the render has more ink
        if delta >= ink['minDelta'] and (signed > ink['maxHeavier'] or -signed > ink['maxLighter']):
            imbalanced.append({'rect': list(box), 'source': ink_source, 'render': ink_render, 'balance': round(signed, 3)})
            failures.append(f'ink {list(box)}: {"more" if signed > 0 else "less"} ink in the render '
                            f'({ink_render} vs {ink_source}): a missing, extra, heavier or lighter element')
    structural = spec['structural']
    strong = diff.point(lambda v: 1 if v > structural['threshold'] else 0)
    blobs = [{'rect': [left, top, right + 1, bottom + 1], 'area': area}
             for area, left, top, right, bottom in components(strong.tobytes(), *diff.size)
             if area >= structural['minArea']]
    for blob in blobs:
        failures.append(f'blob {blob["rect"]}: {blob["area"]} connected px differ by more than {structural["threshold"]}/255')
    return {'profile': profile, 'version': spec['version'], 'diagnostic': True,
            'status': 'fail' if failures else 'pass', 'types': types,
            'groups': len(boxes), 'displaced': displaced, 'inkImbalance': imbalanced, 'structuralBlobs': blobs,
            'failures': failures}
