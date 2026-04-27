---
name: alicloud-ai-image-qwen-image-edit-test
description: Minimal image editing smoke test for Model Studio Qwen Image Edit.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Goals

- Validate only the minimal request path for this skill.
- If execution fails, record exact error details without guessing parameters.

## Prerequisites

- Prepare authentication and region settings based on the skill instructions.
- Target skill: skills/ai/image/alicloud-ai-image-qwen-image-edit

## Test Steps (Minimal)

1) Open the target skill SKILL.md and choose one minimal input example.
2) Send one minimal request or run the example script.
3) Record request summary, response summary, and success/failure reason.

Executable example:

```bash
.venv/bin/python skills/ai/image/alicloud-ai-image-qwen-image-edit/scripts/prepare_edit_request.py \
  --prompt "Replace background with sunrise" \
  --image "https://example.com/input.png"
```

Pass criteria:脚本返回 `{"ok": true, ...}` 且生成 `output/ai-image-qwen-image-edit/request.json`。

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/ai/image/alicloud-ai-image-qwen-image-edit
- Conclusion: pass / fail
- Notes:
