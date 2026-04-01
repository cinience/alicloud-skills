# OpenClaw Configuration Reference

## Contents

1. Complete configuration template
2. Model provider configuration
3. DingTalk channel configuration
4. Feishu channel configuration
5. Discord channel configuration
6. Gateway configuration
7. File locations

## Complete Configuration Template

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "bailian": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "${DASHSCOPE_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3-plus",
            "name": "qwen3-plus",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": {"input": 0.0025, "output": 0.01, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 1048576,
            "maxTokens": 65536
          },
          {
            "id": "glm-5",
            "name": "glm-5",
            "reasoning": false,
            "input": ["text"],
            "cost": {"input": 0.0025, "output": 0.01, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 202752,
            "maxTokens": 16384
          },
          {
            "id": "minimax-m2.5",
            "name": "MiniMax-M2.5",
            "reasoning": false,
            "input": ["text"],
            "cost": {"input": 0.0025, "output": 0.01, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 200000,
            "maxTokens": 8192
          },
          {
            "id": "kimi-k2.5",
            "name": "kimi-k2.5",
            "reasoning": false,
            "input": ["text"],
            "cost": {"input": 0.0025, "output": 0.01, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 131072,
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian/glm-5",
        "fallbacks": [
          "bailian/qwen3-plus",
          "bailian/minimax-m2.5",
          "bailian/kimi-k2.5"
        ]
      },
      "models": {
        "bailian/qwen3-plus": {"alias": "qwen3-plus"},
        "bailian/glm-5": {"alias": "GLM-5"},
        "bailian/minimax-m2.5": {"alias": "MiniMax-M2.5"},
        "bailian/kimi-k2.5": {"alias": "kimi-k2.5"}
      },
      "workspace": "/root/",
      "compaction": {"mode": "safeguard"},
      "maxConcurrent": 4,
      "subagents": {"maxConcurrent": 8},
      "imageModel": {"primary": "bailian/qwen3-plus"},
      "memorySearch": {"enabled": false}
    }
  },
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true,
    "ownerDisplay": "raw"
  },
  "channels": {
    "dingtalk-connector": {
      "enabled": true,
      "clientId": "<APP_KEY>",
      "clientSecret": "<APP_SECRET>",
      "gatewayToken": "<OPENCLAW_GATEWAY_TOKEN>",
      "sessionTimeout": 1800000,
      "dmPolicy": "open",
      "allowFrom": ["*"]
    },
    "feishu": {
      "enabled": true,
      "domain": "feishu",
      "dmPolicy": "pairing",
      "groupPolicy": "open",
      "accounts": {
        "main": {
          "appId": "<FEISHU_APP_ID>",
          "appSecret": "<FEISHU_APP_SECRET>",
          "botName": "OpenClaw Assistant"
        }
      }
    },
    "discord": {
      "enabled": true,
      "token": "<DISCORD_BOT_TOKEN>",
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist",
      "groups": {
        "<CHANNEL_OR_GUILD_ID>": {
          "enabled": true,
          "requireMention": true
        }
      }
    }
  },
  "gateway": {
    "mode": "local",
    "auth": {
      "mode": "token",
      "token": "auto-generated-token"
    }
  },
  "plugins": {
    "enabled": true,
    "allow": ["dingtalk-connector"],
    "entries": {
      "dingtalk-connector": {"enabled": true}
    }
  }
}
```

## Model Provider Configuration

### Bailian (DashScope) Provider

| Field | Type | Description |
|-------|------|-------------|
| `baseUrl` | string | API endpoint URL |
| `apiKey` | string | DashScope API key |
| `api` | string | API type: `openai-completions` |
| `models` | array | Available model definitions |

Protocol and endpoint pairing:

- `openai-completions` -> `https://dashscope.aliyuncs.com/compatible-mode/v1`
- `openai-responses` -> `https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1`

### Model Definition

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Model identifier |
| `name` | string | Display name |
| `input` | array | Supported input types: `text`, `image` |
| `contextWindow` | number | Max context tokens |
| `maxTokens` | number | Max output tokens |

## DingTalk Channel Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `clientId` | ✓ | AppKey from DingTalk |
| `clientSecret` | ✓ | AppSecret from DingTalk |
| `gatewayToken` | | Gateway auth token, usually `gateway.auth.token` |
| `sessionTimeout` | | Session timeout in ms, default `1800000` |
| `dmPolicy` | | Direct message policy: `open`, `pairing`, `allowlist` |
| `allowFrom` | | Allowlist for `dmPolicy: open`, usually `["*"]` |

## Feishu Channel Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `domain` | | `feishu` (default) or `lark` |
| `accounts.<name>.appId` | ✓ | Feishu app ID |
| `accounts.<name>.appSecret` | ✓ | Feishu app secret |
| `accounts.<name>.botName` | | Bot display name |
| `dmPolicy` | | Direct message policy: `open`, `pairing`, `allowlist` |
| `groupPolicy` | | Group chat policy: `open`, `allowlist` |

## Discord Channel Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `token` | ✓ | Discord bot token (or set `DISCORD_BOT_TOKEN`) |
| `dmPolicy` | | Direct message policy: `open`, `pairing`, `allowlist` |
| `groupPolicy` | | Group chat policy: `open`, `allowlist` |
| `groups.<id>.enabled` | | Enable specific server/channel allowlist entry |
| `groups.<id>.requireMention` | | Require explicit bot mention in group |

## Gateway Configuration

| Field | Description |
|-------|-------------|
| `mode` | `local` for local deployment |
| `auth.mode` | `token` for token-based auth |
| `auth.token` | Auto-generated on first install |

## File Locations

| File | Path | Description |
|------|------|-------------|
| Main config | `~/.openclaw/openclaw.json` | Primary configuration |
| Agent model override | `~/.openclaw/agents/main/agent/models.json` | Per-agent model/provider override (higher priority) |
| Auth profiles | `~/.openclaw/agents/main/agent/auth-profiles.json` | Provider credentials |
| Service file | `~/.config/systemd/user/openclaw-gateway.service` | Systemd service |
| Logs | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` | Daily log files |
| Plugins | `~/.openclaw/extensions/` | Installed plugins |

## Notes

- Keep model `id` and `agents.defaults.model.primary` aligned.
- Use `provider/model` format, for example `bailian/glm-5`.
- If model switches do not take effect, check `~/.openclaw/agents/main/agent/models.json` override first.
- For user-level systemd service, import env vars before restart:
  `systemctl --user import-environment DASHSCOPE_API_KEY`
- Store real credentials only on target hosts, not in git-tracked files.
