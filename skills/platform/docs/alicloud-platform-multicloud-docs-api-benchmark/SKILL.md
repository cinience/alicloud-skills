---
name: alicloud-platform-multicloud-docs-api-benchmark
description: Benchmark similar product documentation and API documentation across Alibaba Cloud, AWS, Azure, GCP, Tencent Cloud, Volcano Engine, and Huawei Cloud. Given one product keyword, auto-discover latest official docs/API links, score quality consistently, and output detailed prioritized improvement recommendations.
---

# Multi-Cloud Product Docs/API Benchmark

Use this skill when the user wants cross-cloud documentation/API comparison for similar products.

## Supported clouds

- Alibaba Cloud
- AWS
- Azure
- GCP
- Tencent Cloud
- Volcano Engine
- Huawei Cloud

## Data source policy

- `L0` (highest): user-pinned official links via `--<provider>-links`
- `L1`: machine-readable official metadata/source
  - GCP: Discovery API
  - AWS: API Models repository
  - Azure: REST API Specs repository
- `L2`: official-domain constrained web discovery fallback
- `L3`: insufficient discovery (low confidence)

## Workflow

Run the benchmark script:

```bash
python skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/scripts/benchmark_multicloud_docs_api.py --product "<产品关键词>"
```

Example:

```bash
python skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/scripts/benchmark_multicloud_docs_api.py --product "serverless"
```

LLM 平台横评示例（百炼/Bedrock/Azure OpenAI/Vertex AI/混元/方舟/盘古）：

```bash
python skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/scripts/benchmark_multicloud_docs_api.py --product "百炼" --preset "llm-platform"
```

如不传 `--preset`，脚本会根据关键词自动尝试匹配预设。

评分权重可通过 profile 切换（见 `references/scoring.json`）：

```bash
python skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/scripts/benchmark_multicloud_docs_api.py --product "百炼" --preset "llm-platform" --scoring-profile "llm-platform"
```

## Optional: pin authoritative links

Auto-discovery may miss pages. For stricter comparison, pass official links manually:

```bash
python skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/scripts/benchmark_multicloud_docs_api.py \
  --product "object storage" \
  --aws-links "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html" \
  --azure-links "https://learn.microsoft.com/azure/storage/blobs/"
```

Available manual flags:

- `--alicloud-links`
- `--aws-links`
- `--azure-links`
- `--gcp-links`
- `--tencent-links`
- `--volcengine-links`
- `--huawei-links`

Each flag accepts comma-separated URLs.

## Output policy

All artifacts must be written under:

`output/alicloud-platform-multicloud-docs-api-benchmark/`

Per run:

- `benchmark_evidence.json`
- `benchmark_report.md`

## Reporting guidance

When answering the user:

1) Show score ranking across all providers.
2) Highlight top gaps (P0/P1/P2) and concrete fix actions.
3) If discovery confidence is low, ask user to provide pinned links and rerun.

## References

- Rubric: `references/review-rubric.md`
