---
name: alicloud-platform-aliyun-cli-test
description: Minimal smoke test for generic Alibaba Cloud aliyun CLI skill. Validate CLI install, auth profile, and one read-only API call.
version: 1.0.0
---

Category: test

# 通用 aliyun CLI Minimal Viable Test

## Prerequisites

- `aliyun` CLI is installed.
- A valid profile is configured (default `default`).
- GoalsSkill: `skills/platform/cli/alicloud-platform-aliyun-cli/`。

## Test Steps

1) Run version guard script: `python skills/platform/cli/alicloud-platform-aliyun-cli/scripts/ensure_aliyun_cli.py --interval-hours 24`。
2) 执行 `aliyun version`。
3) 执行 `aliyun configure list`。
4) Run one read-only API (example): `aliyun ecs DescribeRegions`。

## Expected Results

- CLI executes and returns version information.
- `configure list` shows valid credential/profile info (or explicit missing hints).
- Read-only API returns JSON (or explicit permission error).
