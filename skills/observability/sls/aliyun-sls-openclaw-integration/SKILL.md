---
name: aliyun-sls-openclaw-integration
description: Use when the user needs to integrate OpenClaw with Alibaba Cloud SLS/Observability, including collector setup, machine groups, indexes, dashboards, collection configs, or Logtail bindings on Linux.
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["aliyun"] },
      },
  }
---

# OpenClaw SLS Integration

This skill provisions Alibaba Cloud SLS observability for OpenClaw on Linux and keeps reruns safe.

At a high level, execute this flow:

1. Check and install `aliyun` CLI (install latest when missing)
2. Install `LoongCollector` by project region (skip if already running)
3. Create an identifier-based machine group (local identifier + cloud machine group)
4. Create `logstore` index and dashboards
5. Create `logstore` collection config
6. Bind the collection config to the machine group

---

## Capture Intent Before Execution

Before running commands, make sure the user intent is complete:

1. Confirm the target `PROJECT` and `LOGSTORE`.
2. Confirm Linux host access with `sudo` available.
3. Confirm AK/SK are already exported in environment variables.
4. If any required input is missing, ask for it first and do not run partial setup.

---

## Prerequisites

Required:
- `PROJECT`: SLS project name
- `LOGSTORE`: SLS logstore name

Read from environment variables:
- `ALIBABA_CLOUD_ACCESS_KEY_ID`
- `ALIBABA_CLOUD_ACCESS_KEY_SECRET`
- `ALIYUN_UID` (used for the local UID file under `/etc/ilogtail/users`)

Recommended optional:
- `ALIBABA_CLOUD_REGION_ID` (auto-resolved from `PROJECT` when not set)

> If you use different AK/SK variable names, export them to these standard names first.

---

## Expected Result

After successful execution, the environment should contain:

- Running `LoongCollector` (or `ilogtaild`) on the host
- Machine group `openclaw-sls-collector`
- Logstore index created on the target `LOGSTORE`
- Dashboards `openclaw-audit` and `openclaw-gateway`
- Collection config `openclaw-audit_${LOGSTORE}`
- Config binding between `openclaw-audit_${LOGSTORE}` and `openclaw-sls-collector`

---

## One-Time Execution Flow (Idempotent)

> The commands below are designed as "exists -> skip" and are safe to rerun.
> Strict template mode: for index/config/dashboard payloads, always read from files in `references/`.
> Do not handcraft or simplify JSON bodies beyond required placeholder replacement.

```bash
set -euo pipefail

# ===== User inputs =====
: "${PROJECT:?Please export PROJECT}"
: "${LOGSTORE:?Please export LOGSTORE}"
: "${ALIBABA_CLOUD_ACCESS_KEY_ID:?Please export ALIBABA_CLOUD_ACCESS_KEY_ID}"
: "${ALIBABA_CLOUD_ACCESS_KEY_SECRET:?Please export ALIBABA_CLOUD_ACCESS_KEY_SECRET}"
: "${ALIYUN_UID:?Please export ALIYUN_UID}"

MACHINE_GROUP="openclaw-sls-collector"
CONFIG_NAME="openclaw-audit_${LOGSTORE}"

# 1) Install aliyun CLI if missing (Linux)
if ! command -v aliyun >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y aliyun-cli
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y aliyun-cli
  elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y aliyun-cli
  elif command -v zypper >/dev/null 2>&1; then
    sudo zypper -n install aliyun-cli
  else
    echo "aliyun CLI not found. Install aliyun-cli manually for your Linux distribution." >&2
    exit 1
  fi
fi

# Export auth variables for aliyun CLI
export ALIBABA_CLOUD_ACCESS_KEY_ID
export ALIBABA_CLOUD_ACCESS_KEY_SECRET

is_loong_running() {
  if sudo /etc/init.d/loongcollectord status 2>/dev/null | grep -qi "running"; then
    return 0
  fi
  if sudo /etc/init.d/ilogtaild status 2>/dev/null | grep -qi "running"; then
    return 0
  fi
  return 1
}

# 2) Resolve region and install LoongCollector (skip when already running)
REGION_ID="${ALIBABA_CLOUD_REGION_ID:-}"
if [ -z "$REGION_ID" ]; then
  REGION_ID="$(aliyun sls GetProject --project "$PROJECT" --cli-query 'region' --quiet 2>/dev/null | tr -d '\"' || true)"
fi
if [ -z "$REGION_ID" ]; then
  echo "Cannot resolve region from project: $PROJECT. Please set ALIBABA_CLOUD_REGION_ID." >&2
  exit 1
fi

if ! is_loong_running; then
  wget "https://aliyun-observability-release-${REGION_ID}.oss-${REGION_ID}.aliyuncs.com/loongcollector/linux64/latest/loongcollector.sh" -O loongcollector.sh
  chmod +x loongcollector.sh
  ./loongcollector.sh install "${REGION_ID}"
fi

# Post-install verification: one of loongcollectord/ilogtaild must be running.
if ! is_loong_running; then
  sudo /etc/init.d/loongcollectord start >/dev/null 2>&1 || true
  sudo /etc/init.d/ilogtaild start >/dev/null 2>&1 || true
fi
if ! is_loong_running; then
  echo "LoongCollector installation check failed: neither loongcollectord nor ilogtaild is running." >&2
  exit 1
fi

# 3) Local user-defined identifier + create machine group
sudo mkdir -p /etc/ilogtail
sudo mkdir -p /etc/ilogtail/users
if [ ! -f /etc/ilogtail/user_defined_id ]; then
  sudo touch /etc/ilogtail/user_defined_id
fi
RAND8="$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 8)"
USER_DEFINED_ID_PREFIX="${PROJECT}_openclaw_sls_collector_"
EXISTING_USER_DEFINED_ID="$(sudo awk -v p="${USER_DEFINED_ID_PREFIX}" 'index($0,p)==1 {print; exit}' /etc/ilogtail/user_defined_id 2>/dev/null || true)"
if [ -n "${EXISTING_USER_DEFINED_ID}" ]; then
  USER_DEFINED_ID="${EXISTING_USER_DEFINED_ID}"
else
  USER_DEFINED_ID="${USER_DEFINED_ID_PREFIX}${RAND8}"
  echo "${USER_DEFINED_ID}" | sudo tee -a /etc/ilogtail/user_defined_id >/dev/null
fi
if ! sudo grep -Fxq "${USER_DEFINED_ID}" /etc/ilogtail/user_defined_id 2>/dev/null; then
  echo "Failed to persist USER_DEFINED_ID to /etc/ilogtail/user_defined_id" >&2
  exit 1
fi
if [ ! -f "/etc/ilogtail/users/${ALIYUN_UID}" ]; then
  sudo touch "/etc/ilogtail/users/${ALIYUN_UID}"
fi
if [ ! -f "/etc/ilogtail/users/${ALIYUN_UID}" ]; then
  echo "Failed to create UID marker file: /etc/ilogtail/users/${ALIYUN_UID}" >&2
  exit 1
fi

if ! aliyun sls GetMachineGroup --project "$PROJECT" --machineGroup "$MACHINE_GROUP" >/dev/null 2>&1; then
  cat > /tmp/openclaw-machine-group.json <<EOF
{
  "groupName": "${MACHINE_GROUP}",
  "groupType": "",
  "machineIdentifyType": "userdefined",
  "machineList": ["${USER_DEFINED_ID}"]
}
EOF
  aliyun sls CreateMachineGroup \
    --project "$PROJECT" \
    --body "$(cat /tmp/openclaw-machine-group.json)"
fi
if ! aliyun sls GetMachineGroup --project "$PROJECT" --machineGroup "$MACHINE_GROUP" >/dev/null 2>&1; then
  echo "Machine group was not created successfully: ${MACHINE_GROUP}" >&2
  exit 1
fi

# 4) Create logstore (if missing) + index + multiple dashboards
if ! aliyun sls GetLogStore --project "$PROJECT" --logstore "$LOGSTORE" >/dev/null 2>&1; then
  aliyun sls CreateLogStore --project "$PROJECT" \
    --body "{\"logstoreName\":\"${LOGSTORE}\",\"ttl\":30,\"shardCount\":2}"
fi

if ! aliyun sls GetIndex --project "$PROJECT" --logstore "$LOGSTORE" >/dev/null 2>&1; then
  # Use the index template as-is from references/index.json
  aliyun sls CreateIndex \
    --project "$PROJECT" \
    --logstore "$LOGSTORE" \
    --body "$(cat references/index.json)"
fi

sed "s/\${logstoreName}/${LOGSTORE}/g" references/dashboard-audit.json > /tmp/openclaw-audit-dashboard.json
sed "s/\${logstoreName}/${LOGSTORE}/g" references/dashboard-gateway.json > /tmp/openclaw-gateway-dashboard.json

# Create dashboard uses project + body(detail). Update uses path + project + body.
if aliyun sls GET "/dashboards/openclaw-audit" --project "$PROJECT" >/dev/null 2>&1; then
  aliyun sls PUT "/dashboards/openclaw-audit" \
    --project "$PROJECT" \
    --body "$(cat /tmp/openclaw-audit-dashboard.json)"
else
  aliyun sls POST "/dashboards" \
    --project "$PROJECT" \
    --body "$(cat /tmp/openclaw-audit-dashboard.json)"
fi

if aliyun sls GET "/dashboards/openclaw-gateway" --project "$PROJECT" >/dev/null 2>&1; then
  aliyun sls PUT "/dashboards/openclaw-gateway" \
    --project "$PROJECT" \
    --body "$(cat /tmp/openclaw-gateway-dashboard.json)"
else
  aliyun sls POST "/dashboards" \
    --project "$PROJECT" \
    --body "$(cat /tmp/openclaw-gateway-dashboard.json)"
fi

# 5) Create collection config (update when already exists)
# Render collector config strictly from references/collector-config.json
sed \
  -e "s/\${configName}/${CONFIG_NAME}/g" \
  -e "s/\${logstoreName}/${LOGSTORE}/g" \
  -e "s/\${region_id}/${REGION_ID}/g" \
  references/collector-config.json > /tmp/openclaw-collector-config.json

if aliyun sls GetConfig --project "$PROJECT" --configName "$CONFIG_NAME" >/dev/null 2>&1; then
  aliyun sls UpdateConfig \
    --project "$PROJECT" \
    --configName "$CONFIG_NAME" \
    --body "$(cat /tmp/openclaw-collector-config.json)"
else
  aliyun sls CreateConfig \
    --project "$PROJECT" \
    --body "$(cat /tmp/openclaw-collector-config.json)"
fi

# 6) Bind collection config to machine group
aliyun sls ApplyConfigToMachineGroup \
  --project "$PROJECT" \
  --machineGroup "$MACHINE_GROUP" \
  --configName "$CONFIG_NAME"

echo "OpenClaw SLS observability setup completed."
```

---

## Response Format

When this skill completes, return a concise status report with:

1. Inputs used: `PROJECT`, `LOGSTORE`, resolved `REGION_ID`
2. Created/updated resources (machine group, index, dashboards, config, binding)
3. Any skipped steps (already existed / already running)
4. Next verification commands for the user

---

## Verification Commands

```bash
aliyun sls GetMachineGroup --project "$PROJECT" --machineGroup openclaw-sls-collector
aliyun sls GetIndex --project "$PROJECT" --logstore "$LOGSTORE"
aliyun sls GetDashboard --project "$PROJECT" --dashboardName openclaw-audit
aliyun sls GetDashboard --project "$PROJECT" --dashboardName openclaw-gateway
aliyun sls GetConfig --project "$PROJECT" --configName "openclaw-audit_${LOGSTORE}"
```

---

## Reference Files

- Command flow: `references/cli-commands.md`
- Index definition: `references/index.json`
- Dashboard templates: `references/dashboard-audit.json`, `references/dashboard-gateway.json`
- Collection config template: `references/collector-config.json`

Read reference files only when needed:
- Use `cli-commands.md` for step-by-step troubleshooting.
- Use JSON templates when creating/updating resources.
