---
name: xiaohongshu-mcp
description: Start and recover the local Xiaohongshu MCP service on Windows when xiaohongshu MCP tools are unavailable.
metadata: {"abot":{"requires":{"env":[],"bins":[]}}}
---

# Xiaohongshu MCP Recovery (Windows)

Use this skill when Xiaohongshu MCP tools are needed but unavailable.

## When to use

- User asks for Xiaohongshu/RedNote operations.
- Tools named `mcp_xiaohongshu_*` are missing.
- MCP endpoint `http://127.0.0.1:18060/mcp` is not reachable.

## Default strategy (low freedom)

Always use this order. Do not improvise with `go run` or random shell syntax first.

1. Health check: confirm port `18060` is listening.
2. If not listening, start MCP with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "{baseDir}/scripts/start-xhs-mcp.ps1"
```

3. Re-check port `18060`.
4. If still down, ask user for `ABOT_XHS_MCP_EXE` (or explicit exe path) and retry once.
5. If user started service manually, suggest `/mcp-reload`.

## QR code delivery rule (must render)

When calling `mcp_xiaohongshu_get_login_qrcode`:

1. The tool now returns THREE formats of QR code:
   - **Base64 image**: Original image data (for display in GUI)
   - **Terminal QR code**: ASCII art QR code that displays correctly in terminal
   - **HTTP URL**: Temporary hosted URL (valid for 5 minutes) for remote access

2. Display strategy:
   - In terminal/CLI: Show the `terminal_qr` field directly - it's already formatted for terminal display
   - For remote users: Provide the `hosted_url` - they can open it in browser
   - Never paste long base64 text to the user as final output

3. Example response handling:
   ```
    扫码登录二维码已生成：

   [终端二维码显示在这里]

   远程访问链接: http://127.0.0.1:18060/qrcode/qrcode_1234567890.png
   链接过期时间: 2026-03-10T15:30:00+08:00

   请在 2026-03-10 15:25:00 前用小红书 App 扫码登录
   ```

4. After sending QR, tell the user the expiry time and wait for confirmation.

## Failure handling

If startup fails after one scripted retry:

- Ask for one concrete action:
  - provide/correct exe path (`ABOT_XHS_MCP_EXE`)
  - refresh login/cookies with login binary, then retry MCP start

## Notes

- `abot` auto-retries MCP connection on each message.
- If user manually restarted MCP and wants immediate refresh, they can send `/mcp-reload`.
- Terminal QR codes use half-block characters (▀▄█) for better resolution
- HTTP hosted QR codes are automatically cleaned up after 5 minutes