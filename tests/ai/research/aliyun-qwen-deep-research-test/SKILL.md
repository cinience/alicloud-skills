---
name: alicloud-ai-research-qwen-deep-research-test
description: Minimal deep-research smoke test for Model Studio Qwen Deep Research.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/research/alicloud-ai-research-qwen-deep-research`

## Executable Example

```bash
.venv/bin/python skills/ai/research/alicloud-ai-research-qwen-deep-research/scripts/prepare_deep_research_request.py \
  --topic "Compare speech recognition options for meeting transcription." \
  --disable-feedback
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/alicloud-ai-research-qwen-deep-research/requests/request.json`.
