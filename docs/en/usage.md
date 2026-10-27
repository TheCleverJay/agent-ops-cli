# Usage — agent-ops-cli

## budget

Measure fixed overhead (system prompt + tool schemas + extras) against a token budget.

```bash
agent-ops budget --system sys.txt --schemas tools.json --budget 200000 --target-ratio 0.35 --json
```

| Flag | Default | Meaning |
|---|---|---|
| `--system` | | Path to system prompt dump |
| `--schemas` | | Path to tool schemas dump |
| `--extra` | | Extra text files to count |
| `--stdin` | off | Also read stdin as a part |
| `--budget` | 200000 | Token ceiling |
| `--target-ratio` | 0.35 | Retain ratio after compact |
| `--chars-per-token` | 4.0 | Heuristic divisor |
| `--json` | off | Machine-readable |

Heuristic: `tokens ≈ len(chars) / chars_per_token`. Retune with your tokenizer if needed; the point is relative overhead, not vendor law.

## watch

```bash
agent-ops watch --timeout 180 --stall 90 -- make test
```

| Flag | Default | Meaning |
|---|---|---|
| `--timeout` | 120 | Hard timeout seconds |
| `--stall` | 60 | No-output kill seconds (`0` = off) |
| `cmd` after `--` | required | Command to run |

Exit codes: process rc on success/fail; **124** hard timeout; **125** stall; **127** command not found; **130** Ctrl-C; **2** empty command.

Prefer `watch` for foreground chat-tool shells. True multi-hour builds belong in a background delegate, not the chat turn.

## env-audit

```bash
agent-ops env-audit -f required_keys.txt
agent-ops env-audit HOME PATH MY_API_KEY
```

Never prints secret values — only `PRESENT len=N` or `MISSING`.

## log-digest / health / routine-lint

```bash
agent-ops log-digest /var/log/agent.log --tail 300
agent-ops health https://example.com/healthz --port 18789
agent-ops routine-lint ./routines/
```

`routine-lint` requires Trigger/Goal/Steps-like headings, encourages a quiet/silent path, and bans private-key / guaranteed-yield / long hex address patterns.

## Smoke

```bash
./scripts/smoke.sh
# or
PYTHONPATH=src python tests/test_smoke.py
# or (if installed)
python -m pytest tests/ -q
```
