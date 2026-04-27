---
name: alicloud-ai-video-wan-r2v-test
description: Minimal reference-to-video smoke test for Model Studio Wan R2V.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Goals

- Validate only the minimal request path for this skill.
- If execution fails, record exact error details without guessing parameters.

## Prerequisites

- Prepare authentication and region settings based on the skill instructions.
- Target skill: skills/ai/video/alicloud-ai-video-wan-r2v

## Test Steps (Minimal)

1) Open the target skill SKILL.md and choose one minimal input example.
2) Send one minimal request or run the example script.
3) Record request summary, response summary, and success/failure reason.

Executable example:

```bash
.venv/bin/python skills/ai/video/alicloud-ai-video-wan-r2v/scripts/prepare_r2v_request.py \
  --prompt "Generate a short montage" \
  --reference-video "https://example.com/ref.mp4"
```

Pass criteria:脚本返回 `{"ok": true, ...}` 且生成 `output/ai-video-wan-r2v/request.json`。

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/ai/video/alicloud-ai-video-wan-r2v
- Conclusion: pass / fail
- Notes:
