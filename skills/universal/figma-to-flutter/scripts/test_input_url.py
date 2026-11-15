import unittest
from input_url import resolve


class UrlTests(unittest.TestCase):
    ledger = {'fileKey': 'OriginalFile', 'screens': {
        'screen': {'nodeId': '1:2', 'flutter': {'path': 'design/flutter/screen/'}}}}

    def test_same_url_updates_existing_slug(self):
        result = resolve('https://www.figma.com/design/OriginalFile/Name?node-id=1-2&m=dev', self.ledger)
        self.assertEqual(result['action'], 'update')
        self.assertEqual(result['slug'], 'screen')

    def test_encoded_original_id_is_retained(self):
        self.assertEqual(resolve('https://figma.com/file/OriginalFile/Name?node-id=1%3A2', self.ledger)['nodeId'], '1:2')

    def test_new_node_produces_new_screen(self):
        self.assertEqual(resolve('https://figma.com/design/OriginalFile/Name?node-id=1-9', self.ledger)['action'], 'new-screen')

    def test_nested_instance_path_is_one_original_node(self):
        url = 'https://figma.com/design/OriginalFile/Name?node-id=I1-10%3B20-30'
        result = resolve(url, self.ledger)
        self.assertEqual(result['nodeId'], 'I1:10;20:30')
        self.assertEqual(result['inputUrl'], url)

    def test_multiple_selected_nodes_and_empty_ids_are_rejected(self):
        for query in ('node-id=1-2%3B3-4', 'node-id=1-2,3-4',
                      'node-id=1-2&node-id=3-4', 'node-id='):
            with self.assertRaises(ValueError):
                resolve('https://figma.com/design/OriginalFile/Name?' + query, self.ledger)

    def test_same_node_in_a_different_file_is_not_an_update(self):
        result = resolve('https://figma.com/design/OtherFile/Name?node-id=1-2', self.ledger)
        self.assertEqual(result['action'], 'new-screen')
        self.assertIsNone(result['slug'])

    def test_branch_identity_uses_branch_key(self):
        result = resolve('https://figma.com/design/OriginalFile/branch/BranchFile/Name?node-id=1-2', self.ledger)
        self.assertEqual(result['fileKey'], 'BranchFile')
        self.assertEqual(result['parentFileKey'], 'OriginalFile')
        self.assertEqual(result['action'], 'new-screen')

    def test_file_link_does_not_guess_a_node(self):
        result = resolve('https://figma.com/design/OriginalFile/Name', self.ledger)
        self.assertIsNone(result['nodeId'])
        self.assertEqual(result['action'], 'select-frame')

    def test_wrong_host_or_node_is_rejected(self):
        for url in ('https://figma.com.evil/design/key?node-id=1-2',
                    'https://figma.com/design/key?node-id=broken'):
            with self.assertRaises(ValueError):
                resolve(url, self.ledger)


if __name__ == '__main__':
    unittest.main()
