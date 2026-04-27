---
name: alicloud-ai-multimodal-qwen-vl-test
description: Minimal image-understanding smoke test for Model Studio Qwen VL.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Goals

- Validate only the minimal request path for this skill.
- If execution fails, record exact error details without guessing parameters.

## Prerequisites

- Prepare authentication and region settings based on the skill instructions.
- Target skill: skills/ai/multimodal/alicloud-ai-multimodal-qwen-vl

## Test Steps (Minimal)

1) Open the target skill SKILL.md and choose one minimal input example.
2) Send one minimal request or run the example script.
3) Record request summary, response summary, and success/failure reason.

推荐直接运行：

```bash
python tests/ai/multimodal/alicloud-ai-multimodal-qwen-vl-test/scripts/smoke_test_qwen_vl.py \
  --image output/ai-image-qwen-image/images/vl_test_cat.png
```

Pass criteria:

- 返回 JSON 中 `status=pass`。
- 输出文件 `output/ai-multimodal-qwen-vl/smoke-test/result.json` 存在。
- 结果包含非空 `text`，且 `model` 与请求模型一致或同前缀。

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/ai/multimodal/alicloud-ai-multimodal-qwen-vl
- Conclusion: pass / fail
- Notes:
