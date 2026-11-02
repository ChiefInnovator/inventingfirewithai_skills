#!/usr/bin/env python3
"""Check site data and run all maintained Python suites in isolated processes."""

from dataclasses import dataclass
from pathlib import Path
import os
import re
import signal
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
SUITE_TIMEOUT = 180
TERMINATION_GRACE = 5
MIN_CODEX_VERSION = (0, 153, 4)


@dataclass(frozen=True)
class Suite:
    name: str
    directory: str
    requires_codex: bool = False


SUITES = (
    Suite("Repository tests", "tests"),
    Suite("Codex Figma-to-Flutter", "skills/codex/figma-to-flutter/scripts"),
    Suite("Claude Figma-to-Flutter", "skills/claude/figma-to-flutter/scripts"),
    Suite("Copilot Figma-to-Flutter", "skills/copilot/figma-to-flutter/scripts"),
    Suite("Codex MCP Picker", "skills/codex/mcp-pick/tests", requires_codex=True),
    Suite("Copilot MCP Picker", "skills/copilot/mcp-pick/tests"),
)


@dataclass(frozen=True)
class CheckResult:
    name: str
    returncode: int
    output: str = ""
    timed_out: bool = False

    @property
    def passed(self):
        return self.returncode == 0 and not self.timed_out


def terminate_group(process, grace):
    """Stop inherited descendants too, even if the direct child exits on TERM.

    Explicitly detached descendants are outside the runner's cleanup contract.
    """
    try:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        deadline = time.monotonic() + grace
        while time.monotonic() < deadline:
            process.poll()  # Reap the direct child if it has already exited.
            try:
                os.killpg(process.pid, 0)
            except ProcessLookupError:
                break
            time.sleep(min(0.05, max(0, deadline - time.monotonic())))
    finally:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def run_process(name, arguments, root, timeout, grace):
    try:
        process = subprocess.Popen(
            arguments, cwd=root, start_new_session=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, errors="replace",
        )
    except OSError as error:
        return CheckResult(name, 1, f"Could not start: {error}\n")
    try:
        output, _ = process.communicate(timeout=timeout)
        return CheckResult(name, process.returncode, output)
    except subprocess.TimeoutExpired:
        terminate_group(process, grace)
        output, _ = process.communicate()
        return CheckResult(name, process.returncode or 1, output, timed_out=True)
    except BaseException:
        terminate_group(process, grace)
        raise


def codex_problem(root, grace):
    result = run_process("Codex CLI prerequisite", ["codex", "--version"],
                         root, timeout=10, grace=grace)
    match = re.fullmatch(r"codex-cli (\d+)\.(\d+)\.(\d+)(?:[-+][\w.-]+)?",
                         result.output.strip())
    if result.passed and match and tuple(map(int, match.groups())) >= MIN_CODEX_VERSION:
        return None
    detail = result.output.strip() or "version command timed out or produced no version"
    return ("Codex CLI >=0.153.4 is required for this suite. "
            "Install the CI version with npm install --global @openai/codex@0.166.0.\n"
            f"{detail}\n")


def show_result(result):
    if result.output:
        print(result.output, end="" if result.output.endswith("\n") else "\n", flush=True)
    status = "TIMED OUT" if result.timed_out else "PASS" if result.passed else "FAILED"
    print(f"{status}: {result.name} (exit {result.returncode})", flush=True)


def run_checks(root=ROOT, suites=SUITES, timeout=SUITE_TIMEOUT,
               grace=TERMINATION_GRACE):
    if sys.platform not in {"darwin", "linux"}:
        result = CheckResult("Supported operating system", 1,
                             "This runner supports macOS and Linux only; "
                             "process-group cleanup is not verified on this platform.\n")
        show_result(result)
        return [result]

    results = []
    print("RUN: Site data freshness", flush=True)
    data_script = root / "scripts/sync_site_data.py"
    if data_script.is_file():
        result = run_process("Site data freshness",
                             [sys.executable, str(data_script), "--check"], root, timeout, grace)
    else:
        result = CheckResult("Site data freshness", 1, "Missing scripts/sync_site_data.py\n")
    results.append(result)
    show_result(result)

    for suite in suites:
        print(f"RUN: {suite.name}", flush=True)
        directory = root / suite.directory
        if not directory.is_dir() or not any(directory.glob("test*.py")):
            result = CheckResult(suite.name, 1, f"Missing test suite: {suite.directory}\n")
        elif suite.requires_codex and (problem := codex_problem(root, grace)):
            result = CheckResult(suite.name, 1, problem)
        else:
            result = run_process(
                suite.name, [sys.executable, "-m", "unittest", "discover", "-s", suite.directory],
                root, timeout, grace,
            )
        results.append(result)
        show_result(result)

    failed = sum(not result.passed for result in results)
    print(f"{len(results) - failed}/{len(results)} checks passed; {failed} failed.", flush=True)
    return results


def main():
    return int(any(not result.passed for result in run_checks()))


if __name__ == "__main__":
    sys.exit(main())
