"""Tests — run with: python -m pytest tests/  OR  python tests/test_smoke.py"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from agent_ops_cli.budget import analyze, estimate_tokens
from agent_ops_cli.env_audit import audit
from agent_ops_cli.log_digest import digest_text
from agent_ops_cli.routine_lint import lint_text
from agent_ops_cli.watch import run_watched


def test_estimate_tokens():
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("a" * 40) == 10
    assert estimate_tokens("") == 0


def test_estimate_tokens_rejects_bad_cpt():
    try:
        estimate_tokens("x", chars_per_token=0)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_analyze_flags_high_overhead():
    r = analyze({"system": "x" * 4000}, budget=500, target_ratio=0.35, chars_per_token=4.0)
    assert r["fixed_overhead_tokens"] == 1000
    assert r["compaction_needed_soon"] is True


def test_analyze_low_overhead():
    r = analyze({"system": "hi"}, budget=10_000, target_ratio=0.35, chars_per_token=4.0)
    assert r["compaction_needed_soon"] is False
    assert r["history_room_tokens"] > 0


def test_digest_levels():
    assert "level=silent" in digest_text("all good\n", 10, "t.log")
    assert "level=summary" in digest_text("WARN once\n", 10, "t.log")
    assert "level=message" in digest_text("ERROR boom\n", 10, "t.log")


def test_routine_lint_missing():
    issues = lint_text("# Hello\n\nNo sections.\n", "x.md")
    assert any("missing" in i for i in issues)


def test_routine_lint_ok():
    text = """# Goal
Ship quietly.

## Trigger
Weekday cron.

## Steps
1. Check inbox.
When nothing is new, stay silent.
"""
    assert lint_text(text, "ok.md") == []


def test_routine_lint_bans_secrets():
    text = """# Goal
x
## Trigger
y
## Steps
do not paste a private key here
When nothing is new, stay silent.
"""
    issues = lint_text(text, "bad.md")
    assert any("private key" in i.lower() or "ban" in i.lower() for i in issues)


def test_env_audit():
    os.environ["AO_TEST_PRESENT"] = "secret123"
    present, missing = audit(["AO_TEST_PRESENT", "AO_TEST_MISSING_XYZ"])
    assert present == 1 and missing == 1


def test_cli_help():
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    r = subprocess.run(
        [sys.executable, "-m", "agent_ops_cli.cli", "--help"],
        capture_output=True, text=True, env=env,
    )
    assert r.returncode == 0
    for name in ("budget", "watch", "env-audit", "log-digest", "health", "routine-lint"):
        assert name in r.stdout


def test_cli_version():
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    r = subprocess.run(
        [sys.executable, "-m", "agent_ops_cli.cli", "--version"],
        capture_output=True, text=True, env=env,
    )
    assert r.returncode == 0
    assert "0.1.0" in r.stdout


def test_watch_hard_timeout():
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    r = subprocess.run(
        [sys.executable, "-m", "agent_ops_cli.cli", "watch", "--timeout", "1", "--stall", "0", "--", "sleep", "30"],
        capture_output=True, text=True, env=env,
    )
    assert r.returncode == 124
    assert "hard_timeout" in r.stderr


def test_watch_missing_binary():
    rc = run_watched(["definitely-not-a-binary-xyz-agent-ops"], hard_timeout=2.0, stall_seconds=0.0)
    assert rc == 127


def test_watch_empty_cmd():
    assert run_watched([], hard_timeout=1.0, stall_seconds=0.0) == 2


def test_log_digest_cli():
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    with tempfile.NamedTemporaryFile("w", suffix=".log", delete=False) as f:
        f.write("INFO ok\nWARN once\n")
        path = f.name
    try:
        r = subprocess.run(
            [sys.executable, "-m", "agent_ops_cli.cli", "log-digest", path, "--tail", "50"],
            capture_output=True, text=True, env=env,
        )
        assert r.returncode == 0
        assert "level=" in r.stdout
    finally:
        os.unlink(path)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("ok", fn.__name__)
    print("all smoke tests passed")
