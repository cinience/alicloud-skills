---
name: alicloud-ai-audio-livetranslate-test
description: Minimal live speech translation smoke test for Model Studio Qwen LiveTranslate.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Goals

- 仅验证 live translate 请求模板与模型映射存在。

## Prerequisites

- Target skill: `skills/ai/audio/alicloud-ai-audio-livetranslate`

## Recommended check

```bash
python skills/ai/audio/alicloud-ai-audio-livetranslate/scripts/prepare_livetranslate_request.py \
  --output output/alicloud-ai-audio-livetranslate/request.json
```
