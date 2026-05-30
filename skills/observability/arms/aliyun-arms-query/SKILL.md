---
name: aliyun-arms-query
description: Use when querying distributed traces or application metrics in Alibaba Cloud ARMS (Application Real-Time Monitoring Service). Use for trace search by service/duration/tags, trace detail and method stack retrieval, application listing, and performance metrics queries.
version: 1.0.0
---

Category: service

# ARMS Trace & Metrics Query

Query distributed traces and application performance metrics via ARMS Python SDK.

## Prerequisites

- Install SDK (virtual environment recommended):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U alibabacloud_arms20190808 alibabacloud_tea_openapi
```

- Configure environment variables:
  - `ALIBABACLOUD_ACCESS_KEY_ID`
  - `ALIBABACLOUD_ACCESS_KEY_SECRET`
  - `ARMS_REGION_ID` (e.g. `cn-hangzhou`)

## Core Concepts

- **Trace query**: Search traces by service name, span name, duration, tags, error status. Time range in epoch milliseconds. Supports PID and exclusion filters.
- **Trace detail**: Retrieve full span tree for a single TraceID. Supports pagination for large traces.
- **Method stack**: Retrieve the method-level call stack for a specific span (requires TraceID, RpcID, and PID).
- **Metrics query**: Query predefined metric tables (e.g. `appstat.incall`) with dimensions, measures, and filters. Requires application PID. Supports ordering.
- **Application PID**: Unique app identifier in format `xxx@regionId`, obtained via `ListTraceApps`.

## Quickstart — Search Traces (Python SDK)

```python
import os, time
from alibabacloud_arms20190808.client import Client
from alibabacloud_arms20190808 import models
from alibabacloud_tea_openapi.models import Config

config = Config(
    access_key_id=os.environ["ALIBABACLOUD_ACCESS_KEY_ID"],
    access_key_secret=os.environ["ALIBABACLOUD_ACCESS_KEY_SECRET"],
    region_id=os.environ.get("ARMS_REGION_ID", "cn-hangzhou"),
)
config.endpoint = f'arms.{config.region_id}.aliyuncs.com'
client = Client(config)

end_ms = int(time.time() * 1000)
start_ms = end_ms - 15 * 60 * 1000

request = models.SearchTracesByPageRequest(
    region_id=config.region_id,
    start_time=start_ms,
    end_time=end_ms,
    service_name="my-app",
    min_duration=500,
    page_number=1,
    page_size=20,
)
response = client.search_traces_by_page(request)
for trace in response.body.page_bean.trace_infos:
    print(f"{trace.trace_id}  {trace.duration}ms  {trace.service_name}")
```

## Quickstart — Query Metrics (Python SDK)

```python
request = models.QueryMetricByPageRequest(
    region_id=config.region_id,
    metric="appstat.incall",
    start_time=start_ms,
    end_time=end_ms,
    interval_in_sec=60000,
    measures=["rt", "count", "error"],
    dimensions=["rpc"],
    filters=[models.QueryMetricByPageRequestFilters(key="pid", value="xxx@cn-hangzhou")],
    current_page=1,
    page_size=10,
)
response = client.query_metric_by_page(request)
for item in response.body.data.items:
    print(item)
```

## Script Catalog

### Search traces

```bash
python skills/observability/arms/aliyun-arms-query/scripts/search_traces.py \
  --service-name my-app \
  --last-minutes 15
```

Optional args: `--region`, `--operation-name`, `--min-duration`, `--service-ip`, `--pid`, `--error-only`, `--tag KEY=VALUE` (repeatable), `--exclusion-filter KEY=VALUE` (repeatable), `--page`, `--page-size`, `--reverse`.

### Get trace detail

```bash
python skills/observability/arms/aliyun-arms-query/scripts/get_trace_detail.py \
  --trace-id 1c34ffee16xxxxxxxx
```

Optional args: `--region`, `--start`, `--end`, `--page`, `--page-size`.

### Query metrics

```bash
python skills/observability/arms/aliyun-arms-query/scripts/query_metrics.py \
  --metric appstat.incall \
  --pid "xxx@cn-hangzhou" \
  --last-minutes 30
```

Optional args: `--region`, `--measures` (comma-separated), `--dimensions` (comma-separated), `--interval`, `--page`, `--page-size`, `--order-by`, `--order ASC|DESC`.

### List traced applications

```bash
python skills/observability/arms/aliyun-arms-query/scripts/list_trace_apps.py
```

Optional args: `--region`, `--app-type TRACE|EBPF`, `--resource-group-id`.

### Get span method stack

```bash
python skills/observability/arms/aliyun-arms-query/scripts/get_stack.py \
  --trace-id 1c34ffee16xxxxxxxx \
  --rpc-id 0.1 \
  --pid "xxx@cn-hangzhou"
```

Optional args: `--region`, `--span-id`, `--start`, `--end`.

## Common Metric Names

| Metric | Description |
|--------|-------------|
| `appstat.incall` | Inbound call stats (RT, count, error) per endpoint |
| `appstat.outcall` | Outbound call stats (HTTP, RPC, DB) |
| `appstat.sql` | SQL execution stats |
| `appstat.exception` | Exception stats |
| `appstat.host` | Host-level metrics (CPU, memory, load) |

Common measures: `rt` (response time), `count` (request count), `error` (error count).
Common dimensions: `rpc` (endpoint), `type` (call type), `exceptionClass`.

## Workflow

1. List traced apps with `list_trace_apps.py` to obtain PID.
2. Search traces with time range, service name, and optional filters via `search_traces.py`.
3. Get detail for a specific trace using its TraceID via `get_trace_detail.py`.
4. Inspect method stack for a slow or errored span via `get_stack.py` (requires TraceID, RpcID, PID).
5. Query aggregated metrics using PID, metric name, and desired measures/dimensions via `query_metrics.py`.

## AccessKey Priority

1. Environment variables: `ALIBABACLOUD_ACCESS_KEY_ID` / `ALIBABACLOUD_ACCESS_KEY_SECRET`
2. Shared credentials file: `~/.alibabacloud/credentials` (profile `default`)

## API Discovery

- Product code: `ARMS`
- API version: `2019-08-08`
- Metadata: `https://api.aliyun.com/meta/v1/products/ARMS/versions/2019-08-08/api-docs.json`

## Validation

```bash
mkdir -p output/aliyun-arms-query
for f in skills/observability/arms/aliyun-arms-query/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-arms-query/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-arms-query/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-arms-query/`.
- Include key parameters (region, PID, TraceID, time range) in evidence files for reproducibility.

## References

- API reference: `references/api-reference.md`
- Source list: `references/sources.md`
