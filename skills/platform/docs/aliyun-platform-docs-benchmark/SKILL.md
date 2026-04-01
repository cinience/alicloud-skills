---
name: aliyun-platform-docs-benchmark
description: Benchmark similar product documentation and API documentation across Alibaba Cloud, AWS, Azure, GCP, Tencent Cloud, Volcano Engine, and Huawei Cloud. Given one product keyword, auto-discover latest official docs/API links, score quality consistently, and output detailed prioritized improvement recommendations.
version: 1.0.0
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
python skills/platform/docs/aliyun-platform-docs-benchmark/scripts/benchmark_multicloud_docs_api.py --product "<product keyword>"
```

Example:

```bash
python skills/platform/docs/aliyun-platform-docs-benchmark/scripts/benchmark_multicloud_docs_api.py --product "serverless"
```

LLM platform benchmark example (Bailian/Bedrock/Azure OpenAI/Vertex AI/Hunyuan/Ark/Pangu):

```bash
python skills/platform/docs/aliyun-platform-docs-benchmark/scripts/benchmark_multicloud_docs_api.py --product "Bailian" --preset "llm-platform"
```

If `--preset` is omitted, script attempts to auto-match preset based on keyword.

Scoring weights can be switched by profile (see `references/scoring.json`):

```bash
python skills/platform/docs/aliyun-platform-docs-benchmark/scripts/benchmark_multicloud_docs_api.py --product "Bailian" --preset "llm-platform" --scoring-profile "llm-platform"
```

## Optional: pin authoritative links

Auto-discovery may miss pages. For stricter comparison, pass official links manually:

```bash
python skills/platform/docs/aliyun-platform-docs-benchmark/scripts/benchmark_multicloud_docs_api.py \
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

`output/aliyun-platform-docs-benchmark/`

Per run:

- `benchmark_evidence.json`
- `benchmark_report.md`

## Reporting guidance

When answering the user:

1) Show score ranking across all providers.
2) Highlight top gaps (P0/P1/P2) and concrete fix actions.
3) If discovery confidence is low, ask user to provide pinned links and rerun.

## Validation

```bash
mkdir -p output/aliyun-platform-docs-benchmark
for f in skills/platform/docs/aliyun-platform-docs-benchmark/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-platform-docs-benchmark/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-platform-docs-benchmark/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-platform-docs-benchmark/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Prerequisites

- Configure least-privilege Alibaba Cloud credentials before execution.
- Prefer environment variables: `ALICLOUD_ACCESS_KEY_ID`, `ALICLOUD_ACCESS_KEY_SECRET`, optional `ALICLOUD_REGION_ID`.
- If region is unclear, ask the user before running mutating operations.

## References

- Rubric: `references/review-rubric.md`
