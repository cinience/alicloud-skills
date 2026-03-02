---
name: alicloud-platform-openclaw-setup
description: Install and configure OpenClaw with DingTalk, Feishu, Discord, and additional channels with Bailian/DashScope models on Linux hosts. Use when provisioning a new OpenClaw node, troubleshooting gateway/channel startup, standardizing openclaw.json mapping, or automatically discovering extra channels from https://docs.openclaw.ai/channels.
---

# OpenClaw Setup

Deploy OpenClaw on Linux, enable DingTalk, Feishu, Discord, or other documented channels, and verify gateway health.

## Use This Workflow

Run this sequence in order:

1. Prepare Linux runtime and install OpenClaw.
2. Discover channels from official docs (required for new channel requests).
3. Install and verify channel integrations.
4. Create/merge `~/.openclaw/openclaw.json`.
5. Configure and start gateway service.
6. Run health checks and collect logs.

## Prerequisites

- SSH access to target Linux host (Debian/Ubuntu preferred).
- DingTalk enterprise app credentials (`AppKey`, `AppSecret`, `AgentId`, `CorpId`) or Feishu app credentials (`App ID`, `App Secret`) or Discord bot token.
- DashScope API key.

## Step 1: Prepare Runtime

```bash
ssh root@<server>
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
node --version
npm --version
```

## Step 2: Install OpenClaw and Channel Integrations

```bash
npm install -g openclaw@latest
openclaw --version

# DingTalk channel
openclaw plugins install @soimy/dingtalk
openclaw plugins list | grep dingtalk

# Feishu channel
openclaw plugins install @openclaw/feishu
openclaw plugins list | grep feishu

# Discord channel (built-in, no extra plugin needed)
# Configure token in Step 3 and start gateway in Step 4
```

If plugin dependencies are missing:

```bash
cd ~/.openclaw/extensions/dingtalk
npm install dingtalk-stream axios form-data zod --save
```

## Step 3: Auto-Discover Additional Channels from Official Docs

When user asks for any extra channel beyond current setup, do this first:

1. Open `https://docs.openclaw.ai/channels/index`.
2. Identify requested channel pages from the "Supported channels" list.
3. Open each channel page and extract:
   - Whether it is built-in or plugin-based.
   - Exact install command (do not guess package names).
   - Required credentials/tokens and config keys.
4. Apply installation/configuration on host.
5. Record channel-specific notes into `~/.openclaw/openclaw.json`.

Use the exact workflow in [references/channel-discovery.md](references/channel-discovery.md).

## Step 4: Configure `openclaw.json`

Create or update `~/.openclaw/openclaw.json` with:

- `models.providers.bailian` for DashScope endpoint and models.
- `agents.defaults.model.primary` in `provider/model` format.
- `channels.dingtalk`, `channels.feishu`, or `channels.discord` credentials and policy.
- `plugins.allow` including installed channel plugins.

Use the full template in [references/config.md](references/config.md).
Use DingTalk field mapping in [references/dingtalk-setup.md](references/dingtalk-setup.md).
Use Feishu setup and field mapping in [references/feishu-setup.md](references/feishu-setup.md).
Use Discord setup and field mapping in [references/discord-setup.md](references/discord-setup.md).
Use channel discovery workflow in [references/channel-discovery.md](references/channel-discovery.md).

## Step 5: Install and Start Gateway

```bash
openclaw gateway install
openclaw gateway start
openclaw gateway status
```

If running with user-level systemd, reload after config changes:

```bash
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway
```

## Step 6: Verify and Troubleshoot

```bash
openclaw doctor
openclaw gateway status
openclaw gateway logs -f
```

Common failures:

- Plugin not loaded: re-run plugin install and check `plugins.allow`.
- Unknown model: check `agents.defaults.model.primary` format (`provider/model-id`).
- API key error: verify `models.providers.bailian.apiKey`.
- DingTalk no response: check app publish status and required permissions.
- Feishu no response: check event subscription mode is WebSocket and gateway is running.
- Discord no response: verify bot intents, token, and first-DM pairing approval.

## Security Notes

- Do not hardcode real secrets in repository files.
- Keep production keys in server-local configs or secret managers.
- Redact logs before sharing in tickets or chat.
