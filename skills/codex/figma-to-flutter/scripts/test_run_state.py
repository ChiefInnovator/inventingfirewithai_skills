"""Whole-run metrics, lifecycle, portability and concurrent update regressions."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import run_state


class RunStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'metrics'
        self.clock = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.now = patch.object(run_state, 'utc_now', side_effect=lambda: self.clock)
        self.now.start()
        self.addCleanup(self.now.stop)
        run_state.start_run(self.root, 'sync', 'example')
        self.path = self.root / 'example.json'

    def progress(self, slugs, **kwargs):
        return run_state.progress(self.root, 'example', 'website', slugs, **kwargs)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(Path(run_state.__file__)),
                               '--state-dir', str(self.root), *args], capture_output=True, text=True)

    def test_unique_screens_separate_collections_and_parts(self):
        self.progress(['login', 'login'], outcome='completed')
        self.progress(['login'], outcome='completed')
        run_state.progress(self.root, 'example', 'mobile', ['login'], outcome='completed')
        self.progress(['dialog'], kind='part', outcome='completed')
        self.progress(['flow'], kind='flow-card', outcome='completed')
        self.progress(['old'], outcome='skipped')
        self.progress(['pending'])
        self.progress(['failed'], outcome='failed')
        self.progress(['blocked'], outcome='blocked')
        self.clock += timedelta(seconds=120)
        value = run_state.report_run(self.root, 'example')
        self.assertEqual(value['counts']['screen'],
                         {'completed': 2, 'skipped': 1, 'pending': 1, 'failed': 1, 'blocked': 1})
        self.assertEqual(value['counts']['part']['completed'], 1)
        self.assertEqual(value['counts']['flow-card']['completed'], 1)
        self.assertEqual(value['screensPerMinute'], 1)
        self.assertEqual(value['screensPerHour'], 60)
        self.assertEqual(value['secondsPerScreen'], 60)

    def test_zero_screens_and_zero_elapsed(self):
        value = run_state.report_run(self.root, 'example')
        self.assertEqual(value['elapsedSeconds'], 0)
        self.assertEqual(value['screensPerMinute'], 0)
        self.assertIsNone(value['secondsPerScreen'])
        self.progress(['screen'], outcome='completed')
        value = run_state.report_run(self.root, 'example')
        self.assertEqual(value['screensPerHour'], 0)
        self.assertEqual(value['secondsPerScreen'], 0)

    def test_progress_replaces_outcome_and_rejects_kind_change_atomically(self):
        self.progress(['screen'])
        self.progress(['screen'], outcome='completed')
        original = self.path.read_bytes()
        with self.assertRaises(ValueError):
            self.progress(['new', 'screen'], kind='part')
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(run_state.report_run(self.root, 'example')['counts']['screen']['completed'], 1)

    def test_stage_totals_do_not_replace_wall_time(self):
        run_state.measure(self.root, 'example', 'capture', 90, cache_hits=2, retries=1)
        run_state.measure(self.root, 'example', 'render', 80, throttles=3)
        self.clock += timedelta(seconds=60)
        self.progress(['screen'], outcome='completed')
        value = run_state.finish_run(self.root, 'example', 'completed')
        self.assertEqual(value['elapsedSeconds'], 60)
        self.assertEqual(value['totals'], {'seconds': 170, 'cacheHits': 2, 'retries': 1, 'throttles': 3})
        self.assertEqual(value['screensPerMinute'], 1)

    def test_completed_requires_all_registered_work_successful(self):
        for outcome in ('pending', 'failed', 'blocked'):
            with self.subTest(outcome=outcome):
                self.progress(['screen'], outcome=outcome)
                with self.assertRaises(ValueError):
                    run_state.finish_run(self.root, 'example', 'completed')
                self.assertEqual(json.loads(self.path.read_text())['status'], 'running')
        self.progress(['screen'], outcome='skipped')
        self.assertEqual(run_state.finish_run(self.root, 'example', 'completed')['status'], 'completed')

    def test_terminal_records_freeze_and_idempotent_finish_does_not_write(self):
        self.progress(['screen'], outcome='completed')
        self.progress(['next'])
        self.clock += timedelta(seconds=42)
        value = run_state.finish_run(self.root, 'example', 'interrupted')
        original = self.path.read_bytes()
        self.clock += timedelta(hours=1)
        self.assertEqual(run_state.report_run(self.root, 'example'), value)
        self.assertEqual(run_state.finish_run(self.root, 'example', 'interrupted'), value)
        self.assertEqual(self.path.read_bytes(), original)
        for update in (lambda: self.progress(['next'], outcome='completed'),
                       lambda: run_state.measure(self.root, 'example', 'late', 1),
                       lambda: run_state.finish_run(self.root, 'example', 'completed'),
                       lambda: run_state.start_run(self.root, 'retry', 'example')):
            with self.assertRaises(ValueError):
                update()
        self.assertEqual(self.path.read_bytes(), original)

    def test_clock_rollback_does_not_write_terminal_state(self):
        original = self.path.read_bytes()
        self.clock -= timedelta(seconds=1)
        with self.assertRaisesRegex(ValueError, 'backwards'):
            run_state.finish_run(self.root, 'example', 'blocked')
        self.assertEqual(self.path.read_bytes(), original)

    def test_invalid_input_never_overwrites_run(self):
        original = self.path.read_bytes()
        for run_id in ('../escape', '', '/absolute', 'a/b', 'a\\b', '.hidden', 'a' * 129):
            with self.subTest(run_id=run_id), self.assertRaises(ValueError):
                run_state.start_run(self.root, 'sync', run_id)
        for identifier in ('', ' ', '.', '..', '../x', 'x/y', 'x\\y', 'x\n', ' leading'):
            with self.subTest(identifier=identifier):
                with self.assertRaises(ValueError):
                    self.progress([identifier])
                with self.assertRaises(ValueError):
                    run_state.progress(self.root, 'example', identifier, ['screen'])
        for seconds in (-1, float('nan'), float('inf'), True, '1'):
            with self.subTest(seconds=seconds), self.assertRaises(ValueError):
                run_state.measure(self.root, 'example', 'render', seconds)
        for count in (-1, 1.5, True):
            with self.subTest(count=count), self.assertRaises(ValueError):
                run_state.measure(self.root, 'example', 'render', 1, retries=count)
        for command in ('', ' '):
            with self.assertRaises(ValueError):
                run_state.start_run(self.root, command)
        self.assertEqual(self.path.read_bytes(), original)

    def test_report_does_not_create_missing_directory_or_mutate_state(self):
        original = self.path.read_bytes()
        listing = sorted(self.root.iterdir())
        run_state.report_run(self.root, 'example')
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(sorted(self.root.iterdir()), listing)
        missing = self.root / 'missing'
        with self.assertRaises(ValueError):
            run_state.report_run(missing, 'absent')
        self.assertFalse(missing.exists())

    def test_cli_arbitrary_collection_and_explicit_directory(self):
        started = self.cli('start', '--command', 'convert', '--run', 'cli-run')
        self.assertEqual(started.returncode, 0, started.stderr)
        self.assertEqual(json.loads(started.stdout)['metricsFile'], str((self.root / 'cli-run.json').resolve()))
        updated = self.cli('progress', '--run', 'cli-run', '--collection', 'Another app',
                           '--outcome', 'completed', 'profile')
        self.assertEqual(updated.returncode, 0, updated.stderr)
        self.assertIn('Another app/profile', json.loads(updated.stdout)['items'])
        finished = self.cli('finish', '--run', 'cli-run', '--status', 'completed')
        self.assertEqual(finished.returncode, 0, finished.stderr)
        self.assertEqual(json.loads(finished.stdout)['status'], 'completed')
        for invalid in (('measure', '--run', 'example', '--stage', 'render', '--seconds', 'nan'),
                        ('start', '--command', 'sync', '--run', '../bad')):
            self.assertEqual(self.cli(*invalid).returncode, 2)
        without_directory = subprocess.run([sys.executable, str(Path(run_state.__file__)),
                                             'start', '--command', 'sync'], capture_output=True, text=True)
        self.assertEqual(without_directory.returncode, 2)

    def test_concurrent_process_updates_keep_all_items_and_measurements(self):
        def worker(index):
            result = self.cli('progress', '--run', 'example', '--collection', 'parallel',
                              '--outcome', 'completed', f'screen-{index}')
            if result.returncode:
                return result
            return self.cli('measure', '--run', 'example', '--stage', f'worker-{index}',
                            '--seconds', '2', '--cache-hits', '1')
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(worker, range(12)))
        for result in results:
            self.assertEqual(result.returncode, 0, result.stderr)
        value = run_state.report_run(self.root, 'example')
        self.assertEqual(value['counts']['screen']['completed'], 12)
        self.assertEqual(len(value['stages']), 12)
        self.assertEqual(value['totals']['seconds'], 24)
        self.assertEqual(value['totals']['cacheHits'], 12)
        self.assertFalse(list(self.root.glob('*.tmp')))


if __name__ == '__main__':
    unittest.main()
