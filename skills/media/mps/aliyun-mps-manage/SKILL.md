---
name: aliyun-mps-manage
description: Use when managing Alibaba Cloud ApsaraVideo for Media Processing (MPS/MTS) resources and workflows via OpenAPI/SDK, including media ingest and metadata tasks, transcoding/snapshot jobs, pipeline/template/workflow operations, and MPS job troubleshooting.
version: 1.0.0
---

Category: service

# ApsaraVideo for Media Processing (MPS)

## Validation

```bash
mkdir -p output/aliyun-mps-manage
python -m py_compile skills/media/mps/aliyun-mps-manage/scripts/list_openapi_meta_apis.py
echo "py_compile_ok" > output/aliyun-mps-manage/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-mps-manage/validate.txt` is generated.

## Output And Evidence

- Save API inventory and operation evidence under `output/aliyun-mps-manage/`.
- Keep region, pipeline/template/workflow IDs, media IDs, and request parameters in evidence files.

Use Alibaba Cloud OpenAPI (RPC) with official SDKs or OpenAPI Explorer to manage MPS resources.
Prefer metadata-first API discovery before mutate operations.

## Prerequisites

- Prepare least-privilege RAM AccessKey/STS credentials.
- Confirm target region and OSS input/output buckets before changes.
- Use read-only query APIs first.

## Workflow

1) Confirm target media scope, bucket binding, and desired operation.
2) Discover API names and required parameters via OpenAPI metadata and API Explorer.
3) Execute read-only validation calls.
4) Execute pipeline/template/workflow/job operations.
5) Save outputs and evidence under `output/aliyun-mps-manage/`.

## AccessKey Priority

1) Environment variables: `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`.
2) Shared config file: `~/.alibabacloud/credentials`.

If region is ambiguous, ask before write operations.

## API Discovery

- Product code: `Mts`
- Default API version: `2014-06-18`
- Metadata source: `https://api.aliyun.com/meta/v1/products/Mts/versions/2014-06-18/api-docs.json`

## Minimal Executable Quickstart

```bash
python skills/media/mps/aliyun-mps-manage/scripts/list_openapi_meta_apis.py
```

Optional overrides:

```bash
python skills/media/mps/aliyun-mps-manage/scripts/list_openapi_meta_apis.py \
  --product-code Mts \
  --version 2014-06-18 \
  --output-dir output/aliyun-mps-manage
```

## Common Operation Mapping

- Pipeline operations: `AddPipeline`, `UpdatePipeline`, `QueryPipelineList`, `SearchPipeline`
- Template operations: `AddTemplate`, `UpdateTemplate`, `QueryTemplateList`, `SearchTemplate`
- Workflow operations: `AddMediaWorkflow`, `UpdateMediaWorkflow`, `QueryMediaWorkflowList`, `ListMediaWorkflowExecutions`
- Job operations: `SubmitJobs`, `QueryJobList`, `ListJob`, `CancelJob`
- Snapshot and analysis: `SubmitSnapshotJob`, `QuerySnapshotJobList`, `SubmitAnalysisJob`
- Media and bucket management: `AddMedia`, `UpdateMedia`, `DeleteMedia`, `BindInputBucket`, `BindOutputBucket`

## Output Policy

Write all generated files and execution evidence under:
`output/aliyun-mps-manage/`

## References

- Source list: `references/sources.md`
- Task templates: `references/templates.md`
