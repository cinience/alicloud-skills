---
name: aliyun-observability
description: "Integrate Alibaba Cloud Observability (SLS): prepare aliyun CLI and LoongCollector, then create machine groups, index, dashboards, collection config, and binding."
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["aliyun"] },
      },
  }
---

# Alibaba Cloud Observability Integration (OpenClaw)

When you ask OpenClaw to integrate Alibaba Cloud Observability, run this flow:

1. Check and install `aliyun` CLI (install latest when missing)
2. Install `LoongCollector` by project region (skip if already running)
3. Create an identifier-based machine group (local identifier + cloud machine group)
4. Create `logstore` index and dashboards
5. Create `logstore` collection config
6. Bind the collection config to the machine group

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

## One-Time Execution Flow (Idempotent)

> The commands below are designed as "exists -> skip" and are safe to rerun.

```bash
set -euo pipefail

# ===== User inputs =====
: "${PROJECT:?Please export PROJECT}"
: "${LOGSTORE:?Please export LOGSTORE}"
: "${ALIBABA_CLOUD_ACCESS_KEY_ID:?Please export ALIBABA_CLOUD_ACCESS_KEY_ID}"
: "${ALIBABA_CLOUD_ACCESS_KEY_SECRET:?Please export ALIBABA_CLOUD_ACCESS_KEY_SECRET}"
: "${ALIYUN_UID:?Please export ALIYUN_UID}"

MACHINE_GROUP="openclaw-sls-collector"
CONFIG_NAME="openclaw-audit"

# 1) Install aliyun CLI if missing
if ! command -v aliyun >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    brew install aliyun-cli
  else
    echo "aliyun CLI not found and Homebrew is unavailable. Install aliyun-cli first." >&2
    exit 1
  fi
fi

# Export auth variables for aliyun CLI
export ALIBABA_CLOUD_ACCESS_KEY_ID
export ALIBABA_CLOUD_ACCESS_KEY_SECRET

# 2) Resolve region and install LoongCollector (skip when already running)
REGION_ID="${ALIBABA_CLOUD_REGION_ID:-}"
if [ -z "$REGION_ID" ]; then
  REGION_ID="$(aliyun sls GetProject --project "$PROJECT" --cli-query 'region' --quiet 2>/dev/null | tr -d '\"' || true)"
fi
if [ -z "$REGION_ID" ]; then
  echo "Cannot resolve region from project: $PROJECT. Please set ALIBABA_CLOUD_REGION_ID." >&2
  exit 1
fi

LOONG_RUNNING=0
if sudo /etc/init.d/loongcollectord status 2>/dev/null | grep -qi "running"; then
  LOONG_RUNNING=1
fi
if sudo /etc/init.d/ilogtaild status 2>/dev/null | grep -qi "running"; then
  LOONG_RUNNING=1
fi

if [ "$LOONG_RUNNING" -eq 0 ]; then
  wget "https://aliyun-observability-release-${REGION_ID}.oss-${REGION_ID}.aliyuncs.com/loongcollector/linux64/latest/loongcollector.sh" -O loongcollector.sh
  chmod +x loongcollector.sh
  ./loongcollector.sh install "${REGION_ID}"
fi
sudo /etc/init.d/loongcollectord status || true

# 3) Local user-defined identifier + create machine group
sudo mkdir -p /etc/ilogtail
sudo mkdir -p /etc/ilogtail/users
if [ ! -f /etc/ilogtail/user_defined_id ]; then
  sudo touch /etc/ilogtail/user_defined_id
fi
RAND8="$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 8)"
USER_DEFINED_ID="${PROJECT}_${RAND8}"
if ! sudo grep -Fxq "${USER_DEFINED_ID}" /etc/ilogtail/user_defined_id 2>/dev/null; then
  echo "${USER_DEFINED_ID}" | sudo tee -a /etc/ilogtail/user_defined_id >/dev/null
fi
if [ ! -f "/etc/ilogtail/users/${ALIYUN_UID}" ]; then
  sudo touch "/etc/ilogtail/users/${ALIYUN_UID}"
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

# 4) Create logstore (if missing) + index + multiple dashboards
if ! aliyun sls GetLogStore --project "$PROJECT" --logstore "$LOGSTORE" >/dev/null 2>&1; then
  aliyun sls CreateLogStore --project "$PROJECT" \
    --body "{\"logstoreName\":\"${LOGSTORE}\",\"ttl\":30,\"shardCount\":2}"
fi

if ! aliyun sls GetIndex --project "$PROJECT" --logstore "$LOGSTORE" >/dev/null 2>&1; then
  aliyun sls CreateIndex \
    --project "$PROJECT" \
    --logstore "$LOGSTORE" \
    --body "$(cat references/index.json)"
fi

for DASHBOARD_FILE in references/dashboard-audit.json references/dashboard-gateway.json; do
  DASHBOARD_NAME="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], "r", encoding="utf-8"))["title"])' "$DASHBOARD_FILE")"
  sed "s/\${logstoreName}/${LOGSTORE}/g" "$DASHBOARD_FILE" > "/tmp/${DASHBOARD_NAME}.json"
  if aliyun sls GetDashboard --project "$PROJECT" --dashboardName "$DASHBOARD_NAME" >/dev/null 2>&1; then
    aliyun sls UpdateDashboard \
      --project "$PROJECT" \
      --dashboardName "$DASHBOARD_NAME" \
      --body "$(cat "/tmp/${DASHBOARD_NAME}.json")"
  else
    aliyun sls CreateDashboard \
      --project "$PROJECT" \
      --body "$(cat "/tmp/${DASHBOARD_NAME}.json")"
  fi
done

# 5) Create collection config (update when already exists)
sed \
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

## Verification Commands

```bash
aliyun sls GetMachineGroup --project "$PROJECT" --machineGroup openclaw-sls-collector
aliyun sls GetIndex --project "$PROJECT" --logstore "$LOGSTORE"
aliyun sls GetDashboard --project "$PROJECT" --dashboardName openclaw-audit
aliyun sls GetDashboard --project "$PROJECT" --dashboardName openclaw-gateway
aliyun sls GetConfig --project "$PROJECT" --configName openclaw-audit
```

---

## Reference Files

- Command flow: `references/cli-commands.md`
- Index definition: `references/index.json`
- Dashboard templates: `references/dashboard-audit.json`, `references/dashboard-gateway.json`
- Collection config template: `references/collector-config.json`

