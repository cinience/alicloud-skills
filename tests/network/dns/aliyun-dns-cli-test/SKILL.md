---
name: alicloud-network-dns-cli-test
description: Minimal smoke test for Alibaba Cloud DNS CLI skill. Validate aliyun-cli auth and describe-subdomain flow.
version: 1.0.0
---

Category: test

# DNS CLI Minimal Viable Test

## Prerequisites

- `aliyun` CLI is installed and configured.
- AK/SK is configured.
- GoalsSkill: `skills/network/dns/alicloud-network-dns-cli/`。

## Test Steps

1) 执行 `aliyun alidns DescribeSubDomainRecords --DomainName <domain> --SubDomain <sub>`。
2) 若无记录，再执行一次空返回验证。
3) 记录 request id 和返回条目数。

## Expected Results

- 命令可执行，返回 JSON 或明确权限错误。
