# Feishu Channel Setup Guide

## Contents

1. Prerequisites
2. Install plugin
3. Create Feishu app
4. Configure OpenClaw
5. Start and verify
6. Common issues

## Prerequisites

- Feishu or Lark tenant admin access.
- OpenClaw installed on target host.
- Gateway runtime available on target host.

## Install Plugin

```bash
openclaw plugins install @openclaw/feishu
openclaw plugins list | grep feishu
```

## Create Feishu App

1. Visit Feishu Open Platform (`https://open.feishu.cn/app`) and create an enterprise app.
2. Copy `App ID` and `App Secret` from credentials page.
3. Enable bot capability for the app.
4. Use WebSocket event subscription mode.

For international Lark tenant, use `https://open.larksuite.com/app`.

## Configure OpenClaw

Recommended CLI onboarding:

```bash
openclaw onboard
```

If OpenClaw is already initialized, add channel directly:

```bash
openclaw channels add
```

Choose `Feishu` in interactive prompt and provide `App ID` + `App Secret`.

Config file method (`~/.openclaw/openclaw.json`):

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "domain": "feishu",
      "dmPolicy": "pairing",
      "groupPolicy": "open",
      "accounts": {
        "main": {
          "appId": "cli_xxx",
          "appSecret": "<APP_SECRET>",
          "botName": "OpenClaw Assistant"
        }
      }
    }
  }
}
```

Lark international tenant example:

```json
{
  "channels": {
    "feishu": {
      "domain": "lark"
    }
  }
}
```

## Start and Verify

```bash
openclaw gateway
openclaw gateway status
openclaw logs --follow
```

Send a test message to the bot in Feishu. If `dmPolicy` is `pairing`, approve code:

```bash
openclaw pairing list feishu
openclaw pairing approve feishu <PAIRING_CODE>
```

## Common Issues

- No reply: verify Feishu app publish status and WebSocket mode.
- Pairing blocked: approve pending pairing request or switch policy.
- Lark tenant failure: set `channels.feishu.domain` to `lark`.
- Group message ignored: check `groupPolicy` and `groups.<chat_id>.requireMention`.
