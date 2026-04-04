---
name: aliyun-devops-manage
description: Use when managing Alibaba Cloud DevOps (Yunxiao 2020) via OpenAPI/SDK, including project/repository/pipeline resource discovery, read-only inspection, and safe change planning before mutating operations.
version: 1.0.0
---

Category: service

# Alibaba Cloud DevOps (Yunxiao)

## Purpose

Use Alibaba Cloud DevOps OpenAPI to support:

- project, repository, and pipeline inventory
- work item and test resource inspection
- release and execution status checks
- metadata-driven API discovery before production changes

## Prerequisites

- Configure least-privilege Alibaba Cloud credentials.
- Install Python SDK dependencies for local scripts:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U alibabacloud_devops20210625 alibabacloud_tea_openapi
```

- Prefer environment variables:
  - `ALIBABACLOUD_ACCESS_KEY_ID`
  - `ALIBABACLOUD_ACCESS_KEY_SECRET`
  - optional `ALIBABACLOUD_REGION_ID`

## AccessKey Priority

1) Environment variables: `ALIBABACLOUD_ACCESS_KEY_ID` / `ALIBABACLOUD_ACCESS_KEY_SECRET` / `ALIBABACLOUD_REGION_ID`  
2) Shared credentials file: `~/.alibabacloud/credentials`

If region/environment is unclear, confirm with user before mutating operations.

Compatibility note: runtime scripts also accept `ALIBABA_CLOUD_*` and `ALICLOUD_*` aliases, but `ALIBABACLOUD_*` is the preferred prefix for new examples and automation.

## Workflow

1) Confirm target organization/project scope and change window.
2) Run API discovery and confirm exact API names and required parameters.
3) Execute read-only APIs first (`List*` / `Get*` / `Query*`).
4) Run mutating APIs only after rollback and owner confirmation.
5) Save outputs and evidence to `output/aliyun-devops-manage/`.

## API Discovery

- Product code: `devops`
- Default API version: `2021-06-25`
- Metadata source: `https://api.aliyun.com/meta/v1/products/devops/versions/2021-06-25/api-docs.json`

## Minimal Executable Quickstart

```bash
python skills/platform/devops/aliyun-devops-manage/scripts/list_openapi_meta_apis.py
```

Optional arguments:

```bash
python skills/platform/devops/aliyun-devops-manage/scripts/list_openapi_meta_apis.py \
  --product-code devops \
  --version 2021-06-25 \
  --output-dir output/aliyun-devops-manage
```

List projects (read-only):

```bash
python skills/platform/devops/aliyun-devops-manage/scripts/list_projects.py \
  --organization-id <organization-id> \
  --region cn-hangzhou \
  --max-results 20 \
  --output output/aliyun-devops-manage/projects.txt
```

List repositories (read-only):

```bash
python skills/platform/devops/aliyun-devops-manage/scripts/list_repositories.py \
  --organization-id <organization-id> \
  --region cn-hangzhou \
  --page 1 \
  --per-page 20 \
  --output output/aliyun-devops-manage/repositories.txt
```

List pipelines (read-only):

```bash
python skills/platform/devops/aliyun-devops-manage/scripts/list_pipelines.py \
  --organization-id <organization-id> \
  --region cn-hangzhou \
  --max-results 20 \
  --output output/aliyun-devops-manage/pipelines.txt
```

## Common Operation Map

- Project and membership: `CreateProject`, `GetProject`, `ListProjectMembers`, `UpdateProject`
- Code repository: `CreateRepository`, `GetRepository`, `ListRepositories`, `CreateMergeRequest`
- Pipeline and release: `CreatePipeline`, `GetPipeline`, `ListPipelines`, `RunPipeline`
- Work items and test: `CreateWorkitem`, `GetWorkitemDetail`, `ListTestCase`, `CreateTestCase`

See `references/api_quick_map.md` for grouped APIs.

## Script Catalog

- `scripts/list_openapi_meta_apis.py`: fetch metadata and generate API inventory files.
- `scripts/list_projects.py`: list projects in one organization.
- `scripts/list_repositories.py`: list repositories in one organization.
- `scripts/list_pipelines.py`: list pipelines in one organization.

## Validation

```bash
mkdir -p output/aliyun-devops-manage
for f in skills/platform/devops/aliyun-devops-manage/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-devops-manage/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-devops-manage/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-devops-manage/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## References

- Source list: `references/sources.md`
- API quick map: `references/api_quick_map.md`
- Operation templates: `references/templates.md`
