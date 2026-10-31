#!/usr/bin/env python3
"""Record whole-run timing and unique screen outcomes in an explicit state directory.

Metrics do not establish visual approval. Choose a state directory outside the
target repository; this helper never discovers project paths or edits a ledger.
"""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import tempfile
import uuid


KINDS = ('screen', 'part', 'flow-card')
OUTCOMES = ('pending', 'completed', 'skipped', 'failed', 'blocked')
RUN_STATUSES = ('completed', 'blocked', 'failed', 'interrupted')


def utc_now():
    return datetime.now(timezone.utc)


def identifier(value, label):
    if (not isinstance(value, str) or not value.strip() or value != value.strip()
            or value in ('.', '..') or any(c in value for c in ('/', '\\'))
            or any(ord(c) < 32 for c in value)):
        raise ValueError(f'{label} must be a nonempty identifier without path separators')
    return value


def run_path(state_dir, run_id):
    if not isinstance(run_id, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', run_id):
        raise ValueError('Run ID must contain 1–128 letters, digits, underscores, dots or hyphens')
    return Path(state_dir).expanduser().resolve() / (run_id + '.json')


@contextmanager
def file_lock(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        if os.name == 'nt':
            import msvcrt
            if stream.seek(0, os.SEEK_END) == 0:
                stream.write(b'\0')
                stream.flush()
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == 'nt':
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def atomic_json(path, value):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix=path.name + '.', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def load_run(path):
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError as error:
        raise ValueError('Whole-run timer not found; start it before doing work') from error
    if not isinstance(value, dict) or 'startedAt' not in value:
        raise ValueError('State is not a whole-run timer')
    return value


def run_summary(value):
    end = datetime.fromisoformat(value['finishedAt']) if value.get('finishedAt') else utc_now()
    seconds = (end - datetime.fromisoformat(value['startedAt'])).total_seconds()
    if seconds < 0:
        raise ValueError('Run clock moved backwards; elapsed time is unavailable')
    counts = {kind: dict.fromkeys(OUTCOMES, 0) for kind in KINDS}
    for item in value['items'].values():
        counts[item['kind']][item['outcome']] += 1
    completed = counts['screen']['completed']
    return {**value, 'elapsedSeconds': seconds, 'counts': counts,
            'screensPerMinute': completed * 60 / seconds if seconds else 0,
            'screensPerHour': completed * 3600 / seconds if seconds else 0,
            'secondsPerScreen': seconds / completed if completed else None}


def start_run(state_dir, command, run_id=None, repo_root=None, skill_root=None):
    if not isinstance(command, str) or not command.strip():
        raise ValueError('Name the skill command being timed')
    started_at = utc_now().isoformat()
    run_id = run_id if run_id is not None else utc_now().strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:8]
    path = run_path(state_dir, run_id)
    provenance = None
    if repo_root is not None or skill_root is not None:
        from run_history import capture_provenance
        provenance = capture_provenance(repo_root, skill_root)
    if repo_root is not None and Path(repo_root).expanduser().resolve() in path.parents:
        raise ValueError('Mutable run state must be outside the target repository')
    with file_lock(path.with_suffix('.lock')):
        if path.exists():
            raise ValueError('Run already exists; report or finish it without resetting its timer')
        value = {'run': run_id, 'command': command, 'status': 'running', 'metricsFile': str(path),
                 'startedAt': started_at, 'stages': [], 'items': {}}
        if provenance is not None:
            value['provenance'] = provenance
        summary = run_summary(value)
        atomic_json(path, value)
    return summary


def progress(state_dir, run_id, collection, slugs, kind='screen', outcome='pending'):
    identifier(collection, 'Collection')
    if kind not in KINDS or outcome not in OUTCOMES:
        raise ValueError('Unknown item kind or outcome')
    if not slugs or isinstance(slugs, str):
        raise ValueError('Provide at least one screen or part slug')
    for slug in slugs:
        identifier(slug, 'Slug')
    path = run_path(state_dir, run_id)
    with file_lock(path.with_suffix('.lock')):
        value = load_run(path)
        if value['status'] != 'running':
            raise ValueError('Run is already finished')
        for slug in slugs:
            key = collection + '/' + slug
            previous = value['items'].get(key)
            if previous and previous['kind'] != kind:
                raise ValueError('An item cannot change kind during a run: ' + key)
            value['items'][key] = {'kind': kind, 'outcome': outcome}
        summary = run_summary(value)
        atomic_json(path, value)
    return summary


def report_run(state_dir, run_id):
    return run_summary(load_run(run_path(state_dir, run_id)))


def finish_run(state_dir, run_id, status):
    if status not in RUN_STATUSES:
        raise ValueError('Unknown final run status')
    path = run_path(state_dir, run_id)
    with file_lock(path.with_suffix('.lock')):
        value = load_run(path)
        if value['status'] != 'running':
            if value['status'] != status:
                raise ValueError('Run is already finished with a different status')
            return run_summary(value)
        if status == 'completed' and any(item['outcome'] in ('pending', 'failed', 'blocked')
                                         for item in value['items'].values()):
            raise ValueError('Unfinished or unsuccessful items require a blocked, failed or interrupted status')
        value.update(status=status, finishedAt=utc_now().isoformat())
        summary = run_summary(value)
        atomic_json(path, value)
    return summary


def measure(state_dir, run_id, stage, seconds, cache_hits=0, retries=0, throttles=0):
    if not isinstance(stage, str) or not stage.strip():
        raise ValueError('Use a named stage')
    if type(seconds) not in (int, float) or not math.isfinite(seconds) or seconds < 0:
        raise ValueError('Stage seconds must be finite and nonnegative')
    counters = {'cacheHits': cache_hits, 'retries': retries, 'throttles': throttles}
    if any(type(n) is not int or n < 0 for n in counters.values()):
        raise ValueError('Stage counters must be nonnegative integers')
    path = run_path(state_dir, run_id)
    with file_lock(path.with_suffix('.lock')):
        value = load_run(path)
        if value['status'] != 'running':
            raise ValueError('Run is already finished')
        value['stages'].append({'stage': stage, 'seconds': seconds, **counters})
        value['totals'] = {key: sum(row[key] for row in value['stages'])
                           for key in ('seconds', *counters)}
        summary = run_summary(value)
        atomic_json(path, value)
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', required=True, help='explicit metrics directory outside the target repository')
    sub = parser.add_subparsers(dest='action', required=True)
    start = sub.add_parser('start', help='start the whole timer before preflight or planning')
    start.add_argument('--command', required=True)
    start.add_argument('--run')
    start.add_argument('--repo-root', help='optional explicit Git root for starting revision/dirty provenance')
    start.add_argument('--skill-root', help='optional explicit skill folder for a starting content hash')
    update = sub.add_parser('progress', help='record unique screen or part outcomes')
    update.add_argument('--run', required=True)
    update.add_argument('--collection', required=True)
    update.add_argument('--kind', choices=KINDS, default='screen')
    update.add_argument('--outcome', choices=OUTCOMES, required=True)
    update.add_argument('slugs', nargs='+')
    report = sub.add_parser('report', help='read elapsed time and throughput without changing state')
    report.add_argument('--run', required=True)
    finish = sub.add_parser('finish', help='freeze timing on every exit path')
    finish.add_argument('--run', required=True)
    finish.add_argument('--status', choices=RUN_STATUSES, required=True)
    metrics = sub.add_parser('measure', help='record accumulated stage work separately from elapsed time')
    metrics.add_argument('--run', required=True)
    metrics.add_argument('--stage', required=True)
    metrics.add_argument('--seconds', type=float, required=True)
    for counter in ('cache-hits', 'retries', 'throttles'):
        metrics.add_argument('--' + counter, type=int, default=0)
    args = parser.parse_args(argv)
    try:
        if args.action == 'start':
            result = start_run(args.state_dir, args.command, args.run, args.repo_root, args.skill_root)
        elif args.action == 'progress':
            result = progress(args.state_dir, args.run, args.collection, args.slugs, args.kind, args.outcome)
        elif args.action == 'report':
            result = report_run(args.state_dir, args.run)
        elif args.action == 'finish':
            result = finish_run(args.state_dir, args.run, args.status)
        else:
            result = measure(args.state_dir, args.run, args.stage, args.seconds,
                             args.cache_hits, args.retries, args.throttles)
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, str(error) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
