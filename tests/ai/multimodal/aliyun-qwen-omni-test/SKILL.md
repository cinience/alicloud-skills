---
name: alicloud-ai-multimodal-qwen-omni-test
description: Minimal multimodal omni smoke test for Model Studio Qwen Omni.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Goals

- Validate that the omni skill includes the correct latest model family and sample payload.

## Prerequisites

- Target skill: `skills/ai/multimodal/alicloud-ai-multimodal-qwen-omni`

## Recommended check

```bash
python skills/ai/multimodal/alicloud-ai-multimodal-qwen-omni/scripts/prepare_omni_request.py \
  --output output/alicloud-ai-multimodal-qwen-omni/request.json
```
