# agent-ops-cli

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](./pyproject.toml)

**Runnable local CLI** for AI agent host operators: estimate context overhead, wrap slow commands with hard timeout + stall kill, redact-safe env audit, log digest for delivery tiers, HTTP health probe, and routine-doc lint.

- English (this file) · [中文](./README.zh-CN.md)
- License: MIT · Python ≥ 3.10 · **zero runtime deps**
- GitHub: [`YuanAqi/agent-ops-cli`](https://github.com/YuanAqi/agent-ops-cli)

## What it does

When you run AI agents on your own machine, chats often hang on slow commands, context balloons, or secrets leak into logs. **agent-ops-cli** is a small local command-line tool that estimates context size, kills hung commands on a hard timeout, audits environment variables with redaction, digests logs, probes HTTP health, and lints routine docs. For people who operate agent hosts — not a trading or remote-control app.

## Install / run

```bash
# from repo root (no install)
PYTHONPATH=src python -m agent_ops_cli.cli --help

# or editable
pip install -e .
agent-ops --help
```

## One-command demos

```bash
# Context budget from prompt + schema dumps
PYTHONPATH=src python -m agent_ops_cli.cli budget \
  --system examples/system_prompt_snippet.txt \
  --schemas examples/schemas_snippet.txt --budget 5000

# Kill a hung command after 1s hard timeout (exit 124)
PYTHONPATH=src python -m agent_ops_cli.cli watch --timeout 1 --stall 0 -- sleep 30

# Missing binary → exit 127, no traceback
PYTHONPATH=src python -m agent_ops_cli.cli watch --timeout 2 --stall 0 -- no-such-bin-xyz

# Redact-safe env presence (never prints values)
PYTHONPATH=src python -m agent_ops_cli.cli env-audit -f examples/required_keys.txt

# Lint a routine draft
PYTHONPATH=src python -m agent_ops_cli.cli routine-lint examples/sample_routine.md

# Full smoke
./scripts/smoke.sh
```

## Subcommands

| Cmd | What it does |
|---|---|
| `budget` | Char→token heuristic; flags when fixed overhead exceeds retain target |
| `watch` | Runs `cmd` with `--timeout` + `--stall` no-output kill; structured `timeout_reason` |
| `env-audit` | PRESENT/MISSING with length only |
| `log-digest` | `silent` / `summary` / `message` delivery grade from recent log lines |
| `health` | HTTP probe (+ optional local TCP port) |
| `routine-lint` | Requires Trigger/Goal/Steps-ish headings; bans private-key / yield / hardcoded addresses |

### `watch` exit codes

| Code | Meaning |
|---|---|
| process rc | Child exited normally |
| **124** | Hard timeout |
| **125** | Stall (no output) |
| **127** | Command not found / cannot start |
| **130** | Interrupted (Ctrl-C) |
| **2** | Usage error (empty command) |

## Limitations (honesty)

- Token counts are a **char/4 heuristic**, not a vendor tokenizer.
- `watch` uses `select` on stdout; programs that only write to a TTY without newline may look "stalled".
- `health` treats HTTP 401/403 as "reachable" (auth wall ≠ down).
- Not a process supervisor, not a secrets manager, not a cloud agent runtime.

## Docs

- [docs/en/usage.md](./docs/en/usage.md) — full flag reference + tuning notes
- [docs/zh/usage.md](./docs/zh/usage.md) — 中文用法
- [docs/en/design.md](./docs/en/design.md) — why these knobs
- [docs/zh/design.md](./docs/zh/design.md)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) · [中文](./CONTRIBUTING.zh-CN.md).  
Security reports: [SECURITY.md](./SECURITY.md). Code of conduct: [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md). Changelog: [CHANGELOG.md](./CHANGELOG.md).

## Not included

Strategy packs, exchange keys, broker code, live host dumps, paid zip binaries.
