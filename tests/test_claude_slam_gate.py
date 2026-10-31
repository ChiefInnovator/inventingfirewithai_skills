"""Exercise the actual Claude /slam hook with disposable command-line fixtures."""

import json
from pathlib import Path
import subprocess
import tempfile
import textwrap
import time
import unittest

SKILL = Path(__file__).resolve().parents[1] / "skills/claude/slam/SKILL.md"


def hook_command():
    """Return the actual command registered in the skill's frontmatter."""
    front = SKILL.read_text().split("\n---\n", 1)[0]
    return textwrap.dedent(front.split("command: |\n", 1)[1])


class ShipGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="slam-gate-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "home"
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.gates = self.home / ".claude/slam-gates"
        self.gates.mkdir(parents=True)
        self.session = "3f2a9c1e-test-session"

    def fake_gh(self, state=None, fail=False):
        gh = self.bin / "gh"
        body = "exit 1" if fail else f"echo {state}"
        gh.write_text(f'#!/bin/sh\nprintf called >> "$HOME/gh.calls"\n{body}\n')
        gh.chmod(0o755)

    def arm(self, pr=4, repo="Owner/repo"):
        gate = self.gates / self.session
        gate.write_text(json.dumps({"repo": repo, "pr": pr}))
        return gate

    def payload(self, session=None, active=False):
        return {"session_id": self.session if session is None else session,
                "hook_event_name": "Stop", "stop_hook_active": active}

    def run_hook(self, session=None, *, payload=None, active=False, timeout=5):
        if payload is None:
            payload = json.dumps(self.payload(session, active))
        env = {"HOME": str(self.home), "PATH": f"{self.bin}:/usr/bin:/bin"}
        result = subprocess.run(["sh", "-c", hook_command()], input=payload,
                                capture_output=True, text=True, env=env,
                                check=False, timeout=timeout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout.strip()

    def test_no_gate_allows_stop(self):
        self.fake_gh("OPEN")
        self.assertEqual(self.run_hook(), "")

    def test_open_pr_blocks(self):
        self.fake_gh("OPEN")
        self.arm()
        decision = json.loads(self.run_hook())
        self.assertEqual(decision["decision"], "block")
        self.assertIn("PR #4", decision["reason"])
        self.assertIn("OPEN", decision["reason"])

    def test_merged_pr_blocks_until_gate_removed(self):
        self.fake_gh("MERGED")
        gate = self.arm()
        self.assertEqual(json.loads(self.run_hook())["decision"], "block")
        gate.unlink()
        self.assertEqual(self.run_hook(), "")

    def test_active_stop_hook_allows_stop_without_deleting_unfinished_gate(self):
        for state in ("OPEN", "MERGED"):
            with self.subTest(state=state):
                self.fake_gh(state)
                gate = self.arm()
                original = gate.read_bytes()
                self.assertEqual(self.run_hook(active=True), "")
                self.assertTrue(gate.exists())
                self.assertEqual(gate.read_bytes(), original)
        self.assertFalse((self.home / "gh.calls").exists())

    def test_invalid_active_flags_allow_stop_without_github_access(self):
        self.fake_gh("OPEN")
        gate = self.arm()
        for active in (None, "false", "true", 0, 1, [], {}):
            with self.subTest(active=active):
                payload = json.dumps({**self.payload(), "stop_hook_active": active})
                self.assertEqual(self.run_hook(payload=payload), "")
                self.assertTrue(gate.exists())
        self.assertFalse((self.home / "gh.calls").exists())

    def test_closed_pr_allows_stop_and_clears_gate(self):
        self.fake_gh("CLOSED")
        gate = self.arm()
        self.assertEqual(self.run_hook(), "")
        self.assertFalse(gate.exists())

    def test_gh_failure_retains_gate(self):
        self.fake_gh(fail=True)
        gate = self.arm()
        self.assertEqual(self.run_hook(), "")
        self.assertTrue(gate.exists())

    def test_gh_timeout_is_bounded_and_retains_gate(self):
        gh = self.bin / "gh"
        gh.write_text('#!/bin/sh\nprintf called >> "$HOME/gh.calls"\nexec sleep 30\n')
        gh.chmod(0o755)
        gate = self.arm()
        started = time.monotonic()
        self.assertEqual(self.run_hook(timeout=22), "")
        elapsed = time.monotonic() - started
        self.assertGreaterEqual(elapsed, 14)
        self.assertLess(elapsed, 22)
        self.assertTrue(gate.exists())
        self.assertTrue((self.home / "gh.calls").exists())

    def test_unknown_state_retains_gate(self):
        self.fake_gh("UNKNOWN")
        gate = self.arm()
        self.assertEqual(self.run_hook(), "")
        self.assertTrue(gate.exists())

    def test_bad_pr_number_fails_open_without_github_call(self):
        self.fake_gh("OPEN")
        for pr in ("4; rm -rf /", 0, -1, True, None, "", "٤"):
            with self.subTest(pr=pr):
                gate = self.arm(pr=pr)
                self.assertEqual(self.run_hook(), "")
                self.assertTrue(gate.exists())
        self.assertFalse((self.home / "gh.calls").exists())

    def test_invalid_repository_fails_open_without_github_call(self):
        self.fake_gh("OPEN")
        for repo in (None, "", "repo", "https://github.com/Owner/repo", "Owner/repo\nother", 'Owner/repo"'):
            with self.subTest(repo=repo):
                self.arm(repo=repo)
                self.assertEqual(self.run_hook(), "")
        self.assertFalse((self.home / "gh.calls").exists())

    def test_enterprise_host_and_string_pr_are_supported(self):
        self.fake_gh("OPEN")
        self.arm(pr="4", repo="github.example.com/Owner/repo")
        self.assertEqual(json.loads(self.run_hook())["decision"], "block")

    def test_other_sessions_gate_is_ignored(self):
        self.fake_gh("OPEN")
        self.arm()
        self.assertEqual(self.run_hook(session="another-session"), "")
        self.assertEqual(self.run_hook(session=""), "")

    def test_path_traversal_cannot_remove_file_outside_gate_directory(self):
        self.fake_gh("CLOSED")
        victim = self.home / "victim"
        victim.write_text(json.dumps({"repo": "Owner/repo", "pr": 4}))
        self.assertEqual(self.run_hook(session="../../victim"), "")
        self.assertTrue(victim.exists())
        self.assertFalse((self.home / "gh.calls").exists())

    def test_quoted_home_produces_valid_json(self):
        self.fake_gh("OPEN")
        self.home = self.root / 'home"quoted\\name'
        self.gates = self.home / ".claude/slam-gates"
        self.gates.mkdir(parents=True)
        self.arm()
        self.assertEqual(json.loads(self.run_hook())["decision"], "block")

    def test_multiline_json_payload_is_parsed(self):
        self.fake_gh("OPEN")
        self.arm()
        payload = json.dumps(self.payload(), indent=2)
        self.assertEqual(json.loads(self.run_hook(payload=payload))["decision"], "block")

    def test_malformed_payloads_do_not_touch_gate(self):
        self.fake_gh("CLOSED")
        gate = self.arm()
        for payload in ("{", "[]", "null", "{}", '{"session_id": 5}',
                        json.dumps({**self.payload(), "hook_event_name": "Other"})):
            with self.subTest(payload=payload):
                self.assertEqual(self.run_hook(payload=payload), "")
                self.assertTrue(gate.exists())
        self.assertFalse((self.home / "gh.calls").exists())

    def test_malformed_gates_are_retained(self):
        self.fake_gh("CLOSED")
        gate = self.arm()
        for content in ("{", "[]", "null", "repo=Owner/repo\npr=4\n"):
            with self.subTest(content=content):
                gate.write_text(content)
                self.assertEqual(self.run_hook(), "")
                self.assertTrue(gate.exists())
        self.assertFalse((self.home / "gh.calls").exists())

    def test_symlink_gate_is_ignored(self):
        self.fake_gh("CLOSED")
        target = self.root / "target"
        target.write_text(json.dumps({"repo": "Owner/repo", "pr": 4}))
        gate = self.gates / self.session
        gate.symlink_to(target)
        self.assertEqual(self.run_hook(), "")
        self.assertTrue(gate.is_symlink())
        self.assertTrue(target.exists())
        self.assertFalse((self.home / "gh.calls").exists())

    def test_symlink_gate_directory_is_ignored(self):
        self.fake_gh("CLOSED")
        self.gates.rmdir()
        target = self.root / "other-gates"
        target.mkdir()
        self.gates.symlink_to(target, target_is_directory=True)
        gate = self.arm()
        self.assertEqual(self.run_hook(), "")
        self.assertTrue(gate.exists())
        self.assertFalse((self.home / "gh.calls").exists())


if __name__ == "__main__":
    unittest.main()
