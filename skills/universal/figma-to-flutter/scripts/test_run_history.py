"""Finished-history portability, privacy, provenance and no-overwrite regressions."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import run_history
import run_state


class RunHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = self.root / 'state'
        self.history = self.root / 'history'
        self.run_id = 'private-customer-run'
        run_state.start_run(self.state, '/secret/path --token=private-token', self.run_id)

    def finish(self, status='completed'):
        return run_state.finish_run(self.state, self.run_id, status)

    def export(self):
        return run_history.export_run(self.state, self.run_id, self.history)

    def test_finished_export_omits_free_text_and_preserves_metrics(self):
        run_state.progress(self.state, self.run_id, 'private-collection', ['private-screen'],
                           outcome='completed')
        run_state.progress(self.state, self.run_id, 'private-collection', ['private-header'],
                           kind='part', outcome='completed')
        run_state.measure(self.state, self.run_id, 'capture', 2, cache_hits=1)
        run_state.measure(self.state, self.run_id, '/private-stage token=secret', 3, retries=2)
        finished = self.finish()
        before = (self.state / (self.run_id + '.json')).read_bytes()
        path = self.export()
        record = json.loads(path.read_text())
        self.assertEqual(record['schemaVersion'], 1)
        self.assertEqual(record['run'], hashlib.sha256(self.run_id.encode()).hexdigest())
        self.assertEqual(path.stem, record['run'])
        self.assertEqual(record['counts']['screen']['completed'], 1)
        self.assertEqual(record['counts']['part']['completed'], 1)
        self.assertEqual(record['elapsedSeconds'], finished['elapsedSeconds'])
        self.assertEqual(record['totals'], {'seconds': 5, 'cacheHits': 1, 'retries': 2, 'throttles': 0})
        self.assertEqual([stage['stage'] for stage in record['stages']], ['capture', 'other'])
        for private in ('private', 'secret', str(self.root), 'metricsFile', 'command',
                        'items', 'visualApproval', 'productionApproval'):
            self.assertNotIn(private, path.read_text())
        self.assertEqual(before, (self.state / (self.run_id + '.json')).read_bytes())

    def test_running_state_cannot_create_history(self):
        with self.assertRaisesRegex(ValueError, 'Finish the run'):
            self.export()
        self.assertFalse(self.history.exists())

    def test_interrupted_and_blocked_runs_preserve_unsuccessful_counts(self):
        for status in ('interrupted', 'blocked', 'failed'):
            run_state.start_run(self.state, 'audit', status)
            run_state.progress(self.state, status, 'app', ['screen'], outcome='blocked')
            run_state.finish_run(self.state, status, status)
            path = run_history.export_run(self.state, status, self.history)
            record = json.loads(path.read_text())
            self.assertEqual(record['status'], status)
            self.assertEqual(record['counts']['screen']['blocked'], 1)
            self.assertEqual(record['screensPerHour'], 0)

    def test_existing_or_concurrently_written_record_is_never_replaced(self):
        self.finish()
        def attempt(_):
            try:
                return str(self.export())
            except ValueError:
                return None
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(attempt, range(4)))
        self.assertEqual(sum(path is not None for path in results), 1)
        path = Path(next(path for path in results if path is not None))
        before = path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'append-only'):
            self.export()
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual([p.name for p in self.history.iterdir()], [path.name])

    def test_existing_symlink_record_and_overlapping_state_are_refused(self):
        self.finish()
        self.history.mkdir()
        target = self.root / 'keep.json'
        target.write_text('existing evidence')
        record = run_history.build_record(run_state.report_run(self.state, self.run_id))
        (self.history / (record['run'] + '.json')).symlink_to(target)
        with self.assertRaisesRegex(ValueError, 'append-only'):
            self.export()
        self.assertEqual(target.read_text(), 'existing evidence')
        for directory in (self.state, self.state / 'nested', self.root):
            with self.assertRaisesRegex(ValueError, 'disjoint'):
                run_history.export_run(self.state, self.run_id, directory)

    def test_malformed_finished_state_is_rejected_before_writing(self):
        value = self.finish()
        for mutation in ({'status': 'running'}, {'finishedAt': '2026-01-01T00:00:00'},
                         {'stages': [{'stage': 'capture', 'seconds': float('nan'),
                                      'cacheHits': 0, 'retries': 0, 'throttles': 0}]},
                         {'items': {'a/b': {'kind': 'screen', 'outcome': 'pending'}}},
                         {'provenance': {'git': {'commit': 'secret', 'dirty': False}}}):
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                run_history.build_record({**value, **mutation})
        self.assertFalse(self.history.exists())

    def test_cli_is_explicit_and_works_outside_skill_and_target_folders(self):
        self.finish()
        command = [sys.executable, str(Path(run_history.__file__)), '--state-dir', str(self.state),
                   '--run', self.run_id, '--history-dir', str(self.history)]
        result = subprocess.run(command, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(Path(json.loads(result.stdout)['historyFile']).is_file())
        duplicate = subprocess.run(command, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(duplicate.returncode, 2)
        self.assertIn('append-only', duplicate.stderr)

    def test_provenance_is_captured_at_start_and_omits_paths(self):
        repo = self.root / 'project'
        repo.mkdir()
        def git(*args):
            return subprocess.run(['git', '-C', str(repo), *args], check=True,
                                  capture_output=True, text=True).stdout.strip()
        git('init', '-q')
        git('config', 'user.name', 'Test User')
        git('config', 'user.email', 'test@example.invalid')
        (repo / 'file.txt').write_text('one')
        git('add', 'file.txt')
        git('commit', '-qm', 'fixture')
        skill = self.root / 'skill'
        skill.mkdir()
        (skill / 'SKILL.md').write_text('generic fixture')
        started = run_state.start_run(self.state, 'sync', 'provenance', repo, skill)
        expected = started['provenance']
        self.assertEqual(expected['git'], {'commit': git('rev-parse', 'HEAD'), 'dirty': False})
        (repo / 'file.txt').write_text('two')
        (skill / 'SKILL.md').write_text('changed')
        run_state.finish_run(self.state, 'provenance', 'completed')
        path = run_history.export_run(self.state, 'provenance', self.history)
        record = json.loads(path.read_text())
        self.assertEqual(record['provenance'], expected)
        self.assertNotEqual(run_history.capture_provenance(repo, skill), expected)
        self.assertNotIn(str(self.root), path.read_text())
        with self.assertRaisesRegex(ValueError, 'outside the target repository'):
            run_state.start_run(repo / 'state', 'sync', 'inside', repo_root=repo)

    def test_skill_hash_is_location_independent_and_ignores_python_cache(self):
        for name in ('first', 'second'):
            root = self.root / name
            root.mkdir()
            (root / 'SKILL.md').write_text('same content')
        first, second = self.root / 'first', self.root / 'second'
        (first / '__pycache__').mkdir()
        (first / '__pycache__' / 'ignored.pyc').write_bytes(b'cache')
        self.assertEqual(run_history.capture_provenance(skill_root=first),
                         run_history.capture_provenance(skill_root=second))
        (first / 'external').symlink_to(second, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'without symlinks'):
            run_history.capture_provenance(skill_root=first)


if __name__ == '__main__':
    unittest.main()
