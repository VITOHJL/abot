<div align="center">
  <img src="./abot_logo.png" alt="abot logo" width="420" />
  <h1>abot</h1>
  <p><strong>Agent Engineering Lab</strong></p>
  <p>A lightweight, controllable, and evolvable framework for practical agent engineering.</p>
</div>

<div align="center">
  <img src="https://img.shields.io/github/stars/VITOHJL/abot?style=flat&logo=github" alt="GitHub stars" />
  <img src="https://img.shields.io/github/forks/VITOHJL/abot?style=flat&logo=github" alt="GitHub forks" />
  <img src="https://img.shields.io/badge/python-3.11%2B-blue" alt="Python" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License" />
</div>

<div align="center">

[English](./README_en.md) | [中文](./README.md)

</div>

---

<div align="center">

[Quick Start](#quickstart-en) · [Engineering](#engineering-en) · [Channels](#channels-en) · [Commands](#commands-en) · [Acknowledgment](#ack-en)

</div>

| Module | Current choice |
| --- | --- |
| Core capabilities | `agent loop` / `tools` / `skills` / `cron` / `heartbeat` / `MCP` |
| Focus channels | `CLI` / `Telegram` / `Feishu` / `QQ OneBot` |
| Engineering target | A reproducible, measurable, maintainable agent experimentation framework |
| Product direction | Reduce ecosystem noise and maximize control + iteration speed |

<a id="positioning-en"></a>
## Positioning

`abot` is a focused framework for agent engineering experiments.

- Keep the essential core: agent loop, tools, skills, cron, heartbeat, MCP.
- Keep practical channels only: CLI, Telegram, Feishu (Lark), QQ (OneBot).
- Remove low-value ecosystem integrations to reduce maintenance overhead.

<a id="engineering-en"></a>
## Agent Engineering Design (Problem -> Handling)

| Engineering challenge | Current handling |
| --- | --- |
| Context growth in long conversations | Compression is token-budget driven: `budget = max_tokens_input - max_tokens - reserve`, with `compression_start_ratio` / `compression_target_ratio` as watermarks; history chunks are selected by token estimate and consolidated asynchronously in background tasks. |
| Traceability after compression | Session messages are not destructively rewritten. A contiguous `_compressed_until` boundary is maintained, and a compressed view is built only for prompting; raw records remain while summaries are written to `memory/HISTORY.md` and `memory/MEMORY.md`. |
| Inconsistent token accounting across providers | Prefer model `usage` (`total_tokens` or `prompt_tokens + completion_tokens`); fall back to provider-side token counter, then to `tiktoken` estimation. |
| Durable session persistence and migration | Sessions are stored in `sessions/*.jsonl` (metadata header + message lines). The message model stays append-only, and legacy `~/.abot/sessions` files are auto-migrated when detected. |
| Reliable memory updates | Memory writes are normalized via the `save_memory` tool-call contract, with defensive argument parsing for provider differences (dict/string/list). |
| Safe and resilient tool execution | Tool arguments go through schema cast + validation, oversized tool results are truncated before persisting to session history, and `restrict_to_workspace` can scope filesystem/exec tools to workspace boundaries. |
| Runtime control and cancellation | Each inbound message runs as an independent task; `/stop` cancels active session tasks, background compression, and subagents; MCP uses lazy connection with cleanup on failure and retry on later messages. |
| Capability scaling without prompt bloat | Skills use progressive loading: skill summary in system prompt, on-demand `SKILL.md` reads, plus auto-injection for `always` skills. |

<a id="ack-en"></a>
## Acknowledgment

- `abot` originally started as a fork of [`HKUDS/nanobot`](https://github.com/HKUDS/nanobot).
- We appreciate nanobot maintainers and contributors for the open-source groundwork.
- `abot` now follows its own roadmap focused on agent engineering practice.

<a id="quickstart-en"></a>
## Quick Start

1. Install

```bash
git clone https://github.com/VITOHJL/abot.git
cd abot
pip install -e .
```

2. Initialize

```bash
python -m abot onboard
```

3. Configure model provider (`~/.abot/config.json`)

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

4. Start CLI chat

```bash
python -m abot agent
```

<a id="channels-en"></a>
## Channel Configuration

> [!TIP]
> Enable only the channels you actively use to reduce operational and debugging overhead.

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
<summary><strong>Feishu</strong></summary>

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
<summary><strong>QQ (OneBot)</strong></summary>

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

Notes:

- QQ uses the OneBot implementation by default.
- Recommended adapters: Lagrange.onebot / NapCat.

<a id="commands-en"></a>
## Useful Commands

```bash
python -m abot gateway
python -m abot status
python -m abot channels status
python -m abot provider login openai-codex
python -m abot provider login github-copilot
```

## Thanks to Contributors

Even with a small contributor base today, every contribution matters.

### Current Contributor

- [@VITOHJL](https://github.com/VITOHJL) - Maintainer

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
