---
name: alicloud-platform-openapi-product-api-discovery-test
description: Minimal smoke test for product API discovery skill. Validate product pull, merge, and one metadata fetch.
version: 1.0.0
---

Category: test

# OpenAPI 产品发现Minimal Viable Test

## Prerequisites

- AK/SK is configured.
- GoalsSkill: `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery/`。

## Test Steps

1) 运行一个产品源抓取脚本。
2) 运行合并脚本。
3) 限制 `OPENAPI_META_MAX_PRODUCTS=1` 执行元数据抓取。

## Expected Results

- `output/product-scan/` 下产生最小结果文件。
