---
name: aliyun-qwen-asr-realtime-test
description: Minimal realtime ASR smoke test for Model Studio Qwen ASR Realtime.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Goals

- 仅验证实时 ASR 请求模板与最小链路说明存在。

## Prerequisites

- Target skill: `skills/ai/audio/aliyun-qwen-asr-realtime`

## Recommended check

```bash
python skills/ai/audio/aliyun-qwen-asr-realtime/scripts/prepare_realtime_asr_request.py \
  --output output/aliyun-qwen-asr-realtime/request.json
```
