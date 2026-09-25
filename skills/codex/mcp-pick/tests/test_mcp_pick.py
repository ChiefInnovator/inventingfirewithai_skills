"""Behavioral checks; actual Codex config loads/writes use an isolated Codex home."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "mcp_pick.py"
SPEC = importlib.util.spec_from_file_location("mcp_pick", SCRIPT)
picker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(picker)


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="mcp-picker-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "codex-home"
        self.home.mkdir()
        self.project = self.root / "project"
        self.project.mkdir()
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        self.sibling = self.root / "other-project"
        self.sibling.mkdir()
        self.global_config = self.home / "config.toml"
        self.global_config.write_text(
            '[projects.' + json.dumps(str(self.project)) + ']\ntrust_level = "trusted"\n'
            '[mcp_servers.alpha]\ncommand = "echo"\nargs = ["SYNTHETIC_SECRET"]\n'
            '[mcp_servers."name.with.dots"]\ncommand = "echo"\nenabled = false\n'
        )
        self.original_global = self.global_config.read_bytes()
        self.target = self.project / ".codex" / "config.toml"
        self.env = patch.dict(os.environ, {"CODEX_HOME": str(self.home)})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.client = picker.Codex(self.project)
        self.addCleanup(self.client.close)

    def inventory(self):
        return picker.discover(self.client, self.project, "servers")

    def apply(self, mode, ids=()):
        inventory, response = self.inventory()
        keep = picker.selected_entries(inventory, mode, ids)
        return picker.apply_selection(self.client, self.project, inventory, response, keep)

    def runtime(self, project=None):
        result = subprocess.run(["codex", "mcp", "list", "--json"], cwd=project or self.project,
                                capture_output=True, text=True, check=True)
        return {row["name"]: row for row in json.loads(result.stdout)}

    def test_list_is_read_only(self):
        inventory, _ = self.inventory()
        states = {row["id"]: row["enabled"] for row in inventory["entries"]}
        self.assertTrue(states["mcp:alpha"])
        self.assertFalse(states["mcp:name.with.dots"])
        self.assertFalse(self.target.exists())
        self.assertEqual(self.original_global, self.global_config.read_bytes())
        self.assertNotIn("SYNTHETIC_SECRET", json.dumps(inventory))

    def test_keep_isolated_and_runtime_verified(self):
        result = self.apply("keep", ["mcp:name.with.dots"])
        self.assertTrue(result["changed"])
        local = tomllib.loads(self.target.read_text())
        self.assertEqual(local, {"mcp_servers": {"alpha": {"enabled": False}, "name.with.dots": {"enabled": True}}})
        runtime = self.runtime()
        self.assertFalse(runtime["alpha"]["enabled"])
        self.assertTrue(runtime["name.with.dots"]["enabled"])
        self.assertTrue(self.runtime(self.sibling)["alpha"]["enabled"])
        self.assertFalse(self.runtime(self.sibling)["name.with.dots"]["enabled"])
        self.assertEqual(self.original_global, self.global_config.read_bytes())
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o600)

    def test_comments_unrelated_settings_and_backup(self):
        self.target.parent.mkdir()
        original = '# local comment\nmodel_reasoning_effort = "low"\n[mcp_servers]\nalpha = { enabled = true, tool_timeout_sec = 91 } # preserve me\n'
        self.target.write_text(original)
        result = self.apply("none")
        written = self.target.read_text()
        self.assertIn("# local comment", written)
        self.assertIn("# preserve me", written)
        data = tomllib.loads(written)
        self.assertEqual(data["model_reasoning_effort"], "low")
        self.assertEqual(data["mcp_servers"]["alpha"]["tool_timeout_sec"], 91)
        self.assertEqual(Path(result["backup"]).read_text(), original)
        self.assertEqual(Path(result["backup"]).stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.original_global, self.global_config.read_bytes())

    def test_all_none_and_idempotency(self):
        self.apply("none")
        self.assertTrue(all(not row["enabled"] for row in self.runtime().values()))
        self.apply("all")
        self.assertTrue(all(row["enabled"] for row in self.runtime().values()))
        before = self.target.read_bytes()
        result = self.apply("all")
        self.assertFalse(result["changed"])
        self.assertIsNone(result["backup"])
        self.assertEqual(before, self.target.read_bytes())

    def test_stale_and_unknown_selection(self):
        inventory, _ = self.inventory()
        with self.assertRaises(picker.PickerError):
            picker.selected_entries(inventory, "keep", ["mcp:unknown"])
        self.target.parent.mkdir()
        self.target.write_text('model_reasoning_effort = "low"\n')
        result = subprocess.run([sys.executable, str(SCRIPT), "none", "--scope", "servers", "--project", str(self.project),
                                 "--expect", inventory["inventory_version"]], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("changed since review", result.stderr)
        self.assertEqual(self.target.read_text(), 'model_reasoning_effort = "low"\n')

    def test_change_after_discovery_is_preserved(self):
        self.target.parent.mkdir()
        self.target.write_text('# original\n')
        inventory, response = self.inventory()
        concurrent = '# concurrent edit\nmodel_reasoning_effort = "low"\n'
        self.target.write_text(concurrent)
        with self.assertRaises(picker.PickerError):
            picker.apply_selection(self.client, self.project, inventory, response, set())
        self.assertEqual(self.target.read_text(), concurrent)

    def test_untrusted_project_not_enabled(self):
        self.global_config.write_text(self.global_config.read_text().replace('trust_level = "trusted"', 'trust_level = "untrusted"'))
        with self.assertRaises(picker.PickerError):
            self.apply("none")
        self.assertFalse(self.target.exists())
        self.assertIn('trust_level = "untrusted"', self.global_config.read_text())

    def test_symlink_rejected(self):
        self.target.parent.mkdir()
        self.target.symlink_to(self.global_config)
        with self.assertRaises(picker.PickerError):
            picker.safe_target(self.project)
        self.assertEqual(self.original_global, self.global_config.read_bytes())

    def test_cli_documented_argument_order_and_dry_run(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "keep", "--project", str(self.project),
                                 "--scope", "servers", "--dry-run", "--json", "mcp:alpha"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["enabled"], ["mcp:alpha"])
        self.assertFalse(self.target.exists())

    def test_failed_verification_restores_original(self):
        self.target.parent.mkdir()
        self.target.write_text('# before\n')
        inventory, response = self.inventory()
        real_call = self.client.call
        def fail_after_write(method, params):
            value = real_call(method, params)
            if method == 'config/read' and 'enabled' in self.target.read_text():
                value = copy.deepcopy(value)
                value['config']['mcp_servers']['alpha']['enabled'] = True
            return value
        with patch.object(self.client, 'call', side_effect=fail_after_write):
            with self.assertRaises(picker.PickerError):
                picker.apply_selection(self.client, self.project, inventory, response, set())
        self.assertEqual(self.target.read_text(), '# before\n')

    def test_installed_plugin_server_control(self):
        market = self.root / 'market'
        metadata = market / '.agents' / 'plugins'
        metadata.mkdir(parents=True)
        plugin = market / 'plugins' / 'fixture'
        (plugin / '.codex-plugin').mkdir(parents=True)
        (metadata / 'marketplace.json').write_text(json.dumps({'name': 'test', 'plugins': [{
            'name': 'fixture', 'source': {'source': 'local', 'path': './plugins/fixture'},
            'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_USE'}}]}))
        (plugin / '.codex-plugin' / 'plugin.json').write_text(json.dumps({
            'name': 'fixture', 'version': '1.0.0', 'mcpServers': './.mcp.json'}))
        (plugin / '.mcp.json').write_text(json.dumps({'mcpServers': {'fixture_mcp': {'command': 'echo', 'args': ['fixture']}}}))
        with self.global_config.open('a') as stream:
            stream.write('\n[marketplaces.test]\nsource_type="local"\nsource=' + json.dumps(str(market)) + '\n')
        installed = subprocess.run(['codex', 'plugin', 'add', 'fixture@test', '--json'], cwd=self.project,
                                   capture_output=True, text=True)
        self.assertEqual(installed.returncode, 0, installed.stderr)
        self.assertIn('fixture_mcp', self.runtime())
        inventory, _ = self.inventory()
        self.assertIn('plugin:fixture@test/fixture_mcp', [x['id'] for x in inventory['entries']])
        self.apply('none')
        self.assertFalse(self.runtime()['fixture_mcp']['enabled'])

    def test_blocked_entries_preserve_inherited_settings(self):
        inventory, response = self.inventory()
        for entry in inventory['entries']:
            if entry['id'] == 'mcp:alpha':
                entry['blocked'] = 'parent disabled'
        picker.apply_selection(self.client, self.project, inventory, response, set())
        local = tomllib.loads(self.target.read_text())
        self.assertNotIn('alpha', local['mcp_servers'])
        self.assertTrue(self.runtime()['alpha']['enabled'])
        self.assertFalse(self.runtime()['name.with.dots']['enabled'])

    def test_all_blocked_inventory_does_not_create_config(self):
        inventory, response = self.inventory()
        for entry in inventory['entries']:
            entry['blocked'] = 'parent disabled'
        result = picker.apply_selection(self.client, self.project, inventory, response, set())
        self.assertFalse(result['changed'])
        self.assertFalse(self.target.exists())

    def test_app_preference_preserves_tool_policy(self):
        with self.global_config.open('a') as stream:
            stream.write('\n[apps.fixture]\nenabled=true\n[apps.fixture.tools."item.read"]\nenabled=false\n')
        response = self.client.call('config/read', {'cwd': str(self.project), 'includeLayers': True})
        entry = {'id': 'app:fixture', 'path': ['apps', 'fixture', 'enabled'], 'name': 'Fixture', 'enabled': True, 'blocked': None}
        inventory = {'entries': [entry], 'project_config_ignored': False}
        picker.apply_selection(self.client, self.project, inventory, response, set())
        config = self.client.call('config/read', {'cwd': str(self.project), 'includeLayers': True})['config']
        self.assertFalse(picker.setting(config, ['apps', 'fixture', 'enabled']))
        self.assertFalse(picker.setting(config, ['apps', 'fixture', 'tools', 'item.read', 'enabled']))


class DiscoveryTests(unittest.TestCase):
    def test_older_codex_rejected_before_starting_client(self):
        with patch.object(picker.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'codex-cli 0.147.0\n')), patch.object(picker.subprocess, 'Popen') as start:
            with self.assertRaisesRegex(picker.PickerError, '0.153.4'):
                picker.Codex(Path('/fake/project'))
            start.assert_not_called()

    def test_remote_plugin_uses_canonical_source_id(self):
        calls = []
        class Metadata:
            def installed_plugins(self):
                return [{'pluginId': 'display@test', 'name': 'display', 'marketplaceName': 'test',
                         'enabled': True, 'source': {'source': 'remote', 'id': 'canonical'}}]
            def call(self, method, params):
                if method == 'config/read':
                    return {'config': {}, 'layers': []}
                if method == 'plugin/list':
                    return {'marketplaces': []}
                if method == 'plugin/read':
                    calls.append(params)
                    return {'plugin': {'mcpServers': [], 'apps': [{'id': 'actual_id', 'name': 'App'}]}}
                raise AssertionError(method)
        inventory, _ = picker.discover(Metadata(), Path('/fake/project'), 'all')
        self.assertEqual(calls, [{'pluginName': 'canonical', 'remoteMarketplaceName': 'test'}])
        self.assertEqual(inventory['entries'][0]['id'], 'app:actual_id')

    def test_plugin_paths_shadowing_and_installed_apps(self):
        class Metadata:
            def installed_plugins(self):
                return []
            def call(self, method, params):
                if method == 'config/read':
                    return {'config': {'mcp_servers': {'shadow': {'command': 'echo', 'enabled': False}},
                                       'apps': {'connected': {'enabled': False}}}, 'layers': []}
                if method == 'plugin/list':
                    return {'marketplaces': [{'name': 'test', 'path': '/fake/marketplace', 'plugins': [
                        {'id': 'bundle@test', 'name': 'bundle', 'installed': True, 'enabled': True}]}]}
                if method == 'plugin/read':
                    return {'plugin': {'mcpServers': ['shadow', 'useful'], 'apps': [
                        {'id': 'connected', 'name': 'First'}, {'id': 'second', 'name': 'Second'}]}}
                raise AssertionError(method)
        inventory, _ = picker.discover(Metadata(), Path('/fake/project'), 'all')
        entries = {row['id']: row for row in inventory['entries']}
        self.assertEqual(entries['plugin:bundle@test/useful']['path'], ['plugins', 'bundle@test', 'mcp_servers', 'useful', 'enabled'])
        self.assertFalse(entries['plugin:bundle@test/shadow']['enabled'])
        self.assertIsNotNone(entries['plugin:bundle@test/shadow']['blocked'])
        self.assertFalse(entries['app:connected']['enabled'])
        self.assertIn('app:second', entries)
        self.assertNotIn('app:unconnected', entries)
        with self.assertRaises(picker.PickerError):
            picker.selected_entries(inventory, 'keep', ['plugin:bundle@test/shadow'])


if __name__ == '__main__':
    unittest.main()
