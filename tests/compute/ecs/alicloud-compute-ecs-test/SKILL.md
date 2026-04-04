---
name: alicloud-compute-ecs-test
description: Minimal smoke test for ECS skill. Validate auth, region reachability, and DescribeInstances query path.
version: 1.0.0
---

Category: test

# ECS Minimal Viable Test

## Prerequisites

- 已配置 `ALIBABACLOUD_ACCESS_KEY_ID` / `ALIBABACLOUD_ACCESS_KEY_SECRET` / `ALIBABACLOUD_REGION_ID`。
- GoalsSkill: `skills/compute/ecs/alicloud-compute-ecs/`。

## Test Steps

1) 执行最小查询：`DescribeRegions`。
2) 在一个 region 执行 `DescribeInstances`（`PageSize=1`）。
3) 记录请求参数、返回总数、是否成功。

## Expected Results

- API 可达，返回结构正常。
- 无实例时返回空列表，不应报鉴权错误。
