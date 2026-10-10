"""CLI regressions that exercise a globally installed skill against another repo."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class PortableCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'project'
        self.repo.mkdir()
        self.input = self.root / 'node.json'
        self.input.write_text(json.dumps({'id': '1:2', 'type': 'RECTANGLE',
                                          'width': 40, 'height': 20}))

    def compile(self, output):
        return subprocess.run([sys.executable, str(Path(__file__).with_name('convert.py')),
            str(self.input), '--repo-root', str(self.repo), '--file-key', 'ExampleFile',
            '--output', str(output)], capture_output=True, text=True)

    def test_scratch_emission_records_identity_without_project_imports(self):
        output = self.root / 'scratch'
        run = self.compile(output)
        self.assertEqual(run.returncode, 0, run.stderr)
        report = json.loads((output / 'report.json').read_text())
        self.assertEqual(report['fileKey'], 'ExampleFile')
        self.assertEqual(report['rootNodeId'], '1:2')
        self.assertEqual(report['visualApproval'], 'unchecked')
        self.assertFalse(list(self.repo.iterdir()))

    def test_output_in_target_repo_or_symlink_to_it_is_refused(self):
        link = self.root / 'alias'
        link.symlink_to(self.repo, target_is_directory=True)
        for output in (self.repo, self.repo / 'draft', link / 'draft'):
            with self.subTest(output=output):
                run = self.compile(output)
                self.assertEqual(run.returncode, 2)
                self.assertIn('outside the repository', run.stderr)
        self.assertFalse(list(self.repo.iterdir()))

    def test_existing_scratch_work_is_not_overwritten(self):
        output = self.root / 'scratch'
        output.mkdir()
        draft = output / 'draft.dart'
        draft.write_text('existing work')
        self.assertEqual(self.compile(output).returncode, 2)
        self.assertEqual(draft.read_text(), 'existing work')

    def test_url_cli_needs_no_local_project_state(self):
        run = subprocess.run([sys.executable, str(Path(__file__).with_name('input_url.py')),
            'https://www.figma.com/design/ExampleFile/Example?node-id=1-2'],
            cwd=self.repo, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['action'], 'new-screen')
        self.assertFalse(list(self.repo.iterdir()))


if __name__ == '__main__':
    unittest.main()
