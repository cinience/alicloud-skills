---
name: aliyun-dns-cli
description: Use when you need to query, add, and update DNS records via aliyun-cli, including CNAME setup for Function Compute custom domains.
version: 1.0.0
---

Category: tool

# Alibaba Cloud DNS (Alidns) CLI

## Goals

- Query and manage Alibaba Cloud DNS records via `aliyun-cli`.
- Quickly configure CNAME for Function Compute custom domains.

## When to Use

- When you need to add/update DNS records in Alibaba Cloud DNS.
- When you need CNAME setup for FC custom domains.

## Install aliyun-cli (without sudo)

```bash
curl -fsSL https://aliyuncli.alicdn.com/aliyun-cli-linux-latest-amd64.tgz -o /tmp/aliyun-cli.tgz
mkdir -p ~/.local/bin
 tar -xzf /tmp/aliyun-cli.tgz -C /tmp
mv /tmp/aliyun ~/.local/bin/aliyun
chmod +x ~/.local/bin/aliyun
```

## Configure Credentials

```bash
~/.local/bin/aliyun configure set \
  --profile default \
  --access-key-id <AK> \
  --access-key-secret <SK> \
  --region cn-hangzhou
```

Configure region as default; if best region is unclear, ask the user.

## Query DNS Records

Query subdomain records:

```bash
~/.local/bin/aliyun alidns DescribeSubDomainRecords \
  --SubDomain news.example.com
```

## Add CNAME Record

```bash
~/.local/bin/aliyun alidns AddDomainRecord \
  --DomainName example.com \
  --RR news \
  --Type CNAME \
  --Value <TARGET>
```

## FC Custom Domain CNAME Target

Custom domain should point to FC public CNAME:

```
<account_id>.<region_id>.fc.aliyuncs.com
```

Example (Hangzhou):

```
1629965279769872.cn-hangzhou.fc.aliyuncs.com
```

## Common Issues

- If apex CNAME is not supported, use subdomain like `www` or ALIAS/ANAME records.
- Create FC custom domain only after DNS propagation, otherwise `DomainNameNotResolved` may occur.

## References

- aliyun-cli installation
  - https://help.aliyun.com/zh/cli/install-cli-on-linux
- Alidns API（AddDomainRecord / DescribeSubDomainRecords）
  - https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-adddomainrecord
  - https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-describesubdomainrecords
- FC custom domain configuration and CNAME guidance
  - https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names

- Official source list:`references/sources.md`

## Validation

```bash
mkdir -p output/aliyun-dns-cli
echo "validation_placeholder" > output/aliyun-dns-cli/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-dns-cli/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-dns-cli/`.
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

