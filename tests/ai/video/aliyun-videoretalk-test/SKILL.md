---
name: aliyun-videoretalk-test
description: Minimal lip-sync replacement smoke test for Model Studio VideoRetalk.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/video/aliyun-videoretalk`

## Executable Example

```bash
.venv/bin/python skills/ai/video/aliyun-videoretalk/scripts/prepare_retalk_request.py \
  --video-url "https://example.com/talking-head.mp4" \
  --audio-url "https://example.com/new-voice.wav" \
  --video-extension
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/aliyun-videoretalk/request.json`.

