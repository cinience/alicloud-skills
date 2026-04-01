---
name: aliyun-qwen-tts-realtime
description: Use when real-time speech synthesis is needed with Alibaba Cloud Model Studio Qwen TTS Realtime models. Use when low-latency interactive speech is required, including instruction-controlled realtime synthesis.
version: 1.0.0
---

Category: provider

# Model Studio Qwen TTS Realtime

Use realtime TTS models for low-latency streaming speech output.

## Critical model names

Use one of these exact model strings:
- `qwen3-tts-flash-realtime`
- `qwen3-tts-instruct-flash-realtime`
- `qwen3-tts-instruct-flash-realtime-2026-01-22`
- `qwen3-tts-vd-realtime-2026-01-15`
- `qwen3-tts-vc-realtime-2026-01-15`

## Prerequisites

- Install SDK in a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Normalized interface (tts.realtime)

### Request
- `text` (string, required)
- `voice` (string, required)
- `instruction` (string, optional)
- `sample_rate` (int, optional)

### Response
- `audio_base64_pcm_chunks` (array<string>)
- `sample_rate` (int)
- `finish_reason` (string)

## Operational guidance

- Use websocket or streaming endpoint for realtime mode.
- Keep each utterance short for lower latency.
- For instruction models, keep instruction explicit and concise.
- Some SDK/runtime combinations may reject realtime model calls over `MultiModalConversation`; use the probe script below to verify compatibility.

## Local demo script

Use the probe script to verify realtime compatibility in your current SDK/runtime, and optionally fallback to a non-realtime model for immediate output:

```bash
.venv/bin/python skills/ai/audio/aliyun-qwen-tts-realtime/scripts/realtime_tts_demo.py \
  --text "This is a realtime speech demo." \
  --fallback \
  --output output/ai-audio-tts-realtime/audio/fallback-demo.wav
```

Strict mode (for CI / gating):

```bash
.venv/bin/python skills/ai/audio/aliyun-qwen-tts-realtime/scripts/realtime_tts_demo.py \
  --text "realtime health check" \
  --strict
```

## Output location

- Default output: `output/ai-audio-tts-realtime/audio/`
- Override base dir with `OUTPUT_DIR`.

## Validation

```bash
mkdir -p output/aliyun-qwen-tts-realtime
for f in skills/ai/audio/aliyun-qwen-tts-realtime/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-qwen-tts-realtime/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-qwen-tts-realtime/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-qwen-tts-realtime/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Workflow

1) Confirm user intent, region, identifiers, and whether the operation is read-only or mutating.
2) Run one minimal read-only query first to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.

## References

- `references/sources.md`
