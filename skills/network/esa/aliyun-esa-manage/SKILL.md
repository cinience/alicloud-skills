---
name: aliyun-esa-manage
description: Use when managing Alibaba Cloud ESA — deploy HTML/static sites via Pages, manage Edge Routines (ER) for serverless edge functions, use Edge KV for distributed key-value storage, handle site management, DNS records, cache rules, and query traffic analytics via OpenAPI/SDK. Use when working with ESA, edge deployment, edge functions, Pages, ER, KV storage, DNS, cache, site configuration, traffic analytics, bandwidth trends, or top-N rankings.
---

Category: service

# Edge Security Acceleration (ESA) - Pages, Edge Routine, KV, Site Management, Analytics & More

Use Alibaba Cloud OpenAPI (RPC) with official Python SDK to manage all ESA capabilities.

Alibaba Cloud ESA provides five core capabilities:
- **Pages** — Deploy HTML or static directories to edge nodes (quick deployment flow based on Edge Routine)
- **Edge Routine (ER)** — Full lifecycle management of serverless edge functions
- **Edge KV** — Distributed edge key-value storage with Namespace/Key/Value management
- **Site Management** — Site management, DNS records, cache rules, certificates, etc.
- **Analytics** — Traffic analysis, time-series trends, Top-N rankings, bandwidth statistics, request metrics

Use Python SDK uniformly to call ESA OpenAPI.

## Prerequisites

- Prepare AccessKey (RAM user/role with least privilege).
- Install Python SDK: `pip install alibabacloud_esa20240910 alibabacloud_tea_openapi alibabacloud_credentials`
- ESA OpenAPI is RPC style; prefer SDK or OpenAPI Explorer to avoid manual signing.

## SDK quickstart

```python
from alibabacloud_esa20240910.client import Client as Esa20240910Client
from alibabacloud_esa20240910 import models as esa_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str = "cn-hangzhou") -> Esa20240910Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint="esa.cn-hangzhou.aliyuncs.com",
    )
    return Esa20240910Client(config)
```

## Pages — Edge Page Deployment

Pages is a quick deployment flow based on Edge Routine, deploying HTML or static directories to the edge.

### HTML Page Deployment Flow

```
CreateRoutine → GetRoutineStagingCodeUploadInfo → Upload code to OSS
→ CommitRoutineStagingCode → PublishRoutineCodeVersion(staging)
→ PublishRoutineCodeVersion(production) → GetRoutine(get access URL)
```

### Static Directory Deployment Flow

```
CreateRoutine → CreateRoutineWithAssetsCodeVersion → Package zip and upload to OSS
→ Poll GetRoutineCodeVersionInfo(wait for available)
→ CreateRoutineCodeDeployment(staging) → CreateRoutineCodeDeployment(production)
→ GetRoutine(get access URL)
```

### Zip Package Structure

The zip package structure depends on `EDGE_ROUTINE_TYPE` (automatically determined by `checkEdgeRoutineType` based on whether entry file and assets directory exist):

- **JS_ONLY**: `routine/index.js` (bundled with esbuild or `--no-bundle` to read source files directly)
- **ASSETS_ONLY**: All static files under `assets/`, maintaining original directory structure
- **JS_AND_ASSETS**: `routine/index.js` + `assets/` static resources (most common)

The `assets/` path is relative to `assets.directory` in configuration. Configuration priority: CLI args > `esa.jsonc` / `esa.toml`.

### Key Notes

- **Function name rules**: lowercase letters/numbers/hyphens, start with lowercase letter, length >= 2
- **Same name function**: Reuse if exists, deploy new version code
- Deploy to both staging and production by default
- After successful deployment, get `defaultRelatedRecord` via `GetRoutine` as access domain

Detailed reference: `references/pages.md`

## Edge Routine (ER) — Edge Functions

Manage the complete lifecycle of serverless edge functions via Python SDK.

### Core Workflow

```
CreateRoutine → GetRoutineStagingCodeUploadInfo → Upload code to OSS
→ CommitRoutineStagingCode → PublishRoutineCodeVersion
→ (CreateRoutineRoute) → GetRoutine
```

### API Summary

- **Function Management**: `CreateRoutine`, `DeleteRoutine`, `GetRoutine`, `GetRoutineUserInfo`, `ListUserRoutines`
- **Code Version**: `GetRoutineStagingCodeUploadInfo`, `CommitRoutineStagingCode`, `PublishRoutineCodeVersion`, `DeleteRoutineCodeVersion`
- **Routes**: `CreateRoutineRoute`, `UpdateRoutineRoute`, `DeleteRoutineRoute`, `GetRoutineRoute`, `ListRoutineRoutes`, `ListSiteRoutes`
- **Related Records**: `CreateRoutineRelatedRecord`, `DeleteRoutineRelatedRecord`, `ListRoutineRelatedRecords`

### ER Code Format

```javascript
export default {
  async fetch(request) {
    return new Response("Hello", {
      headers: { "content-type": "text/html;charset=UTF-8" },
    });
  },
};
```

Detailed reference: `references/er.md`

## Edge KV — Edge Key-Value Storage

Distributed edge key-value storage, readable and writable in Edge Routine, also manageable via OpenAPI/SDK.

### Core Concepts

- **Namespace**: Isolation container for KV data, Key max 512 chars, Value max 2MB (high capacity 25MB)
- Supports TTL expiration: `Expiration` (Unix timestamp) or `ExpirationTtl` (seconds)

### API Summary

- **Namespace**: `CreateKvNamespace`, `DeleteKvNamespace`, `GetKvNamespace`, `GetKvAccount`, `DescribeKvAccountStatus`
- **Single Key Operations**: `PutKv`, `GetKv`, `GetKvDetail`, `DeleteKv`, `PutKvWithHighCapacity`
- **Batch Operations**: `BatchPutKv`, `BatchDeleteKv`, `BatchPutKvWithHighCapacity`, `BatchDeleteKvWithHighCapacity`, `ListKvs`

### Quick Start

```python
client = create_client()

# Create namespace
client.create_kv_namespace(esa_models.CreateKvNamespaceRequest(namespace="my-ns"))

# Write
client.put_kv(esa_models.PutKvRequest(namespace="my-ns", key="k1", value="v1"))

# Read
resp = client.get_kv(esa_models.GetKvRequest(namespace="my-ns", key="k1"))
```

Detailed reference: `references/kv.md`

## Site Management — Site Management

Use Python SDK to manage ESA sites, DNS records, cache rules, etc.

### API behavior notes

- Most list APIs support pagination via `PageNumber` + `PageSize`.
- `ListSites` returns sites across all regions; no need to iterate regions.
- Newly created sites start as `pending`; complete access verification via `VerifySite` to activate.
- Deleting a site removes all associated configuration.
- `UpdateSiteAccessType` can switch between CNAME and NS, but switching to CNAME may fail if incompatible DNS records exist.
- DNS record APIs (`CreateRecord`, `ListRecords`, etc.) work for both NS and CNAME connected sites. **CNAME sites** are limited to `CNAME` and `A/AAAA` types only, and records cannot disable acceleration (proxy must stay enabled).
- DNS record `Type` parameter must be exact: use `A/AAAA` (not `A`), `CNAME`, `MX`, `TXT`, `NS`, `SRV`, `CAA`.
- `CreateCacheRule` supports two config types: `global` (site-wide default) and `rule` (conditional rule with match expression).

### Workflow

1) Confirm target site ID, access type (CNAME/NS), and desired action.
2) Find API group and exact operation name in `references/api_overview.md`.
3) Call API with Python SDK (preferred) or OpenAPI Explorer.
4) Verify results with describe/list APIs.
5) If you need repeatable inventory or summaries, use `scripts/` and write outputs under `output/aliyun-esa-manage/`.

### SDK priority

1) Python SDK (preferred)
2) OpenAPI Explorer
3) Other SDKs (only if Python is not feasible)

### Python SDK scripts (recommended for inventory)

- List all ESA sites: `scripts/list_sites.py`
- Summarize sites by plan: `scripts/summary_sites_by_plan.py`
- Check site status: `scripts/check_site_status.py`
- List DNS records for a site: `scripts/list_dns_records.py`

## Analytics — Traffic Analysis

Query and analyze ESA site traffic data using `DescribeSiteTimeSeriesData` and `DescribeSiteTopData` APIs.

### Core Features

- **Time-Series Data**: Query traffic trends with configurable time granularity
- **Top-N Rankings**: Get rankings by country/IP/host/path/status code dimensions
- **Multiple Metrics**: Traffic, Requests, RequestTraffic, PageView
- **Rich Dimensions**: Country, province, ISP, browser, device, host, path, status code, etc.

### Two Main APIs

#### 1. DescribeSiteTimeSeriesData - Time-Series Trends

Query traffic trends over time, returning aggregated data points.

**Time Granularity Rules:**

| Time Range | Interval | Interval Value |
|------------|----------|----------------|
| <= 3 hours | 1 minute | `60` |
| 3-12 hours | 5 minutes | `300` |
| 12 hours - 1 day | 15 minutes | `900` |
| 1-10 days | 1 hour | `3600` |
| 10-31 days | 1 day | `86400` |

#### 2. DescribeSiteTopData - Top-N Rankings

Query Top-N ranking data by various dimensions.

**Limit Options:** `5`, `10`, `150`

### Available Metrics (FieldName)

| Field | Type | Description |
|-------|------|-------------|
| `Traffic` | int | Response traffic from ESA to client (bytes) |
| `Requests` | int | Number of requests |
| `RequestTraffic` | int | Client request traffic (bytes) |
| `PageView` | int | Page views |

### Available Dimensions

**Geographic Dimensions:** `ClientCountryCode` (country), `ClientProvinceCode` (province), `ClientISP` (ISP), `ClientASN`

**Client Info:** `ClientIP`, `ClientIPVersion`, `ClientBrowser`, `ClientDevice`, `ClientOS`

**Request Details:** `ClientRequestHost`, `ClientRequestMethod`, `ClientRequestPath`, `ClientRequestProtocol`, `ClientRequestQuery`, `ClientRequestReferer`, `ClientRequestUserAgent`

**Response/Cache:** `EdgeCacheStatus`, `EdgeResponseStatusCode`, `EdgeResponseContentType`, `OriginResponseStatusCode`

**Others:** `ALL` (aggregated), `SiteId` (account-level query), `Version`, `ClientSSLProtocol`, `ClientXRequestedWith`

### Error Handling

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 400 | `InvalidParameter.TimeRange` | Time range exceeded (max 31 days) |
| 400 | `InvalidEndTime.Mismatch` | EndTime earlier than StartTime |
| 400 | `InvalidParameter.Field` | Invalid field name |
| 400 | `InvalidParameter.Dimension` | Invalid dimension |
| 400 | `InvalidTime.Malformed` | Time format error (use yyyy-MM-ddTHH:mm:ssZ) |

Detailed reference: `references/time-series.md`, `references/top-data.md`, `references/fields.md`

## Common operation mapping

### Site Management

- Create site: `CreateSite`
- List sites: `ListSites` (supports `SiteName`, `Status`, `AccessType`, `Coverage` filters)
- Get site details: `GetSite`
- Delete site: `DeleteSite`
- Check site name availability: `CheckSiteName`
- Verify site ownership: `VerifySite`
- Update access type: `UpdateSiteAccessType`
- Update coverage: `UpdateSiteCoverage`
- Get current nameservers: `GetSiteCurrentNS`
- Update custom nameservers: `UpdateSiteVanityNS`
- Pause/resume site: `UpdateSitePause`, `GetSitePause`
- Site exclusivity: `UpdateSiteNameExclusive`, `GetSiteNameExclusive`
- Version management: `ActivateVersionManagement`, `DeactivateVersionManagement`

### Site Configuration

- IPv6: `GetIPv6`, `UpdateIPv6`

### DNS Records

NS access: full record type support. CNAME access: only `CNAME` and `A/AAAA`, proxy must stay enabled.

- Create record: `CreateRecord`
- List records: `ListRecords` (supports `Type`, `RecordName`, `Proxied` filters)
- Get record: `GetRecord`
- Update record: `UpdateRecord`
- Delete record: `DeleteRecord`
- Batch create: `BatchCreateRecords`
- Export records: `ExportRecords`

### Cache Rules

- Create cache rule: `CreateCacheRule`
- List cache rules: `ListCacheRules`
- Get cache rule: `GetCacheRule`
- Update cache rule: `UpdateCacheRule`
- Delete cache rule: `DeleteCacheRule`

**Cache rule expression notes (important):**
- `CreateCacheRule` parameters are **flat**, not a nested JSON `Rule` object.
- The `Rule` parameter is a match condition expression string. See **Rule Expression Syntax** section below.
- Quick reminders: `ends_with()`/`starts_with()` must use function-call style; `matches` (regex) requires standard plan or above.
- Set edge cache TTL with `--EdgeCacheMode override_origin --EdgeCacheTtl <seconds>`.

## Rule Expression Syntax

ESA uses a unified rule engine expression syntax across multiple features (cache rules, WAF custom rules, rate limiting, URL rewrite, header modification, etc.).

### When to use

Use this syntax for the `Rule` parameter in any ESA API that accepts a match condition expression:
- `CreateCacheRule` / `UpdateCacheRule` - Cache rules
- `CreateWafRule` / `UpdateWafRule` - WAF custom rules
- `CreateRatePlanRule` - Rate limiting rules
- `CreateRewriteUrlRule` / `UpdateRewriteUrlRule` - URL rewrite rules
- Origin rules, redirect rules, header modification rules, etc.

### Expression format

```
(condition)
(condition1 and condition2)
(condition1) or (condition2)
```

Max nesting depth: **2 levels**.

### Operator syntax - two styles

**Infix style** (operator between field and value):
```
(field eq "value")
(field ne "value")
(field contains "value")
(field in {"value1" "value2"})
(field matches "regex")
```

**Function style** (operator wraps field):
```
(starts_with(field, "value"))
(ends_with(field, "value"))
(exists(field))
(len(field) gt 100)
(lower(field) eq "value")
```

### Common patterns

```bash
# Match file extension
--Rule '(http.request.uri.path.extension eq "html")'

# Match multiple extensions
--Rule '(http.request.uri.path.extension in {"js" "css" "png" "jpg"})'

# Match URL prefix
--Rule '(starts_with(http.request.uri, "/api/"))'

# Match URL suffix
--Rule '(ends_with(http.request.uri, ".html"))'

# Match URL containing substring (value MUST start with /)
--Rule '(http.request.uri contains "/test")'

# Match specific host
--Rule '(http.host eq "www.example.com")'

# Combined conditions
--Rule '(http.request.uri contains "/test" and ip.geoip.country eq "CN")'

# Match by country
--Rule '(ip.geoip.country eq "CN")'

# Exclude path
--Rule '(not starts_with(http.request.uri, "/admin/"))'

# Negating set membership
--Rule '(not http.host in {"a.com" "b.com"})'
```

### Key Gotchas

1. `ends_with` and `starts_with` must use **function-call syntax**, NOT infix.
2. `matches` (regex) requires **standard plan or above**; basic plan returns `RuleRegexQuotaCheckFailed`.
3. `contains` with URI must include path separator: `"/test"` is correct; `"test"` alone causes `CompileRuleError`.
4. List values in `in` operator are **space-separated** inside braces: `{"a.com" "b.com"}`.
5. Outer parentheses are **optional** for single conditions.
6. Use `ne` for "not equal", **never** use `not...eq`.
7. Use `not...in` for negating set membership (not before field), not `not in`.

### Plan Limitations

| Plan | eq/ne/in/starts_with/ends_with | contains | matches (regex) |
|------|-------------------------------|----------|----------------|
| Basic | Supported | Supported | Not supported |
| Standard | Supported | Supported | Supported |
| Enterprise | Supported | Supported | Supported |

## AccessKey priority (must follow, align with README)

1) Environment variables: `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`
Region policy: `ALICLOUD_REGION_ID` is an optional default. If unset, decide the most reasonable region for the task; if unclear, ask the user.
2) Shared config file: `~/.alibabacloud/credentials` (region still from env)

### Auth setup (README-aligned)

Environment variables:

```bash
export ALICLOUD_ACCESS_KEY_ID="your-ak"
export ALICLOUD_ACCESS_KEY_SECRET="your-sk"
export ALICLOUD_REGION_ID="cn-hangzhou"
```

Also supported by the Alibaba Cloud SDKs:

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="your-ak"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-sk"
```

Shared config file:

`~/.alibabacloud/credentials`

```ini
[default]
type = access_key
access_key_id = your-ak
access_key_secret = your-sk
```

## API discovery

- Product code: `ESA`
- Default API version: `2024-09-10`
- Metadata endpoint: `https://api.aliyun.com/meta/v1/products/ESA/versions/2024-09-10/api-docs.json`
- Use OpenAPI metadata endpoints to list APIs and get schemas (see references).

## Output policy

If you need to save responses or generated artifacts, write them under:
`output/aliyun-esa-manage/`

## References

### Pages, ER & KV
- **Pages Deployment Reference**: `references/pages.md`
- **Edge Routine Reference**: `references/er.md`
- **Edge KV Storage Reference**: `references/kv.md`

### Site Management
- API overview: `references/api_overview.md`
- Endpoints: `references/endpoints.md`
- Sites: `references/sites.md`
- DNS records: `references/dns-records.md`
- Cache: `references/cache.md`
- Sources: `references/sources.md`
- **Rule expression - generation guide**: `references/rule-generation-guide.md`
- **Rule expression - match fields**: `references/rule-match-fields.md`
- **Rule expression - operators**: `references/rule-operators.md`
- **Rule expression - examples**: `references/rule-examples.md`

### Analytics
- **Time-Series Data API**: `references/time-series.md`
- **Top-N Data API**: `references/top-data.md`
- **Metrics and Dimensions Reference**: `references/fields.md`
