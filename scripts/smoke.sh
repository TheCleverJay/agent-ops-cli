#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH=src
rm -rf src/agent_ops_cli/__pycache__ tests/__pycache__
python3 -m agent_ops_cli.cli --help >/dev/null
python3 -m agent_ops_cli.cli --version | grep -q 0.1.0
python3 -m agent_ops_cli.cli budget --system examples/system_prompt_snippet.txt --schemas examples/schemas_snippet.txt --budget 5000
python3 -m agent_ops_cli.cli env-audit -f examples/required_keys.txt || true
python3 -m agent_ops_cli.cli routine-lint examples/sample_routine.md
set +e
python3 -m agent_ops_cli.cli watch --timeout 1 --stall 0 -- sleep 30
rc=$?
set -e
test "$rc" -eq 124
set +e
python3 -m agent_ops_cli.cli watch --timeout 2 --stall 0 -- definitely-not-a-binary-xyz
rc2=$?
set -e
test "$rc2" -eq 127
python3 tests/test_smoke.py
test -f SECURITY.md && test -f CONTRIBUTING.md && test -f CHANGELOG.md && test -f CODE_OF_CONDUCT.md && test -f .gitignore
if grep -REi 'TODO|FIXME' src README.md README.zh-CN.md; then
  echo 'FAIL: TODO/FIXME on public surface' >&2; exit 1
fi
echo SMOKE_OK
