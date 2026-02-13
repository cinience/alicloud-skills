---
name: alicloud-platform-docs-api-review
description: Automatically review latest Alibaba Cloud product docs and OpenAPI docs by product name, then output detailed prioritized improvement suggestions with evidence and scoring. Use when user asks to audit product documentation quality, API documentation quality, or wants actionable doc/API optimization recommendations.
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
python skills/platform/docs/alicloud-platform-docs-api-review/scripts/review_product_docs_and_api.py --product "<产品名或产品代码>"
```

Example:

```bash
python skills/platform/docs/alicloud-platform-docs-api-review/scripts/review_product_docs_and_api.py --product "ECS"
```

## Output policy

All generated artifacts must be written under:

`output/alicloud-platform-docs-api-review/`

For each run, the script creates:

- `review_evidence.json`
- `review_report.md`

## Reporting guidance

When answering the user:

1) State resolved product + version first.
2) Summarize the score and the top 3 issues.
3) List P0/P1/P2 recommendations with concrete actions.
4) Provide source links used in the report.

## References

- Review rubric: `references/review-rubric.md`
