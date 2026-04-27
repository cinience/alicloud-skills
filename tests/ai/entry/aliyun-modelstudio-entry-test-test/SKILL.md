---
name: aliyun-modelstudio-entry-test-test
description: Smoke test for aliyun-modelstudio-entry-test. Validate minimal authentication, API reachability, and one read-only query path.
version: 1.0.0
---

Category: test

# AI ENTRY MODELSTUDIO TEST Smoke Test

## Prerequisites

- Configure credentials with least privilege (`ALIBABACLOUD_ACCESS_KEY_ID` / `ALIBABACLOUD_ACCESS_KEY_SECRET` / optional `ALIBABACLOUD_REGION_ID`).
- Target skill: `skills/ai/entry/aliyun-modelstudio-entry-test/`.

## Test Steps

1) Run offline script compilation check (no network needed):

```bash
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/ai/entry/aliyun-modelstudio-entry-test \
  --output output/aliyun-modelstudio-entry-test-test/compile-check.json
```

2) Read the target skill `SKILL.md` and identify one lowest-risk read-only API (for example `Describe*` / `List*` / `Get*`).
3) Execute one minimal call with bounded scope (region + page size / limit).
4) Save request summary, response summary, and raw output under `output/aliyun-modelstudio-entry-test-test/`.
5) If the call fails, record exact error code/message without guessing.

## Pass Criteria

- Script compilation check passes (`compile-check.json.status=pass`).
- The selected read-only API call succeeds and returns valid response structure.
- Evidence files exist in `output/aliyun-modelstudio-entry-test-test/` with timestamp and parameters.

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/ai/entry/aliyun-modelstudio-entry-test
- Conclusion: pass / fail
- Notes:
