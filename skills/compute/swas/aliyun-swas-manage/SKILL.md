---
name: aliyun-swas-manage
description: Use when managing Alibaba Cloud Simple Application Server (SWAS OpenAPI 2020-06-01) resources end-to-end, including querying instances, starting/stopping/rebooting, executing commands (cloud assistant), managing disks/snapshots/images, firewall rules/templates, key pairs, tags, monitoring, and lightweight database operations.
version: 1.0.0
---

Category: service

# Simple Application Server (SWAS-OPEN 2020-06-01)

Use SWAS-OPEN OpenAPI to manage full SAS resources: instances, disks, snapshots, images, key pairs, firewall, Cloud Assistant, monitoring, tags, and lightweight databases.

## Prerequisites

- Prepare AccessKey with least-privilege RAM user/role.
- Choose correct region and matching endpoint (public/VPC).`ALICLOUD_REGION_ID` can be used as default region; if unset choose the most reasonable region, ask user if unclear.
- This OpenAPI uses RPC signing; prefer Python SDK or OpenAPI Explorer instead of manual signing.

## SDK Priority

1) Python SDK (preferred)
2) OpenAPI Explorer
3) Other SDKs

### Python SDK quick query (instance ID / IP / plan)

Virtual environment is recommended (avoid PEP 668 system install restrictions).

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install alibabacloud_swas_open20200601 alibabacloud_tea_openapi alibabacloud_credentials
```

```python
import os
from alibabacloud_swas_open20200601.client import Client as SwasClient
from alibabacloud_swas_open20200601 import models as swas_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> SwasClient:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"swas.{region_id}.aliyuncs.com",
    )
    ak = os.getenv("ALICLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALICLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if ak and sk:
        config.access_key_id = ak
        config.access_key_secret = sk
    return SwasClient(config)


def list_regions():
    client = create_client("cn-hangzhou")
    resp = client.list_regions(swas_models.ListRegionsRequest())
    return [r.region_id for r in resp.body.regions]


def list_instances(region_id: str):
    client = create_client(region_id)
    resp = client.list_instances(swas_models.ListInstancesRequest(region_id=region_id))
    return resp.body.instances


def main():
    for region_id in list_regions():
        for inst in list_instances(region_id):
            ip = getattr(inst, "public_ip_address", None) or getattr(inst, "inner_ip_address", None)
            spec = getattr(inst, "plan_name", None) or getattr(inst, "plan_id", None)
            print(inst.instance_id, ip or "-", spec or "-", region_id)


if __name__ == "__main__":
    main()
```

### Python SDK scripts (recommended for inventory and summary)

- All-region instance inventory (TSV/JSON):`scripts/list_instances_all_regions.py`
- Count instances by plan:`scripts/summary_instances_by_plan.py`
- Count instances by status:`scripts/summary_instances_by_status.py`
- Fix SSH key-based access (custom port supported):`scripts/fix_ssh_access.py`
- Get current SSH port of an instance:`scripts/get_ssh_port.py`

## CLI Notes

- `aliyun` CLI may not expose `swas-open` as product name; prefer Python SDK.
  If CLI is mandatory, generate request examples in OpenAPI Explorer first, then migrate to CLI.

## Workflow

1) Confirm resource type and region (instance/disk/snapshot/image/firewall/command/database/tag).  
2) Identify API group and operation in `references/api_overview.md`.  
3) Choose invocation method (Python SDK / OpenAPI Explorer / other SDK).  
4) After mutations, verify state/results with query APIs.  

## Common Operation Map

- Instance query/start/stop/reboot:`ListInstances`、`StartInstance(s)`、`StopInstance(s)`、`RebootInstance(s)`  
- Command execution:`RunCommand` or `CreateCommand` + `InvokeCommand`; use `DescribeInvocations`/`DescribeInvocationResult`  
- Firewall:`ListFirewallRules`/`CreateFirewallRule(s)`/`ModifyFirewallRule`/`EnableFirewallRule`/`DisableFirewallRule`  
- Snapshot/disk/image:`CreateSnapshot`、`ResetDisk`、`CreateCustomImage` etc.  

## Cloud Assistant Execution Notes

- Target instance must be in Running state.
- Cloud Assistant agent must be installed (use `InstallCloudAssistant`).
- For PowerShell commands, ensure required modules are available on Windows instances.
- After execution, use `DescribeInvocations` or `DescribeInvocationResult` to fetch status and outputs.

See `references/command-assistant.md` for details.

## Clarifying questions (ask when uncertain)

1. What is the target region? Is VPC endpoint required?
2. What are target instance IDs? Are they currently Running?
3. What command/script type/timeout is needed? Linux or Windows?
4. Do you need batch execution or scheduled execution?

## Output Policy

If you need to save results or responses, write to:
`output/compute-swas-open/`

## Validation

```bash
mkdir -p output/aliyun-swas-manage
for f in skills/compute/swas/aliyun-swas-manage/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-swas-manage/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-swas-manage/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-swas-manage/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Prerequisites

- Configure least-privilege Alibaba Cloud credentials before execution.
- Prefer environment variables: `ALICLOUD_ACCESS_KEY_ID`, `ALICLOUD_ACCESS_KEY_SECRET`, optional `ALICLOUD_REGION_ID`.
- If region is unclear, ask the user before running mutating operations.

## Workflow

1) Confirm user intent, region, identifiers, and whether the operation is read-only or mutating.
2) Run one minimal read-only query first to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.

## References

- API overview and operation groups:`references/api_overview.md`
- Endpoints and integration:`references/endpoints.md`
- Cloud Assistant highlights:`references/command-assistant.md`
- Official source list:`references/sources.md`
