"""Run the Claude picker against disposable configuration and CLI fixtures."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/claude/mcp-pick/scripts/mcp-pick.sh'


class ClaudePickerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.config = self.root / 'config.json'
        self.original = {'unrelated': True, 'projects': {str(self.root): {
            'disabledMcpServers': ['unseen', 'http-server'], 'other': 'preserve'}}}
        self.config.write_text(json.dumps(self.original))
        self.inventory = self.root / 'servers'
        self.inventory.write_text('http-server\n')
        self.env = {**os.environ, 'MCP_CFG': str(self.config),
                    'MCP_SERVER_LIST': str(self.inventory)}

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
