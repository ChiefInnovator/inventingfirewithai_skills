"""Keep shared Slam resources aligned without erasing host-specific entrypoints."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / "skills"
CLIENTS = ("codex", "claude", "copilot")


def resources(client, directory):
    root = ROOT / client / "slam" / directory
    return {str(path.relative_to(root)): path.read_bytes()
            for path in root.rglob("*") if path.is_file()
            and "__pycache__" not in path.parts and path.suffix != ".pyc"}


class SlamPackageParityTests(unittest.TestCase):
    def test_all_clients_bundle_the_same_cleanup_helpers(self):
        expected = resources("codex", "scripts")
        self.assertEqual(set(expected), {"check_cleanup.py", "delete_remote_branch.py"})
        for client in CLIENTS[1:]:
            with self.subTest(client=client):
                self.assertEqual(resources(client, "scripts"), expected)

    def test_shared_phases_match_with_explicit_host_exceptions(self):
        expected = resources("codex", "references")
        for client in CLIENTS[1:]:
            with self.subTest(client=client):
                actual = resources(client, "references")
                self.assertEqual(set(actual) - set(expected),
                                 {"phase-g.md"} if client == "claude" else set())
                self.assertFalse(set(expected) - set(actual))
                for name, content in expected.items():
                    # PR attribution wording and Claude gate reporting are host-specific.
                    if name == "phase-4.md" or (client == "claude" and name == "phase-report.md"):
                        continue
                    with self.subTest(resource=name):
                        self.assertEqual(actual[name], content)


if __name__ == "__main__":
    unittest.main()
