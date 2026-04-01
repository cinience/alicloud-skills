---
name: aliyun-sls-log-query
description: Use when querying or troubleshooting logs in Alibaba Cloud Log Service (SLS) using query|analysis syntax and the Python SDK. Use for time-bounded log search, error investigation, and root-cause analysis workflows.
version: 1.0.0
---

Category: service

# SLS Log Query and Troubleshooting

Use SLS query|analysis syntax and Python SDK for log search, filtering, and analytics.

## Prerequisites

- Install SDK (virtual environment recommended to avoid PEP 668 restrictions):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U aliyun-log-python-sdk
```
- Configure environment variables:
  - `ALIBABA_CLOUD_ACCESS_KEY_ID`
  - `ALIBABA_CLOUD_ACCESS_KEY_SECRET`
  - `SLS_ENDPOINT` (e.g. `cn-hangzhou.log.aliyuncs.com`)
  - `SLS_PROJECT`
  - `SLS_LOGSTORE`(supports a single value or comma-separated values)

## Query Composition

- Query clause: filters logs (e.g. `status:500`).
- Analysis clause: statistical aggregation, format `query|analysis`.
- Example: `* | SELECT status, count(*) AS pv GROUP BY status`

See `references/query-syntax.md` for full syntax.

## Quickstart (Python SDK)

```python
import os
import time
from aliyun.log import LogClient, GetLogsRequest

client = LogClient(
    os.environ["SLS_ENDPOINT"],
    os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
    os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
)

project = os.environ["SLS_PROJECT"]
logstore = os.environ["SLS_LOGSTORE"]

query = "status:500"
start_time = int(time.time()) - 15 * 60
end_time = int(time.time())

request = GetLogsRequest(project, logstore, start_time, end_time, query=query)
response = client.get_logs(request)
for log in response.get_logs():
    print(log.contents)
```

## Script quickstart

```bash
python skills/observability/sls/aliyun-sls-log-query/scripts/query_logs.py \
  --query "status:500" \
  --last-minutes 15
```

Optional args: `--project`, `--logstore`(repeatable, or comma-separated values), `--endpoint`, `--start`, `--end`, `--last-minutes`, `--limit`, `--parallel`.

## Troubleshooting script

```bash
python skills/observability/sls/aliyun-sls-log-query/scripts/troubleshoot.py \
  --group-field status \
  --last-minutes 30 \
  --limit 20
```

Optional args: `--error-query`, `--group-field`, `--limit`, `--logstore`(repeatable, or comma-separated values), `--parallel`, plus the time range args above.

## Workflow

1) Ensure Logstore indexing is enabled (queries/analysis fail without index).
2) Write query clause and append analysis clause when needed.
3) Execute with SDK/script and inspect results.
4) Control returned rows with `limit`; narrow time range when needed.

## Validation

```bash
mkdir -p output/aliyun-sls-log-query
for f in skills/observability/sls/aliyun-sls-log-query/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-sls-log-query/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-sls-log-query/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-sls-log-query/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## References

- Syntax and examples:`references/query-syntax.md`
- Python SDK initialization and queries:`references/python-sdk.md`
- Troubleshooting templates:`references/templates.md`

- Source list: `references/sources.md`
