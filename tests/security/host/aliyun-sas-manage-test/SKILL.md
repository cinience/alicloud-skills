---
name: alicloud-security-center-sas-test
description: Minimal smoke test for Security Center SAS skill. Validate read-only query flow.
version: 1.0.0
---

Category: test

# SAS Minimal Viable Test

## Prerequisites

- AK/SK and region are configured.
- GoalsSkill: `skills/security/host/alicloud-security-center-sas/`。

## Test Steps

1) 获取 SAS 的 API 列表。
2) 执行一个只读查询 API。
3) 记录成功/失败及错误码。

## Expected Results

- 请求链路可达，返回可解析 JSON。
