---
name: aliyun-dlf-manage-test
description: Minimal smoke test for DataLake skill. Validate metadata discovery and one read-only API call.
version: 1.0.0
---

Category: test

# DataLake Minimal Viable Test

## Prerequisites

- AK/SK and region are configured.
- GoalsSkill: `skills/data-lake/aliyun-dlf-manage/`。

## Test Steps

1) Run `python scripts/list_openapi_meta_apis.py`.
2) Select one read-only API and run a minimal request.
3) Save outputs under `output/aliyun-dlf-manage-test/`。

## Expected Results

- Metadata retrieval succeeds.
- Read-only API returns success or an explicit permission error.
