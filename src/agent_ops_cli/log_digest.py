"""One-line log digest for delivery-tier decisions."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FAIL_RE = re.compile(r"FAIL|ERROR|FATAL", re.I)
WARN_RE = re.compile(r"WARN|WARNING", re.I)
PASS_RE = re.compile(r"\bPASS\b|OK |succeeded", re.I)


def digest_text(text: str, n_hint: int, name: str) -> str:
    lines = text.splitlines()[-n_hint:] if n_hint > 0 else text.splitlines()
    chunk = "\n".join(lines)
    fails = len(FAIL_RE.findall(chunk))
    warns = len(WARN_RE.findall(chunk))
    passes = len(PASS_RE.findall(chunk))
    level = "silent"
    if warns:
        level = "summary"
    if fails:
        level = "message"
    return f"digest level={level} pass≈{passes} warn={warns} fail={fails} lines={len(lines)} file={name}"


def cmd_log_digest(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_file():
        print(f"not a file: {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8", errors="replace")
    print(digest_text(text, args.tail, path.name))
    return 0
