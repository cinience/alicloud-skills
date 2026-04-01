---
name: aliyun-platform-docs-review
description: Use when reviewing latest Alibaba Cloud product docs and OpenAPI docs by product name, then output detailed prioritized improvement suggestions with evidence and scoring. Use when user asks to audit product documentation quality, API documentation quality, or wants actionable doc/API optimization recommendations.
version: 1.0.0
---

# Alibaba Cloud Product Docs + API Docs Reviewer

Use this skill when the user gives a product name and asks for an end-to-end documentation/API quality review.

## What this skill does

1) Resolve product from latest OpenAPI metadata.
2) Fetch latest API docs for default version.
3) Discover product/help-doc links from official product page.
4) Produce a structured review report with:
- score
- evidence
- prioritized suggestions (P0/P1/P2)

## Workflow

Run the bundled script:

```bash
python skills/platform/docs/aliyun-platform-docs-review/scripts/review_product_docs_and_api.py --product "<product name or product code>"
```

Example:

```bash
python skills/platform/docs/aliyun-platform-docs-review/scripts/review_product_docs_and_api.py --product "ECS"
```

## Output policy

All generated artifacts must be written under:

`output/aliyun-platform-docs-review/`

For each run, the script creates:

- `review_evidence.json`
- `review_report.md`

## Reporting guidance

When answering the user:

1) State resolved product + version first.
2) Summarize the score and the top 3 issues.
3) List P0/P1/P2 recommendations with concrete actions.
4) Provide source links used in the report.

## Validation

```bash
mkdir -p output/aliyun-platform-docs-review
for f in skills/platform/docs/aliyun-platform-docs-review/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-platform-docs-review/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-platform-docs-review/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-platform-docs-review/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Prerequisites

- Configure least-privilege Alibaba Cloud credentials before execution.
- Prefer environment variables: `ALICLOUD_ACCESS_KEY_ID`, `ALICLOUD_ACCESS_KEY_SECRET`, optional `ALICLOUD_REGION_ID`.
- If region is unclear, ask the user before running mutating operations.

## References

- Review rubric: `references/review-rubric.md`
