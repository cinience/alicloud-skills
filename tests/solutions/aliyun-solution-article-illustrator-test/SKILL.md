---
name: aliyun-solution-article-illustrator-test
description: Smoke test for aliyun-solution-article-illustrator. Validate solution-skill structure, compatibility-oriented documentation, prompt-before-image workflow, backend recommendation policy, and final Markdown output artifacts.
version: 1.0.0
---

Category: test

# Content Article Illustrator Smoke Test

## Prerequisites

- Target skill path: `skills/solutions/aliyun-solution-article-illustrator/`
- Python 3

## Test Steps

1) Compile helper scripts:

```bash
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/solutions/aliyun-solution-article-illustrator \
  --output output/aliyun-solution-article-illustrator-test/compile-check.json
```

2) Run the executable smoke test:

```bash
python3 tests/solutions/aliyun-solution-article-illustrator-test/scripts/smoke_test_article_illustrator.py \
  --output output/aliyun-solution-article-illustrator-test/smoke-test-result.json
```

3) Save command outputs under `output/aliyun-solution-article-illustrator-test/`.

## Pass Criteria

- `SKILL.md` contains valid frontmatter.
- Helper scripts compile successfully.
- `load_preferences.py` honors project-over-user fallback.
- `load_preferences.py` captures watermark, output-dir, and custom style names from project preferences.
- References document Type and Style as separate axes.
- Style docs include a Type x Style compatibility matrix and auto-selection guidance.
- Backend contract documents recommendation without hard-binding.
- Prompt docs and generated prompt files use structured sections such as `ZONES`, `LABELS`, `COLORS`, and `ASPECT`.
- Workflow and prompt docs explain `direct`, `style`, and `palette` reference usage.
- `run_workflow.py` executes the mock backend flow and writes workflow evidence.
- Prompt files exist before generated images.
- Final `article.with-images.md` uses relative `images/...` links.
- Evidence exists under `output/aliyun-solution-article-illustrator-test/`.

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/solutions/aliyun-solution-article-illustrator
- Conclusion: pass / fail
- Notes:
