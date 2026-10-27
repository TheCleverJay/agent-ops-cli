"""Lint agent routine markdown/YAML drafts for required sections."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    re.compile(r"(?i)^#+\s*(trigger|suggested trigger|cron|schedule)\b", re.M),
    re.compile(r"(?i)^#+\s*(goal|purpose|objective)\b", re.M),
    re.compile(r"(?i)^#+\s*(steps|procedure|playbook)\b", re.M),
]
BAN_PATTERNS = [
    (re.compile(r"(?i)private[_\s-]?key"), "mentions private key"),
    (re.compile(r"(?i)guaranteed\s+yield"), "mentions guaranteed yield"),
    (re.compile(r"0x[a-fA-F0-9]{40,}"), "looks like a hardcoded chain address"),
]


def lint_text(text: str, path: str) -> list[str]:
    issues: list[str] = []
    for rx in REQUIRED_HEADINGS:
        if not rx.search(text):
            issues.append(f"{path}: missing section matching /{rx.pattern}/")
    for rx, label in BAN_PATTERNS:
        if rx.search(text):
            issues.append(f"{path}: ban — {label}")
    if "when nothing" not in text.lower() and "silent" not in text.lower() and "quiet" not in text.lower():
        issues.append(f"{path}: advise adding a quiet/silent path when there is nothing to report")
    return issues


def cmd_routine_lint(args: argparse.Namespace) -> int:
    paths = [Path(p) for p in args.paths]
    all_issues: list[str] = []
    for path in paths:
        if path.is_dir():
            files = list(path.rglob("*.md")) + list(path.rglob("*.yml")) + list(path.rglob("*.yaml"))
        else:
            files = [path]
        for f in files:
            text = f.read_text(encoding="utf-8", errors="replace")
            all_issues.extend(lint_text(text, str(f)))
    if all_issues:
        for i in all_issues:
            print(i)
        print(f"summary issues={len(all_issues)}")
        return 1
    print("summary issues=0")
    return 0
