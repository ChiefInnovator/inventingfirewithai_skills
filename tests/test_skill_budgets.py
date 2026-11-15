"""Keep every skill a single shared package with a bounded entrypoint.

Budgets are whole-file SKILL.md characters (about four per token), the text a
host reads on every invocation. Raise one only with a stated reason.
"""

from pathlib import Path
import unittest

import yaml

from test_travel_packages import check_links

SKILLS = Path(__file__).resolve().parents[1] / "skills"
BUDGETS = {
    "figma-to-flutter": 9000,
    "mcp-pick": 2000,
    "pragmatic-coder": 4000,
    "slam": 9000,  # includes the 3 KB Claude Stop hook in frontmatter
    "travel-like-a-local": 6500,
}


class SkillPackageTests(unittest.TestCase):
    def test_every_skill_is_one_shared_package(self):
        self.assertEqual([path.name for path in SKILLS.iterdir() if not path.name.startswith(".")], ["universal"])
        self.assertEqual({path.name for path in (SKILLS / "universal").iterdir() if path.is_dir()}, set(BUDGETS))

    def test_entrypoints_are_valid_named_and_within_budget(self):
        for name, budget in BUDGETS.items():
            with self.subTest(skill=name):
                folder = SKILLS / "universal" / name
                content = (folder / "SKILL.md").read_text(encoding="utf-8")
                metadata = yaml.safe_load(content.split("\n---\n", 1)[0].removeprefix("---\n"))
                self.assertEqual(metadata["name"], name)
                self.assertTrue(metadata["description"].strip())
                self.assertLessEqual(len(content), budget)
                interface = yaml.safe_load((folder / "agents" / "openai.yaml").read_text())["interface"]
                self.assertTrue(interface["display_name"].strip())

    def test_local_links_and_anchors_resolve(self):
        for name in BUDGETS:
            with self.subTest(skill=name):
                check_links(SKILLS / "universal" / name)


if __name__ == "__main__":
    unittest.main()
