#!/usr/bin/env python3
"""Read-only Git containment check. Does not verify PR state or delete anything."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


class Refusal(Exception):
    pass


def git(root, *args, absent=False):
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True,
        timeout=45, check=False,
    )
    if absent and result.returncode == 1:
        return None
    if result.returncode:
        # stderr may contain remote URLs/credentials; do not echo it.
        raise Refusal(f"Git {args[0]} failed (exit {result.returncode}); inspect locally.")
    return result.stdout.strip()


def require(condition, reason):
    if not condition:
        raise Refusal(reason)


def check_cleanup(root, base, branch, head, merge_commit, protected=()):
    """Require a clean synced base and containment of the exact captured head."""
    root = Path(root)
    protected = set(protected) | {base, "main", "master", "develop"}
    for name in (base, branch):
        require(bool(name) and not name.startswith(("-", "origin/", "refs/")),
                "Empty or unsafe branch name.")
        git(root, "check-ref-format", f"refs/heads/{name}")
    require(branch not in protected, "Feature branch is protected; retain it.")
    for sha in (head, merge_commit):
        require(bool(re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", sha)),
                "Use full captured commit SHAs.")
    head, merge_commit = head.lower(), merge_commit.lower()
    require(git(root, "rev-parse", "--is-inside-work-tree") == "true", "Not a worktree.")
    require(git(root, "branch", "--show-current") == base, "Checkout is not the captured base.")
    require(not git(root, "status", "--porcelain=v1", "-z"), "Working tree is dirty; retain branches.")
    worktrees = git(root, "worktree", "list", "--porcelain", "-z").split("\0")
    require(f"branch refs/heads/{branch}" not in worktrees,
            "Feature branch is checked out in a worktree; retain it.")

    base_ref = f"refs/remotes/origin/{base}"
    branch_ref = f"refs/heads/{branch}"
    remote_branch_ref = f"refs/heads/{branch}"
    base_sha = git(root, "rev-parse", "--verify", f"{base_ref}^{{commit}}")
    require(git(root, "rev-parse", "HEAD") == base_sha,
            "Local base is not exactly synchronized with origin; retain branches.")
    remote_lines = git(root, "ls-remote", "--heads", "origin",
                       f"refs/heads/{base}", remote_branch_ref)
    remote = dict((ref, sha) for sha, ref in (line.split() for line in remote_lines.splitlines()))
    require(remote.get(f"refs/heads/{base}") == base_sha,
            "Remote base changed or is missing; fetch and recheck.")
    remote_head = remote.get(remote_branch_ref)
    require(remote_head is None or remote_head == head,
            "Remote feature branch differs from the captured PR head; retain it.")
    local_head = git(root, "rev-parse", "--verify", "--quiet", f"{branch_ref}^{{commit}}", absent=True)
    require(local_head is None or local_head == head,
            "Local feature branch differs from the captured PR head; retain it.")

    git(root, "merge-base", "--is-ancestor", head, base_sha)
    git(root, "merge-base", "--is-ancestor", merge_commit, base_sha)
    return {
        "git_checks": "passed",
        "branch": branch,
        "expected_head": head,
        "base_head": base_sha,
        "local_candidate_exists": local_head is not None,
        "remote_candidate_exists": remote_head is not None,
        "deletion_performed": False,
        "remaining_gate": "Verify GitHub merged PR identity, current protection rules, and authorization.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-dir", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--merge-commit", required=True)
    parser.add_argument("--protected", action="append", default=[])
    args = parser.parse_args()
    try:
        result = check_cleanup(args.repo_dir, args.base, args.branch, args.head,
                               args.merge_commit, args.protected)
    except (Refusal, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        # Never print raw subprocess output or command strings containing secrets.
        reason = str(exc) if isinstance(exc, Refusal) else type(exc).__name__
        print(json.dumps({"git_checks": "refused", "reason": reason}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
