---
name: alicloud-compute-swas-open
description: Manage Alibaba Cloud Simple Application Server (SWAS OpenAPI 2020-06-01) resources end-to-end. Use for querying instances, starting/stopping/rebooting, executing commands (cloud assistant), managing disks/snapshots/images, firewall rules/templates, key pairs, tags, monitoring, and lightweight database operations.
---

Category: service

# 轻量应用服务器（SWAS-OPEN 2020-06-01）

使用 SWAS-OPEN OpenAPI 管控轻量应用服务器的全量资源：实例、磁盘、快照、镜像、密钥对、防火墙、命令助手、监控、标签、轻量数据库等。

## 前置要求

- 准备 AccessKey（建议 RAM 用户/角色最小权限）。
- 选择正确 Region 并使用对应接入点（公网/VPC）。`ALICLOUD_REGION_ID` 可作为默认 Region；未设置时可选择最合理 Region，无法判断则询问用户。
- 该产品 OpenAPI 为 RPC 签名风格，优先使用 Python SDK 或 OpenAPI Explorer，避免手写签名。

## SDK 优先级

1) Python SDK（优先）
2) OpenAPI Explorer
3) 其他 SDK

### Python SDK 快速查询（实例 ID / IP / 规格）

推荐使用虚拟环境（避免 PEP 668 的系统安装限制）。

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

### Python SDK scripts（推荐用于清单与统计）

- 全地域实例清单（TSV/JSON）：`scripts/list_instances_all_regions.py`
- 按套餐统计实例数：`scripts/summary_instances_by_plan.py`
- 按状态统计实例数：`scripts/summary_instances_by_status.py`
- 修复 SSH 免密（支持自定义端口）：`scripts/fix_ssh_access.py`
- 获取实例当前 SSH 端口：`scripts/get_ssh_port.py`

## CLI 注意事项

- `aliyun` CLI 可能没有 `swas-open` 作为产品名；优先使用 Python SDK。
  如必须用 CLI，请先通过 OpenAPI Explorer 生成调用示例，再迁移到 CLI。

## 工作流

1) 明确资源类型与 Region（实例/磁盘/快照/镜像/防火墙/命令/数据库/标签）。  
2) 在 `references/api_overview.md` 中确定 API 组与具体接口。  
3) 选择调用方式（Python SDK / OpenAPI Explorer / 其他 SDK）。  
4) 执行变更后，用查询接口校验状态或结果。  

## 常见操作映射

- 实例查询/启动/停止/重启：`ListInstances`、`StartInstance(s)`、`StopInstance(s)`、`RebootInstance(s)`  
- 执行命令：`RunCommand` 或 `CreateCommand` + `InvokeCommand`，结果用 `DescribeInvocations`/`DescribeInvocationResult`  
- 防火墙：`ListFirewallRules`/`CreateFirewallRule(s)`/`ModifyFirewallRule`/`EnableFirewallRule`/`DisableFirewallRule`  
- 快照/磁盘/镜像：`CreateSnapshot`、`ResetDisk`、`CreateCustomImage` 等  

## 命令助手执行提示

- 目标实例必须为运行中（Running）。
- 需要安装云助手 Agent（可通过 `InstallCloudAssistant` 安装）。
- PowerShell 命令需确保 Windows 实例已配置 PowerShell 模块。
- 执行后用 `DescribeInvocations` 或 `DescribeInvocationResult` 取回结果与状态。

详见 `references/command-assistant.md`。

## 选择问题（不确定时提问）

1. 目标 Region 是什么？是否需要 VPC 接入点？
2. 目标实例 ID 列表是什么？实例当前状态是否为 Running？
3. 要执行的命令内容/脚本类型/超时时间？Linux 还是 Windows？
4. 是否需要批量操作或定时执行？

## Output Policy

若需保存结果或响应，写入：
`output/compute-swas-open/`

## References

- API 总览与接口分组：`references/api_overview.md`
- 接入点与集成方式：`references/endpoints.md`
- 命令助手要点：`references/command-assistant.md`
- 官方文档来源清单：`references/sources.md`
