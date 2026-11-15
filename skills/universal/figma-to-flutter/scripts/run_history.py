#!/usr/bin/env python3
"""Explicitly export finished run metrics as private, append-only history records.

Raw commands, paths, screen identifiers and arbitrary stage labels are omitted.
Exporting a record neither commits it nor grants visual or production approval.
"""
import argparse
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile


SCHEMA_VERSION = 1
STAGES = {'planning', 'capture', 'convert', 'render', 'pixel', 'check', 'review'}
COUNTERS = ('cacheHits', 'retries', 'throttles')


def capture_provenance(repo_root=None, skill_root=None):
    """Capture only requested Git revision/dirty state and skill bytes at run start."""
    result = {}
    if repo_root is not None:
        root = Path(repo_root).expanduser().resolve(strict=True)
        def git(*args):
            return subprocess.run(['git', '-C', str(root), *args], check=True,
                                  capture_output=True, text=True, timeout=30).stdout.strip()
        try:
            if Path(git('rev-parse', '--show-toplevel')).resolve() != root:
                raise ValueError('repo-root must be the Git working tree root')
            commit = git('rev-parse', 'HEAD')
            if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', commit):
                raise ValueError('Git returned an invalid commit')
            result['git'] = {'commit': commit, 'dirty': bool(git('status', '--porcelain'))}
        except (OSError, subprocess.SubprocessError) as error:
            raise ValueError('Cannot capture Git provenance for the supplied repository') from error
    if skill_root is not None:
        root = Path(skill_root).expanduser().resolve(strict=True)
        if not (root / 'SKILL.md').is_file():
            raise ValueError('skill-root must contain SKILL.md')
        digest = hashlib.sha256()
        def fail_walk(error):
            raise error
        for directory, dirs, files in os.walk(root, onerror=fail_walk):
            dirs[:] = sorted(d for d in dirs if d not in ('.git', '__pycache__'))
            for name in (*dirs, *files):
                if (Path(directory) / name).is_symlink():
                    raise ValueError('Skill provenance requires materialized files, without symlinks')
            for name in sorted(files):
                if name.endswith(('.pyc', '.pyo')):
                    continue
                path = Path(directory) / name
                digest.update(path.relative_to(root).as_posix().encode() + b'\0')
                digest.update(hashlib.sha256(path.read_bytes()).digest())
        result['skill'] = {'treeHash': digest.hexdigest()}
    return result


def nonnegative(value, integer=False):
    if (type(value) not in ((int,) if integer else (int, float))
            or not math.isfinite(value) or value < 0):
        raise ValueError('History metrics must be finite and nonnegative')
    return value


def build_record(value):
    """Version 1 contains allowlisted metrics only; never copy arbitrary state fields."""
    import run_state
    if value.get('status') not in run_state.RUN_STATUSES or not value.get('finishedAt'):
        raise ValueError('Finish the run before exporting its history')
    if not isinstance(value.get('run'), str) or not value['run']:
        raise ValueError('A history record requires a run identifier')
    for key in ('startedAt', 'finishedAt'):
        stamp = datetime.fromisoformat(value[key])
        if stamp.tzinfo is None:
            raise ValueError('History timestamps must include a timezone')
    items = value.get('items')
    if not isinstance(items, dict) or any(not isinstance(item, dict)
            or item.get('kind') not in run_state.KINDS
            or item.get('outcome') not in run_state.OUTCOMES for item in items.values()):
        raise ValueError('History items require known kinds and outcomes')
    if value['status'] == 'completed' and any(item['outcome'] in ('pending', 'failed', 'blocked')
                                             for item in items.values()):
        raise ValueError('Completed history cannot contain unfinished or unsuccessful items')
    summary = run_state.run_summary(value)
    stages = []
    for stage in value.get('stages', []):
        stages.append({'stage': stage['stage'] if stage['stage'] in STAGES else 'other',
                       'seconds': nonnegative(stage['seconds']),
                       **{key: nonnegative(stage[key], integer=True) for key in COUNTERS}})
    provenance = {}
    source = value.get('provenance', {})
    if 'git' in source:
        git = source['git']
        if (not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', git.get('commit', ''))
                or type(git.get('dirty')) is not bool):
            raise ValueError('Invalid captured Git provenance')
        provenance['git'] = {'commit': git['commit'], 'dirty': git['dirty']}
    if 'skill' in source:
        digest = source['skill'].get('treeHash', '')
        if not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError('Invalid captured skill provenance')
        provenance['skill'] = {'treeHash': digest}
    return {'schemaVersion': SCHEMA_VERSION,
            'run': hashlib.sha256(value['run'].encode()).hexdigest(), 'status': value['status'],
            'startedAt': value['startedAt'], 'finishedAt': value['finishedAt'],
            **{key: summary[key] for key in ('elapsedSeconds', 'counts', 'screensPerMinute',
                                             'screensPerHour', 'secondsPerScreen')},
            'stages': stages,
            'totals': {key: sum(stage[key] for stage in stages) for key in ('seconds', *COUNTERS)},
            'provenance': provenance}


def export_run(state_dir, run_id, history_dir):
    """Publish a complete record atomically; an existing record is never overwritten."""
    import run_state
    state = Path(state_dir).expanduser().resolve()
    history = Path(history_dir).expanduser().resolve()
    if state == history or state in history.parents or history in state.parents:
        raise ValueError('History and mutable run state must use separate, disjoint directories')
    value = run_state.load_run(run_state.run_path(state, run_id))
    record = build_record(value)
    data = json.dumps(record, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
    history.mkdir(parents=True, exist_ok=True)
    destination = history / (record['run'] + '.json')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=history,
                                         prefix='.run-', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, destination)
        except FileExistsError as error:
            raise ValueError('Run history already exists; append-only records cannot be overwritten') from error
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', required=True)
    parser.add_argument('--run', required=True)
    parser.add_argument('--history-dir', required=True)
    args = parser.parse_args()
    try:
        print(json.dumps({'historyFile': str(export_run(args.state_dir, args.run, args.history_dir))}))
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as error:
        parser.exit(2, str(error) + '\n')


if __name__ == '__main__':
    main()
