# ARMS Query API Reference

Product code: `ARMS` | Version: `2019-08-08` | Endpoint: `arms.<regionId>.aliyuncs.com`

## Trace APIs

### SearchTracesByPage

Search traces with filters and pagination.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| RegionId | string | yes | Region ID |
| StartTime | long | yes | Start time (epoch ms) |
| EndTime | long | yes | End time (epoch ms) |
| ServiceName | string | no | Application/service name |
| OperationName | string | no | Span/endpoint name |
| MinDuration | long | no | Minimum duration (ms) |
| ServiceIp | string | no | Machine IP |
| Pid | string | no | Application PID filter |
| Reverse | boolean | no | true = descending by time |
| Tags | array | no | Tag filters `[{Key, Value}]` |
| ExclusionFilters | array | no | Exclusion filters `[{Key, Value}]` |
| IsError | boolean | no | Filter error traces only |
| PageNumber | int | no | Page number |
| PageSize | int | no | Items per page, max 100 |

### SearchTraces

Search traces without pagination (returns all matching traces up to limit).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| RegionId | string | yes | Region ID |
| StartTime | long | yes | Start time (epoch ms) |
| EndTime | long | yes | End time (epoch ms) |
| ServiceName | string | no | Application/service name |
| OperationName | string | no | Span/endpoint name |
| MinDuration | long | no | Minimum duration (ms) |
| ServiceIp | string | no | Machine IP |
| Pid | string | no | Application PID filter |
| Reverse | boolean | no | true = descending by time |
| Tag | array | no | Tag filters `[{Key, Value}]` |
| ExclusionFilters | array | no | Exclusion filters `[{Key, Value}]` |

### GetTrace

Get full span tree for a single trace.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| TraceID | string | yes | Trace ID |
| RegionId | string | yes | Region ID |
| StartTime | long | conditional | Required if TraceID length != 30 |
| EndTime | long | conditional | Required if TraceID length != 30 |
| PageNumber | int | no | Page number for paginated span retrieval |
| PageSize | int | no | Spans per page |

Response fields per span: `SpanId`, `ParentSpanId`, `OperationName`, `ServiceName`, `ServiceIp`, `Duration`, `Timestamp`, `ResultCode`, `HaveStack`, `RpcId`, `TagEntryList`, `LogEventList`.

### GetMultipleTrace

Batch retrieve trace details.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| RegionId | string | no | Region ID |
| TraceIDs | array | yes | List of trace IDs |
| StartTime | long | no | Start time (epoch ms) |
| EndTime | long | no | End time (epoch ms) |
| PageNumber | int | no | Page number |
| PageSize | int | no | Items per page |

### GetStack

Get method-level call stack for a specific span.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| TraceID | string | yes | Trace ID |
| RpcID | string | yes | RPC ID of the span |
| Pid | string | yes | Application PID |
| RegionId | string | no | Region ID |
| SpanID | string | no | Span ID (alternative to RpcID) |
| StartTime | long | no | Start time (epoch ms) |
| EndTime | long | no | End time (epoch ms) |

Response fields per stack entry: `Api`, `Duration`, `Exception`, `Line`, `RpcId`, `ServiceName`, `StartTime`.

## Application APIs

### ListTraceApps

List all traced applications to obtain PIDs.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| RegionId | string | no | Region ID |
| AppType | string | no | `TRACE` or `EBPF` |
| ResourceGroupId | string | no | Resource group filter |
| Tags | array | no | Tag filters |

Response fields: `Pid`, `AppName`, `Type`, `RegionId`, `CreateTime`, `UpdateTime`.

### SearchTraceAppByName

Search traced applications by name.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| TraceAppName | string | no | App name (fuzzy match) |
| RegionId | string | no | Region ID |

### SearchTraceAppByPage

Search traced applications with pagination.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| TraceAppName | string | no | App name filter |
| RegionId | string | no | Region ID |
| PageNumber | int | no | Page number |
| PageSize | int | no | Items per page |
| ResourceGroupId | string | no | Resource group filter |

### GetTraceApp

Get details for a single traced application.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| Pid | string | yes | Application PID |
| RegionId | string | yes | Region ID |

## Metrics APIs

### QueryMetricByPage

Primary metrics query with pagination.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| Metric | string | yes | Metric name (e.g. `appstat.incall`) |
| StartTime | long | yes | Start time (epoch ms) |
| EndTime | long | yes | End time (epoch ms) |
| IntervalInSec | int | no | Aggregation interval (ms, min 60000) |
| Measures | array | no | Measurement fields to return |
| Dimensions | array | no | Group-by dimensions |
| Filters | array | no | Filter conditions `[{Key, Value}]` |
| CustomFilters | array | no | Custom filter conditions |
| CurrentPage | int | no | Page number |
| PageSize | int | no | Items per page |
| OrderBy | string | no | Sort field |
| Order | string | no | `ASC` or `DESC` |

### GetAppApiByPage

Per-endpoint performance metrics (request count, error count, average RT).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| PId | string | yes | Application PID |
| RegionId | string | yes | Region ID |
| StartTime | long | yes | Start time (epoch ms) |
| EndTime | long | yes | End time (epoch ms) |
| IntervalMills | int | no | Interval in ms (min 60000) |
| CurrentPage | int | no | Page number |
| PageSize | int | no | Items per page |

Use `Completed` field in response to check if more pages exist.

## Metric Names Quick Reference

| Metric | Measures | Dimensions |
|--------|----------|------------|
| `appstat.incall` | rt, count, error | rpc, type |
| `appstat.outcall` | rt, count, error | rpc, type |
| `appstat.sql` | rt, count, error | rpc |
| `appstat.exception` | rt, count | rpc, exceptionClass |
| `appstat.host` | cpuUsage, memUsage, load | pid |

## CLI Examples

```bash
# Search traces
aliyun arms SearchTracesByPage \
  --RegionId cn-hangzhou \
  --StartTime 1700000000000 \
  --EndTime 1700003600000 \
  --ServiceName my-app \
  --MinDuration 500 \
  --PageNumber 1 --PageSize 20

# Get trace detail
aliyun arms GetTrace \
  --RegionId cn-hangzhou \
  --TraceID 1c34ffee16xxxxxxxx

# Get method stack
aliyun arms GetStack \
  --RegionId cn-hangzhou \
  --TraceID 1c34ffee16xxxxxxxx \
  --RpcID 0.1 \
  --Pid "xxx@cn-hangzhou"

# Query metrics
aliyun arms QueryMetricByPage \
  --RegionId cn-hangzhou \
  --Metric appstat.incall \
  --StartTime 1700000000000 \
  --EndTime 1700003600000 \
  --IntervalInSec 60000 \
  --Measures.1 rt --Measures.2 count --Measures.3 error \
  --Dimensions.1 rpc \
  --Filters.1.Key pid --Filters.1.Value "xxx@cn-hangzhou"

# List traced apps
aliyun arms ListTraceApps --RegionId cn-hangzhou
```
