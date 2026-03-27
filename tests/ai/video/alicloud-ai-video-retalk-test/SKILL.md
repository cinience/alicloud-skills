---
name: alicloud-ai-video-retalk-test
description: Minimal lip-sync replacement smoke test for Model Studio VideoRetalk.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/video/alicloud-ai-video-retalk`

## Executable Example

```bash
.venv/bin/python skills/ai/video/alicloud-ai-video-retalk/scripts/prepare_retalk_request.py \
  --video-url "https://example.com/talking-head.mp4" \
  --audio-url "https://example.com/new-voice.wav" \
  --video-extension
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/alicloud-ai-video-retalk/request.json`.

