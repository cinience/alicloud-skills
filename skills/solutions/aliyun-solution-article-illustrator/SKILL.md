---
name: aliyun-solution-article-illustrator
description: Use when the user needs an end-to-end article illustration workflow in this repository that preserves Type x Style planning, loads article-illustration preferences, recommends Alibaba Cloud image backends, and produces a Markdown article with inserted local image references.
version: 1.0.0
---

Category: solution

# Content Article Illustrator

Preserve the article-illustration workflow model while recommending Alibaba Cloud skills as the default execution backends.

## Two Dimensions

| Dimension | Controls | Examples |
|-----------|----------|----------|
| **Type** | Information structure | infographic, scene, flowchart, comparison, framework, timeline |
| **Style** | Visual aesthetics | notion, warm, minimal, blueprint, watercolor, editorial |

## Validation

```bash
mkdir -p output/aliyun-solution-article-illustrator
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/solutions/aliyun-solution-article-illustrator \
  --output output/aliyun-solution-article-illustrator/compile-check.json
```

Pass criteria: command exits 0 and `output/aliyun-solution-article-illustrator/compile-check.json` is generated with `"status": "pass"`.

## Output And Evidence

- Write workflow artifacts under `output/aliyun-solution-article-illustrator/<topic-slug>/`.
- Save at least: `source.md`, `outline.md`, one prompt file, generated images, `article.with-images.md`, and `delivery-report.md`.
- Keep evidence for prompt-before-generation ordering and any edit pass used during repair.

## Prerequisites

- A source Markdown article.
- A generation backend that satisfies `references/backend-contract.md`.
- If you want repository-default behavior, prefer `aliyun-modelstudio-qwen-image` and `aliyun-modelstudio-qwen-image-edit`.
- Optional `EXTEND.md` preferences at project or user scope.

## Workflow

1. Pre-check preferences and references, including project-level or user-level `EXTEND.md`.
2. Analyze the source Markdown article and identify candidate illustration positions.
3. Confirm settings in one batch: Type, Density, Style, optional Language, and output size.
4. Choose or recommend a backend and build `outline.md`.
5. Save prompt files before any generation step.
6. Use the selected generation backend for first-pass images. Recommend `aliyun-modelstudio-qwen-image` by default.
7. If needed, use the selected edit backend for one repair pass per image. Recommend `aliyun-modelstudio-qwen-image-edit` by default.
8. Write `article.with-images.md` with relative `images/...` Markdown links.
9. Save evidence and produce `delivery-report.md`.

## Minimal Executable Run

```bash
python3 skills/solutions/aliyun-solution-article-illustrator/scripts/run_workflow.py \
  --source path/to/article.md \
  --output-dir output/aliyun-solution-article-illustrator/example-run \
  --generation-backend mock
```

## State Gates

- `drafted`: source article and initial outline exist
- `confirmed`: user settings, preferences, and backend choice are confirmed
- `generated`: prompt files and first-pass images exist
- `validated`: artifact structure and Markdown insertion pass checks
- `delivered`: final article and report are written

## References

- Detailed workflow: `references/workflow.md`
- Usage examples: `references/usage.md`
- Style system: `references/styles.md`
- Backend contract: `references/backend-contract.md`
- Prompt construction rules: `references/prompt-construction.md`
- Output contract: `references/output-spec.md`
- Validation and test expectations: `references/test-plan.md`
- Config setup: `references/config/first-time-setup.md`
- Preferences schema: `references/config/preferences-schema.md`
- Source references: `references/sources.md`
- Helper scripts: `scripts/load_preferences.py`, `scripts/validate_inputs.py`, `scripts/build_outline.py`, `scripts/collect_evidence.py`
