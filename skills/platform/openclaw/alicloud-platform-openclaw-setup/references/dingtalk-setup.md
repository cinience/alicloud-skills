# DingTalk Bot Setup Guide

## Contents

1. Prerequisites
2. Create application
3. Collect credentials
4. Configure robot (Stream mode)
5. Configure permissions
6. Publish app
7. Install official connector plugin
8. Field mapping and troubleshooting

## Prerequisites

- DingTalk administrator access
- Enterprise account (not personal)

## Step 1: Create Application

1. Go to [DingTalk Open Platform](https://open.dingtalk.com/)
2. Login with admin account
3. Navigate to: **App Development** → **Enterprise Internal Development** → **Create App**
4. Fill in application info:
   - App name: Your bot name
   - App description: Brief description
   - App icon: Upload an icon

## Step 2: Get Credentials

After creating the application, find these values:

| Credential | Location |
|------------|----------|
| **ClientId (AppKey)** | Basic Info → Credentials and Basic Info |
| **ClientSecret (AppSecret)** | Basic Info → Credentials and Basic Info |

## Step 3: Configure Robot

1. Navigate to: **App Features** → **Bot**
2. Enable robot feature
3. Configure:
   - Bot type: **Stream mode** (recommended, no public IP required)
   - Message receiving mode: Stream
   - Bot name: Your bot name

## Step 4: Permission Configuration

Navigate to: **Permission Management** → **Permission Requests**

Required permissions:
- `qyapi_chat_manage` - Group chat management
- `qyapi_robot_sendmsg` - Robot send message
- `Contact.User.Read` - Read user info
- `Card.Streaming.Write` - AI card streaming write
- `Card.Instance.Write` - AI card instance write

## Step 5: Deploy & Publish

1. Navigate to: **Version Management and Release**
2. Create new version
3. Fill in version details
4. Submit for review (internal apps usually auto-approve)
5. Publish to enterprise

## Step 6: Install Official OpenClaw Connector

```bash
openclaw plugins install @dingtalk-real-ai/dingtalk-connector --pin
# or install from official GitHub repo
openclaw plugins install https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector.git
openclaw plugins list | grep dingtalk
```

## Configuration Mapping

| DingTalk Field | OpenClaw Config Field |
|----------------|----------------------|
| AppKey | `channels.dingtalk-connector.clientId` |
| AppSecret | `channels.dingtalk-connector.clientSecret` |
| Gateway token | `channels.dingtalk-connector.gatewayToken` |
| Session timeout (optional) | `channels.dingtalk-connector.sessionTimeout` |

## Stream Mode vs Webhook

| Feature | Stream Mode | Webhook Mode |
|---------|-------------|--------------|
| Public IP required | No | Yes |
| Setup complexity | Simple | Complex |
| Firewall friendly | Yes | No |
| Recommended | ✓ | |

OpenClaw official DingTalk connector uses **Stream Mode** by default.

## Troubleshooting

### Bot not responding

1. Check robot is published
2. Verify Stream mode is enabled
3. Check `openclaw gateway logs -f` for errors

### Permission errors

1. Verify all required permissions are approved
2. Re-publish after adding permissions

### Card not rendering

1. Verify `Card.Streaming.Write` and `Card.Instance.Write` are approved
2. Re-publish app after permission changes
3. Check `openclaw logs --follow` for `gateway/channels/dingtalk-connector` errors
