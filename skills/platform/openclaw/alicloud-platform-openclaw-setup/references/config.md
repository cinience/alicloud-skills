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
        "apiKey": "<YOUR_DASHSCOPE_API_KEY>",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "qwen3.5-plus",
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
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {"primary": "bailian/qwen3.5-plus"},
      "models": {
        "bailian/glm-5": {"alias": "GLM-5"},
        "bailian/qwen3.5-plus": {"alias": "qwen3.5-plus"}
      },
      "workspace": "/root/",
      "compaction": {"mode": "safeguard"},
      "maxConcurrent": 4,
      "subagents": {"maxConcurrent": 8},
      "imageModel": {"primary": "bailian/qwen3.5-plus"},
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
    "dingtalk": {
      "enabled": true,
      "clientId": "<APP_KEY>",
      "clientSecret": "<APP_SECRET>",
      "robotCode": "<ROBOT_CODE_OR_APP_KEY>",
      "corpId": "<CORP_ID>",
      "agentId": "<AGENT_ID>",
      "dmPolicy": "open",
      "groupPolicy": "open",
      "allowFrom": ["*"],
      "messageType": "card",
      "cardTemplateId": "<TEMPLATE_ID>.schema",
      "cardTemplateKey": "content",
      "debug": false
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
    "allow": ["dingtalk"],
    "entries": {
      "dingtalk": {"enabled": true}
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
| `robotCode` | ✓ | Robot code (usually same as clientId) |
| `corpId` | ✓ | Enterprise ID |
| `agentId` | ✓ | Application ID |
| `dmPolicy` | | Direct message policy: `open`, `pairing`, `allowlist` |
| `groupPolicy` | | Group chat policy: `open`, `allowlist` |
| `messageType` | | Response type: `markdown`, `card` |
| `cardTemplateId` | | AI card template ID (if using card) |

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
| Auth profiles | `~/.openclaw/agents/main/agent/auth-profiles.json` | Provider credentials |
| Service file | `~/.config/systemd/user/openclaw-gateway.service` | Systemd service |
| Logs | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` | Daily log files |
| Plugins | `~/.openclaw/extensions/` | Installed plugins |

## Notes

- Keep model `id` and `agents.defaults.model.primary` aligned.
- Use `provider/model` format, for example `bailian/qwen3.5-plus`.
- Store real credentials only on target hosts, not in git-tracked files.
