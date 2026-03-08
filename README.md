<div align="center">
  <img src="./abot_logo.png" alt="abot logo" width="420" />
  <h1>abot</h1>
  <p><strong>Agent Engineering Lab</strong></p>
  <p>面向 Agent 工程实践的轻量、可控、可演进框架</p>
</div>

<div align="center">
  <img src="https://img.shields.io/github/stars/VITOHJL/abot?style=flat&logo=github" alt="GitHub stars" />
  <img src="https://img.shields.io/github/forks/VITOHJL/abot?style=flat&logo=github" alt="GitHub forks" />
  <img src="https://img.shields.io/badge/python-3.11%2B-blue" alt="Python" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License" />
</div>

<div align="center">

[中文](./README.md) | [English](./README_en.md)

</div>

---

<div align="center">

[快速开始](#quickstart-zh) · [工程实现](#engineering-zh) · [通道配置](#channels-zh) · [常用命令](#commands-zh) · [致谢](#ack-zh)

</div>

| 模块 | 当前取舍 |
| --- | --- |
| 核心能力 | `agent loop` / `tools` / `skills` / `cron` / `heartbeat` / `MCP` |
| 重点通道 | `CLI` / `Telegram` / `飞书` / `QQ OneBot` |
| 工程目标 | 可复现、可评估、可维护的 Agent 实验框架 |
| 设计方向 | 精简生态干扰，强调可控性与演进速度 |

<a id="positioning-zh"></a>
## 项目定位

`abot` 是一个聚焦 Agent 工程实验的框架，核心目标是把“能跑”升级为“可复现、可评估、可维护”。

- 保留核心能力：agent loop、tools、skills、cron、heartbeat、MCP。
- 保留高价值通道：CLI、Telegram、飞书、QQ（OneBot）。
- 移除与当前研究目标弱相关的生态模块，降低复杂度与维护成本。

<a id="engineering-zh"></a>
## Agent 工程实现（问题 -> 处理方式）

| 工程挑战 | 处理方式（当前实现） |
| --- | --- |
| 长对话上下文膨胀 | 基于 token 预算触发压缩：`budget = max_tokens_input - max_tokens - reserve`，用 `compression_start_ratio` / `compression_target_ratio` 控制启停；按 token 选择历史 chunk 做 consolidation，后台异步执行。 |
| 压缩后如何保持可追溯 | 不直接改写会话消息，使用 `_compressed_until` 记录连续压缩边界，仅在推理时构造压缩视图；原始记录保留，摘要写入 `memory/HISTORY.md` 和 `memory/MEMORY.md`。 |
| Token 统计口径不一致 | 优先用模型 `usage`（`total_tokens` 或 `prompt_tokens + completion_tokens`）；不足时退化到 provider token counter，再退化到 `tiktoken`。 |
| 长会话持久化与兼容迁移 | 会话保存为 `sessions/*.jsonl`（首行 metadata + 后续消息）；消息模型保持 append-only；检测到旧目录 `~/.abot/sessions` 时自动迁移。 |
| 记忆写入稳定性 | 通过 `save_memory` 工具调用统一落盘；对 provider 返回参数做防御式解析（dict/string/list）以避免格式差异造成写入失败。 |
| 工具执行安全与稳健 | 工具参数先做 schema cast + validate；过长 tool result 写入会话前截断；可开启 `restrict_to_workspace` 限制文件/执行工具作用域。 |
| 运行时可控性 | 每条消息独立 task；`/stop` 可取消当前会话活跃任务、后台压缩和 subagent；MCP 使用懒连接与失败清理，后续消息可自动重试。 |
| 能力扩展与上下文平衡 | Skills 采用“摘要进系统提示 + 按需读取 `SKILL.md` + always 技能自动注入”的渐进加载方式，兼顾能力覆盖与上下文成本。 |

<a id="ack-zh"></a>
## 致谢与来源

- `abot` 最初基于 [`HKUDS/nanobot`](https://github.com/HKUDS/nanobot) 分叉。
- 感谢 nanobot 维护者与贡献者提供的架构基础和开源工作。
- `abot` 当前沿着自身路线持续演进，重点聚焦 Agent 工程实验场景。

<a id="quickstart-zh"></a>
## 快速开始

1. 安装

```bash
git clone https://github.com/VITOHJL/abot.git
cd abot
pip install -e .
```

2. 初始化

```bash
python -m abot onboard
```

3. 配置模型（编辑 `~/.abot/config.json`）

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "openrouter"
    }
  }
}
```

4. CLI 对话

```bash
python -m abot agent
```

<a id="channels-zh"></a>
## 通道配置

> [!TIP]
> 当前推荐仅启用你实际使用的通道，减少运维噪音与排障面。

<details>
<summary><strong>Telegram</strong></summary>

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

</details>

<details>
<summary><strong>飞书</strong></summary>

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "allowFrom": ["ou_xxx"]
    }
  }
}
```

</details>

<details>
<summary><strong>QQ（OneBot）</strong></summary>

```json
{
  "channels": {
    "qq": {
      "enabled": true,
      "apiUrl": "http://127.0.0.1:5700",
      "wsReverseUrl": "ws://127.0.0.1:8080/ws/reverse",
      "botQq": 123456789,
      "accessToken": "",
      "allowFrom": ["*"]
    }
  }
}
```

</details>

说明：

- QQ 默认使用 OneBot 通道实现。
- 推荐适配器：Lagrange.onebot / NapCat。

<a id="commands-zh"></a>
## 常用命令

```bash
python -m abot gateway
python -m abot status
python -m abot channels status
python -m abot provider login openai-codex
python -m abot provider login github-copilot
```

## 感谢贡献者

即使目前贡献者还不多，我们依然认真感谢每一位参与者。

### 当前贡献者

- [@VITOHJL](https://github.com/VITOHJL) - 项目维护者

<div align="center">
  <a href="https://github.com/VITOHJL/abot/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=VITOHJL/abot" alt="contributors" />
  </a>
</div>

## Star History

<div align="center">
  <a href="https://star-history.com/#VITOHJL/abot&Date">
    <img src="https://api.star-history.com/svg?repos=VITOHJL/abot&type=Date" alt="Star History Chart" />
  </a>
</div>

---

## License

MIT
