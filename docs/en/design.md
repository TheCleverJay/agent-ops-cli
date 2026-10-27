# Design notes

## Why these six commands

Agent hosts fail in repeatable ways. Each subcommand maps to one failure mode:

| Failure | Command |
|---|---|
| Context balloon / premature compaction | `budget` |
| Hung foreground shell eating the chat turn | `watch` |
| Secrets echoed while debugging env | `env-audit` |
| Noisy routines that should stay quiet | `log-digest` + `routine-lint` |
| “Is the side service up?” | `health` |

## Constraints we keep on purpose

- **Zero runtime deps** — install friction kills ops tools.
- **Exit codes that match Unix muscle memory** (`124` timeout family).
- **Never print secret values** from `env-audit`.
- **Refuse proprietary / paid attachments** in the public tree.

## What we will not add

Process supervisors, cloud agent schedulers, broker adapters, secret stores with encryption at rest, or anything that needs a daemon. Keep the CLI boring and scriptable.
