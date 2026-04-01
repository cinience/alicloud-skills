---
name: aliyun-cdn-manage
description: Use when managing Alibaba Cloud CDN via OpenAPI/SDK, including CDN domain onboarding and lifecycle operations, cache refresh/preload, HTTPS certificate updates, and log/monitoring data queries.
version: 1.0.0
---

Category: service

# Alibaba Cloud CDN

## Purpose

Use Alibaba Cloud CDN OpenAPI (RPC) for common operations and integrations including:

- accelerated domain lifecycle (create/configure/start-stop/delete)
- cache refresh and preload (directory/file/domain)
- HTTPS certificate configuration and updates
- log and monitoring queries (real-time/offline)

## Prerequisites

- least-privilege RAM credentials are ready (STS temporary creds recommended).
- domain ownership and acceleration scope policy are confirmed (mainland/global).
- before mutating operations, validate current state using read-only APIs.

## Workflow

1) Define target resources: accelerated domains, business type, change window, and rollback criteria.  
2) Run API discovery and confirm target API names, required parameters, and version.  
3) Query current config/state with read-only APIs (`Describe*`) first.  
4) Execute mutating APIs (`Add*`/`Set*`/`BatchSet*`/`Delete*`) and record request context.  
5) Validate changes with monitoring/log APIs and save evidence in `output/aliyun-cdn-manage/`.

## AccessKey Priority

1) Environment variables:`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
2) Shared credentials file:`~/.alibabacloud/credentials`

If region/environment is unclear, confirm with user before mutating operations.

## API Discovery

- Product code: `cdn`
- Default API version: `2018-05-10`
- Metadata source: `https://api.aliyun.com/meta/v1/products/cdn/versions/2018-05-10/api-docs.json`

## Minimal Executable Quickstart

```bash
python skills/network/cdn/aliyun-cdn-manage/scripts/list_openapi_meta_apis.py
```

Optional arguments:

```bash
python skills/network/cdn/aliyun-cdn-manage/scripts/list_openapi_meta_apis.py \
  --product-code cdn \
  --version 2018-05-10 \
  --output-dir output/aliyun-cdn-manage
```

## Common Operation Map

- Domain management:`AddCdnDomain`、`DescribeUserDomains`、`DescribeCdnDomainDetail`、`DeleteCdnDomain`
- Cache refresh/preload:`RefreshObjectCaches`（refresh）、`PushObjectCache`（preload）
- HTTPS certificate: `SetDomainServerCertificate`, `DescribeDomainCertificateInfo`
- Logs and monitoring:`DescribeCdnDomainLogs`、`DescribeDomainRealTimeRequestStatData`、`DescribeDomainRealTimeBpsData`

## Output Policy

Write generated files and execution evidence to:
`output/aliyun-cdn-manage/`

## Validation

```bash
mkdir -p output/aliyun-cdn-manage
for f in skills/network/cdn/aliyun-cdn-manage/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-cdn-manage/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-cdn-manage/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-cdn-manage/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Prerequisites

- Configure least-privilege Alibaba Cloud credentials before execution.
- Prefer environment variables: `ALICLOUD_ACCESS_KEY_ID`, `ALICLOUD_ACCESS_KEY_SECRET`, optional `ALICLOUD_REGION_ID`.
- If region is unclear, ask the user before running mutating operations.

## References

- Source list: `references/sources.md`
