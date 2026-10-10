import tempfile
import json
import subprocess
import sys
import unittest
from pathlib import Path

from PIL import Image
from visual_check import compare


class VisualTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.source = self.root / 'source.png'
        self.render = self.root / 'render.png'
        Image.new('RGBA', (100, 100), 'black').save(self.source)
        Image.new('RGBA', (100, 100), 'black').save(self.render)

    def test_metric_reports_mean_of_per_pixel_max_channel_deltas(self):
        Image.new('RGBA', (100, 100), (20, 0, 0, 255)).save(self.render)
        result = compare(self.source, self.render)
        self.assertEqual(result['wholeFrame']['meanMaxChannelDifference'], 20)
        self.assertNotIn('meanChannelDifference', result['wholeFrame'])

    def test_identical_pixels_do_not_grant_human_approval(self):
        result = compare(self.source, self.render, output=self.root / 'evidence')
        self.assertEqual(result['pixelStatus'], 'pass')
        self.assertEqual(result['humanApproval'], 'unchecked')
        self.assertTrue((self.root / 'evidence/difference.png').exists())

    def test_malformed_manifest_types_rejected(self):
        for manifest in ([], False, '', 0, ['regions'], True, 'invalid', 1):
            with self.subTest(manifest=manifest), self.assertRaisesRegex(ValueError, 'JSON object'):
                compare(self.source, self.render, manifest)
        for regions in (None, {}, '', False, [False], [[]], ['region']):
            with self.subTest(regions=regions), self.assertRaisesRegex(ValueError, 'array of objects'):
                compare(self.source, self.render, {'regions': regions})

    def test_cli_reports_invalid_manifest_without_traceback(self):
        manifest = self.root / 'manifest.json'
        for value in ([], False, 'invalid', None):
            manifest.write_text(json.dumps(value))
            result = subprocess.run([sys.executable, str(Path(__file__).with_name('visual_check.py')),
                str(self.source), str(self.render), '--manifest', str(manifest),
                '--output', str(self.root / 'evidence')], capture_output=True, text=True)
            with self.subTest(value=value):
                self.assertEqual(result.returncode, 2)
                self.assertIn('Manifest must be a JSON object', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse((self.root / 'evidence/pixels.json').exists())

    def test_missing_small_control_fails_critical_region_despite_screen_budget(self):
        image = Image.open(self.render)
        image.putpixel((50, 50), (255, 255, 255, 255))
        image.save(self.render)
        result = compare(self.source, self.render, {'maxChangedFraction': .001,
            'budgetReason': 'test reference rasterization', 'regions': [
                {'name': 'primary-action', 'rect': [49, 49, 52, 52], 'maxChangedFraction': 0}]})
        self.assertEqual(result['wholeFrame']['status'], 'pass')
        self.assertEqual(result['regions']['primary-action']['status'], 'fail')
        self.assertEqual(result['pixelStatus'], 'fail')

    def test_dimensions_fail_without_stretching(self):
        Image.new('RGB', (101, 100), 'black').save(self.render)
        result = compare(self.source, self.render)
        self.assertEqual(result['pixelStatus'], 'fail')
        self.assertEqual(result['renderComparedSize'], [101, 100])

    def test_transparency_difference_is_not_lost(self):
        Image.new('RGBA', (100, 100), (0, 0, 0, 0)).save(self.render)
        self.assertEqual(compare(self.source, self.render)['wholeFrame']['changedFraction'], 1)

    def test_unrecorded_crop_mask_and_invalid_budgets_rejected(self):
        for manifest in [{'sourceCrop': [0, 0, 100, 100]}, {'ignoreMask': 'dock'},
                         {'maxChangedFraction': .01}, {'channelTolerance': 256},
                         {'maxChangedFraction': float('nan')},
                         {'regions': [{'name': 'dock', 'rect': [0, 0, 101, 100]}]},
                         {'sourceCrop': [0, 0, 0, 100], 'cropReason': 'test'}]:
            with self.subTest(manifest=manifest), self.assertRaises(ValueError):
                compare(self.source, self.render, manifest)


if __name__ == '__main__':
    unittest.main()
