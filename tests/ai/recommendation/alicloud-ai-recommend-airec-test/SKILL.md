---
name: alicloud-ai-recommend-airec-test
description: Smoke test for alicloud-ai-recommend-airec. Validate minimal authentication, API reachability, and one read-only query path.
version: 1.0.0
---

Category: test

# AI RECOMMEND AIREC Smoke Test

## Prerequisites

- Configure credentials with least privilege (`ALIBABACLOUD_ACCESS_KEY_ID` / `ALIBABACLOUD_ACCESS_KEY_SECRET` / optional `ALIBABACLOUD_REGION_ID`).
- Target skill: `skills/ai/recommendation/alicloud-ai-recommend-airec/`.

## Test Steps

1) Run offline script compilation check (no network needed):

```bash
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/ai/recommendation/alicloud-ai-recommend-airec \
  --output output/alicloud-ai-recommend-airec-test/compile-check.json
```

2) Read the target skill `SKILL.md` and identify one lowest-risk read-only API (for example `Describe*` / `List*` / `Get*`).
3) Execute one minimal call with bounded scope (region + page size / limit).
4) Save request summary, response summary, and raw output under `output/alicloud-ai-recommend-airec-test/`.
5) If the call fails, record exact error code/message without guessing.

## Pass Criteria

- Script compilation check passes (`compile-check.json.status=pass`).
- The selected read-only API call succeeds and returns valid response structure.
- Evidence files exist in `output/alicloud-ai-recommend-airec-test/` with timestamp and parameters.

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/ai/recommendation/alicloud-ai-recommend-airec
- Conclusion: pass / fail
- Notes:
