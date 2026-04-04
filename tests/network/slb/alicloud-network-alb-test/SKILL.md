---
name: alicloud-network-alb-test
description: Smoke test for Alibaba Cloud ALB skill. Validates SDK auth, script compilation, list instances, and health check flows.
version: 1.0.0
---

Category: test

# ALB Smoke Test

## Prerequisites

- AK/SK configured via environment variables (`ALIBABACLOUD_ACCESS_KEY_ID` / `ALIBABACLOUD_ACCESS_KEY_SECRET`).
- SDK installed: `pip install alibabacloud_alb20200616 alibabacloud_tea_openapi alibabacloud_credentials`.
- Target skill: `skills/network/slb/alicloud-network-alb/`.

## Test Steps

### 1. Script compilation check (offline, no credentials needed)

```bash
python tests/network/slb/alicloud-network-alb-test/scripts/smoke_test_alb.py --compile-only
```

Pass criteria: exits 0, all 28 scripts compile successfully.

### 2. Full smoke test (requires credentials and region)

```bash
python tests/network/slb/alicloud-network-alb-test/scripts/smoke_test_alb.py \
  --region cn-hangzhou
```

Pass criteria:
- `status=pass` in JSON output.
- Output file `output/alicloud-network-alb-test/smoke-test-result.json` exists.
- `list_instances` returns valid JSON (even if empty).
- `list_server_groups` returns valid JSON (even if empty).
- `list_acls` returns valid JSON (even if empty).

### 3. Instance-specific test (requires a running ALB)

```bash
python tests/network/slb/alicloud-network-alb-test/scripts/smoke_test_alb.py \
  --region cn-hangzhou --lb-id alb-xxx
```

Additional pass criteria:
- `get_instance_status` returns tree output.
- `list_listeners` returns valid response.
- `check_health_status` returns health data.

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/network/slb/alicloud-network-alb
- Conclusion: pass / fail
- Notes:
