#!/bin/bash
# Pick which MCP servers stay enabled in the current repo.
# State: ~/.claude.json -> projects["<cwd>"].disabledMcpServers  (same store /mcp writes)
set -euo pipefail

export MCP_CWD="$(pwd)"
export MCP_CFG="${MCP_CFG:-$HOME/.claude.json}"
MODE="${1:-ask}"
[ -f "$MCP_CFG" ] || { echo "no $MCP_CFG" >&2; exit 1; }

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
export MCP_ALL="$TMP/all" MCP_KEEP="$TMP/keep"

if [ -n "${MCP_SERVER_LIST:-}" ] && [ -s "${MCP_SERVER_LIST:-}" ]; then
  cp "$MCP_SERVER_LIST" "$MCP_ALL"
else
  claude mcp list 2>/dev/null | python3 -c '
import sys
for line in sys.stdin:
    name, separator, details = line.strip().partition(": ")
    if separator and name and " - " in details:
        print(name)
' > "$MCP_ALL"
fi
[ -s "$MCP_ALL" ] || { echo "no MCP servers found" >&2; exit 1; }

python3 -c "
import json,os
d=json.load(open(os.environ['MCP_CFG']))
dis=d.get('projects',{}).get(os.environ['MCP_CWD'],{}).get('disabledMcpServers',[])
open(os.environ['MCP_ALL']+'.dis','w').write('\n'.join(dis))
"
: > "$MCP_KEEP"

case "$MODE" in
  list)
    echo "MCP servers for $MCP_CWD"
    while IFS= read -r s; do
      if grep -qxF "$s" "$MCP_ALL.dis" 2>/dev/null; then echo "  [ ] $s"; else echo "  [x] $s"; fi
    done < "$MCP_ALL"
    exit 0 ;;
  all)  cp "$MCP_ALL" "$MCP_KEEP" ;;
  keep)
    shift
    for s in "$@"; do
      if grep -qxF "$s" "$MCP_ALL"; then printf '%s\n' "$s" >> "$MCP_KEEP"
      else echo "unknown server: $s" >&2; exit 3; fi
    done ;;
  none) : ;;
  ask)
    echo "Enable each MCP server in $MCP_CWD?   y = enable, n = disable, Enter = keep current"
    echo
    while IFS= read -r s; do
      if grep -qxF "$s" "$MCP_ALL.dis" 2>/dev/null; then cur="disabled"; def="n"; else cur="enabled"; def="y"; fi
      printf "  %-28s [%s] (y/n) [%s]: " "$s" "$cur" "$def"
      if [ -r /dev/tty ]; then read -r a </dev/tty || a=""; else read -r a || a=""; fi
      [ -z "$a" ] && a="$def"
      case "$a" in [Yy]*) printf '%s\n' "$s" >> "$MCP_KEEP" ;; esac
    done < "$MCP_ALL"
    echo ;;
  *) echo "usage: mcp-pick.sh [ask|all|none|list|keep <name>...]" >&2; exit 2 ;;
esac

BACKUP="$(mktemp "$MCP_CFG.bak.XXXXXX")"
cp "$MCP_CFG" "$BACKUP"
python3 -c "
import json,os,tempfile,stat
allsrv=[l.rstrip('\n') for l in open(os.environ['MCP_ALL']) if l.strip()]
keep={l.rstrip('\n') for l in open(os.environ['MCP_KEEP']) if l.strip()}
cfg=os.environ['MCP_CFG']
d=json.load(open(cfg))
e=d.setdefault('projects',{}).setdefault(os.environ['MCP_CWD'],{})
unseen=set(e.get('disabledMcpServers',[]))-set(allsrv)
e['disabledMcpServers']=sorted(unseen | (set(allsrv)-keep))
descriptor,temporary=tempfile.mkstemp(prefix='.mcp-pick-',dir=os.path.dirname(cfg) or '.')
try:
    with os.fdopen(descriptor,'w') as stream:
        os.fchmod(stream.fileno(),stat.S_IMODE(os.stat(cfg).st_mode))
        json.dump(d,stream,indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary,cfg)
finally:
    if os.path.exists(temporary):
        os.unlink(temporary)
print('enabled : '+(', '.join(sorted(keep)) or '(none)'))
print('disabled: '+(', '.join(e['disabledMcpServers']) or '(none)'))
"
echo
echo "Takes effect in a NEW session (tool definitions load at startup)."
