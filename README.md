<div align="center">
  <img src="abot_logo.png" alt="abot logo" width="420" />
  <h1>abot</h1>
  <p><strong>Agent Engineering Lab</strong></p>
  <p>
    Lightweight, controllable, and hackable agent framework for real engineering experiments.
  </p>
  <p>
    <a href="#english">English</a> |
    <a href="#chinese">中文</a>
  </p>
</div>

---

<a id="english"></a>
## English

### Overview

`abot` is a focused agent-engineering fork designed for practical experimentation.

- Keep a compact core: agent loop, tools, skills, cron, heartbeat, MCP.
- Keep only practical channels: CLI, Telegram, Feishu (Lark), QQ (OneBot).
- Remove broad integrations that add maintenance cost without research value.

### Acknowledgment

- `abot` started as a fork of [`HKUDS/nanobot`](https://github.com/HKUDS/nanobot).
- We appreciate the nanobot maintainers and contributors for the original architecture and groundwork.
- `abot` now follows its own roadmap focused on agent engineering experiments.

### Quick Start

1. Install from source

```bash
git clone <your-repo-url>
cd abot
pip install -e .
```

2. Initialize config

```bash
python -m abot onboard
```

This creates:

- `~/.abot/config.json`
- `~/.abot/workspace/`

3. Configure provider (`~/.abot/config.json`)

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

4. Start chatting in CLI

```bash
python -m abot agent
```

### Channel Configuration

#### Telegram

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

#### Feishu

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

#### QQ (OneBot)

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

- QQ channel uses OneBot by default.
- Recommended adapters: Lagrange.onebot / NapCat.

### Run Gateway

```bash
python -m abot gateway
```

### Useful Commands

```bash
python -m abot status
python -m abot channels status
python -m abot provider login openai-codex
python -m abot provider login github-copilot
```

### Packaging

- package name: `abot-ai`
- CLI entry: `abot`

### Docker

```bash
docker compose up -d abot-gateway
```

### Development

```bash
pytest
```

### License

MIT

---

<a id="chinese"></a>
## 中文

### 项目简介

`abot` 是一个面向 Agent 工程实践的轻量框架。

- 保留核心能力：agent loop、tools、skills、cron、heartbeat、MCP。
- 只保留高价值通道：CLI、Telegram、飞书、QQ（OneBot）。
- 去掉对当前研究目标帮助不大的生态模块，降低维护复杂度。

### 致谢与来源

- `abot` 最初基于 [`HKUDS/nanobot`](https://github.com/HKUDS/nanobot) 分叉而来。
- 感谢 nanobot 维护者与贡献者提供的架构基础与开源工作。
- `abot` 当前已按自身路线演进，重点聚焦 Agent 工程实验与可复现实践。

### 快速开始

1. 从源码安装

```bash
git clone <你的仓库地址>
cd abot
pip install -e .
```

2. 初始化配置

```bash
python -m abot onboard
```

将创建：

- `~/.abot/config.json`
- `~/.abot/workspace/`

3. 配置模型提供商（编辑 `~/.abot/config.json`）

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

### 通道配置

#### Telegram

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

#### 飞书

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

#### QQ（OneBot）

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

说明：

- QQ 默认使用 OneBot 实现。
- 推荐适配器：Lagrange.onebot / NapCat。

### 启动网关

```bash
python -m abot gateway
```

### 常用命令

```bash
python -m abot status
python -m abot channels status
python -m abot provider login openai-codex
python -m abot provider login github-copilot
```

### 打包信息

- 包名：`abot-ai`
- 命令入口：`abot`

### Docker

```bash
docker compose up -d abot-gateway
```

### 开发与测试

```bash
pytest
```

### 许可证

MIT
