"""Synthetic image regressions for heuristic diagnostics and strict comparison."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import pixel_policy
from visual_check import compare

SIZE = (220, 150)
BACKGROUND = (15, 15, 15, 255)
SCALE = 4


def font(size=14):
    return ImageFont.load_default(size=size * SCALE)


def screen(offset=(0, 0), shift_second=0, stroke=0, icon=True, background=BACKGROUND):
    """Dark screen with two text lines, a ring icon and a card; offset is in 1/4 px steps of the text only."""
    big = Image.new('RGBA', (SIZE[0] * SCALE, SIZE[1] * SCALE), background)
    draw = ImageDraw.Draw(big)
    ink = (242, 240, 234, 255)
    draw.text((12 * SCALE + offset[0], 12 * SCALE + offset[1]), 'Example information', font=font(), fill=ink, stroke_width=stroke, stroke_fill=ink)
    draw.text((12 * SCALE + shift_second * SCALE, 40 * SCALE), 'Open sample details', font=font(), fill=ink, stroke_width=stroke, stroke_fill=ink)
    image = big.resize(SIZE, Image.BOX)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((12, 70, 208, 138), radius=10, fill=(42, 40, 40, 255))
    if icon:
        draw.ellipse((24, 82, 52, 110), outline=(40, 140, 230, 255), width=4)
        draw.line((34, 96, 42, 96), fill=(40, 140, 230, 255), width=3)
    return image


def verdict(source, render, **kwargs):
    return pixel_policy.evaluate(source, render, **kwargs)


class FloorTests(unittest.TestCase):
    def test_identical_images_pass(self):
        report = verdict(screen(), screen())
        self.assertEqual(report['status'], 'pass', report['failures'])
        self.assertTrue(report['diagnostic'])

    def test_quarter_pixel_text_offset_is_rasterization_and_passes(self):
        report = verdict(screen(), screen(offset=(1, 0)))
        self.assertEqual(report['status'], 'pass', report['failures'])

    def test_one_level_flat_rounding_passes(self):
        report = verdict(screen(), screen(background=(16, 16, 16, 255)))
        self.assertNotEqual(report['types']['flat']['status'], 'fail', report['failures'])


class StructuralDefectTests(unittest.TestCase):
    def test_whole_pixel_shift_is_reported_as_displacement_with_its_vector(self):
        report = verdict(screen(), screen(offset=(0, SCALE)))
        self.assertEqual(report['status'], 'fail')
        self.assertTrue(report['displaced'])
        self.assertEqual({tuple(group['shift']) for group in report['displaced']}, {(0, -1)})

    def test_one_moved_word_is_displaced_even_when_the_rest_matches(self):
        report = verdict(screen(), screen(shift_second=2))
        self.assertTrue(any(group['shift'] == [-2, 0] or group['shift'] == [2, 0] for group in report['displaced']), report['failures'])

    def test_flat_colour_drift_fails_although_every_pixel_is_within_16(self):
        report = verdict(screen(), screen(background=(26, 26, 26, 255)))
        self.assertEqual(report['types']['flat']['status'], 'fail')
        self.assertGreater(report['types']['flat']['changedFraction'], .5)

    def test_missing_icon_fails_by_ink(self):
        report = verdict(screen(), screen(icon=False))
        self.assertEqual(report['status'], 'fail')
        self.assertTrue(report['inkImbalance'] or report['structuralBlobs'], report['failures'])
        self.assertTrue(any(group['balance'] < 0 for group in report['inkImbalance']), report['inkImbalance'])

    def test_heavier_text_fails_by_ink(self):
        report = verdict(screen(), screen(stroke=2))
        self.assertTrue(any(group['balance'] > pixel_policy.PROFILES['diagnostic']['ink']['maxHeavier']
                            for group in report['inkImbalance']), report['failures'])

    def test_signature_differs_between_rasterization_and_defects(self):
        floor = verdict(screen(), screen(offset=(1, 0)))
        shifted = verdict(screen(), screen(offset=(0, SCALE)))
        self.assertEqual((len(floor['displaced']), len(floor['structuralBlobs'])), (0, 0))
        self.assertGreater(len(shifted['displaced']), 0)


class RegionKindTests(unittest.TestCase):
    def test_region_kind_overrides_the_detected_type(self):
        source, render = screen(), screen(background=(17, 17, 17, 255))
        forced = verdict(source, render, regions=[{'name': 'all', 'rect': [0, 0, SIZE[0], SIZE[1]], 'kind': 'effect'}])
        self.assertEqual(forced['types']['flat']['pixels'], 0)
        self.assertEqual(forced['types']['effect']['pixels'], SIZE[0] * SIZE[1])

    def test_unknown_kind_and_profile_and_size_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'kind'):
            verdict(screen(), screen(), regions=[{'rect': [0, 0, 10, 10], 'kind': 'photo'}])
        with self.assertRaises(KeyError):
            verdict(screen(), screen(), profile='lenient')
        with self.assertRaisesRegex(ValueError, 'same-size'):
            verdict(screen(), Image.new('RGBA', (10, 10)))


class ComponentTests(unittest.TestCase):
    def test_components_are_eight_connected_with_areas_and_boxes(self):
        mask = bytes([1, 1, 0, 0,
                      0, 0, 1, 0,
                      0, 0, 0, 0,
                      1, 0, 0, 1])
        found = sorted(pixel_policy.components(mask, 4, 4), reverse=True)
        self.assertEqual(found[0], (3, 0, 0, 2, 1))
        self.assertEqual(sorted(area for area, *_ in found), [1, 1, 3])


class WiringTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        screen().save(self.root / 'source.png')
        screen(offset=(1, 0)).save(self.root / 'render.png')

    def test_default_report_is_unchanged_and_carries_no_profile(self):
        result = compare(self.root / 'source.png', self.root / 'render.png')
        self.assertNotIn('profile', result)
        self.assertEqual(result['pixelStatus'], 'fail')

    def test_profile_is_diagnostic_and_never_changes_the_zero_budget_verdict(self):
        result = compare(self.root / 'source.png', self.root / 'render.png', profile='diagnostic')
        self.assertEqual(result['pixelStatus'], 'fail')
        self.assertEqual(result['profile']['status'], 'pass')
        self.assertEqual(result['wholeFrame']['channelTolerance'], 0)

    def test_unknown_profile_is_invalid_input(self):
        with self.assertRaisesRegex(ValueError, 'Unknown profile'):
            compare(self.root / 'source.png', self.root / 'render.png', profile='lenient')

    def test_cli_records_the_profile_but_keeps_the_zero_budget_exit_code(self):
        run = subprocess.run([sys.executable, str(Path(__file__).with_name('visual_check.py')),
                              str(self.root / 'source.png'), str(self.root / 'render.png'),
                              '--output', str(self.root / 'evidence'), '--profile', 'diagnostic'],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 1, run.stderr)
        summary = json.loads(run.stdout)
        self.assertEqual(summary['pixelStatus'], 'fail')
        self.assertEqual(summary['profile']['status'], 'pass')
        self.assertTrue(summary['profile']['diagnostic'])
        self.assertIn('profile', json.loads((self.root / 'evidence/pixels.json').read_text()))

    def test_region_kind_is_accepted_in_a_manifest_and_validated(self):
        manifest = {'regions': [{'name': 'all', 'rect': [0, 0, SIZE[0], SIZE[1]], 'kind': 'text'}]}
        self.assertIn('all', compare(self.root / 'source.png', self.root / 'render.png', manifest, profile='diagnostic')['regions'])
        manifest['regions'][0]['kind'] = 'photo'
        with self.assertRaisesRegex(ValueError, 'kind'):
            compare(self.root / 'source.png', self.root / 'render.png', manifest)


if __name__ == '__main__':
    unittest.main()
