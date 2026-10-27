# 用法 — agent-ops-cli

## budget

估算系统提示 + 工具 schema + 附加文本相对 token 预算的固定开销。

```bash
agent-ops budget --system sys.txt --schemas tools.json --budget 200000 --target-ratio 0.35 --json
```

启发式：`tokens ≈ 字符数 / chars_per_token`（默认 4）。需要时可按你的分词器重标定；重点是相对开销，不是厂商真理。

## watch

```bash
agent-ops watch --timeout 180 --stall 90 -- make test
```

退出码：子进程 rc；**124** 硬超时；**125** 无输出卡死；**127** 命令不存在；**130** Ctrl-C；**2** 空命令。

适合前台对话工具壳。真正跑数小时的构建请交给后台委托，不要占住对话轮。

## env-audit

```bash
agent-ops env-audit -f required_keys.txt
agent-ops env-audit HOME PATH MY_API_KEY
```

永不打印密钥值——只报 `PRESENT len=N` 或 `MISSING`。

## log-digest / health / routine-lint

```bash
agent-ops log-digest /var/log/agent.log --tail 300
agent-ops health https://example.com/healthz --port 18789
agent-ops routine-lint ./routines/
```

`routine-lint` 要求 Trigger/Goal/Steps 类标题，建议写安静路径，并禁止私钥 / 保本话术 / 长十六进制地址模式。

## 冒烟

```bash
./scripts/smoke.sh
PYTHONPATH=src python tests/test_smoke.py
```
