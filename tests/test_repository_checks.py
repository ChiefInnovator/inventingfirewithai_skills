"""Exercise the maintainer runner and literal Pages data with disposable files."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


runner = load_script("check_repository")
data = load_script("sync_site_data")


class DisposableRepository(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "scripts").mkdir()
        shutil.copy(ROOT / "scripts/sync_site_data.py", self.root / "scripts")
        self.source = self.root / data.SOURCE
        self.source.parent.mkdir(parents=True)
        self.source.write_bytes(b"---\ntitle: Fixture\n---\n\n{{ site.title }}\n{% raw %}literal{% endraw %}\n")
        self.asset = self.root / "docs" / data.ASSET
        self.asset.parent.mkdir(parents=True)
        self.asset.write_bytes(data.PREFIX + self.source.read_bytes())

    def suite(self, directory, body="pass", *, requires_codex=False):
        destination = self.root / directory
        destination.mkdir()
        code = ("import unittest\n\nclass Fixture(unittest.TestCase):\n"
                "    def test_fixture(self):\n" + textwrap.indent(textwrap.dedent(body), "        ") + "\n")
        (destination / "test_shared.py").write_text(code)
        return runner.Suite(directory, directory, requires_codex=requires_codex)

    def run_checks(self, suites, **kwargs):
        output = io.StringIO()
        with redirect_stdout(output):
            results = runner.run_checks(self.root, suites, **kwargs)
        return results, output.getvalue()

    def fake_codex(self, version):
        binary = self.root / "bin"
        binary.mkdir()
        command = binary / "codex"
        command.write_text(f"#!{sys.executable}\nprint('codex-cli {version}')\n")
        command.chmod(0o755)
        return str(binary)


@unittest.skipUnless(sys.platform in {"darwin", "linux"}, "POSIX session cleanup requires macOS/Linux")
class RepositoryRunnerTests(DisposableRepository):
    def test_duplicate_module_names_run_in_separate_sessions_with_same_interpreter(self):
        suites = []
        for name in ("first", "second"):
            suites.append(self.suite(name, f"""
                import json, os, sys
                from pathlib import Path
                Path('{name}.json').write_text(json.dumps({{
                    'pid': os.getpid(), 'group': os.getpgrp(),
                    'session': os.getsid(0), 'python': sys.executable
                }}))
            """))
        results, _ = self.run_checks(suites)
        self.assertTrue(all(result.passed for result in results))
        records = [json.loads((self.root / f"{name}.json").read_text()) for name in ("first", "second")]
        self.assertNotEqual(records[0]["pid"], records[1]["pid"])
        for record in records:
            self.assertEqual(record["pid"], record["group"])
            self.assertEqual(record["pid"], record["session"])
            self.assertEqual(Path(record["python"]).resolve(), Path(sys.executable).resolve())

    def test_failure_is_named_and_does_not_hide_later_suite(self):
        bad = self.suite("failing", "self.fail('intentional fixture failure')")
        good = self.suite("following")
        results, output = self.run_checks([bad, good])
        self.assertFalse(results[1].passed)
        self.assertTrue(results[2].passed)
        self.assertIn("FAILED: failing", output)
        self.assertIn("PASS: following", output)

    def test_missing_and_empty_suites_fail_while_later_suite_runs(self):
        (self.root / "empty").mkdir()
        suites = [runner.Suite("missing", "absent"), runner.Suite("empty", "empty"), self.suite("following")]
        results, output = self.run_checks(suites)
        self.assertEqual([result.passed for result in results], [True, False, False, True])
        self.assertIn("Missing test suite: absent", output)
        self.assertIn("Missing test suite: empty", output)

    def test_timeout_kills_term_resistant_descendant_and_reaps_child_before_continuing(self):
        descendant = self.root / "descendant.py"
        descendant.write_text(textwrap.dedent("""
            import os, signal, time
            from pathlib import Path
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            Path('descendant.pid').write_text(str(os.getpid()))
            while True:
                time.sleep(1)
        """))
        hanging = self.suite("hanging", """
            import os, subprocess, sys, time
            from pathlib import Path
            Path('parent.pid').write_text(str(os.getpid()))
            subprocess.Popen([sys.executable, 'descendant.py'])
            while True:
                time.sleep(1)
        """)
        self.addCleanup(self.kill_fixture_group)
        results, output = self.run_checks([hanging, self.suite("following")], timeout=2, grace=0.2)
        self.assertTrue(results[1].timed_out)
        self.assertTrue(results[2].passed)
        self.assertIn("TIMED OUT: hanging", output)
        parent = int((self.root / "parent.pid").read_text())
        with self.assertRaises(ChildProcessError):
            os.waitpid(parent, os.WNOHANG)
        child = int((self.root / "descendant.pid").read_text())
        deadline = time.monotonic() + 3
        while self.process_is_running(child) and time.monotonic() < deadline:
            time.sleep(0.05)
        self.assertFalse(self.process_is_running(child), "TERM-resistant descendant survived group cleanup")

    @staticmethod
    def process_is_running(pid):
        status = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)],
                                capture_output=True, text=True, timeout=3)
        # A terminated orphan can remain a zombie briefly until the OS reaps it.
        return status.returncode == 0 and bool(status.stdout.strip()) and not status.stdout.strip().startswith("Z")

    def kill_fixture_group(self):
        path = self.root / "parent.pid"
        if path.exists():
            try:
                os.killpg(int(path.read_text()), signal.SIGKILL)
            except ProcessLookupError:
                pass

    def test_interrupt_cleans_owned_child_group_and_reraises_keyboard_interrupt(self):
        shutil.copy(ROOT / "scripts/check_repository.py", self.root / "scripts")
        (self.root / "interrupt_child.py").write_text(textwrap.dedent("""
            import os, signal, subprocess, sys, time
            from pathlib import Path
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            Path('parent.pid').write_text(str(os.getpid()))
            subprocess.Popen([sys.executable, '-c',
                "import os, signal, time; from pathlib import Path; "
                "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
                "Path('descendant.pid').write_text(str(os.getpid())); time.sleep(60)"])
            while True:
                time.sleep(1)
        """))
        wrapper = textwrap.dedent("""
            import sys
            from pathlib import Path
            sys.path.insert(0, 'scripts')
            from check_repository import run_process
            run_process('interrupted', [sys.executable, 'interrupt_child.py'],
                        Path.cwd(), timeout=30, grace=0.2)
            Path('unexpected-pass').write_text('interruption was swallowed')
        """)
        process = subprocess.Popen([sys.executable, "-c", wrapper], cwd=self.root,
                                   start_new_session=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True)
        self.addCleanup(self.cleanup_wrapper, process)
        self.addCleanup(self.kill_fixture_group)
        deadline = time.monotonic() + 5
        while not (self.root / "descendant.pid").exists() and time.monotonic() < deadline:
            self.assertIsNone(process.poll(), "interruption fixture exited before starting its children")
            time.sleep(0.02)
        self.assertTrue((self.root / "descendant.pid").exists(), "interruption fixture did not start")
        process.send_signal(signal.SIGINT)
        output, _ = process.communicate(timeout=5)
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("KeyboardInterrupt", output)
        self.assertFalse((self.root / "unexpected-pass").exists())
        for filename in ("parent.pid", "descendant.pid"):
            with self.subTest(process=filename):
                self.assertFalse(self.process_is_running(int((self.root / filename).read_text())))

    @staticmethod
    def cleanup_wrapper(process):
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
        process.communicate(timeout=5)

    def test_missing_codex_fails_only_its_suite(self):
        cli_suite = self.suite("codex-tests", "self.fail('must not run without Codex')", requires_codex=True)
        following = self.suite("following")
        with patch.dict(os.environ, {"PATH": str(self.root / "no-binaries")}):
            results, output = self.run_checks([cli_suite, following])
        self.assertEqual([result.passed for result in results], [True, False, True])
        self.assertIn("Codex CLI >=0.153.4", output)
        self.assertIn("FAILED: codex-tests", output)

    def test_old_codex_is_rejected_but_compatible_codex_runs_suite(self):
        suites = [self.suite("codex-tests", requires_codex=True), self.suite("following")]
        binary_path = self.fake_codex("0.153.3")
        with patch.dict(os.environ, {"PATH": binary_path}):
            results, _ = self.run_checks(suites)
        self.assertEqual([result.passed for result in results], [True, False, True])
        (self.root / "bin/codex").write_text(f"#!{sys.executable}\nprint('codex-cli 0.166.0')\n")
        with patch.dict(os.environ, {"PATH": binary_path}):
            results, _ = self.run_checks(suites)
        self.assertTrue(all(result.passed for result in results))

    def test_stale_site_data_does_not_prevent_suite_results(self):
        self.source.write_bytes(b"Changed source\n")
        results, output = self.run_checks([self.suite("following")])
        self.assertEqual([result.passed for result in results], [False, True])
        self.assertIn("Stale scorecard asset", output)
        self.assertIn("PASS: following", output)

    def test_unsupported_os_fails_before_running_any_child(self):
        suite = self.suite("never-run", "self.fail('unsupported OS must not start this suite')")
        with patch.object(runner.sys, "platform", "win32"):
            results, output = self.run_checks([suite])
        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].passed)
        self.assertIn("macOS and Linux only", output)


class SiteDataTests(DisposableRepository):
    def sync(self, **kwargs):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return data.sync_data(self.root, **kwargs)

    def test_snapshot_preserves_front_matter_and_liquid_after_non_yaml_prefix(self):
        original = self.source.read_bytes()
        self.asset.unlink()
        self.assertEqual(self.sync(), 0)
        generated = self.asset.read_bytes()
        self.assertFalse(generated.startswith(b"---"))
        self.assertEqual(generated, data.PREFIX + original)
        self.assertEqual(self.source.read_bytes(), original)
        self.assertEqual(self.sync(check=True), 0)

    def test_check_detects_stale_and_missing_asset_without_writing(self):
        self.asset.write_bytes(b"stale")
        self.assertEqual(self.sync(check=True), 1)
        self.assertEqual(self.asset.read_bytes(), b"stale")
        self.asset.unlink()
        self.assertEqual(self.sync(check=True), 1)
        self.assertFalse(self.asset.exists())

    def test_built_output_must_exist_and_match_the_literal_snapshot(self):
        built_dir = self.root / "_site"
        built_asset = built_dir / data.ASSET
        self.assertEqual(self.sync(check=True, built_dir=built_dir), 1)
        self.assertFalse(built_asset.exists())
        built_asset.parent.mkdir(parents=True)
        built_asset.write_bytes(self.source.read_bytes())
        self.assertEqual(self.sync(check=True, built_dir=built_dir), 1)
        built_asset.write_bytes(self.asset.read_bytes())
        self.assertEqual(self.sync(check=True, built_dir=built_dir), 0)
        self.asset.write_bytes(b"stale source asset")
        self.assertEqual(self.sync(check=True, built_dir=built_dir), 1)

    def test_built_dir_requires_read_only_check_mode(self):
        self.asset.unlink()
        result = subprocess.run([sys.executable, str(self.root / "scripts/sync_site_data.py"),
                                 "--built-dir", "_site"], cwd=self.root,
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--built-dir requires --check", result.stderr)
        self.assertFalse(self.asset.exists())

    def test_missing_source_is_an_explicit_failure(self):
        self.source.unlink()
        self.assertEqual(self.sync(check=True), 1)


if __name__ == "__main__":
    unittest.main()
