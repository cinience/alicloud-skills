---
name: alicloud-ai-audio-tts
description: Generate human-like speech audio with Model Studio DashScope Qwen TTS (qwen3-tts-flash). Use when converting text to speech, producing voice lines for short drama/news videos, or documenting TTS request/response fields for DashScope.
---

Category: provider

# Model Studio Qwen TTS

## Critical model name

Use the recommended model:
- `qwen3-tts-flash`

## Prerequisites

- Install SDK (recommended in a venv to avoid PEP 668 limits):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials` (env takes precedence).

## Normalized interface (tts.generate)

### Request
- `text` (string, required)
- `voice` (string, required)
- `language_type` (string, optional; default `Auto`)
- `stream` (bool, optional; default false)

### Response
- `audio_url` (string, when stream=false)
- `audio_base64_pcm` (string, when stream=true)
- `sample_rate` (int, 24000)
- `format` (string, wav or pcm depending on mode)

## Quick start (Python + DashScope SDK)

```python
import os
import dashscope

# Prefer env var for auth: export DASHSCOPE_API_KEY=...
# Or use ~/.alibabacloud/credentials with dashscope_api_key under [default].
# Beijing region; for Singapore use: https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

text = "Hello, this is a short voice line."
response = dashscope.MultiModalConversation.call(
    model="qwen3-tts-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    text=text,
    voice="Cherry",
    language_type="English",
    stream=False,
)

audio_url = response.output.audio.url
print(audio_url)
```

## Streaming notes

- `stream=True` returns Base64-encoded PCM chunks at 24kHz.
- Decode chunks and play or concatenate to a pcm buffer.
- The response contains `finish_reason == "stop"` when the stream ends.

## Operational guidance

- Keep requests concise; split long text into multiple calls if you hit size or timeout errors.
- Use `language_type` consistent with the text to improve pronunciation.
- Cache by `(text, voice, language_type)` to avoid repeat costs.

## Output location

- Default output: `output/ai-audio-tts/audio/`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/api_reference.md` for parameter mapping and streaming example.

- Source list: `references/sources.md`
