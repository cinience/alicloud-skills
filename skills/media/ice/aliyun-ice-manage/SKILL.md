---
name: aliyun-ice-manage
description: Use when managing Alibaba Cloud Intelligent Cloud Editing (ICE) media workflows via OpenAPI/SDK, including media processing jobs, template/workflow orchestration, editing and production pipelines, and job status troubleshooting.
version: 1.0.0
---

Category: service

# Intelligent Cloud Editing (ICE)

## Validation

```bash
mkdir -p output/aliyun-ice-manage
python -m py_compile skills/media/ice/aliyun-ice-manage/scripts/list_openapi_meta_apis.py
echo "py_compile_ok" > output/aliyun-ice-manage/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-ice-manage/validate.txt` is generated.

## Output And Evidence

- Save API inventory and operation evidence under `output/aliyun-ice-manage/`.
- Keep region, workflow IDs, job IDs, and request parameters in evidence files.

Use Alibaba Cloud OpenAPI (RPC) with official SDKs or OpenAPI Explorer to manage ICE resources.
Prefer metadata-first API discovery before mutate operations.

## Prerequisites

- Prepare least-privilege RAM AccessKey/STS credentials.
- Confirm target region, input/output OSS locations, and workflow scope before changes.
- Query current state with read-only APIs before invoking processing jobs.

## Workflow

1) Confirm target workflow/template and media input/output locations.
2) Discover API names and required parameters via metadata and API Explorer.
3) Validate prerequisite resources using read-only APIs.
4) Submit and monitor processing jobs.
5) Save outputs and evidence under `output/aliyun-ice-manage/`.

## AccessKey Priority

1) Environment variables: `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`.
2) Shared config file: `~/.alibabacloud/credentials`.

If region is ambiguous, ask before write operations.

## API Discovery

- Product code: `ice`
- Default API version: `2020-11-09`
- Metadata source: `https://api.aliyun.com/meta/v1/products/ice/versions/2020-11-09/api-docs.json`

## Minimal Executable Quickstart

```bash
python skills/media/ice/aliyun-ice-manage/scripts/list_openapi_meta_apis.py
```

Optional overrides:

```bash
python skills/media/ice/aliyun-ice-manage/scripts/list_openapi_meta_apis.py \
  --product-code ice \
  --version 2020-11-09 \
  --output-dir output/aliyun-ice-manage
```

## Common Operation Mapping

- Media info and metadata: `GetMediaInfo`, `SearchMedia`, `UpdateMediaMeta`
- Workflow/template: `CreateMediaWorkflow`, `UpdateMediaWorkflow`, `ListMediaWorkflowExecutions`
- Job submission: `SubmitMediaProducingJob`, `SubmitBatchMediaProducingJob`, `GetMediaProducingJob`
- Editing/material: `CreateSourceLocation`, `AddMedia`, `GetDefaultMaterial`
- Task status/troubleshooting: `GetTaskInfo`, `ListJobs`, `GetBatchMediaProducingJob`

## Output Policy

Write all generated files and execution evidence under:
`output/aliyun-ice-manage/`

## References

- Source list: `references/sources.md`
- Task templates: `references/templates.md`
