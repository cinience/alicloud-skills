---
name: aliyun-vpc-manage
description: Use when managing Alibaba Cloud Virtual Private Cloud (VPC) via OpenAPI/SDK, including listing or creating VPCs and VSwitches, querying available zones, deleting VPC resources, managing route tables, and troubleshooting VPC network configurations.
version: 1.0.0
---

Category: service

# Virtual Private Cloud (VPC)

## Validation

```bash
mkdir -p output/aliyun-vpc-manage
for f in skills/network/vpc/aliyun-vpc-manage/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-vpc-manage/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-vpc-manage/validate.txt` is generated.

## Output And Evidence

- Save list/summarize outputs under `output/aliyun-vpc-manage/`.
- Keep command arguments and region scope in each evidence file.

Use Alibaba Cloud OpenAPI (RPC) with official SDKs or OpenAPI Explorer to manage VPC resources.
Prefer the Python SDK for all examples and execution.

## Prerequisites

```bash
pip install alibabacloud_vpc20160428 alibabacloud_tea_openapi alibabacloud_credentials
```

- Prepare AccessKey (RAM user/role with least privilege).
- Choose the correct region and endpoint (public/VPC).
- VPC OpenAPI is RPC style; prefer SDK or OpenAPI Explorer to avoid manual signing.

## API behavior notes (from VPC docs)

- `DescribeVpcs` and `DescribeVSwitches` support pagination via `PageNumber` + `PageSize`.
- `DescribeVpcs` requires `RegionId` in the request.
- `CreateVpc` returns `VpcId` immediately but VPC enters `Pending` status; poll with `DescribeVpcs` until `Available`.
- `CreateVSwitch` requires an existing VPC in `Available` status and a valid `ZoneId`.
- `DeleteVpc` fails if VPC still has VSwitches, security groups, or other resources attached.
- `DeleteVSwitch` fails if VSwitch still has ECS instances or other resources.

## Workflow

1) Confirm region, resource identifiers, and desired action.
2) Find API group and exact operation name in `references/api_overview.md`.
3) Call API with Python SDK (preferred) or OpenAPI Explorer.
4) Verify results with describe/list APIs.
5) If you need repeatable inventory or summaries, use `scripts/` and write outputs under `output/aliyun-vpc-manage/`.

## SDK priority

1) Python SDK (preferred)
2) OpenAPI Explorer
3) Other SDKs (only if Python is not feasible)

### Python SDK quickstart (list VPCs)

Virtual environment is recommended (avoid PEP 668 system install restrictions).

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install alibabacloud_vpc20160428 alibabacloud_tea_openapi alibabacloud_credentials
```

```python
from alibabacloud_vpc20160428.client import Client as Vpc20160428Client
from alibabacloud_vpc20160428 import models as vpc_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Vpc20160428Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"vpc.{region_id}.aliyuncs.com",
    )
    return Vpc20160428Client(config)


def list_vpcs(region_id: str):
    client = create_client(region_id)
    resp = client.describe_vpcs(vpc_models.DescribeVpcsRequest(
        region_id=region_id,
        page_number=1,
        page_size=50,
    ))
    for v in resp.body.vpcs.vpc:
        print(v.vpc_id, v.vpc_name, v.cidr_block, v.status)


if __name__ == "__main__":
    list_vpcs("cn-hangzhou")
```

### Python SDK scripts (recommended for inventory)

- List VPCs in a region: `scripts/list_vpcs.py`
- List VSwitches in a region: `scripts/list_vswitches.py`
- Create a VPC: `scripts/create_vpc.py`
- Create a VSwitch: `scripts/create_vswitch.py`
- Delete a VPC: `scripts/delete_vpc.py`
- Delete a VSwitch: `scripts/delete_vswitch.py`
- Query available zones: `scripts/describe_zones.py`

## VPC 网络规划设计原则

### CIDR 地址规划

- **每个地域的业务 VPC 使用独立的 /16 网段**，避免跨地域互联时 CIDR 冲突。推荐分配方式：

| 地域 | 推荐 CIDR |
|------|-----------|
| cn-hangzhou | 10.1.0.0/16 |
| cn-shanghai | 10.2.0.0/16 |
| ap-southeast-1 | 10.3.0.0/16 |
| cn-beijing | 10.4.0.0/16 |
| 更多地域 | 10.5~254.0.0/16 |

- **不要使用过大的 CIDR**（如 `10.0.0.0/8`），即使 VSwitch 只用了很小一部分。大网段会阻止与其他 `10.x` 段 VPC 通过 CEN 互联。
- **VSwitch 统一使用 /24**（252 可用 IP），对大多数业务足够。如果单可用区需要大量实例，可用 /20（4092 IP）。
- **预留网段间隔**用于未来扩展。如应用层用 0-9，数据库层用 10-19，中间件用 20-29。

### 可用区与高可用

- **生产环境至少覆盖 2~3 个可用区**，每个可用区至少 1 个 VSwitch。
- **应用层和数据层分布在不同可用区**，确保单 AZ 故障时服务不中断。
- 创建 VSwitch 前先用 `scripts/describe_zones.py` 查询可用区列表，不同地域的可用区编号不同。

### VSwitch 分层隔离

按业务功能对 VSwitch 进行分段，便于通过 ACL 和安全组实现网络隔离：

```
10.x.0~9.0/24    → 应用层（Web/API 服务器）
10.x.10~19.0/24  → 数据层（RDS、Redis、MongoDB）
10.x.20~29.0/24  → 中间件（MQ、ES、Nacos）
10.x.30~39.0/24  → 管理层（跳板机、运维工具）
```

### VSwitch 命名规范

推荐格式：`vsw-{region简写}-{可用区}-{用途}`

示例：`vsw-sg-a-app`、`vsw-hz-h-db`、`vsw-sh-e-middleware`

### 跨地域互联（CEN）

- 需要互联的 VPC 的 CIDR **必须不重叠**。
- 自动生成的 VPC（如 FC 组件创建的）通常使用 `10.0.0.0/8`，**不要将其加入 CEN**，否则会与其他地域的 `10.x` 段冲突。
- 业务 VPC 规划时应预先考虑 CEN 互联需求，从一开始就使用不重叠的 /16 网段。

### 常见陷阱

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| CEN 挂载失败，提示 CIDR 冲突 | 两个 VPC 使用了重叠的 CIDR | 新建 VPC 使用不重叠的 /16 网段 |
| DeleteVpc 失败 | VPC 下仍有 VSwitch/安全组/NAT 等资源 | 先删除所有子资源，再删 VPC |
| DeleteVSwitch 失败 | VSwitch 下仍有 ECS/RDS 等实例 | 先释放或迁移实例 |
| 创建 VSwitch 报 ZoneId 无效 | 该可用区不支持或已售罄 | 用 describe_zones.py 查询有效可用区 |
| 默认 VPC 用于生产 | 默认 VPC 网段不可控，且无法与其他 VPC 合理互联 | 生产环境始终新建 VPC，规划好 CIDR |

## Common operation mapping

- VPC lifecycle: `CreateVpc`, `DeleteVpc`, `ModifyVpcAttribute`
- VPC query: `DescribeVpcs`, `DescribeVpcAttribute`
- VSwitch lifecycle: `CreateVSwitch`, `DeleteVSwitch`, `ModifyVSwitchAttribute`
- VSwitch query: `DescribeVSwitches`, `DescribeVSwitchAttributes`
- Route tables: `CreateRouteTable`, `DeleteRouteTable`, `DescribeRouteTables`, `CreateRouteEntry`, `DeleteRouteEntry`
- NAT Gateway: `CreateNatGateway`, `DeleteNatGateway`, `DescribeNatGateways`
- EIP: `AllocateEipAddress`, `AssociateEipAddress`, `UnassociateEipAddress`, `ReleaseEipAddress`, `DescribeEipAddresses`
- Tags: `TagResources`, `UntagResources`, `ListTagResources`

## Query patterns

- List VPCs: `DescribeVpcs` (supports filters: `VpcId`, `VpcName`, `IsDefault`, `ResourceGroupId`)
- List VSwitches: `DescribeVSwitches` (supports filters: `VpcId`, `VSwitchId`, `ZoneId`, `VSwitchName`, `IsDefault`)
- Available zones: use ECS `DescribeZones` API to find valid zones for VSwitch creation

## AccessKey priority (must follow, align with README)

1) Environment variables: `ALIBABACLOUD_ACCESS_KEY_ID` / `ALIBABACLOUD_ACCESS_KEY_SECRET` / `ALIBABACLOUD_REGION_ID`
Region policy: `ALIBABACLOUD_REGION_ID` is an optional default. If unset, decide the most reasonable region for the task; if unclear, ask the user.
2) Shared config file: `~/.alibabacloud/credentials` (region still from env)

### Auth setup (README-aligned)

Environment variables:

```bash
export ALIBABACLOUD_ACCESS_KEY_ID="your-ak"
export ALIBABACLOUD_ACCESS_KEY_SECRET="your-sk"
export ALIBABACLOUD_REGION_ID="cn-hangzhou"
```

Also supported by the Alibaba Cloud SDKs:

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="your-ak"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-sk"
```

Legacy compatibility:

```bash
export ALICLOUD_ACCESS_KEY_ID="your-ak"
export ALICLOUD_ACCESS_KEY_SECRET="your-sk"
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

- Product code: `Vpc`
- Default API version: `2016-04-28`
- Use OpenAPI metadata endpoints to list APIs and get schemas (see references).

## Output policy

If you need to save responses or generated artifacts, write them under:
`output/aliyun-vpc-manage/`

## References

- API overview: `references/api_overview.md`
- Sources: `references/sources.md`
