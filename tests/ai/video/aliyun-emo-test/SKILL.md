---
name: aliyun-emo-test
description: Minimal expressive portrait smoke test for Model Studio EMO.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/video/aliyun-emo`

## Executable Example

```bash
.venv/bin/python skills/ai/video/aliyun-emo/scripts/prepare_emo_request.py \
  --image-url "https://example.com/portrait.png" \
  --audio-url "https://example.com/speech.mp3" \
  --face-bbox 302,286,610,593 \
  --ext-bbox 71,9,840,778 \
  --style-level active
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/aliyun-emo/request.json`.

