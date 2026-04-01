---
name: aliyun-qwen-asr-realtime
description: Use when low-latency realtime speech recognition is needed with Alibaba Cloud Model Studio Qwen ASR Realtime models, including streaming microphone input, live captions, or duplex voice agents.
version: 1.0.0
---

Category: provider

# Model Studio Qwen ASR Realtime

## Validation

```bash
mkdir -p output/aliyun-qwen-asr-realtime
python -m py_compile skills/ai/audio/aliyun-qwen-asr-realtime/scripts/prepare_realtime_asr_request.py && echo "py_compile_ok" > output/aliyun-qwen-asr-realtime/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-qwen-asr-realtime/validate.txt` is generated.

## Output And Evidence

- Save session payloads and response samples under `output/aliyun-qwen-asr-realtime/`.

## Critical model names

Use one of these exact model strings:
- `qwen3-asr-flash-realtime`
- `qwen3-asr-flash-realtime-2026-02-10`

## Use cases

- Realtime subtitles and captions
- Voice-agent duplex input
- Streaming speech-to-text in browser or terminal clients

## Prerequisites

- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.
- Realtime sessions generally require WebSocket or streaming session handling in the client.

## Normalized interface (asr.realtime)

### Request
- `model` (string, optional): default `qwen3-asr-flash-realtime`
- `language_hints` (array<string>, optional)
- `format` (string, optional): e.g. `pcm`, `wav`
- `sample_rate` (int, optional): e.g. `16000`
- `chunk_ms` (int, optional): frame size in milliseconds

### Response
- `text` (string): recognized transcript fragment
- `is_final` (bool): finalization marker
- `usage` (object, optional)

## Quick start

Generate a request template:

```bash
python skills/ai/audio/aliyun-qwen-asr-realtime/scripts/prepare_realtime_asr_request.py \
  --output output/aliyun-qwen-asr-realtime/request.json
```

## Operational guidance

- Prefer 16kHz mono PCM unless your client stack requires another format.
- Keep chunks small enough for responsive partial results.
- If you only have recorded files, use `skills/ai/audio/aliyun-qwen-asr/` instead.

## References

- `references/sources.md`
