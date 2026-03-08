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

## Positioning

`abot` is a focused framework for agent engineering experiments.

- Keep the essential core: agent loop, tools, skills, cron, heartbeat, MCP.
- Keep practical channels only: CLI, Telegram, Feishu (Lark), QQ (OneBot).
- Remove low-value ecosystem integrations to reduce maintenance overhead.

## Acknowledgment

- `abot` originally started as a fork of [`HKUDS/nanobot`](https://github.com/HKUDS/nanobot).
- We appreciate nanobot maintainers and contributors for the open-source groundwork.
- `abot` now follows its own roadmap focused on agent engineering practice.

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

## Channel Configuration

### Telegram

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

### Feishu

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

### QQ (OneBot)

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

Notes:

- QQ uses the OneBot implementation by default.
- Recommended adapters: Lagrange.onebot / NapCat.

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
