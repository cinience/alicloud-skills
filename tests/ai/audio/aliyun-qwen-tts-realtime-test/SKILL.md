---
name: alicloud-ai-audio-tts-realtime-test
description: Minimal realtime TTS smoke test for Model Studio Qwen TTS Realtime.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Goals

- Validate only the minimal request path for this skill.
- If execution fails, record exact error details without guessing parameters.

## Prerequisites

- Prepare authentication and region settings based on the skill instructions.
- Target skill: skills/ai/audio/alicloud-ai-audio-tts-realtime

## Test Steps (Minimal)

1) Open the target skill SKILL.md and choose one minimal input example.
2) Send one minimal request or run the example script.
3) Record request summary, response summary, and success/failure reason.

可执行示例（兼容性探测 + 可选降级）：

```bash
.venv/bin/python skills/ai/audio/alicloud-ai-audio-tts-realtime/scripts/realtime_tts_demo.py \
  --text "realtime test" \
  --fallback
```

Strict mode (CI):

```bash
.venv/bin/python skills/ai/audio/alicloud-ai-audio-tts-realtime/scripts/realtime_tts_demo.py \
  --text "realtime test" \
  --strict
```

Pass criteria:
- Non-strict mode:`realtime_probe.ok=true` 或 `fallback.ok=true`
- 严格模式：`realtime_probe.ok=true`（否则脚本非 0 退出）

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/ai/audio/alicloud-ai-audio-tts-realtime
- Conclusion: pass / fail
- Notes:
