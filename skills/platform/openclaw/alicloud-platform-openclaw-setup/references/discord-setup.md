# Discord Channel Setup Guide

## Contents

1. Prerequisites
2. Create Discord bot
3. Configure OpenClaw
4. Start and verify
5. Pairing and policy checks
6. Common issues

## Prerequisites

- Discord application admin access.
- OpenClaw installed on target host.
- Gateway runtime available on target host.

## Create Discord Bot

1. Open Discord Developer Portal (`https://discord.com/developers/applications`).
2. Create a new application and add a bot.
3. Copy the bot token.
4. Enable required intents in bot settings:
   - Message Content Intent
   - Direct Messages / Guild Messages intents as needed
5. Invite bot to target server/channel with message permissions.

## Configure OpenClaw

Set token using one of these methods:

1. In `~/.openclaw/openclaw.json`:

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "<DISCORD_BOT_TOKEN>",
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist"
    }
  }
}
```

2. Or environment variable:

```bash
export DISCORD_BOT_TOKEN=<DISCORD_BOT_TOKEN>
```

For group controls, define allowlist with mention requirement:

```json
{
  "channels": {
    "discord": {
      "groups": {
        "<CHANNEL_OR_GUILD_ID>": {
          "enabled": true,
          "requireMention": true
        }
      }
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

Send a DM to the bot in Discord. If `dmPolicy` is `pairing`, approve first:

```bash
openclaw pairing list discord
openclaw pairing approve discord <PAIRING_CODE>
```

## Pairing and Policy Checks

- `dmPolicy=pairing`: first DM requires approval code.
- `groupPolicy=allowlist`: only allowed groups/channels are processed.
- `requireMention=true`: bot responds only when explicitly mentioned.

## Common Issues

- Bot offline: token invalid or bot not invited to server.
- No replies in server: missing intents or insufficient bot permissions.
- DM not working: pairing pending; approve with `openclaw pairing`.
- Group messages ignored: check `groupPolicy` and allowlist IDs.
