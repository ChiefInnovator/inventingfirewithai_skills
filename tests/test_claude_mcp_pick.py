"""Run the Claude picker against disposable configuration and CLI fixtures."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/universal/mcp-pick/scripts/claude_mcp_pick.sh'


class ClaudePickerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.config = self.root / 'config.json'
        self.original = {'unrelated': True, 'projects': {str(self.root): {
            'disabledMcpServers': ['unseen'], 'other': 'preserve'}}}
        self.config.write_text(json.dumps(self.original))
        self.inventory = self.root / 'servers'
        self.inventory.write_text('http-server\n')
        self.env = {**os.environ, 'MCP_CFG': str(self.config),
                    'MCP_SERVER_LIST': str(self.inventory),
                    'MCP_CACHE_DIR': str(self.root / 'cache')}

    def run_picker(self, *args):
        return subprocess.run(['bash', str(SCRIPT), *args], cwd=self.root,
                              env=self.env, capture_output=True, text=True, check=True)

    def test_modes_preserve_unseen_disabled_servers(self):
        for mode, args, expected in [('none', [], ['http-server', 'unseen']),
                                     ('all', [], ['unseen']),
                                     ('keep', ['http-server'], ['unseen'])]:
            with self.subTest(mode=mode):
                self.config.write_text(json.dumps(self.original))
                self.run_picker(mode, *args)
                actual = json.loads(self.config.read_text())
                self.assertEqual(actual['projects'][str(self.root)]['disabledMcpServers'], expected)
                self.assertEqual(actual['projects'][str(self.root)]['other'], 'preserve')
                self.assertTrue(actual['unrelated'])

    def test_discovery_includes_stdio_and_plugin_names(self):
        binary = self.root / 'claude'
        binary.write_text("#!/bin/sh\ncat <<'EOF'\nChecking MCP server health...\nhttp-server: https://example.invalid/mcp (HTTP) - Connected\nstdio-server: node server.js - Connected\nplugin:bundle:server: /usr/bin/tool - Failed to connect\nclaude.ai Calendar: https://example.invalid/calendar (HTTP) - Connected\nEOF\n")
        binary.chmod(0o700)
        self.env.pop('MCP_SERVER_LIST')
        self.env['PATH'] = str(self.root) + os.pathsep + self.env['PATH']
        self.run_picker('none')
        disabled = json.loads(self.config.read_text())['projects'][str(self.root)]['disabledMcpServers']
        self.assertEqual(disabled, ['claude.ai Calendar', 'http-server',
                                    'plugin:bundle:server', 'stdio-server', 'unseen'])

    def test_repeated_writes_keep_distinct_backups(self):
        self.run_picker('none')
        self.run_picker('all')
        backups = list(self.root.glob('config.json.bak.*'))
        self.assertEqual(len(backups), 2)
        self.assertTrue(all(json.loads(p.read_text()) for p in backups))

    def test_only_three_newest_backups_are_kept(self):
        for index, mode in enumerate(['none', 'all', 'none', 'all', 'none']):
            self.run_picker(mode)
            for backup in self.root.glob('config.json.bak.*'):
                if not backup.name.endswith('.aged'):
                    aged = backup.with_name(backup.name + '.aged')
                    backup.rename(aged)
                    os.utime(aged, (index, index))
        self.assertEqual(len(list(self.root.glob('config.json.bak.*'))), 3)

    def test_unchanged_selection_writes_no_config_or_backup(self):
        self.run_picker('none')
        before = self.config.read_bytes()
        result = self.run_picker('none')
        self.assertIn('unchanged', result.stdout)
        self.assertEqual(self.config.read_bytes(), before)
        self.assertEqual(len(list(self.root.glob('config.json.bak.*'))), 1)

    def test_write_reuses_names_saved_by_list(self):
        binary = self.root / 'claude'
        calls = self.root / 'calls'
        binary.write_text("#!/bin/sh\necho x >> '%s'\necho 'http-server: https://example.invalid/mcp (HTTP) - Connected'\n" % calls)
        binary.chmod(0o700)
        self.env.pop('MCP_SERVER_LIST')
        self.env['PATH'] = str(self.root) + os.pathsep + self.env['PATH']
        self.run_picker('list')
        self.run_picker('all')
        self.assertEqual(calls.read_text().count('x'), 1)
        self.run_picker('list')
        self.assertEqual(calls.read_text().count('x'), 2)

    def test_failed_replace_preserves_live_config(self):
        before = self.config.read_bytes()
        wrapper = self.root / 'python3'
        wrapper.write_text('#!' + sys.executable + '\n'
                           'import os,sys\n'
                           'def fail(*args): raise OSError("injected replace failure")\n'
                           'os.replace=fail\n'
                           'exec(sys.argv[2])\n')
        wrapper.chmod(0o700)
        self.env['PATH'] = str(self.root) + os.pathsep + self.env['PATH']
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_picker('none')
        self.assertEqual(self.config.read_bytes(), before)
        self.assertEqual(list(self.root.glob('.mcp-pick-*')), [])

    def test_concurrent_config_edit_is_preserved(self):
        wrapper = self.root / 'python3'
        wrapper.write_text('#!' + sys.executable + '\n'
                           'import os,sys,json\n'
                           'real_fsync=os.fsync\n'
                           'def edit(fd):\n'
                           '    real_fsync(fd)\n'
                           '    p=os.environ["MCP_CFG"]\n'
                           '    d=json.load(open(p)); d["concurrent"]=True\n'
                           '    with open(p,"w") as f: json.dump(d,f)\n'
                           'os.fsync=edit\n'
                           'exec(sys.argv[2])\n')
        wrapper.chmod(0o700)
        self.env['PATH'] = str(self.root) + os.pathsep + self.env['PATH']
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_picker('none')
        expected = {**self.original, 'concurrent': True}
        self.assertEqual(json.loads(self.config.read_text()), expected)
        self.assertEqual(list(self.root.glob('.mcp-pick-*')), [])

    def test_list_is_read_only(self):
        before = self.config.read_bytes()
        self.run_picker('list')
        self.assertEqual(self.config.read_bytes(), before)

    def test_unknown_selection_does_not_write(self):
        before = self.config.read_bytes()
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_picker('keep', 'unknown')
        self.assertEqual(self.config.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
