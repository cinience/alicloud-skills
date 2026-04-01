---
name: aliyun-live-manage
description: Use when managing Alibaba Cloud ApsaraVideo Live resources and workflows via OpenAPI/SDK, including live domain configuration, stream ingest and playback setup, recording/transcoding templates, monitoring queries, and live stream operations.
version: 1.0.0
---

Category: service

# ApsaraVideo Live

## Validation

```bash
mkdir -p output/aliyun-live-manage
python -m py_compile skills/media/live/aliyun-live-manage/scripts/list_openapi_meta_apis.py
echo "py_compile_ok" > output/aliyun-live-manage/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-live-manage/validate.txt` is generated.

## Output And Evidence

- Save API inventory and operation evidence under `output/aliyun-live-manage/`.
- Keep region, domain, app/stream, and request parameters in evidence files.

Use Alibaba Cloud OpenAPI (RPC) with official SDKs or OpenAPI Explorer to manage Live resources.
Prefer metadata-first API discovery before mutate operations.

## Prerequisites

- Prepare least-privilege RAM AccessKey/STS credentials.
- Confirm target region and live domain scope before changes.
- Query current state with read-only APIs (`Describe*` / `List*`) before `Add*` / `Set*` / `Delete*`.

## Workflow

1) Confirm target live domain, app name/stream name, and desired operation.
2) Discover API names and required parameters via metadata and API Explorer.
3) Execute read-only validation calls.
4) Apply change operations with rollback plan.
5) Save results and context under `output/aliyun-live-manage/`.

## AccessKey Priority

1) Environment variables: `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`.
2) Shared config file: `~/.alibabacloud/credentials`.

If region is ambiguous, ask before write operations.

## API Discovery

- Product code: `live`
- Default API version: `2016-11-01`
- Metadata source: `https://api.aliyun.com/meta/v1/products/live/versions/2016-11-01/api-docs.json`

## Minimal Executable Quickstart

```bash
python skills/media/live/aliyun-live-manage/scripts/list_openapi_meta_apis.py
```

Optional overrides:

```bash
python skills/media/live/aliyun-live-manage/scripts/list_openapi_meta_apis.py \
  --product-code live \
  --version 2016-11-01 \
  --output-dir output/aliyun-live-manage
```

## Common Operation Mapping

- Domain management: `AddLiveDomain`, `DeleteLiveDomain`, `DescribeLiveDomains`
- Stream ingest/play auth: `AddLiveDomainMapping`, `SetLiveDomainStagingConfig`
- Record/transcode/template: `AddLiveRecordTemplate`, `AddLiveTranscodeTemplate`, `DescribeLiveRecordConfig`
- Monitor and metrics: `DescribeLiveStreamOnlineList`, `DescribeLiveDomainBpsData`, `DescribeLiveDomainTrafficData`
- Stream control: `ForbidLiveStream`, `ResumeLiveStream`, `AddLiveAppRecordConfig`

## Output Policy

Write all generated files and execution evidence under:
`output/aliyun-live-manage/`

## References

- Source list: `references/sources.md`
- Task templates: `references/templates.md`
