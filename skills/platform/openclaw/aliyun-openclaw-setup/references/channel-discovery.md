# Channel Discovery and Auto-Install Workflow

## Contents

1. Trigger conditions
2. Discovery workflow
3. Installation decision rules
4. Configuration merge rules
5. Verification checklist

## Trigger Conditions

Run this workflow when:

- The user asks to add a new channel not already covered by local references.
- Existing channel setup fails and the docs may have changed.
- You need to verify whether a channel is built-in or plugin-based.

## Discovery Workflow

1. Open `https://docs.openclaw.ai/channels/index`.
2. Read the current supported channels list.
3. For each target channel, open its channel page from that list.
4. Extract exactly from docs:
   - Required install method.
   - CLI steps.
   - Required credentials.
   - `openclaw.json` key paths.
   - Any policy defaults (dm/group/allowlist).

Do not infer package names or field names when docs provide exact values.

## Installation Decision Rules

Use the following decision tree per channel page:

1. If docs state channel is built-in:
   - Do not install plugin.
   - Configure channel keys and credentials only.
2. If docs provide a plugin package:
   - Install exactly with documented command.
   - Verify with `openclaw plugins list`.
3. If docs show interactive onboarding:
   - Prefer `openclaw onboard` / `openclaw channels add` first.
   - Use direct JSON edit as fallback for automation.

## Configuration Merge Rules

1. Keep existing working channel configs unchanged.
2. Add new channel config under `channels.<channel_name>`.
3. Update `plugins.allow` only for plugin-based channels.
4. Keep secrets as placeholders in repo docs and real values only on target hosts.
5. Preserve `agents.defaults.model.primary` and provider settings unless user requests model changes.

## Verification Checklist

After adding a channel:

1. Run `openclaw doctor`.
2. Run `openclaw gateway status`.
3. Check logs (`openclaw gateway logs -f` or `openclaw logs --follow`).
4. Send one real message from that channel and confirm response.
5. If channel uses pairing, run `openclaw pairing list <channel>` and approve pending code.
