# DingTalk Bot Setup Guide

## Contents

1. Prerequisites
2. Create application
3. Collect credentials
4. Configure robot (Stream mode)
5. Create AI card template
6. Configure permissions
7. Publish app
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
| **AgentId** | Basic Info → Credentials and Basic Info |
| **CorpId** | Developer Console header (top-right) |

## Step 3: Configure Robot

1. Navigate to: **App Features** → **Bot**
2. Enable robot feature
3. Configure:
   - Bot type: **Stream mode** (recommended, no public IP required)
   - Message receiving mode: Stream
   - Bot name: Your bot name

## Step 4: Create AI Card Template

For interactive card responses:

1. Go to: **Card Platform** → **AI Cards** → **My Cards**
2. Create new card template
3. Select: **AI Interactive Card** template
4. Configure card layout
5. Save and get **Card Template ID** (format: `xxxxx-xxxxx-xxxxx.schema`)

## Step 5: Permission Configuration

Navigate to: **Permission Management** → **Permission Requests**

Required permissions:
- `qyapi_chat_manage` - Group chat management
- `qyapi_robot_sendmsg` - Robot send message
- `Contact.User.Read` - Read user info

## Step 6: Deploy & Publish

1. Navigate to: **Version Management and Release**
2. Create new version
3. Fill in version details
4. Submit for review (internal apps usually auto-approve)
5. Publish to enterprise

## Configuration Mapping

| DingTalk Field | OpenClaw Config Field |
|----------------|----------------------|
| AppKey | `channels.dingtalk.clientId` |
| AppSecret | `channels.dingtalk.clientSecret` |
| AppKey (same) | `channels.dingtalk.robotCode` |
| CorpId | `channels.dingtalk.corpId` |
| AgentId | `channels.dingtalk.agentId` |
| Card Template ID | `channels.dingtalk.cardTemplateId` |

## Stream Mode vs Webhook

| Feature | Stream Mode | Webhook Mode |
|---------|-------------|--------------|
| Public IP required | No | Yes |
| Setup complexity | Simple | Complex |
| Firewall friendly | Yes | No |
| Recommended | ✓ | |

OpenClaw DingTalk plugin uses **Stream Mode** by default.

## Troubleshooting

### Bot not responding

1. Check robot is published
2. Verify Stream mode is enabled
3. Check `openclaw gateway logs -f` for errors

### Permission errors

1. Verify all required permissions are approved
2. Re-publish after adding permissions

### Card not rendering

1. Verify `cardTemplateId` ends with `.schema`
2. Check card template is published
3. Ensure `messageType` is set to `card`
