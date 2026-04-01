---
name: aliyun-rds-supabase
description: Manage Alibaba Cloud RDS Supabase (RDS AI Service 2025-05-07) via OpenAPI. Use for creating, starting/stopping/restarting instances, resetting passwords, querying endpoints/auth/storage, configuring auth/RAG/SSL/IP whitelist, and listing instance details or conversations.
version: 1.0.0
---

Category: service

# Alibaba Cloud RDS Supabase (RDS AI Service 2025-05-07)

Manage RDS Supabase app instances and related configurations via RDS AI Service OpenAPI, including lifecycle, auth, storage, RAG, IP whitelist, and SSL.

## Prerequisites

- Use least-privilege RAM user/role AccessKey and prefer environment variables for AK/SK.
- OpenAPI uses RPC signing; prefer official SDKs or OpenAPI Explorer.

## Workflow

1) Confirm resource type: instance / auth / storage / RAG / security configuration.  
2) Locate operations in `references/api_overview.md`.  
3) Choose invocation method (SDK / OpenAPI Explorer / custom signing).  
4) After changes, verify state and configuration with query APIs.  

## AccessKey Priority (Required)

1) Environment variables (preferred):`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`
Region policy: `ALICLOUD_REGION_ID` is optional default; if unset choose the most reasonable region and ask when unclear.  
2) Standard credentials file:`~/.alibabacloud/credentials`

## Default Region Strategy

- If region is not specified, choose the most reasonable region; ask the user when unclear.  
- Only run all-region queries when explicitly needed or user-approved (call `ListRegions` first, then query each region).  
- If user provides region, query only that region.  

## Common Operation Map

- Instance:`CreateAppInstance` / `DeleteAppInstance` / `StartInstance` / `StopInstance` / `RestartInstance`
- Connectivity and auth:`DescribeInstanceEndpoints` / `DescribeInstanceAuthInfo` / `ModifyInstanceAuthConfig`
- Storage:`DescribeInstanceStorageConfig` / `ModifyInstanceStorageConfig`
- Security:`ModifyInstanceIpWhitelist` / `DescribeInstanceIpWhitelist` / `ModifyInstanceSSL` / `DescribeInstanceSSL`
- RAG：`ModifyInstanceRAGConfig` / `DescribeInstanceRAGConfig`

## Clarifying questions (ask when uncertain)

1. What is the target instance ID and region?
2. Is this instance lifecycle management or configuration changes (auth/storage/RAG/IP whitelist/SSL)?
3. Do you need batch operations or an initial state query first?

## Output Policy

If you need to save results or responses, write to:
`output/database-rds-supabase/`

## Validation

```bash
mkdir -p output/aliyun-rds-supabase
echo "validation_placeholder" > output/aliyun-rds-supabase/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-rds-supabase/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-rds-supabase/`.
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
- Core API parameter quick reference:`references/api_reference.md`
- All-region query examples:`references/query-examples.md`
- Official source list:`references/sources.md`
