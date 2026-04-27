---
name: alicloud-security-cloudfw-test
description: Minimal smoke test for Cloud Firewall skill. Validate read-only inventory query path.
version: 1.0.0
---

Category: test

# CloudFW Minimal Viable Test

## Prerequisites

- AK/SK and region are configured.
- GoalsSkill: `skills/security/firewall/alicloud-security-cloudfw/`。

## Test Steps

1) 先跑元数据 API 列表脚本。
2) 选择一个只读列表/详情 API 执行。
3) 记录请求摘要和响应摘要。

## Expected Results

- 可拿到资源列表或明确无权限提示。
