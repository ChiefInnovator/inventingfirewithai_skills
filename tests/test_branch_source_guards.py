"""Execute the source gates that GitHub runs, without creating test PRs."""

import os
from pathlib import Path
import subprocess
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "owner/skills"


def workflow(name):
    return yaml.safe_load((ROOT / ".github/workflows" / name).read_text())


def run_guard(name, job, branch, repository=REPOSITORY):
    script = workflow(name)["jobs"][job]["steps"][0]["run"]
    env = dict(os.environ, HEAD_REF=branch, HEAD_REPO=repository,
               GITHUB_REPOSITORY=REPOSITORY)
    return subprocess.run(["bash", "--noprofile", "--norc", "-ec", script],
                          env=env, capture_output=True, text=True, timeout=5)


class BranchSourceGuardTests(unittest.TestCase):
    def test_main_accepts_only_same_repository_develop(self):
        self.assertEqual(run_guard("main-source-guard.yml", "develop-only", "develop").returncode, 0)
        for branch, repository in (("main", REPOSITORY), ("feature/example", REPOSITORY),
                                   ("develop", "fork/skills"), ("", REPOSITORY)):
            with self.subTest(branch=branch, repository=repository):
                self.assertNotEqual(run_guard("main-source-guard.yml", "develop-only",
                                              branch, repository).returncode, 0)

    def test_develop_accepts_existing_feature_branch_conventions(self):
        for prefix in ("feature", "feat", "fix", "bugfix", "hotfix", "improve", "chore",
                       "docs", "test", "refactor", "perf", "build", "ci", "style"):
            with self.subTest(prefix=prefix):
                self.assertEqual(run_guard("develop-source-guard.yml", "feature-only",
                                           prefix + "/example").returncode, 0)

    def test_develop_rejects_protected_bare_empty_and_fork_sources(self):
        for branch, repository in (("main", REPOSITORY), ("master", REPOSITORY),
                                   ("develop", REPOSITORY), ("example", REPOSITORY),
                                   ("feature/", REPOSITORY), ("", REPOSITORY),
                                   ("feature/example", "fork/skills")):
            with self.subTest(branch=branch, repository=repository):
                self.assertNotEqual(run_guard("develop-source-guard.yml", "feature-only",
                                              branch, repository).returncode, 0)

    def test_develop_guard_uses_trusted_base_without_running_pr_code(self):
        data = workflow("develop-source-guard.yml")
        triggers = data.get("on", data.get(True))
        self.assertEqual(set(triggers), {"pull_request_target"})
        event = triggers["pull_request_target"]
        self.assertEqual(event["branches"], ["develop"])
        self.assertTrue({"opened", "edited", "reopened", "synchronize", "ready_for_review"}.issubset(event["types"]))
        self.assertNotIn("paths", event)
        self.assertNotIn("paths-ignore", event)
        self.assertEqual(data["permissions"], {})
        self.assertTrue(all("uses" not in step for step in data["jobs"]["feature-only"]["steps"]))


if __name__ == "__main__":
    unittest.main()
