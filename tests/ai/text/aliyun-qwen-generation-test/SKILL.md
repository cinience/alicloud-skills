---
name: aliyun-qwen-generation-test
description: Minimal text generation smoke test for Model Studio Qwen text models.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/text/aliyun-qwen-generation`

## Executable Example

```bash
.venv/bin/python skills/ai/text/aliyun-qwen-generation/scripts/prepare_generation_request.py \
  --prompt "Summarize the role of object storage in a media pipeline." \
  --model qwen3.5-plus
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/aliyun-qwen-generation/requests/request.json`.

