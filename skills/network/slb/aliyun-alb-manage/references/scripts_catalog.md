# ALB Scripts Catalog

This file groups all local scripts by operation so `SKILL.md` can stay focused on the decision workflow.

## Inventory and inspection

- `scripts/list_instances.py` - list ALB instances with filters.
- `scripts/get_instance_status.py` - inspect one ALB instance (tree/detail view).
- `scripts/list_listeners.py` - list listeners under one ALB.
- `scripts/get_listener_attribute.py` - inspect listener details.
- `scripts/list_server_groups.py` - list server groups.
- `scripts/list_server_group_servers.py` - list backend servers in one group.
- `scripts/list_rules.py` - list forwarding rules.
- `scripts/check_health_status.py` - query listener health status.
- `scripts/list_listener_certificates.py` - list listener certificates.
- `scripts/list_security_policies.py` - list custom/system TLS policies.
- `scripts/list_acls.py` - list ACL resources.
- `scripts/list_acl_entries.py` - list ACL entries.

## Create and update resources

- `scripts/create_load_balancer.py` / `scripts/delete_load_balancer.py`
- `scripts/deletion_protection.py`
- `scripts/create_listener.py` / `scripts/update_listener.py` / `scripts/start_listener.py` / `scripts/stop_listener.py` / `scripts/delete_listener.py`
- `scripts/create_server_group.py` / `scripts/delete_server_group.py`
- `scripts/add_servers.py` / `scripts/remove_servers.py`
- `scripts/create_rule.py` / `scripts/update_rule.py` / `scripts/delete_rule.py`

## Async and operation tracking

- `scripts/wait_for_job.py` - wait for ALB async job completion and return final state.

## Suggested sequence for production changes

1. Snapshot current state with `list_*` and `get_*` scripts.
2. Apply one change operation (create/update/delete).
3. Wait with `wait_for_job.py` if the API returns an async job id.
4. Re-check listeners, server groups, and health status.
5. Save all evidence under `output/aliyun-alb-manage/`.
