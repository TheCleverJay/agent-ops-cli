"""Redact-safe environment key presence audit."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def audit(keys: list[str]) -> tuple[int, int]:
    present = missing = 0
    for key in keys:
        val = os.environ.get(key)
        if val is None or val == "":
            print(f"MISSING  {key}")
            missing += 1
        else:
            print(f"PRESENT  {key}  len={len(val)}")
            present += 1
    print(f"summary present={present} missing={missing}")
    return present, missing


def cmd_env_audit(args: argparse.Namespace) -> int:
    keys: list[str] = []
    if args.file:
        for line in Path(args.file).read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                keys.append(line)
    keys.extend(args.keys or [])
    if not keys:
        print("Provide --file REQUIRED_KEYS.txt and/or KEY names", file=sys.stderr)
        return 2
    _, missing = audit(keys)
    return 1 if missing else 0
