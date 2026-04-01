---
name: aliyun-qwen-omni
description: Use when tasks require all-in-one multimodal understanding or generation with Alibaba Cloud Model Studio Qwen Omni models, including image-plus-audio interaction, voice assistants, and realtime multimodal agents.
version: 1.0.0
---

Category: provider

# Model Studio Qwen Omni

## Validation

```bash
mkdir -p output/aliyun-qwen-omni
python -m py_compile skills/ai/multimodal/aliyun-qwen-omni/scripts/prepare_omni_request.py && echo "py_compile_ok" > output/aliyun-qwen-omni/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-qwen-omni/validate.txt` is generated.

## Critical model names

Use one of these exact model strings:
- `qwen3-omni-flash`
- `qwen3-omni-flash-realtime`
- `qwen-omni-turbo`
- `qwen-omni-turbo-realtime`

## Typical use

- Image + audio + text assistant
- Realtime multimodal agents
- Spoken responses grounded in visual input

## Normalized interface (omni.chat)

### Request
- `model` (string, optional): default `qwen3-omni-flash`
- `text` (string, optional)
- `image` (string, optional)
- `audio` (string, optional)
- `response_modalities` (array<string>, optional): e.g. `["text"]`, `["text","audio"]`

### Response
- `text` (string, optional)
- `audio_url` or `audio_chunk` (optional)
- `usage` (object, optional)

## Quick start

```bash
python skills/ai/multimodal/aliyun-qwen-omni/scripts/prepare_omni_request.py \
  --output output/aliyun-qwen-omni/request.json
```

## References

- `references/sources.md`
