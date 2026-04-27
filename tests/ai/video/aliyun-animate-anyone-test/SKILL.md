---
name: alicloud-ai-video-animate-anyone-test
description: Minimal motion-transfer smoke test for Model Studio AnimateAnyone.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/video/alicloud-ai-video-animate-anyone`

## Executable Example

```bash
.venv/bin/python skills/ai/video/alicloud-ai-video-animate-anyone/scripts/prepare_animate_anyone_request.py \
  --image-url "https://example.com/dancer.png" \
  --template-id "tmpl_xxx" \
  --use-ref-img-bg
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/alicloud-ai-video-animate-anyone/request.json`.

