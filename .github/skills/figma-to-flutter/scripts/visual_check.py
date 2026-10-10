"""Compare source/render pixels without resizing, alignment or ignore masks.

Pillow required. Exit 0: pixel pass; 1: mismatch; 2: invalid input. Defaults
are zero-budget. Explicit manifest budgets change the metric, never human
approval. --profile diagnostic adds heuristics without changing the verdict.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageChops

import pixel_policy


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rectangle(value, size):
    if not isinstance(value, list) or len(value) != 4 or any(type(x) is not int for x in value):
        raise ValueError('Rectangle must contain four integer pixel coordinates')
    left, top, right, bottom = value
    if not (0 <= left < right <= size[0] and 0 <= top < bottom <= size[1]):
        raise ValueError('Rectangle must be nonempty and inside the image')
    return tuple(value)


def budget(spec, default=None):
    default = default or {}
    tolerance = spec.get('channelTolerance', default.get('channelTolerance', 0))
    fraction = spec.get('maxChangedFraction', default.get('maxChangedFraction', 0))
    if type(tolerance) is not int or not 0 <= tolerance <= 255:
        raise ValueError('channelTolerance must be an integer from 0 to 255')
    if type(fraction) not in (int, float) or not math.isfinite(fraction) or not 0 <= fraction <= 1:
        raise ValueError('maxChangedFraction must be finite and from 0 to 1')
    if (tolerance or fraction) and not (spec.get('budgetReason') or default.get('budgetReason')):
        raise ValueError('Nonzero pixel budgets require budgetReason')
    return tolerance, fraction


def metrics(diff, spec, default=None):
    tolerance, limit = budget(spec, default)
    histogram = diff.histogram()
    count = diff.width * diff.height
    changed = sum(histogram[tolerance + 1:])
    return {'status': 'pass' if changed / count <= limit else 'fail',
            'changedPixels': changed, 'pixels': count, 'changedFraction': changed / count,
            'meanMaxChannelDifference': sum(i * n for i, n in enumerate(histogram)) / count,
            'channelTolerance': tolerance, 'maxChangedFraction': limit}


def compare(source_path, render_path, manifest=None, output=None, profile=None):
    spec = {} if manifest is None else manifest
    if not isinstance(spec, dict):
        raise ValueError('Manifest must be a JSON object')
    regions = spec.get('regions', [])
    if not isinstance(regions, list) or any(not isinstance(region, dict) for region in regions):
        raise ValueError('Manifest regions must be an array of objects')
    if profile is not None and profile not in pixel_policy.PROFILES:
        raise ValueError('Unknown profile: ' + str(profile))
    allowed = {'sourceCrop', 'renderCrop', 'cropReason', 'channelTolerance',
               'maxChangedFraction', 'budgetReason', 'regions', 'provenance'}
    if set(spec) - allowed:
        raise ValueError('Unsupported manifest keys (no masks or automatic alignment): ' +
                         ', '.join(sorted(set(spec) - allowed)))
    budget(spec)
    source = Image.open(source_path).convert('RGBA')
    render = Image.open(render_path).convert('RGBA')
    result = {'pixelStatus': 'fail', 'humanApproval': 'unchecked',
              'sourceSha256': sha256(source_path), 'renderSha256': sha256(render_path),
              'sourceOriginalSize': list(source.size), 'renderOriginalSize': list(render.size),
              'manifest': spec, 'regions': {}}
    for key, im in [('sourceCrop', source), ('renderCrop', render)]:
        if key in spec:
            if not spec.get('cropReason'):
                raise ValueError('Recorded frame crops require cropReason')
            cropped = im.crop(rectangle(spec[key], im.size))
            if key == 'sourceCrop':
                source = cropped
            else:
                render = cropped
    result.update(sourceComparedSize=list(source.size), renderComparedSize=list(render.size))
    if source.size != render.size:
        result['reason'] = 'Frame geometry differs; images were not resized'
    else:
        channels = ImageChops.difference(source, render).split()
        diff = channels[0]
        for channel in channels[1:]:
            diff = ImageChops.lighter(diff, channel)
        result['wholeFrame'] = metrics(diff, spec)
        for region in regions:
            if set(region) - {'name', 'rect', 'channelTolerance', 'maxChangedFraction', 'budgetReason', 'kind'}:
                raise ValueError('Unsupported region keys')
            name = region.get('name')
            if not isinstance(name, str) or not name.strip() or name in result['regions']:
                raise ValueError('Regions require unique nonempty names')
            if 'kind' in region and region['kind'] not in pixel_policy.KINDS:
                raise ValueError('Region kind must be one of ' + ', '.join(pixel_policy.KINDS))
            box = rectangle(region.get('rect'), source.size)
            result['regions'][name] = metrics(diff.crop(box), region, spec)
        checks = [result['wholeFrame'], *result['regions'].values()]
        result['pixelStatus'] = 'pass' if all(x['status'] == 'pass' for x in checks) else 'fail'
        if profile:
            result['profile'] = pixel_policy.evaluate(source, render, profile, regions)
        if output:
            directory = Path(output)
            directory.mkdir(parents=True, exist_ok=True)
            # Include alpha differences in the heatmap; composite overlay on black.
            Image.merge('RGB', (diff, Image.new('L', diff.size), Image.new('L', diff.size))).save(directory / 'difference.png')
            background = Image.new('RGBA', source.size, 'black')
            Image.blend(Image.alpha_composite(background, source),
                        Image.alpha_composite(background, render), .5).convert('RGB').save(directory / 'overlay.png')
    if output:
        directory = Path(output)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'pixels.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('render', type=Path)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--profile', choices=sorted(pixel_policy.PROFILES),
                        help='also record the optional diagnostic result; the exit code follows the explicit manifest, zero-budget by default')
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text()) if args.manifest else {}
        if not isinstance(manifest, dict):
            raise ValueError('Manifest must be a JSON object')
        result = compare(args.source, args.render, manifest, args.output, args.profile)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, str(error) + '\n')
    summary = {'pixelStatus': result['pixelStatus'], 'humanApproval': 'unchecked',
               'report': str(args.output / 'pixels.json')}
    if 'profile' in result:
        summary['profile'] = {'name': result['profile']['profile'], 'status': result['profile']['status'],
                              'diagnostic': True, 'failures': len(result['profile']['failures'])}
    print(json.dumps(summary))
    raise SystemExit(0 if result['pixelStatus'] == 'pass' else 1)


if __name__ == '__main__':
    main()
