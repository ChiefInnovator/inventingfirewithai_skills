#!/usr/bin/env python3
"""Generate or verify the literal scorecard snapshot served by GitHub Pages."""

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("docs/evaluations/referenced_skills_scorecard.md")
ASSET = Path("assets/data/referenced-skills-scorecard.txt")
PREFIX = ("Generated scorecard snapshot. Source: " + SOURCE.as_posix() + "\n\n").encode("utf-8")


def sync_data(root=ROOT, *, check=False, built_dir=None):
    if built_dir is not None and not check:
        raise ValueError("--built-dir requires --check")
    try:
        expected = PREFIX + (root / SOURCE).read_bytes()
    except OSError as error:
        print(f"Cannot read scorecard source: {error}", file=sys.stderr)
        return 1

    destination = root / "docs" / ASSET
    if not check:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(expected)
        print(f"Updated {destination.relative_to(root)}")
        return 0

    paths = [destination]
    if built_dir is not None:
        paths.append(Path(built_dir) / ASSET)
    failed = False
    for path in paths:
        try:
            actual = path.read_bytes()
        except OSError as error:
            print(f"Missing/unreadable scorecard asset: {path}: {error}", file=sys.stderr)
            failed = True
            continue
        if actual != expected:
            print(f"Stale scorecard asset: {path}; run python scripts/sync_site_data.py "
                  "and rebuild Pages if checking built output.", file=sys.stderr)
            failed = True
        else:
            print(f"Fresh scorecard asset: {path}")
    return int(failed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare assets without writing them")
    parser.add_argument("--built-dir", type=Path, help="Also verify a Jekyll output directory")
    args = parser.parse_args()
    if args.built_dir is not None and not args.check:
        parser.error("--built-dir requires --check")
    return sync_data(check=args.check, built_dir=args.built_dir)


if __name__ == "__main__":
    sys.exit(main())
