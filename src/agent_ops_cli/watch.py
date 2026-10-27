"""Slow-command watchdog: hard timeout + stall (no-output) kill."""
from __future__ import annotations

import argparse
import os
import select
import signal
import subprocess
import sys
import time


def _kill(proc: subprocess.Popen) -> None:
    try:
        if proc.poll() is None:
            if os.name == "nt":
                proc.terminate()
            else:
                try:
                    if hasattr(os, "killpg"):
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    else:
                        proc.kill()
                except Exception:
                    proc.kill()
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def run_watched(cmd: list[str], hard_timeout: float, stall_seconds: float) -> int:
    """Run *cmd* with hard timeout and optional no-output stall kill.

    Exit codes:
      - process return code on normal exit
      - 124 hard timeout
      - 125 stall (no output)
      - 127 command not found / not executable
      - 130 interrupted (Ctrl-C)
    """
    if hard_timeout <= 0:
        raise ValueError("hard_timeout must be > 0")
    if not cmd:
        print("usage: agent-ops watch -- <command> [args...]", file=sys.stderr)
        return 2

    def _preexec() -> None:
        if hasattr(os, "setsid"):
            os.setsid()

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            preexec_fn=_preexec if os.name != "nt" else None,
        )
    except FileNotFoundError:
        print(f"[agent-ops watch] command not found: {cmd[0]!r}", file=sys.stderr)
        return 127
    except OSError as e:
        print(f"[agent-ops watch] cannot start {cmd[0]!r}: {e}", file=sys.stderr)
        return 127

    start = time.monotonic()
    last_out = start
    assert proc.stdout is not None
    try:
        while True:
            ready, _, _ = select.select([proc.stdout], [], [], 0.2)
            now = time.monotonic()
            if ready:
                chunk = proc.stdout.readline()
                if chunk:
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                    last_out = now
                elif proc.poll() is not None:
                    break
            else:
                if proc.poll() is not None:
                    rest = proc.stdout.read()
                    if rest:
                        sys.stdout.write(rest)
                        sys.stdout.flush()
                    break
            elapsed = now - start
            if elapsed >= hard_timeout:
                _kill(proc)
                print(
                    f"\n[agent-ops watch] timeout_reason=hard_timeout elapsed={elapsed:.1f}s "
                    f"limit={hard_timeout:.1f}s",
                    file=sys.stderr,
                )
                return 124
            if stall_seconds > 0 and (now - last_out) >= stall_seconds and elapsed > stall_seconds:
                _kill(proc)
                print(
                    f"\n[agent-ops watch] timeout_reason=stall_no_output quiet={now - last_out:.1f}s "
                    f"stall_limit={stall_seconds:.1f}s elapsed={elapsed:.1f}s",
                    file=sys.stderr,
                )
                return 125
        rc = proc.wait()
        return rc if rc is not None else 0
    except KeyboardInterrupt:
        _kill(proc)
        return 130


def cmd_watch(args: argparse.Namespace) -> int:
    return run_watched(list(args.cmd or []), args.timeout, args.stall)
