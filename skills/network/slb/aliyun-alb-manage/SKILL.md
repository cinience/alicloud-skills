---
name: aliyun-alb-manage
description: Use when managing and troubleshoot Alibaba Cloud ALB (Application Load Balancer), including the user asks to inspect, create, change, or debug ALB instances, listeners, server groups, rules, certificates, ACLs, security policies, or health checks in Alibaba Cloud.
version: 1.0.0
---

Category: service

# Application Load Balancer (ALB)

Use this skill for end-to-end ALB operations via local Python scripts and OpenAPI-compatible workflows.

## Validation

```bash
mkdir -p output/aliyun-alb-manage
for f in skills/network/slb/aliyun-alb-manage/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-alb-manage/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-alb-manage/validate.txt` is generated.

## Output And Evidence

- Save all command outputs, request parameters, and API responses under `output/aliyun-alb-manage/`.
- For change operations, keep before/after snapshots plus health-check results.

## Prerequisites

```bash
pip install alibabacloud_alb20200616 alibabacloud_tea_openapi alibabacloud_credentials
```

Credential priority:

1. `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET`
2. Optional STS token: `ALICLOUD_SECURITY_TOKEN`
3. Shared config: `~/.alibabacloud/credentials`

## Workflow

1. Confirm region, VPC context, target ALB resource IDs, and expected change window.
2. Run inventory scripts first (`list_*`, `get_*`) and save baseline outputs.
3. Apply one change at a time (listener/server-group/rule/lb lifecycle).
4. Wait for async completion when needed (`scripts/wait_for_job.py`).
5. Validate final state with health checks and state re-query.

## Top task playbooks

### 1) Read-only inventory and quick diagnosis

```bash
python3 scripts/list_instances.py --region cn-hangzhou --json --output output/aliyun-alb-manage/instances.json
python3 scripts/list_server_groups.py --region cn-hangzhou --json --output output/aliyun-alb-manage/server-groups.json
python3 scripts/list_acls.py --region cn-hangzhou --json --output output/aliyun-alb-manage/acls.json
```

### 2) Inspect one ALB and listener details

```bash
python3 scripts/get_instance_status.py --region cn-hangzhou --lb-id alb-xxx --view detail --output output/aliyun-alb-manage/lb-detail.json
python3 scripts/list_listeners.py --region cn-hangzhou --lb-id alb-xxx --json --output output/aliyun-alb-manage/listeners.json
python3 scripts/get_listener_attribute.py --region cn-hangzhou --listener-id lsn-xxx --output output/aliyun-alb-manage/listener-attr.json
```

### 3) Validate traffic path health

```bash
python3 scripts/check_health_status.py --region cn-hangzhou --listener-id lsn-xxx --output output/aliyun-alb-manage/health.json
python3 scripts/list_server_group_servers.py --region cn-hangzhou --server-group-id sgp-xxx --output output/aliyun-alb-manage/server-group-members.json
```

### 4) Controlled change flow (example: update listener)

```bash
python3 scripts/update_listener.py --region cn-hangzhou --listener-id lsn-xxx --request-timeout 120 --output output/aliyun-alb-manage/update-listener.json
python3 scripts/check_health_status.py --region cn-hangzhou --listener-id lsn-xxx --output output/aliyun-alb-manage/health-after-update.json
```

### 5) Resource lifecycle operations

- ALB lifecycle: `create_load_balancer.py`, `delete_load_balancer.py`, `deletion_protection.py`
- Listener lifecycle: `create_listener.py`, `start_listener.py`, `stop_listener.py`, `delete_listener.py`
- Server-group lifecycle: `create_server_group.py`, `add_servers.py`, `remove_servers.py`, `delete_server_group.py`
- Rule lifecycle: `create_rule.py`, `update_rule.py`, `delete_rule.py`

## References

- API quick map: `references/api_quick_map.md`
- Script catalog: `references/scripts_catalog.md`
- Troubleshooting: `references/troubleshooting.md`
- Logs and analysis: `references/log-analysis.md`
- Dependencies/order: `references/resource-dependencies.md`
- Sources: `references/sources.md`
