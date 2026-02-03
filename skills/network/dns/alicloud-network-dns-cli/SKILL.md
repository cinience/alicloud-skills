---
name: alicloud-network-dns-cli
description: Alibaba Cloud DNS (Alidns) CLI skill. Use to query, add, and update DNS records via aliyun-cli, including CNAME setup for Function Compute custom domains.
---

Category: tool

# 阿里云 DNS（Alidns）CLI

## 目标

- 通过 `aliyun-cli` 查询与管理阿里云 DNS 解析记录。
- 快速为函数计算自定义域名配置 CNAME。

## 何时使用

- 需要在阿里云 DNS 中新增或修改解析记录。
- 需要为 FC 自定义域名完成 CNAME 解析。

## 安装 aliyun-cli（无 sudo 方式）

```bash
curl -fsSL https://aliyuncli.alicdn.com/aliyun-cli-linux-latest-amd64.tgz -o /tmp/aliyun-cli.tgz
mkdir -p ~/.local/bin
 tar -xzf /tmp/aliyun-cli.tgz -C /tmp
mv /tmp/aliyun ~/.local/bin/aliyun
chmod +x ~/.local/bin/aliyun
```

## 配置凭证

```bash
~/.local/bin/aliyun configure set \
  --profile default \
  --access-key-id <AK> \
  --access-key-secret <SK> \
  --region cn-hangzhou
```

Region 作为默认值配置；若不确定最合适的 Region，执行时应询问用户。

## 查询解析记录

查询子域名记录：

```bash
~/.local/bin/aliyun alidns DescribeSubDomainRecords \
  --SubDomain news.example.com
```

## 新增 CNAME 记录

```bash
~/.local/bin/aliyun alidns AddDomainRecord \
  --DomainName example.com \
  --RR news \
  --Type CNAME \
  --Value <TARGET>
```

## FC 自定义域名 CNAME 目标

自定义域名需要指向 FC 公网 CNAME：

```
<account_id>.<region_id>.fc.aliyuncs.com
```

示例（杭州）：

```
1629965279769872.cn-hangzhou.fc.aliyuncs.com
```

## 常见问题

- 根域名 CNAME 不被 DNS 服务商支持时，使用 `www` 等子域名或 ALIAS/ANAME 记录。
- 解析生效后再创建 FC 自定义域名，否则会触发 `DomainNameNotResolved`。

## 参考

- aliyun-cli 安装
  - https://help.aliyun.com/zh/cli/install-cli-on-linux
- Alidns API（AddDomainRecord / DescribeSubDomainRecords）
  - https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-adddomainrecord
  - https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-describesubdomainrecords
- FC 自定义域名配置与 CNAME 说明
  - https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names

- 官方文档来源清单：`references/sources.md`
