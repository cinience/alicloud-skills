---
name: alicloud-ai-audio-asr-test
description: Minimal non-realtime ASR smoke test for Model Studio Qwen ASR.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Goals

- 仅验证非实时 ASR 最小请求链路可用。
- If execution fails, record exact error details without guessing parameters.

## Prerequisites

- Prepare authentication and region settings based on the skill instructions.
- Target skill: `skills/ai/audio/alicloud-ai-audio-asr`

## Test Steps (Minimal)

1) 打开对应技能的 `SKILL.md`，选择一个最小输入示例。
2) 运行示例脚本或发起最小请求。
3) Record request summary, response summary, and success/failure reason.

## 推荐最小命令

```bash
python skills/ai/audio/alicloud-ai-audio-asr/scripts/transcribe_audio.py \
  --audio "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3" \
  --model qwen3-asr-flash \
  --print-response
```

## Result Template

- Date: YYYY-MM-DD
- Skill: `skills/ai/audio/alicloud-ai-audio-asr`
- Conclusion: pass / fail
- Notes:
