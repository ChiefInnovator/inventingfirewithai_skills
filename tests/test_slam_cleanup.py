"""Exercise cleanup gates against disposable local Git repositories."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/codex/slam/scripts/check_cleanup.py"
SPEC = importlib.util.spec_from_file_location("slam_cleanup", SCRIPT)
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="slam-cleanup-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.origin = self.root / "origin.git"
        self.repo = self.root / "repo"
        self.env = patch.dict(os.environ, {
            "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
        })
        self.env.start()
        self.addCleanup(self.env.stop)
        self.command("git", "init", "--bare", "--initial-branch=main", str(self.origin))
        self.command("git", "init", "--initial-branch=main", str(self.repo))
        self.git("config", "user.name", "Slam Test")
        self.git("config", "user.email", "slam@example.invalid")
        self.git("remote", "add", "origin", str(self.origin))
        (self.repo / "sample.txt").write_text("base\n")
        self.git("add", "sample.txt")
        self.git("commit", "-m", "base")
        self.git("switch", "-c", "feature/sample")
        (self.repo / "sample.txt").write_text("feature\n")
        self.git("commit", "-am", "feature")
        self.head = self.git("rev-parse", "HEAD")
        self.git("switch", "main")

    def command(self, *args):
        result = subprocess.run(args, capture_output=True, text=True, check=True, timeout=15)
        return result.stdout.strip()

    def git(self, *args):
        return self.command("git", "-C", str(self.repo), *args)

    def land(self, squash=False):
        if squash:
            self.git("merge", "--squash", "feature/sample")
            self.git("commit", "-m", "squash feature")
        else:
            self.git("merge", "--no-ff", "feature/sample", "-m", "merge feature")
        self.merge = self.git("rev-parse", "HEAD")
        self.git("push", "origin", "main", "feature/sample")
        self.git("fetch", "origin", "--prune")

    def check(self, **overrides):
        args = dict(root=self.repo, base="main", branch="feature/sample",
                    head=self.head, merge_commit=self.merge)
        args.update(overrides)
        return GUARD.check_cleanup(**args)

    def test_merged_branch_passes_without_mutating_refs(self):
        self.land()
        before = self.git("show-ref")
        result = self.check()
        self.assertTrue(result["local_candidate_exists"])
        self.assertTrue(result["remote_candidate_exists"])
        self.assertFalse(result["deletion_performed"])
        self.assertEqual(before, self.git("show-ref"))

    def test_protected_and_unsafe_names_refused(self):
        self.land()
        for branch in ("", "main", "master", "develop", "-bad", "origin/main", "refs/heads/x", "bad..name"):
            with self.subTest(branch=branch), self.assertRaises(GUARD.Refusal):
                self.check(branch=branch)
        with self.assertRaisesRegex(GUARD.Refusal, "protected"):
            self.check(protected=["feature/sample"])

    def test_custom_base_is_protected(self):
        self.land()
        with self.assertRaisesRegex(GUARD.Refusal, "protected"):
            self.check(base="release/stable", branch="release/stable")

    def test_dirty_tree_refused(self):
        self.land()
        (self.repo / "user-work.txt").write_text("preserve this\n")
        with self.assertRaisesRegex(GUARD.Refusal, "dirty"):
            self.check()

    def test_wrong_checkout_refused(self):
        self.land()
        self.git("switch", "feature/sample")
        with self.assertRaisesRegex(GUARD.Refusal, "Checkout"):
            self.check()

    def test_new_local_feature_work_refused(self):
        self.land()
        self.git("switch", "feature/sample")
        self.git("commit", "--allow-empty", "-m", "new user work")
        self.git("switch", "main")
        with self.assertRaisesRegex(GUARD.Refusal, "Local feature"):
            self.check()

    def test_new_remote_feature_work_refused_even_with_stale_tracking_ref(self):
        self.land()
        self.git("switch", "-c", "peer-work", "feature/sample")
        self.git("commit", "--allow-empty", "-m", "remote work")
        self.git("push", "origin", "peer-work:feature/sample")
        self.git("switch", "main")
        self.git("update-ref", "refs/remotes/origin/feature/sample", self.head)
        with self.assertRaisesRegex(GUARD.Refusal, "Remote feature"):
            self.check()

    def test_stale_remote_base_refused(self):
        self.land()
        self.git("switch", "-c", "peer-base", "main")
        self.git("commit", "--allow-empty", "-m", "remote base work")
        self.git("push", "origin", "peer-base:main")
        self.git("switch", "main")
        self.git("update-ref", "refs/remotes/origin/main", self.merge)
        with self.assertRaisesRegex(GUARD.Refusal, "Remote base changed"):
            self.check()

    def test_unsynced_local_base_refused(self):
        self.land()
        self.git("commit", "--allow-empty", "-m", "local base work")
        with self.assertRaisesRegex(GUARD.Refusal, "not exactly synchronized"):
            self.check()

    def test_other_worktree_refused(self):
        self.land()
        self.git("worktree", "add", str(self.root / "other"), "feature/sample")
        with self.assertRaisesRegex(GUARD.Refusal, "worktree"):
            self.check()

    def test_squash_does_not_pass_ancestry_gate(self):
        self.land(squash=True)
        with self.assertRaises(GUARD.Refusal):
            self.check()

    def test_missing_remote_branch_is_reported(self):
        self.land()
        self.git("push", "origin", "--delete", "feature/sample")
        self.git("fetch", "origin", "--prune")
        result = self.check()
        self.assertFalse(result["remote_candidate_exists"])
        self.assertTrue(result["local_candidate_exists"])

    def test_missing_local_branch_is_reported(self):
        self.land()
        self.git("branch", "-d", "feature/sample")
        result = self.check()
        self.assertFalse(result["local_candidate_exists"])
        self.assertTrue(result["remote_candidate_exists"])

    def test_invalid_sha_refused(self):
        self.land()
        with self.assertRaisesRegex(GUARD.Refusal, "full captured"):
            self.check(head="HEAD")

    def test_unavailable_remote_refused(self):
        self.land()
        self.git("remote", "set-url", "origin", str(self.root / "missing-origin"))
        with self.assertRaises(GUARD.Refusal):
            self.check()

    def test_cli_returns_json_without_deletion(self):
        self.land()
        output = self.command(sys.executable, str(SCRIPT), "--repo-dir", str(self.repo),
                              "--base", "main", "--branch", "feature/sample",
                              "--head", self.head, "--merge-commit", self.merge)
        self.assertEqual(json.loads(output)["git_checks"], "passed")
        self.assertEqual(self.head, self.git("rev-parse", "feature/sample"))


if __name__ == "__main__":
    unittest.main()
