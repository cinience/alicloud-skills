---
name: aliyun-emoji-test
description: Minimal template-driven emoji video smoke test for Model Studio Emoji.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/video/aliyun-emoji`

## Executable Example

```bash
.venv/bin/python skills/ai/video/aliyun-emoji/scripts/prepare_emoji_request.py \
  --image-url "https://example.com/portrait.png" \
  --face-bbox 302,286,610,593 \
  --ext-bbox-face 71,9,840,778 \
  --template-id emoji_001
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/aliyun-emoji/request.json`.

