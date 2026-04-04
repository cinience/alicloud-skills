---
name: alicloud-observability-pts-test
description: Smoke test for alicloud-observability-pts. Validate script compilation and one bounded read-only PTS metadata query path.
version: 1.0.0
---

Category: test

# OBSERVABILITY PTS Smoke Test

## Prerequisites

- Configure credentials with least privilege (`ALIBABACLOUD_ACCESS_KEY_ID` / `ALIBABACLOUD_ACCESS_KEY_SECRET` / optional `ALIBABACLOUD_REGION_ID`) if you plan to execute real PTS APIs.
- Target skill: `skills/observability/pts/alicloud-observability-pts/`.
- Optional online SDK test dependency:

```bash
python -m pip install -U alibabacloud_pts20201020 alibabacloud_tea_openapi
```

## Test Steps

1) Run offline script compilation check (no network needed):

```bash
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/observability/pts/alicloud-observability-pts \
  --output output/alicloud-observability-pts-test/compile-check.json
```

2) Run metadata API discovery script:

```bash
python3 skills/observability/pts/alicloud-observability-pts/scripts/list_openapi_meta_apis.py \
  --product-code PTS \
  --version 2020-10-20 \
  --output-dir output/alicloud-observability-pts-test
```

3) Verify generated files and API count:

```bash
test -f output/alicloud-observability-pts-test/PTS_2020-10-20_api_docs.json
test -f output/alicloud-observability-pts-test/PTS_2020-10-20_api_list.md
rg -n "API count: [1-9][0-9]*" output/alicloud-observability-pts-test/PTS_2020-10-20_api_list.md
```

4) Save request summary, response summary, and raw output under `output/alicloud-observability-pts-test/`.
5) If the call fails, record exact error code/message without guessing.

## Optional Online Read-only Check

Run one bounded read-only scene query:

```bash
python3 skills/observability/pts/alicloud-observability-pts/scripts/list_pts_scenes.py \
  --region "${ALIBABACLOUD_REGION_ID:-cn-hangzhou}" \
  --page-number 1 \
  --page-size 10 \
  --json \
  --output output/alicloud-observability-pts-test/list-scenes.json
```

Then verify output contains response metadata:

```bash
rg -n '\"RequestId\"|\"Success\"|\"Code\"' output/alicloud-observability-pts-test/list-scenes.json
```

## Pass Criteria

- Script compilation check passes (`compile-check.json.status=pass`).
- Metadata API discovery succeeds and produces both JSON and markdown output files.
- API list markdown shows a positive API count.
- Evidence files exist in `output/alicloud-observability-pts-test/`.
- Optional online read-only check returns a valid PTS response structure.

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/observability/pts/alicloud-observability-pts
- Conclusion: pass / fail
- Notes:
