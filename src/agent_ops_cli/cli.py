"""agent-ops CLI entrypoint."""
from __future__ import annotations

import argparse
import sys

from . import __version__
from .budget import cmd_budget
from .env_audit import cmd_env_audit
from .health import cmd_health
from .log_digest import cmd_log_digest
from .routine_lint import cmd_routine_lint
from .watch import cmd_watch


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="agent-ops",
        description="Local AI agent host ops toolkit (budget / watch / env-audit / log-digest / health / routine-lint)",
    )
    p.add_argument("--version", action="version", version=f"agent-ops {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("budget", help="Estimate context fixed overhead vs budget")
    b.add_argument("--system", help="Path to system prompt text dump")
    b.add_argument("--schemas", help="Path to tool schemas dump")
    b.add_argument("--extra", nargs="*", default=[], help="Extra text files to count")
    b.add_argument("--stdin", action="store_true", help="Also read stdin as a part")
    b.add_argument("--budget", type=int, default=200_000, help="Token budget ceiling")
    b.add_argument("--target-ratio", type=float, default=0.35, help="Retain ratio after compact")
    b.add_argument("--chars-per-token", type=float, default=4.0)
    b.add_argument("--json", action="store_true")
    b.set_defaults(func=cmd_budget)

    w = sub.add_parser("watch", help="Run a command with hard timeout + stall kill")
    w.add_argument("--timeout", type=float, default=120.0, help="Hard timeout seconds")
    w.add_argument("--stall", type=float, default=60.0, help="No-output stall seconds (0=off)")
    w.add_argument("cmd", nargs=argparse.REMAINDER, help="Command after --")
    w.set_defaults(func=cmd_watch)

    e = sub.add_parser("env-audit", help="Redact-safe required env key audit")
    e.add_argument("--file", "-f", help="File with one KEY per line")
    e.add_argument("keys", nargs="*", help="KEY names")
    e.set_defaults(func=cmd_env_audit)

    d = sub.add_parser("log-digest", help="One-line WARN/FAIL digest for delivery tiers")
    d.add_argument("file")
    d.add_argument("--tail", type=int, default=200)
    d.set_defaults(func=cmd_log_digest)

    h = sub.add_parser("health", help="HTTP (+ optional local port) health probe")
    h.add_argument("url")
    h.add_argument("--port", type=int, default=None)
    h.add_argument("--timeout", type=float, default=15.0)
    h.set_defaults(func=cmd_health)

    r = sub.add_parser("routine-lint", help="Lint routine markdown/YAML drafts")
    r.add_argument("paths", nargs="+")
    r.set_defaults(func=cmd_routine_lint)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # Allow: agent-ops watch -- cmd → strip leading --
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "cmd", None) is not None and isinstance(args.cmd, list):
        if args.cmd and args.cmd[0] == "--":
            args.cmd = args.cmd[1:]
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
