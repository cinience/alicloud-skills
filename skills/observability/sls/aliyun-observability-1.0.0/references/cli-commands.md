# Alibaba Cloud Observability Command Reference

> The commands below match `SKILL.md` and are intended for step-by-step troubleshooting.

## 0. Environment Variables

```bash
export PROJECT="<your-project>"
export LOGSTORE="<your-logstore>"
export ALIBABA_CLOUD_ACCESS_KEY_ID="<your-ak>"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="<your-sk>"
export ALIYUN_UID="<your-aliyun-uid>"
```

## 1. Install and Verify aliyun CLI

```bash
command -v aliyun >/dev/null 2>&1 || brew install aliyun-cli
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

aliyun sls GetIndex --project "$PROJECT" --logstore "$LOGSTORE"
aliyun sls CreateIndex --project "$PROJECT" --logstore "$LOGSTORE" --body "$(cat references/index.json)"

# Replace ${logstoreName} in templates with the user input LOGSTORE
sed "s/\${logstoreName}/${LOGSTORE}/g" references/dashboard-audit.json > /tmp/openclaw-audit.json
sed "s/\${logstoreName}/${LOGSTORE}/g" references/dashboard-gateway.json > /tmp/openclaw-gateway.json

aliyun sls GetDashboard --project "$PROJECT" --dashboardName openclaw-audit
aliyun sls CreateDashboard --project "$PROJECT" --body "$(cat /tmp/openclaw-audit.json)"
aliyun sls UpdateDashboard --project "$PROJECT" --dashboardName openclaw-audit --body "$(cat /tmp/openclaw-audit.json)"

aliyun sls GetDashboard --project "$PROJECT" --dashboardName openclaw-gateway
aliyun sls CreateDashboard --project "$PROJECT" --body "$(cat /tmp/openclaw-gateway.json)"
aliyun sls UpdateDashboard --project "$PROJECT" --dashboardName openclaw-gateway --body "$(cat /tmp/openclaw-gateway.json)"
```

## 5. Collection Config and Binding

```bash
aliyun sls GetConfig --project "$PROJECT" --configName openclaw-audit
aliyun sls CreateConfig --project "$PROJECT" --body "$(cat /tmp/openclaw-collector-config.json)"
aliyun sls UpdateConfig --project "$PROJECT" --configName openclaw-audit --body "$(cat /tmp/openclaw-collector-config.json)"

aliyun sls ApplyConfigToMachineGroup \
  --project "$PROJECT" \
  --machineGroup "openclaw-sls-collector" \
  --configName "openclaw-audit"
```

