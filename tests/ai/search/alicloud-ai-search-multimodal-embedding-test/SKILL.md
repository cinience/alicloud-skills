---
name: alicloud-ai-search-multimodal-embedding-test
description: Minimal multimodal embedding smoke test for Model Studio VL embedding models.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/search/alicloud-ai-search-multimodal-embedding`

## Executable Example

```bash
.venv/bin/python skills/ai/search/alicloud-ai-search-multimodal-embedding/scripts/prepare_multimodal_embedding_request.py \
  --text "A cat sitting on a red chair" \
  --image "https://example.com/cat.jpg" \
  --dimension 1024
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/alicloud-ai-search-multimodal-embedding/request.json`.

