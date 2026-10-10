import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location('inventory',
    Path(__file__).resolve().parents[1] / 'scripts/inventory.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class InventoryTests(unittest.TestCase):
    def test_only_names_and_enablement_leave_inventory(self):
        data = {'mcpServers': {
            'z': {'enabled': False, 'env': {'TOKEN': 'secret'}, 'url': 'private'},
            'a': {'enabled': True, 'command': 'secret', 'args': ['secret']}}}
        self.assertEqual(MODULE.summarize(data), [
            {'name': 'a', 'enabled': True}, {'name': 'z', 'enabled': False}])

    def test_schema_and_unknown_states_fail_closed(self):
        for data in ([], {}, {'mcpServers': []},
                     {'mcpServers': {'a': {'enabled': 'true'}}},
                     {'mcpServers': {'a': {}}}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                MODULE.summarize(data)

    def test_empty_inventory_is_valid(self):
        self.assertEqual(MODULE.summarize({'mcpServers': {}}), [])


if __name__ == '__main__':
    unittest.main()
