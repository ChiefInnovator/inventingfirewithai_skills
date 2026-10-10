#!/usr/bin/env python3
"""Resolve an exact Figma design URL to original identity and ledger work."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlparse


def resolve(url, ledger):
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname not in ('figma.com', 'www.figma.com'):
        raise ValueError('Use an HTTPS Figma design/frame link')
    path = [part for part in parsed.path.split('/') if part]
    if len(path) < 2 or path[0] not in ('design', 'file', 'proto'):
        raise ValueError('Use a Figma design/frame URL; Make, FigJam and Slides have different workflows')
    parent_key = path[1]
    file_key = path[3] if len(path) > 3 and path[2] == 'branch' else parent_key
    if not all(re.fullmatch(r'[A-Za-z0-9]+', key) for key in (parent_key, file_key)):
        raise ValueError('Invalid Figma file key')
    node_ids = parse_qs(parsed.query, keep_blank_values=True).get('node-id', [])
    if len(node_ids) > 1:
        raise ValueError('Select one Figma node URL at a time')
    node_id = node_ids[0] if node_ids else None
    if node_id is not None:
        node_id = node_id.replace('-', ':')
        # I-prefixed semicolon paths identify one nested instance descendant.
        if not re.fullmatch(r'(?:\d+:\d+|I\d+:\d+(?:;\d+:\d+)*)', node_id):
            raise ValueError('Invalid Figma node-id in URL')
    found = [(slug, screen) for slug, screen in ledger.get('screens', {}).items()
             if screen.get('fileKey', ledger.get('fileKey')) == file_key and screen.get('nodeId') == node_id]
    if len(found) > 1:
        raise ValueError('Duplicate original file/node identity in ledger')
    base = f'https://www.figma.com/design/{parent_key}'
    if file_key != parent_key:
        base += f'/branch/{file_key}'
    return {'inputUrl': url, 'fileKey': file_key, 'parentFileKey': parent_key, 'nodeId': node_id,
            'figmaFileUrl': base, 'figmaUrl': base + '?node-id=' + node_id.replace(':', '-') + '&m=dev' if node_id else base,
            'action': 'select-frame' if not node_id else 'update' if found else 'new-screen',
            'slug': found[0][0] if found else None,
            'flutterPath': found[0][1].get('flutter', {}).get('path') if found else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url')
    parser.add_argument('--ledger', type=Path, help='Existing project ledger; omitted means no known screens')
    args = parser.parse_args()
    try:
        result = resolve(args.url, json.loads(args.ledger.read_text()) if args.ledger else {})
    except (ValueError, OSError) as error:
        parser.error(str(error))
        return
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
