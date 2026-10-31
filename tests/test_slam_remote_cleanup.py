"""Guarded branch deletion against real disposable Git repositories and hooks."""

import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/codex/slam/scripts/delete_remote_branch.py"


class RemoteCleanupTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="slam-remote-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.origin = self.root / "origin.git"
        self.repo = self.root / "repo"
        self.environment = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull,
                            "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0",
                            "PYTHONDONTWRITEBYTECODE": "1"}
        self.command("git", "init", "--bare", "--initial-branch=main", str(self.origin))
        self.command("git", "init", "--initial-branch=main", str(self.repo))
        self.git("config", "user.name", "Cleanup Test")
        self.git("config", "user.email", "cleanup@example.invalid")
        self.git("remote", "add", "origin", str(self.origin))
        (self.repo / "work.txt").write_text("base\n")
        self.git("add", "work.txt")
        self.git("commit", "-m", "base")
        self.git("switch", "-c", "feature/sample")
        (self.repo / "work.txt").write_text("feature\n")
        self.git("commit", "-am", "feature")
        self.head = self.git("rev-parse", "HEAD")
        self.git("switch", "main")
        self.git("merge", "--no-ff", "feature/sample", "-m", "merge feature")
        self.merge = self.git("rev-parse", "HEAD")
        self.git("push", "origin", "main", "feature/sample")
        self.git("fetch", "origin")

    def command(self, *args):
        return subprocess.run(args, capture_output=True, text=True, check=True,
                              timeout=15, env=self.environment).stdout.strip()

    def git(self, *args):
        return self.command("git", "-C", str(self.repo), *args)

    def remote_head(self, branch="feature/sample"):
        result = self.git("ls-remote", "--heads", "origin", "refs/heads/" + branch)
        return result.split()[0] if result else None

    def delete(self, **overrides):
        values = {"repo-dir": str(self.repo), "base": "main", "branch": "feature/sample",
                  "head": self.head, "merge-commit": self.merge,
                  "expected-origin": str(self.origin)}
        values.update(overrides)
        args = [sys.executable, str(SCRIPT)]
        for name, value in values.items():
            args.extend(["--" + name, value])
        return subprocess.run(args, capture_output=True, text=True, timeout=20,
                              env=self.environment)

    def hook(self, body, name="pre-push", directory=None):
        directory = directory or self.repo / ".git/hooks"
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / name
        path.write_text("#!/bin/sh\nset -eu\n" + body + "\n")
        path.chmod(0o755)
        return path

    def advance_remote(self):
        self.git("switch", "-c", "peer", "feature/sample")
        (self.repo / "work.txt").write_text("peer work\n")
        self.git("commit", "-am", "peer work")
        new_head = self.git("rev-parse", "HEAD")
        self.git("push", "origin", "peer")
        self.git("switch", "main")
        return new_head

    def assert_refused(self, result):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stderr)["remote_cleanup"], "refused")

    def test_exact_merged_remote_deleted_without_deleting_local_branch(self):
        config = self.git("config", "--local", "--list")
        result = self.delete()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["deletion_performed"])
        self.assertIsNone(self.remote_head())
        self.assertEqual(self.git("rev-parse", "feature/sample"), self.head)
        self.assertEqual(self.git("config", "--local", "--list"), config)
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_missing_remote_is_idempotent(self):
        self.git("push", "origin", ":refs/heads/feature/sample")
        result = self.delete()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout),
                         {"remote_absent": True, "deletion_performed": False, "already_absent": True})

    def test_advanced_remote_is_preserved(self):
        new_head = self.advance_remote()
        self.command("git", "--git-dir", str(self.origin), "update-ref",
                     "refs/heads/feature/sample", new_head, self.head)
        self.assert_refused(self.delete())
        self.assertEqual(self.remote_head(), new_head)

    def test_update_after_advertisement_is_rejected_by_receive_pack(self):
        new_head = self.advance_remote()
        marker = self.root / "hook-ran"
        self.hook("cat >/dev/null\n" +
                  "git --git-dir=" + shlex.quote(str(self.origin)) + " update-ref refs/heads/feature/sample " +
                  new_head + " " + self.head + "\n" +
                  "printf ran > " + shlex.quote(str(marker)))
        result = self.delete()
        self.assert_refused(result)
        self.assertTrue(marker.exists(), "Existing pre-push hook must run after advertisement")
        self.assertEqual(self.remote_head(), new_head)

    def test_existing_pre_push_receives_original_arguments_and_input(self):
        observed = self.root / "observed"
        self.hook("printf '%s\\n%s\\n' \"$1\" \"$2\" > " + shlex.quote(str(observed)) +
                  "\ncat >> " + shlex.quote(str(observed)))
        result = self.delete()
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = observed.read_text().splitlines()
        self.assertEqual(lines[:2], ["origin", str(self.origin)])
        self.assertEqual(lines[2].split(),
                         ["(delete)", "0" * 40, "refs/heads/feature/sample", self.head])

    def test_existing_hook_failure_prevents_deletion(self):
        self.hook("cat >/dev/null\nexit 7")
        self.assert_refused(self.delete())
        self.assertEqual(self.remote_head(), self.head)

    def test_custom_hook_path_and_other_hooks_are_preserved(self):
        directory = self.repo / ".git/custom hooks"
        sibling = directory / "helper.txt"
        directory.mkdir()
        sibling.write_text("preserved\n")
        observed = self.root / "resource"
        transaction = self.root / "transaction"
        self.hook('cat "$(dirname "$0")/helper.txt" > ' + shlex.quote(str(observed)) +
                  "\ncat >/dev/null", directory=directory)
        self.hook("printf '%s\\n' \"$1\" >> " + shlex.quote(str(transaction)) +
                  "\ncat >/dev/null", name="reference-transaction", directory=directory)
        self.git("config", "core.hooksPath", str(directory))
        config = self.git("config", "--local", "--list")
        result = self.delete()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(observed.read_text(), "preserved\n")
        self.assertIn("committed", transaction.read_text())
        self.assertEqual(self.git("config", "--local", "--list"), config)

    def test_unexpected_push_destination_is_refused(self):
        self.assert_refused(self.delete(**{"expected-origin": str(self.root / "wrong.git")}))
        self.assertEqual(self.remote_head(), self.head)

    def test_transaction_hook_retains_parent_relative_resources_and_tracking_state(self):
        directory = self.repo / ".git/project hooks"
        policy = directory.parent / "policy.txt"
        policy.write_text("parent-policy\n")
        observed = self.root / "policy-observed"
        invocation = self.root / "hook-invocation"
        hook = self.hook('cat "$(dirname "$0")/../policy.txt" >> ' +
                         shlex.quote(str(observed)) +
                         "\nprintf '%s\\n' \"$0\" > " + shlex.quote(str(invocation)) +
                         "\ncat >/dev/null", name="reference-transaction", directory=directory)
        self.git("config", "core.hooksPath", str(directory))
        # Establish that the real hook works before the helper introduces forwarding hooks.
        self.git("update-ref", "refs/heads/policy-check", self.merge)
        self.git("update-ref", "-d", "refs/heads/policy-check", self.merge)
        self.assertEqual(invocation.read_text().strip(), str(hook))
        observed.unlink()
        result = self.delete()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIsNone(self.remote_head())
        self.assertEqual(Path(invocation.read_text().strip()).resolve(), hook.resolve())
        self.assertTrue(observed.read_text().splitlines())
        self.assertEqual(set(observed.read_text().splitlines()), {"parent-policy"})
        tracking = subprocess.run(["git", "-C", str(self.repo), "show-ref", "--verify", "--quiet",
                                   "refs/remotes/origin/feature/sample"], capture_output=True,
                                  timeout=5, env=self.environment)
        self.assertEqual(tracking.returncode, 1, "Successful deletion must remove its tracking ref")
        self.assertEqual(self.git("rev-parse", "feature/sample"), self.head)

    def test_multiple_push_destinations_are_refused(self):
        self.git("remote", "set-url", "--add", "--push", "origin", str(self.origin))
        self.git("remote", "set-url", "--add", "--push", "origin", str(self.root / "other.git"))
        self.assert_refused(self.delete())
        self.assertEqual(self.remote_head(), self.head)

    def test_dirty_worktree_is_preserved(self):
        path = self.repo / "user-work.txt"
        path.write_text("preserve\n")
        self.assert_refused(self.delete())
        self.assertEqual(path.read_text(), "preserve\n")
        self.assertEqual(self.remote_head(), self.head)

    def test_protected_branch_is_refused(self):
        self.assert_refused(self.delete(branch="main"))
        self.assertEqual(self.remote_head("main"), self.merge)

    def test_mismatched_local_head_is_refused(self):
        self.git("switch", "feature/sample")
        (self.repo / "work.txt").write_text("new local work\n")
        self.git("commit", "-am", "new local work")
        self.git("switch", "main")
        self.assert_refused(self.delete())
        self.assertEqual(self.remote_head(), self.head)

    def test_checked_out_feature_worktree_is_refused(self):
        other = self.root / "other-worktree"
        self.git("worktree", "add", str(other), "feature/sample")
        self.assert_refused(self.delete())
        self.assertEqual(self.remote_head(), self.head)

    def test_guard_rejects_extra_refs_and_mismatched_advertisement(self):
        state = self.root / "state.json"
        state.write_text(json.dumps({"branch": "feature/sample", "head": self.head,
                                     "origin": str(self.origin), "originalHook": None}))
        expected = "(delete) " + "0" * 40 + " refs/heads/feature/sample " + self.head + "\n"
        for data in (expected + expected, expected.replace(self.head, "1" * 40), "",
                     expected.replace("refs/heads/feature/sample", "refs/heads/main")):
            with self.subTest(data=data):
                result = subprocess.run([sys.executable, str(SCRIPT), "--hook-state", str(state),
                                         "origin", str(self.origin)], input=data, capture_output=True,
                                        text=True, timeout=5, env=self.environment)
                self.assertEqual(result.returncode, 1)
        self.assertEqual(self.remote_head(), self.head)


if __name__ == "__main__":
    unittest.main()
