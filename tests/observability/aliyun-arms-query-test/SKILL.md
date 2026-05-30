---
name: aliyun-arms-query-test
description: Smoke test for aliyun-arms-query skill. Validates script compilation and basic SDK client initialization.
version: 1.0.0
---

Category: test

# ARMS Query Skill Smoke Test

## Prerequisites

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U alibabacloud_arms20190808 alibabacloud_tea_openapi
```

- `ALIBABACLOUD_ACCESS_KEY_ID`
- `ALIBABACLOUD_ACCESS_KEY_SECRET`
- `ARMS_REGION_ID` (default: `cn-hangzhou`)

## Test 1: Script compilation (5 scripts)

```bash
mkdir -p output/aliyun-arms-query-test
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/observability/arms/aliyun-arms-query \
  --output output/aliyun-arms-query-test/compile.json
```

Fallback if shared helper is unavailable:

```bash
mkdir -p output/aliyun-arms-query-test
for f in skills/observability/arms/aliyun-arms-query/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-arms-query-test/validate.txt
```

Pass: exits 0 and evidence file exists. Expected scripts: `search_traces.py`, `get_trace_detail.py`, `query_metrics.py`, `list_trace_apps.py`, `get_stack.py`.

## Test 2: ListTraceApps (read-only)

```bash
python -c "
import os
from alibabacloud_arms20190808.client import Client
from alibabacloud_arms20190808 import models
from alibabacloud_tea_openapi.models import Config

region = os.environ.get('ARMS_REGION_ID', 'cn-hangzhou')
config = Config(
    access_key_id=os.environ['ALIBABACLOUD_ACCESS_KEY_ID'],
    access_key_secret=os.environ['ALIBABACLOUD_ACCESS_KEY_SECRET'],
    region_id=region,
)
config.endpoint = f'arms.{region}.aliyuncs.com'
client = Client(config)
resp = client.list_trace_apps(models.ListTraceAppsRequest(region_id=region))
apps = resp.body.trace_apps or []
print(f'Found {len(apps)} traced apps')
for app in apps[:5]:
    print(f'  {app.pid}  {app.app_name}')
" 2>&1 | tee output/aliyun-arms-query-test/list_apps.txt
```

Pass: command exits 0 and lists apps (may be 0 if no apps instrumented).

## Output

Evidence saved under `output/aliyun-arms-query-test/`.
