# Security Policy

## Supported Scope

This repository currently focuses on:

- core agent runtime
- tools / skills / MCP integration
- channels: CLI, Telegram, Feishu, QQ (OneBot)

Legacy channel implementations that were removed are out of scope.

## Reporting a Vulnerability

If you find a security issue, please report it privately to the maintainers.
Include:

- affected version / commit
- reproduction steps
- impact assessment
- suggested fix (optional)

Please avoid public disclosure before a fix is available.

## Security Recommendations

- Keep API keys in `~/.abot/config.json`; do not commit them.
- Use per-channel `allowFrom` allowlists in production.
- Keep `tools.restrictToWorkspace=true` when running on shared machines.
- Run with least privilege and isolated runtime users where possible.
- Review `exec` and MCP server configs before enabling untrusted commands.

## Third-Party Dependencies

- Update Python dependencies regularly.
- Pin versions in production deployments.
- Rebuild containers after dependency updates.

## OneBot Channel Notes

- Prefer reverse WebSocket on trusted local/private networks.
- Set `accessToken` for OneBot adapters when supported.
- Restrict adapter bind addresses and firewall exposure.

## Disclosure Process

1. Acknowledge report.
2. Reproduce and assess severity.
3. Prepare and verify fix.
4. Release patch and publish advisory notes.
