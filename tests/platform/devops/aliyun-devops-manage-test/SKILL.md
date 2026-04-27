---
name: aliyun-devops-manage-test
description: Smoke test for aliyun-devops-manage. Validate script compilation and one bounded DevOps metadata query path.
version: 1.0.0
---

Category: test

# PLATFORM DEVOPS Smoke Test

## Prerequisites

- Target skill: `skills/platform/devops/aliyun-devops-manage/`.
- Optional online SDK test dependency:

```bash
python -m pip install -U alibabacloud_devops20210625 alibabacloud_tea_openapi
```

## Test Steps

1) Run offline script compilation check:

```bash
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/platform/devops/aliyun-devops-manage \
  --output output/aliyun-devops-manage-test/compile-check.json
```

2) Run metadata API discovery script:

```bash
python3 skills/platform/devops/aliyun-devops-manage/scripts/list_openapi_meta_apis.py \
  --product-code devops \
  --version 2021-06-25 \
  --output-dir output/aliyun-devops-manage-test
```

3) Verify generated files and API count:

```bash
test -f output/aliyun-devops-manage-test/devops_2021-06-25_api_docs.json
test -f output/aliyun-devops-manage-test/devops_2021-06-25_api_list.md
rg -n "API count: [1-9][0-9]*" output/aliyun-devops-manage-test/devops_2021-06-25_api_list.md
```

4) Save request summary, response summary, and raw output under `output/aliyun-devops-manage-test/`.

## Optional Online Read-only Check

Set one organization id:

```bash
export DEVOPS_ORGANIZATION_ID=<organization-id>
```

Run bounded read-only calls:

```bash
python3 skills/platform/devops/aliyun-devops-manage/scripts/list_projects.py \
  --organization-id \"$DEVOPS_ORGANIZATION_ID\" \
  --max-results 10 \
  --json \
  --output output/aliyun-devops-manage-test/list-projects.json

python3 skills/platform/devops/aliyun-devops-manage/scripts/list_repositories.py \
  --organization-id \"$DEVOPS_ORGANIZATION_ID\" \
  --page 1 \
  --per-page 10 \
  --json \
  --output output/aliyun-devops-manage-test/list-repositories.json

python3 skills/platform/devops/aliyun-devops-manage/scripts/list_pipelines.py \
  --organization-id \"$DEVOPS_ORGANIZATION_ID\" \
  --max-results 10 \
  --json \
  --output output/aliyun-devops-manage-test/list-pipelines.json
```

Verify basic response structure:

```bash
rg -n '\"requestId\"|\"success\"|\"errorCode\"|\"errorMessage\"' \
  output/aliyun-devops-manage-test/list-projects.json \
  output/aliyun-devops-manage-test/list-repositories.json \
  output/aliyun-devops-manage-test/list-pipelines.json
```

## Pass Criteria

- Script compilation check passes (`compile-check.json.status=pass`).
- Metadata API discovery succeeds and produces both JSON and markdown output files.
- API list markdown shows a positive API count.
- Evidence files exist in `output/aliyun-devops-manage-test/`.
- Optional online read-only check returns valid response structures.

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/platform/devops/aliyun-devops-manage
- Conclusion: pass / fail
- Notes:
