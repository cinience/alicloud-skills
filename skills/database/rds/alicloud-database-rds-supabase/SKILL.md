---
name: alicloud-database-rds-supabase
description: Manage Alibaba Cloud RDS Supabase (RDS AI Service 2025-05-07) via OpenAPI. Use for creating, starting/stopping/restarting instances, resetting passwords, querying endpoints/auth/storage, configuring auth/RAG/SSL/IP whitelist, and listing instance details or conversations.
---

Category: service

# 阿里云 RDS Supabase（RDS AI 服务 2025-05-07）

使用 RDS AI 服务 OpenAPI 管理 RDS Supabase 应用实例及相关配置，包括实例生命周期、认证、存储、RAG、白名单与 SSL。

## 前置要求

- 使用 RAM 用户/角色最小权限的 AccessKey，优先从环境变量读取 AK/SK。
- OpenAPI 为 RPC 签名机制，优先使用官方 SDK 或 OpenAPI Explorer。

## 工作流

1) 明确资源类型：实例 / 认证 / 存储 / RAG / 安全配置。  
2) 在 `references/api_overview.md` 中定位接口。  
3) 选择调用方式（SDK / OpenAPI Explorer / 自签名）。  
4) 变更后使用查询接口确认状态与配置。  

## AccessKey 读取优先级（必须遵循）

1) 环境变量（优先）：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`
Region 规则：`ALICLOUD_REGION_ID` 作为可选默认值；若未设置，执行时应选择最合理的 Region，无法判断则主动询问。  
2) 标准配置文件：`~/.alibabacloud/credentials`

## Region 默认策略

- 如未指定 Region，优先选择最合理 Region；无法判断则询问用户。  
- 仅在明确需要或用户同意时，才进行全地域查询（先调 `ListRegions`，再对每个 Region 调用查询接口）。  
- 若用户提供 Region，则只查询指定 Region。  

## 常见操作映射

- 实例：`CreateAppInstance` / `DeleteAppInstance` / `StartInstance` / `StopInstance` / `RestartInstance`
- 连接与认证：`DescribeInstanceEndpoints` / `DescribeInstanceAuthInfo` / `ModifyInstanceAuthConfig`
- 存储：`DescribeInstanceStorageConfig` / `ModifyInstanceStorageConfig`
- 安全：`ModifyInstanceIpWhitelist` / `DescribeInstanceIpWhitelist` / `ModifyInstanceSSL` / `DescribeInstanceSSL`
- RAG：`ModifyInstanceRAGConfig` / `DescribeInstanceRAGConfig`

## 选择问题（不确定时提问）

1. 目标实例 ID 是什么？所在地域？
2. 要做的是实例生命周期，还是配置变更（认证/存储/RAG/白名单/SSL）？
3. 是否需要批量操作或先查询现有配置？

## Output Policy

若需保存结果或响应，写入：
`output/database-rds-supabase/`

## References

- API 总览与接口分组：`references/api_overview.md`
- 核心接口参数速查：`references/api_reference.md`
- 全地域查询示例：`references/query-examples.md`
- 官方文档来源清单：`references/sources.md`
