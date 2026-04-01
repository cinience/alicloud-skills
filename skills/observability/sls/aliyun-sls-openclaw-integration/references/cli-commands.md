# Alibaba Cloud Observability Command Reference

> The commands below match `SKILL.md` and are intended for step-by-step troubleshooting.

## 0. Environment Variables

```bash
export PROJECT="<your-project>"
export LOGSTORE="<your-logstore>"
export ALIBABA_CLOUD_ACCESS_KEY_ID="<your-ak>"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="<your-sk>"
export ALIYUN_UID="<your-aliyun-uid>"
CONFIG_NAME="openclaw-audit_${LOGSTORE}"
```

## 1. Install and Verify aliyun CLI

```bash
if ! command -v aliyun >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update && sudo apt-get install -y aliyun-cli
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y aliyun-cli
  elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y aliyun-cli
  elif command -v zypper >/dev/null 2>&1; then
    sudo zypper -n install aliyun-cli
  else
    echo "Install aliyun-cli manually for your Linux distribution." >&2
    exit 1
  fi
fi
aliyun --version
```

## 2. Query Project Region

```bash
aliyun sls GetProject --project "$PROJECT"
aliyun sls GetProject --project "$PROJECT" --cli-query 'region' --quiet
```

## 3. Machine Group

```bash
aliyun sls GetMachineGroup --project "$PROJECT" --machineGroup openclaw-sls-collector
aliyun sls CreateMachineGroup --project "$PROJECT" --body "$(cat /tmp/openclaw-machine-group.json)"
```

## 4. Logstore / Index / Dashboard

```bash
aliyun sls GetLogStore --project "$PROJECT" --logstore "$LOGSTORE"
aliyun sls CreateLogStore --project "$PROJECT" --body "{\"logstoreName\":\"${LOGSTORE}\",\"ttl\":30,\"shardCount\":2}"

# Strictly use references/index.json as request body
aliyun sls GetIndex --project "$PROJECT" --logstore "$LOGSTORE"
aliyun sls CreateIndex --project "$PROJECT" --logstore "$LOGSTORE" --body "$(cat references/index.json)"

# Replace ${logstoreName} in templates with the user input LOGSTORE
sed "s/\${logstoreName}/${LOGSTORE}/g" references/dashboard-audit.json > /tmp/openclaw-audit.json
sed "s/\${logstoreName}/${LOGSTORE}/g" references/dashboard-gateway.json > /tmp/openclaw-gateway.json

# Create dashboard: project + body(detail). Update dashboard: path + project + body.
aliyun sls GET "/dashboards/openclaw-audit" --project "$PROJECT"
aliyun sls POST "/dashboards" --project "$PROJECT" --body "$(cat /tmp/openclaw-audit.json)"
aliyun sls PUT "/dashboards/openclaw-audit" --project "$PROJECT" --body "$(cat /tmp/openclaw-audit.json)"

aliyun sls GET "/dashboards/openclaw-gateway" --project "$PROJECT"
aliyun sls POST "/dashboards" --project "$PROJECT" --body "$(cat /tmp/openclaw-gateway.json)"
aliyun sls PUT "/dashboards/openclaw-gateway" --project "$PROJECT" --body "$(cat /tmp/openclaw-gateway.json)"
```

## 5. Collection Config and Binding

```bash
CONFIG_NAME="openclaw-audit_${LOGSTORE}"

sed \
  -e "s/\${configName}/${CONFIG_NAME}/g" \
  -e "s/\${logstoreName}/${LOGSTORE}/g" \
  -e "s/\${region_id}/${REGION_ID}/g" \
  references/collector-config.json > /tmp/openclaw-collector-config.json

aliyun sls GetConfig --project "$PROJECT" --configName "$CONFIG_NAME"
# Strictly render from references/collector-config.json with placeholder replacement only
aliyun sls CreateConfig --project "$PROJECT" --body "$(cat /tmp/openclaw-collector-config.json)"
aliyun sls UpdateConfig --project "$PROJECT" --configName "$CONFIG_NAME" --body "$(cat /tmp/openclaw-collector-config.json)"

aliyun sls ApplyConfigToMachineGroup \
  --project "$PROJECT" \
  --machineGroup "openclaw-sls-collector" \
  --configName "$CONFIG_NAME"
```

