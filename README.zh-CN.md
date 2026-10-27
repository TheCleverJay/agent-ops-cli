# agent-ops-cli

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](./pyproject.toml)

面向本地 AI Agent 主机运维的 **可运行 CLI**：估算上下文固定开销、慢命令硬超时 + 无输出卡死杀掉、脱敏环境变量审计、日志摘要（投递等级）、HTTP 健康检查、例行任务文档 lint。

- [English](./README.md) · 中文（本文件）
- 许可证：MIT · Python ≥ 3.10 · **无第三方运行时依赖**
- 仓库：[`YuanAqi/agent-ops-cli`](https://github.com/YuanAqi/agent-ops-cli)

## 做什么

自己机器上跑 AI Agent 时，常见问题是：慢命令卡住整轮对话、上下文越来越大、排障时把密钥打进日志。**agent-ops-cli** 是一个本机命令行小工具：估算上下文开销、给慢命令设硬超时并杀掉、脱敏检查环境变量、摘要日志、探测 HTTP 健康、检查例行任务文档是否写全。给运维 Agent 主机的人用——不是交易软件，也不远程操控别人的电脑。

## 安装 / 运行

```bash
PYTHONPATH=src python -m agent_ops_cli.cli --help
# 或
pip install -e .
agent-ops --help
```

## 一条命令演示

```bash
PYTHONPATH=src python -m agent_ops_cli.cli budget \
  --system examples/system_prompt_snippet.txt \
  --schemas examples/schemas_snippet.txt --budget 5000

PYTHONPATH=src python -m agent_ops_cli.cli watch --timeout 1 --stall 0 -- sleep 30
PYTHONPATH=src python -m agent_ops_cli.cli watch --timeout 2 --stall 0 -- no-such-bin-xyz   # 退出码 127
PYTHONPATH=src python -m agent_ops_cli.cli env-audit -f examples/required_keys.txt
PYTHONPATH=src python -m agent_ops_cli.cli routine-lint examples/sample_routine.md
./scripts/smoke.sh
```

## 子命令

| 命令 | 作用 |
|---|---|
| `budget` | 字符→token 启发式；固定开销超过保留目标时告警 |
| `watch` | `--timeout` 硬超时 + `--stall` 无输出杀掉，输出 `timeout_reason` |
| `env-audit` | 只报 PRESENT/MISSING 与长度 |
| `log-digest` | 从日志得出 `silent` / `summary` / `message` |
| `health` | HTTP（+ 可选本地端口）探测 |
| `routine-lint` | 检查 Trigger/Goal/Steps 类标题；禁止私钥 / 保本话术 / 硬编码地址 |

### `watch` 退出码

| 码 | 含义 |
|---|---|
| 进程 rc | 子进程正常结束 |
| **124** | 硬超时 |
| **125** | 无输出卡死 |
| **127** | 命令不存在 / 无法启动 |
| **130** | Ctrl-C |
| **2** | 用法错误（空命令） |

## 局限（诚实说明）

- token 数是 **字符/4 启发式**，不是厂商分词器。
- `watch` 用 `select` 读 stdout；只往 TTY 写且无换行的程序可能被当成「卡死」。
- `health` 把 HTTP 401/403 视为「可达」（鉴权墙 ≠ 宕机）。
- 不是进程守护、不是密钥保险箱、不是云端 Agent 运行时。

## 文档

- [docs/zh/usage.md](./docs/zh/usage.md)
- [docs/en/usage.md](./docs/en/usage.md)
- [docs/zh/design.md](./docs/zh/design.md)

## 贡献

见 [CONTRIBUTING.md](./CONTRIBUTING.md) · [中文](./CONTRIBUTING.zh-CN.md)。  
安全：[SECURITY.md](./SECURITY.md)。行为准则：[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)。变更：[CHANGELOG.md](./CHANGELOG.md)。

## 不包含

策略包、交易所密钥、券商代码、真实主机 dump、付费 zip。
