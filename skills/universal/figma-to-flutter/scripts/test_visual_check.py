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

    def test_nodes_rank_changed_pixels_by_smallest_covering_box_without_changing_verdict(self):
        image = Image.new('RGBA', (200, 200), 'black')
        image.paste((255, 255, 255, 255), (40, 40, 60, 50))    # 200 px inside the button
        image.paste((255, 255, 255, 255), (0, 180, 10, 190))   # 100 px on the card only
        image.paste((10, 10, 10, 255), (100, 0, 200, 20))      # under the 16/255 threshold
        image.paste((255, 255, 255, 255), (150, 100, 160, 110))  # clipped away from the hidden and overflow nodes
        image.save(self.render)
        Image.new('RGBA', (200, 200), 'black').save(self.source)
        tree = {'id': '1:1', 'name': 'Card', 'type': 'FRAME', 'width': 100, 'height': 100, 'children': [
            {'id': '1:2', 'name': 'Row', 'type': 'FRAME', 'x': 10, 'y': 10, 'width': 50, 'height': 30,
             'clipsContent': True, 'children': [
                {'id': '1:3', 'name': 'Button', 'type': 'RECTANGLE', 'x': 5, 'y': 5, 'width': 20, 'height': 20},
                {'id': '1:4', 'name': 'Overflow', 'type': 'RECTANGLE', 'x': 60, 'y': 35, 'width': 20, 'height': 20}]},
            {'id': '1:5', 'name': 'Ghost', 'type': 'RECTANGLE', 'x': 70, 'y': 45, 'width': 20, 'height': 20, 'opacity': 0}]}
        plain = compare(self.source, self.render)
        result = compare(self.source, self.render, output=self.root / 'evidence', nodes=tree)
        self.assertEqual(result['changedOver16'], 400)
        self.assertEqual([(n['id'], n['name'], n['rect'], n['changedPixels']) for n in result['worstNodes']],
                         [('1:3', 'Button', [30, 30, 70, 70], 200), ('1:1', 'Card', [0, 0, 200, 200], 200)])
        self.assertEqual(json.loads((self.root / 'evidence/pixels.json').read_text())['worstNodes'], result['worstNodes'])
        self.assertNotIn('worstNodes', plain)
        self.assertEqual((result['pixelStatus'], result['wholeFrame']), (plain['pixelStatus'], plain['wholeFrame']))
        # REST bounds are absolute; a recorded source crop moves the boxes with the compared pixels.
        rest = {'id': '1:1', 'width': 100, 'height': 100, 'absoluteBoundingBox': {'x': 500, 'y': 500, 'width': 100, 'height': 100},
                'children': [{'id': '1:3', 'x': 0, 'y': 0, 'width': 20, 'height': 20,
                              'absoluteBoundingBox': {'x': 515, 'y': 515, 'width': 20, 'height': 20}}]}
        crop = {'sourceCrop': [20, 20, 200, 200], 'renderCrop': [20, 20, 200, 200], 'cropReason': 'test'}
        self.assertEqual(compare(self.source, self.render, crop, nodes=rest)['worstNodes'][0]['rect'], [10, 10, 50, 50])
        for invalid in ([], {'id': '1:1'}, {'id': '1:1', 'width': 0, 'height': 10}):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(ValueError, 'normalized.json'):
                compare(self.source, self.render, nodes=invalid)

    def test_cli_nodes_keeps_exit_codes(self):
        script = str(Path(__file__).with_name('visual_check.py'))
        nodes = self.root / 'normalized.json'
        nodes.write_text(json.dumps({'id': '1:1', 'name': 'Root', 'type': 'FRAME', 'width': 100, 'height': 100}))
        run = lambda: subprocess.run([sys.executable, script, str(self.source), str(self.render), '--nodes', str(nodes),
            '--output', str(self.root / 'evidence')], capture_output=True, text=True)
        report = lambda: json.loads((self.root / 'evidence/pixels.json').read_text())
        self.assertEqual(run().returncode, 0)
        self.assertEqual((report()['changedOver16'], report()['worstNodes']), (0, []))
        Image.new('RGBA', (100, 100), 'white').save(self.render)
        self.assertEqual(run().returncode, 1)
        self.assertEqual(report()['worstNodes'][0]['changedPixels'], 10000)
        nodes.write_text('[]')
        result = run()
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)

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
