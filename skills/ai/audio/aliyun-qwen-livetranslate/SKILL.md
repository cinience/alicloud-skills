---
name: aliyun-qwen-livetranslate
description: Use when live speech translation is needed with Alibaba Cloud Model Studio Qwen LiveTranslate models, including bilingual meetings, realtime interpretation, and speech-to-speech or speech-to-text translation flows.
version: 1.0.0
---

Category: provider

# Model Studio Qwen LiveTranslate

## Validation

```bash
mkdir -p output/aliyun-qwen-livetranslate
python -m py_compile skills/ai/audio/aliyun-qwen-livetranslate/scripts/prepare_livetranslate_request.py && echo "py_compile_ok" > output/aliyun-qwen-livetranslate/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-qwen-livetranslate/validate.txt` is generated.

## Output And Evidence

- Save translation session payloads and response summaries under `output/aliyun-qwen-livetranslate/`.

## Critical model names

Use one of these exact model strings:
- `qwen3-livetranslate-flash`
- `qwen3-livetranslate-flash-realtime`

## Typical use

- Chinese/English meeting interpretation
- Live subtitles in another language
- Call-center agent assist with translated captions

## Normalized interface (audio.livetranslate)

### Request
- `model` (string, optional): default `qwen3-livetranslate-flash`
- `source_language` (string, required)
- `target_language` (string, required)
- `audio_format` (string, optional): e.g. `pcm`
- `sample_rate` (int, optional): e.g. `16000`

### Response
- `translated_text` (string)
- `source_text` (string, optional)
- `audio_url` or `audio_chunk` (optional, model dependent)

## Quick start

```bash
python skills/ai/audio/aliyun-qwen-livetranslate/scripts/prepare_livetranslate_request.py \
  --source-language zh \
  --target-language en \
  --output output/aliyun-qwen-livetranslate/request.json
```

## Notes

- Prefer the realtime model for continuous streaming sessions.
- Prefer the non-realtime flash model for simpler integration and lower client complexity.

## References

- `references/sources.md`
