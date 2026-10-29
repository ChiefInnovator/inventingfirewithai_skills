"""Exercise the Claude /slam ship-gate Stop hook against a fake gh."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest

SKILL = Path(__file__).resolve().parents[1] / "skills/claude/slam/SKILL.md"


def hook_command():
    """Return the Stop hook's command block from the SKILL.md frontmatter."""
    front = SKILL.read_text().split("\n---\n", 1)[0]
    block = front.split("command: |\n", 1)[1]
    return textwrap.dedent(block)


class ShipGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="slam-gate-test-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.bin = self.home / "bin"
        self.bin.mkdir()
        self.gates = self.home / ".claude/slam-gates"
        self.gates.mkdir(parents=True)
        self.session = "3f2a9c1e-test-session"

    def fake_gh(self, state=None, fail=False):
        gh = self.bin / "gh"
        body = "exit 1" if fail else f"echo {state}"
        gh.write_text(f"#!/bin/sh\n{body}\n")
        gh.chmod(0o755)

    def arm(self, pr="4", repo="Owner/repo"):
        gate = self.gates / self.session
        gate.write_text(f"repo={repo}\npr={pr}\n")
        return gate

    def run_hook(self, session=None):
        payload = json.dumps({
            "session_id": session if session is not None else self.session,
            "hook_event_name": "Stop",
            "stop_hook_active": False,
        })
        env = {"HOME": str(self.home), "PATH": f"{self.bin}:/usr/bin:/bin"}
        result = subprocess.run(["sh", "-c", hook_command()], input=payload,
                                capture_output=True, text=True, env=env, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
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

    def test_closed_pr_allows_stop_and_clears_gate(self):
        self.fake_gh("CLOSED")
        gate = self.arm()
        self.assertEqual(self.run_hook(), "")
        self.assertFalse(gate.exists())

    def test_gh_failure_fails_open(self):
        self.fake_gh(fail=True)
        self.arm()
        self.assertEqual(self.run_hook(), "")

    def test_bad_pr_number_fails_open(self):
        self.fake_gh("OPEN")
        self.arm(pr="4; rm -rf /")
        self.assertEqual(self.run_hook(), "")

    def test_other_sessions_gate_is_ignored(self):
        self.fake_gh("OPEN")
        self.arm()
        self.assertEqual(self.run_hook(session="another-session"), "")
        self.assertEqual(self.run_hook(session=""), "")


if __name__ == "__main__":
    unittest.main()
