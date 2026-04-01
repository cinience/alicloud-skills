---
name: aliyun-modelstudio-tts
description: Generate human-like speech audio with Model Studio DashScope Qwen TTS models (qwen3-tts-flash, qwen3-tts-instruct-flash). Use when converting text to speech, producing voice lines for short drama/news videos, or documenting TTS request/response fields for DashScope.
version: 1.0.0
---

Category: provider

# Model Studio Qwen TTS

## Validation

```bash
mkdir -p output/aliyun-modelstudio-tts
python -m py_compile skills/ai/audio/aliyun-modelstudio-tts/scripts/generate_tts.py && echo "py_compile_ok" > output/aliyun-modelstudio-tts/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-modelstudio-tts/validate.txt` is generated.

## Output And Evidence

- Save generated audio links, sample audio files, and request payloads to `output/aliyun-modelstudio-tts/`.
- Keep one validation log per execution.

## Critical model names

Use one of the recommended models:
- `qwen3-tts-flash`
- `qwen3-tts-instruct-flash`
- `qwen3-tts-instruct-flash-2026-01-26`

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
- `instruction` (string, optional; recommended for instruct models)
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
    model="qwen3-tts-instruct-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    text=text,
    voice="Cherry",
    language_type="English",
    instruction="Warm and calm tone, slightly slower pace.",
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
- Use `instruction` only when you need explicit style/tone control.
- Cache by `(text, voice, language_type)` to avoid repeat costs.

## Output location

- Default output: `output/aliyun-modelstudio-tts/audio/`
- Override base dir with `OUTPUT_DIR`.

## Workflow

1) Confirm user intent, region, identifiers, and whether the operation is read-only or mutating.
2) Run one minimal read-only query first to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.

## References

- `references/api_reference.md` for parameter mapping and streaming example.
- Realtime mode is provided by `skills/ai/audio/aliyun-modelstudio-tts-realtime/`.
- Voice cloning/design are provided by `skills/ai/audio/aliyun-modelstudio-tts-voice-clone/` and `skills/ai/audio/aliyun-modelstudio-tts-voice-design/`.

- Source list: `references/sources.md`
