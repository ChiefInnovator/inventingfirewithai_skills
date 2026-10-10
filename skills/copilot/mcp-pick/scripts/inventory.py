"""Read Copilot CLI MCP enablement without exposing server connection details."""
import json
import subprocess
import sys


def summarize(data):
    if not isinstance(data, dict) or not isinstance(data.get('mcpServers'), dict):
        raise ValueError('Unsupported MCP inventory schema')
    result = []
    for name, server in sorted(data['mcpServers'].items()):
        if not isinstance(name, str) or not name or not isinstance(server, dict):
            raise ValueError('Invalid server identity')
        enabled = server.get('enabled')
        if not isinstance(enabled, bool):
            raise ValueError('Unknown server enablement; inspect host support')
        result.append({'name': name, 'enabled': enabled})
    return result


def main():
    try:
        run = subprocess.run(['copilot', 'mcp', 'list', '--json'],
                             capture_output=True, text=True, timeout=30)
        if run.returncode:
            raise ValueError('Copilot inventory failed; raw output omitted')
        result = summarize(json.loads(run.stdout))
    except (OSError, subprocess.TimeoutExpired, ValueError):
        print('Unable to read a supported MCP inventory; raw output omitted', file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
