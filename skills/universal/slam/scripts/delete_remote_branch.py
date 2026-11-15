#!/usr/bin/env python3
"""Delete one verified merged origin branch without force or bypassing hooks.

The caller must first verify GitHub PR identity, deletion policy, and authority.
The pre-push guard binds deletion to the server's actual advertised object ID;
receive-pack then rejects a ref that changes before the deletion is committed.
"""

import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
from check_cleanup import Refusal, check_cleanup, git, require


def origin_matches(root, expected):
    require(bool(expected) and "\n" not in expected and "\r" not in expected,
            "Provide the captured origin URL.")
    for direction in ((), ("--push",)):
        urls = git(root, "remote", "get-url", *direction, "--all", "origin").splitlines()
        require(urls == [expected], "Origin fetch/push destination changed or is ambiguous.")


def validate_update(data, branch, head):
    lines = data.decode("utf-8").splitlines()
    expected = ["(delete)", "0" * len(head), "refs/heads/" + branch, head]
    require(len(lines) == 1 and lines[0].split() == expected,
            "Push advertisement differs from the exact captured deletion.")


def run_hook(state_path, arguments):
    state = json.loads(Path(state_path).read_text(encoding="utf-8"))
    require(arguments == ["origin", state["origin"]], "Unexpected push destination.")
    data = sys.stdin.buffer.read()
    validate_update(data, state["branch"], state["head"])
    original = state["originalHook"]
    if original:
        result = subprocess.run([original, *arguments], input=data, capture_output=True,
                                timeout=30, check=False)
        require(result.returncode == 0, "Existing pre-push hook rejected the deletion.")
    # Existing hooks run normally, but cannot broaden the guarded update.
    validate_update(data, state["branch"], state["head"])
    return 0


def delete_remote_branch(root, base, branch, head, merge_commit, expected_origin, protected=()):
    root = Path(root).resolve()
    origin_matches(root, expected_origin)
    checks = check_cleanup(root, base, branch, head, merge_commit, protected)
    head = checks["expected_head"]
    if not checks["remote_candidate_exists"]:
        return {"remote_absent": True, "deletion_performed": False, "already_absent": True}

    hook_path = Path(git(root, "rev-parse", "--path-format=absolute", "--git-path", "hooks/pre-push"))
    original = str(hook_path) if hook_path.is_file() and os.access(hook_path, os.X_OK) else None
    with tempfile.TemporaryDirectory(prefix="slam-delete-") as temporary:
        directory = Path(temporary)
        hooks = directory / "hooks"
        hooks.mkdir()
        # Preserve all other hooks and sibling resources, including custom hook paths.
        if hook_path.parent.is_dir():
            for entry in hook_path.parent.iterdir():
                if entry.name != "pre-push":
                    destination = hooks / entry.name
                    if entry.is_file() and os.access(entry, os.X_OK):
                        # Preserve the original invocation path: hooks may read ../policy.txt
                        # relative to $0. A symlink invoked through our directory changes it.
                        destination.write_text("#!/bin/sh\nexec " + shlex.quote(str(entry)) +
                                               ' "$@"\n', encoding="utf-8")
                        destination.chmod(0o700)
                    else:
                        destination.symlink_to(entry.resolve(), target_is_directory=entry.is_dir())
        state_path = directory / "state.json"
        state_path.write_text(json.dumps({"branch": branch, "head": head,
                                         "origin": expected_origin, "originalHook": original}),
                              encoding="utf-8")
        wrapper = hooks / "pre-push"
        wrapper.write_text("#!/bin/sh\nexec " + shlex.quote(sys.executable) + " " +
                           shlex.quote(str(Path(__file__).resolve())) + " --hook-state " +
                           shlex.quote(str(state_path)) + ' "$@"\n', encoding="utf-8")
        wrapper.chmod(0o700)
        origin_matches(root, expected_origin)
        result = subprocess.run(["git", "-C", str(root), "-c", f"core.hooksPath={hooks}",
                                 "push", "origin", f":refs/heads/{branch}"],
                                capture_output=True, text=True, timeout=45, check=False)
        require(result.returncode == 0,
                "Guarded remote deletion failed; inspect the current ref before retrying.")
    remaining = git(root, "ls-remote", "--heads", "origin", "refs/heads/" + branch)
    require(not remaining, "Remote branch exists after deletion; preserve any new work.")
    return {"remote_absent": True, "deletion_performed": True, "already_absent": False}


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments[:1] == ["--hook-state"]:
        try:
            require(len(arguments) == 4, "Invalid hook invocation.")
            return run_hook(arguments[1], arguments[2:])
        except (Refusal, OSError, ValueError, KeyError, UnicodeError, subprocess.SubprocessError) as error:
            reason = str(error) if isinstance(error, Refusal) else type(error).__name__
            print(reason, file=sys.stderr)
            return 1
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repo-dir", "base", "branch", "head", "merge-commit", "expected-origin"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--protected", action="append", default=[])
    args = parser.parse_args(arguments)
    try:
        result = delete_remote_branch(args.repo_dir, args.base, args.branch, args.head,
                                      args.merge_commit, args.expected_origin, args.protected)
    except (Refusal, OSError, ValueError, subprocess.SubprocessError) as error:
        reason = str(error) if isinstance(error, Refusal) else type(error).__name__
        print(json.dumps({"remote_cleanup": "refused", "reason": reason}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
