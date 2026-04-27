---
name: alicloud-platform-openclaw-setup-test
description: Minimal smoke test for OpenClaw setup skill. Validate official channel discovery workflow, DingTalk/Feishu integrations, Discord token configuration, and gateway health checks with non-destructive commands.
version: 1.0.0
---

Category: test

# OpenClaw Setup Minimal Smoke Test

## Prerequisites

- Target host has Node.js 20+ installed.
- `openclaw` command is available.
- DashScope API key and DingTalk/Feishu app credentials or Discord bot token are prepared (masked placeholders are acceptable).
- Target skill: `skills/platform/openclaw/alicloud-platform-openclaw-setup/`.

## Test Steps

1) Run `openclaw --version` and verify CLI availability.
2) Open `https://docs.openclaw.ai/channels/index` and verify target channel is discoverable from official list.
3) Run `openclaw plugins list` and verify `dingtalk` or `feishu` plugin is installed/detected (if those channels are used).
4) Check `~/.openclaw/openclaw.json` and verify Discord uses `channels.discord.token` or environment variable `DISCORD_BOT_TOKEN`.
5) Run `openclaw doctor` and record the configuration checks.
6) Run `openclaw gateway status` and record runtime/probe status.

## Expected Results

- CLI commands execute successfully with exit code 0.
- Official channels index is reachable and channel page can be resolved.
- Plugin list contains `dingtalk` or `feishu` when those channels are configured.
- Discord configuration includes a valid token source (`channels.discord.token` or `DISCORD_BOT_TOKEN`).
- `doctor` shows no fatal errors (missing-credential warnings are acceptable).
- `gateway status` output is structurally complete; if not running, error details are actionable.

## Evidence Storage

- Save command outputs to: `output/alicloud-platform-openclaw-setup-test/`.
