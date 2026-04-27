---
name: alicloud-ai-audio-tts-voice-clone-test
description: Minimal voice cloning TTS smoke test for Model Studio Qwen TTS VC.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Goals

- Validate only the minimal request path for this skill.
- If execution fails, record exact error details without guessing parameters.

## Prerequisites

- Prepare authentication and region settings based on the skill instructions.
- Target skill: skills/ai/audio/alicloud-ai-audio-tts-voice-clone

## Test Steps (Minimal)

1) Open the target skill SKILL.md and choose one minimal input example.
2) Send one minimal request or run the example script.
3) Record request summary, response summary, and success/failure reason.

Executable example:

```bash
.venv/bin/python skills/ai/audio/alicloud-ai-audio-tts-voice-clone/scripts/prepare_voice_clone_request.py \
  --text "voice clone test" \
  --voice-sample "https://example.com/sample.wav"
```

Pass criteria:脚本返回 `{"ok": true, ...}` 且生成 `output/ai-audio-tts-voice-clone/request.json`。

## Result Template

- Date: YYYY-MM-DD
- Skill: skills/ai/audio/alicloud-ai-audio-tts-voice-clone
- Conclusion: pass / fail
- Notes:
