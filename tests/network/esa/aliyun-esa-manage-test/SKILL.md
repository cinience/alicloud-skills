---
name: alicloud-network-esa-test
description: Minimal smoke test for Alibaba Cloud ESA skill. Validate OpenAPI metadata discovery and API inventory generation for product ESA.
version: 1.0.0
---

Category: test

# ESA Minimal Viable Test

## Prerequisites

- Network access is available.
- GoalsSkill: `skills/network/esa/alicloud-network-esa/`。

## Test Steps

1) 执行：

```bash
python skills/network/esa/alicloud-network-esa/scripts/list_openapi_meta_apis.py \
  --product-code ESA \
  --version 2024-09-10 \
  --output-dir output/alicloud-network-esa-test
```

2) 检查输出文件是否存在：
- `output/alicloud-network-esa-test/ESA_2024-09-10_api_docs.json`
- `output/alicloud-network-esa-test/ESA_2024-09-10_api_list.md`

## Expected Results

- Command execution succeeds.
- API list output file contains multiple API names (non-empty).
