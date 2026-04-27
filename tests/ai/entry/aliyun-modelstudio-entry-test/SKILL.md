---
name: aliyun-modelstudio-entry-test
description: Minimal routing smoke test for aliyun-modelstudio-entry entry skill.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Goals

- Validate only the minimal request path for this skill.
- If execution fails, record exact error details without guessing parameters.

## Prerequisites

- Prepare authentication and region settings based on the skill instructions.
- 安装 DashScope SDK：`python -m pip install dashscope`
- 配置 `DASHSCOPE_API_KEY`（建议使用环境变量或 .env）。
- Target skill: skills/ai/entry/aliyun-modelstudio-entry

## Test Steps (Minimal)

1) Open the target skill SKILL.md and choose one minimal input example.
2) Send one minimal request or run the example script.
3) Record request summary, response summary, and success/failure reason.

## 输出建议

- 将结果保存为 `output/aliyun-modelstudio-entry-test-results.md`。

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/ai/entry/aliyun-modelstudio-entry
- Conclusion: pass / fail
- Notes:
