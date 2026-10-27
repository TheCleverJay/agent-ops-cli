"""Rough context-budget estimator (chars → tokens heuristic)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def estimate_tokens(text: str, chars_per_token: float = 4.0) -> int:
    if chars_per_token <= 0:
        raise ValueError("chars_per_token must be > 0")
    return max(0, int(round(len(text) / chars_per_token)))


def analyze(parts: dict[str, str], budget: int, target_ratio: float, chars_per_token: float) -> dict:
    breakdown = {k: estimate_tokens(v, chars_per_token) for k, v in parts.items()}
    fixed = sum(breakdown.values())
    room = max(0, budget - fixed)
    retain_target = int(budget * target_ratio)
    return {
        "budget_tokens": budget,
        "target_ratio": target_ratio,
        "chars_per_token": chars_per_token,
        "fixed_overhead_tokens": fixed,
        "breakdown": breakdown,
        "history_room_tokens": room,
        "retain_target_tokens": retain_target,
        "compaction_needed_soon": fixed > retain_target,
        "advice": (
            "Fixed overhead already exceeds retain target — compact or lazy-load schemas."
            if fixed > retain_target
            else "Overhead fits under retain target; keep measuring on quiet turns."
        ),
    }


def cmd_budget(args: argparse.Namespace) -> int:
    parts: dict[str, str] = {}
    if args.system:
        parts["system"] = Path(args.system).read_text(encoding="utf-8", errors="replace")
    if args.schemas:
        parts["schemas"] = Path(args.schemas).read_text(encoding="utf-8", errors="replace")
    if args.extra:
        for i, path in enumerate(args.extra):
            parts[f"extra_{i}:{Path(path).name}"] = Path(path).read_text(encoding="utf-8", errors="replace")
    if args.stdin:
        parts["stdin"] = sys.stdin.read()
    if not parts:
        print("Provide --system/--schemas/--extra and/or --stdin", file=sys.stderr)
        return 2
    result = analyze(parts, args.budget, args.target_ratio, args.chars_per_token)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"budget={result['budget_tokens']} fixed={result['fixed_overhead_tokens']} "
              f"room={result['history_room_tokens']} retain_target={result['retain_target_tokens']}")
        for k, v in result["breakdown"].items():
            print(f"  {k}: {v} tokens")
        print(f"advice: {result['advice']}")
    return 0
