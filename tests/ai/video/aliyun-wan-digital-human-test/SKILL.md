---
name: aliyun-wan-digital-human-test
description: Minimal digital-human smoke test for Model Studio wan2.2-s2v.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/video/aliyun-wan-digital-human`

## Executable Example

```bash
.venv/bin/python skills/ai/video/aliyun-wan-digital-human/scripts/prepare_digital_human_request.py \
  --image-url "https://example.com/anchor.png" \
  --audio-url "https://example.com/voice.mp3" \
  --resolution 720P \
  --scenario talk
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/aliyun-wan-digital-human/request.json`.

