---
name: aliyun-ecs-manage
description: Manage Alibaba Cloud Elastic Compute Service (ECS) via OpenAPI/SDK. Use for listing or creating instances, starting/stopping/rebooting, managing disks/snapshots/images/security groups/key pairs/ENIs, querying status, and troubleshooting workflows for this product.
version: 1.0.0
---

Category: service

# Elastic Compute Service (ECS)

## Validation

```bash
mkdir -p output/aliyun-ecs-manage
python -m py_compile skills/compute/ecs/aliyun-ecs-manage/scripts/list_instances_all_regions.py
python -m py_compile skills/compute/ecs/aliyun-ecs-manage/scripts/query_instance_usage.py
python -m py_compile skills/compute/ecs/aliyun-ecs-manage/scripts/run_remote_command.py
echo "py_compile_ok" > output/aliyun-ecs-manage/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-ecs-manage/validate.txt` is generated.

## Output And Evidence

- Save list/summarize outputs under `output/aliyun-ecs-manage/`.
- Keep command arguments and region scope in each evidence file.

Use Alibaba Cloud OpenAPI (RPC) with official SDKs or OpenAPI Explorer to manage ECS resources.
Prefer the Python SDK for all examples and execution.

## Prerequisites

- Prepare AccessKey (RAM user/role with least privilege).
- Choose the correct region and endpoint (public/VPC).
- ECS OpenAPI is RPC style; prefer SDK or OpenAPI Explorer to avoid manual signing.

## API behavior notes (from ECS docs)

- Most list/describe APIs support pagination via `PageNumber` + `PageSize` or `NextToken` + `MaxResults`.
- `DescribeInstances` returns an empty list if the RAM user/role lacks permissions; use `DryRun` to validate permissions.
- For `DescribeInstances`, `NextToken` + `MaxResults` is the recommended paged query pattern; use the returned `NextToken` to fetch subsequent pages.
- `DescribeInstances` requires `RegionId` in the request even if the client has a region set.
- Filters are ANDed; set only the filters you need.

## Workflow

1) Confirm region, resource identifiers, and desired action.
2) Find API group and exact operation name in `references/api_overview.md`.
3) Call API with Python SDK (preferred) or OpenAPI Explorer.
4) Verify results with describe/list APIs.
5) If you need repeatable inventory or summaries, use `scripts/` and write outputs under `output/aliyun-ecs-manage/`.

## SDK priority

1) Python SDK (preferred)
2) OpenAPI Explorer
3) Other SDKs (only if Python is not feasible)

### Python SDK quickstart (list instances)

Virtual environment is recommended (avoid PEP 668 system install restrictions).

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install alibabacloud_ecs20140526 alibabacloud_tea_openapi alibabacloud_credentials
```

```python
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_ecs20140526 import models as ecs_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Ecs20140526Client:
    config = open_api_models.Config(
        # Use env vars or shared config files per AccessKey priority.
        region_id=region_id,
        endpoint=f"ecs.{region_id}.aliyuncs.com",
    )
    return Ecs20140526Client(config)


def list_instances(region_id: str):
    client = create_client(region_id)
    resp = client.describe_instances(ecs_models.DescribeInstancesRequest(
        region_id=region_id,
        page_number=1,
        page_size=50,
    ))
    for inst in resp.body.instances.instance:
        print(inst.instance_id, inst.instance_name, inst.instance_type, inst.status)


if __name__ == "__main__":
    list_instances("cn-hangzhou")
```

### Python SDK scripts (recommended for inventory)

- List all instances across regions (TSV/JSON): `scripts/list_instances_all_regions.py`
- Query resource usage (CPU/Memory/Network) for one instance: `scripts/query_instance_usage.py`
- Run remote commands via Cloud Assistant (RunCommand): `scripts/run_remote_command.py`
- Summarize instance specs across regions: `scripts/summary_instance_specs.py`
- Summarize instance counts by region (optional status breakdown): `scripts/summary_instances_by_region.py`
- Summarize instance counts by status: `scripts/summary_instances_by_status.py`
- Summarize instance counts by instance type: `scripts/summary_instances_by_instance_type.py`
- Summarize instance counts by VPC: `scripts/summary_instances_by_vpc.py`
- Summarize instance counts by security group: `scripts/summary_instances_by_security_group.py`

### Python SDK: query one instance resource usage

Install dependencies (add CMS SDK):

```bash
python -m pip install alibabacloud_ecs20140526 alibabacloud_cms20190101 alibabacloud_tea_openapi alibabacloud_credentials
```

Example (last 1 hour, 5-minute period):

```bash
python skills/compute/ecs/aliyun-ecs-manage/scripts/query_instance_usage.py \
  --instance-id i-xxxxxxxxxxxxxxxxx \
  --region-id cn-shanghai \
  --hours 1 \
  --period 300 \
  --summary-only \
  --output output/aliyun-ecs-manage/ecs-usage-i-xxxxxxxxxxxxxxxxx-1h.json
```

Recommended default metrics:
- `CPUUtilization`
- `memory_usedutilization`
- `InternetInRate`, `InternetOutRate`
- `IntranetInRate`, `IntranetOutRate`

### Python SDK: run remote command on one ECS instance

Example (`ps -ef`):

```bash
python skills/compute/ecs/aliyun-ecs-manage/scripts/run_remote_command.py \
  --instance-id i-xxxxxxxxxxxxxxxxx \
  --region-id cn-shanghai \
  --command 'ps -ef' \
  --output output/aliyun-ecs-manage/runcommand-i-xxxxxxxxxxxxxxxxx-ps-ef.json
```

Behavior:
- Submit `RunCommand` with `RunShellScript`.
- Poll `DescribeInvocationResults` until final status.
- Decode base64 stdout and save normalized JSON evidence.

### Python SDK: list instances for all regions

```python
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_ecs20140526 import models as ecs_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Ecs20140526Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"ecs.{region_id}.aliyuncs.com",
    )
    return Ecs20140526Client(config)


def list_regions() -> list[str]:
    client = create_client("cn-hangzhou")
    resp = client.describe_regions(ecs_models.DescribeRegionsRequest())
    return [r.region_id for r in resp.body.regions.region]


def list_instances_all_regions():
    for region_id in list_regions():
        client = create_client(region_id)
        req = ecs_models.DescribeInstancesRequest(
            region_id=region_id,
            page_number=1,
            page_size=100,
        )
        resp = client.describe_instances(req)
        print(f"== {region_id} ({resp.body.total_count}) ==")
        for inst in resp.body.instances.instance:
            print(inst.instance_id, inst.instance_name, inst.instance_type, inst.status)


if __name__ == "__main__":
    list_instances_all_regions()
```

### Python SDK: paginated instance listing

```python
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_ecs20140526 import models as ecs_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Ecs20140526Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"ecs.{region_id}.aliyuncs.com",
    )
    return Ecs20140526Client(config)


def list_instances_paged(region_id: str):
    client = create_client(region_id)
    page_number = 1
    page_size = 100
    while True:
        resp = client.describe_instances(ecs_models.DescribeInstancesRequest(
            region_id=region_id,
            page_number=page_number,
            page_size=page_size,
        ))
        for inst in resp.body.instances.instance:
            print(inst.instance_id, inst.instance_name, inst.instance_type, inst.status)
        total = resp.body.total_count
        if page_number * page_size >= total:
            break
        page_number += 1


if __name__ == "__main__":
    list_instances_paged("cn-hangzhou")
```

### Python SDK: list instance types and pricing inputs

```python
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_ecs20140526 import models as ecs_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Ecs20140526Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"ecs.{region_id}.aliyuncs.com",
    )
    return Ecs20140526Client(config)


def list_types(region_id: str, zone_id: str | None = None, instance_type_family: str | None = None):
    client = create_client(region_id)
    req = ecs_models.DescribeInstanceTypesRequest(
        zone_id=zone_id,
        instance_type_family=instance_type_family,
    )
    resp = client.describe_instance_types(req)
    for t in resp.body.instance_types.instance_type:
        print(t.instance_type_id, t.cpu_core_count, t.memory_size)


if __name__ == "__main__":
    list_types("cn-hangzhou", "cn-hangzhou-k")
```

## Common operation mapping

- Instance lifecycle: `RunInstances`, `CreateInstance`, `StartInstance(s)`, `StopInstance(s)`, `RebootInstance(s)`, `DeleteInstance(s)`
- Instance details: `DescribeInstances`, `DescribeInstanceStatus`, `DescribeInstanceAttribute`
- Spec changes: `ModifyInstanceSpec`, `ModifyPrepayInstanceSpec`, `DescribeResourcesModification`
- System disk changes: `ReplaceSystemDisk`, `ResetDisk`
- Data disks: `CreateDisk`, `AttachDisk`, `DetachDisk`, `ResizeDisk`, `DescribeDisks`
- Snapshots: `CreateSnapshot`, `CopySnapshot`, `DescribeSnapshots`, `DeleteSnapshot`
- Images: `CreateImage`, `CopyImage`, `DescribeImages`, `DeleteImage`, `ModifyImageAttribute`
- Security groups: `CreateSecurityGroup`, `AuthorizeSecurityGroup`, `RevokeSecurityGroup`, `DescribeSecurityGroupAttribute`
- Key pairs: `CreateKeyPair`, `ImportKeyPair`, `DescribeKeyPairs`, `DeleteKeyPairs`
- ENI: `CreateNetworkInterface`, `AttachNetworkInterface`, `DetachNetworkInterface`, `DescribeNetworkInterfaces`
- Tags: `TagResources`, `UntagResources`, `ListTagResources`
- Monitoring/events: `DescribeInstancesFullStatus`, `DescribeInstanceHistoryEvents`, `DescribeInstanceMonitorData`

## Query patterns

- List instances: `DescribeInstances` (supports filters such as `VpcId`, `VSwitchId`, `ZoneId`, `SecurityGroupId`, `InstanceIds`)
- Count instances: `DescribeInstances` with `PageSize=1` and read `TotalCount`
- Region discovery: `DescribeRegions` then loop all regions for inventory

## Cloud Assistant (RunCommand) tips

- Instances must be in `Running` state.
- Ensure the Cloud Assistant agent is installed and online.
- Use shell for Linux, PowerShell for Windows.
- Poll results via `DescribeInvocations` and `DescribeInvocationResults`.

See `references/command-assistant.md`.

## AccessKey priority (must follow, align with README)

1) Environment variables: `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`
Region policy: `ALICLOUD_REGION_ID` is an optional default. If unset, decide the most reasonable region for the task; if unclear, ask the user.
2) Shared config file: `~/.alibabacloud/credentials` (region still from env)

### Auth setup (README-aligned)

Environment variables:

```bash
export ALICLOUD_ACCESS_KEY_ID="your-ak"
export ALICLOUD_ACCESS_KEY_SECRET="your-sk"
export ALICLOUD_REGION_ID="cn-hangzhou"
```

Also supported by the Alibaba Cloud SDKs:

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="your-ak"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-sk"
```

Shared config file:

`~/.alibabacloud/credentials`

```ini
[default]
type = access_key
access_key_id = your-ak
access_key_secret = your-sk
```


## API discovery

- Product code: `Ecs`
- Default API version: `2014-05-26`
- Use OpenAPI metadata endpoints to list APIs and get schemas (see references).

## Output policy

If you need to save responses or generated artifacts, write them under:
`output/aliyun-ecs-manage/`

Resource usage query evidence example:
`output/aliyun-ecs-manage/ecs-usage-<instance-id>-<window>.json`

Remote command evidence example:
`output/aliyun-ecs-manage/runcommand-<instance-id>-<name>.json`

## References

- API overview: `references/api_overview.md`
- Endpoints: `references/endpoints.md`
- Cloud Assistant: `references/command-assistant.md`
- DescribeInstances: `references/describe-instances.md`
- Instances: `references/instances.md`
- Disks: `references/disks.md`
- Snapshots: `references/snapshots.md`
- Images: `references/images.md`
- Security groups: `references/security-groups.md`
- Network interfaces: `references/network-interfaces.md`
- Key pairs: `references/keypairs.md`
- Tags: `references/tags.md`
- Monitoring/events: `references/monitoring-events.md`
- Sources: `references/sources.md`
