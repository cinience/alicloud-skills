---
name: alicloud-ai-video-liveportrait-test
description: Minimal lightweight portrait animation smoke test for Model Studio LivePortrait.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/video/alicloud-ai-video-liveportrait`

## Executable Example

```bash
.venv/bin/python skills/ai/video/alicloud-ai-video-liveportrait/scripts/prepare_liveportrait_request.py \
  --image-url "https://example.com/portrait.png" \
  --audio-url "https://example.com/speech.mp3" \
  --template-id calm \
  --video-fps 24 \
  --paste-back
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/alicloud-ai-video-liveportrait/request.json`.

