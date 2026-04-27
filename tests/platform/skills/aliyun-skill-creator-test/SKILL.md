---
name: alicloud-skill-creator-test
description: Smoke test for alicloud-skill-creator. Validate repository path conventions, frontmatter quality, script compilation, and README index refresh workflow.
version: 1.0.0
---

Category: test

# ALICLOUD SKILL CREATOR Smoke Test

## Prerequisites

- Target skill path: `skills/platform/skills/alicloud-skill-creator/`
- Python 3

## Test Steps

1) Validate target skill scripts compile:

```bash
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/platform/skills/alicloud-skill-creator \
  --output output/alicloud-skill-creator-test/compile-check.json
```

2) Check frontmatter fields exist in target `SKILL.md`:

- `name`
- `description`

3) Regenerate skill index and confirm new category/path appears:

```bash
scripts/update_skill_index.sh
rg -n "alicloud-skill-creator|platform/skills" README.md README.zh-CN.md README.zh-TW.md
```

4) Save command outputs under `output/alicloud-skill-creator-test/`.

## Pass Criteria

- Compilation check passes (`compile-check.json.status=pass`).
- `SKILL.md` contains required frontmatter.
- README skill index includes `alicloud-skill-creator` with `platform/skills` category.
- Evidence exists in `output/alicloud-skill-creator-test/`.

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/platform/skills/alicloud-skill-creator
- Conclusion: pass / fail
- Notes:
