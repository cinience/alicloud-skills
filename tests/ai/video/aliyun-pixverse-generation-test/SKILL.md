---
name: alicloud-ai-video-aishi-generation-test
description: Minimal PixVerse video generation smoke test for Model Studio Aishi.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/video/alicloud-ai-video-aishi-generation`

## Executable Example

```bash
.venv/bin/python skills/ai/video/alicloud-ai-video-aishi-generation/scripts/prepare_aishi_request.py \
  --model pixverse/pixverse-v5.6-t2v \
  --prompt "A compact robot walks through a rainy neon alley." \
  --size 1280*720 \
  --duration 5
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/alicloud-ai-video-aishi-generation/request.json`.

