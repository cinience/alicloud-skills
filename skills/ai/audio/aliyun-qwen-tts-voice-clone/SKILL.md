---
name: aliyun-qwen-tts-voice-clone
description: Voice cloning workflows with Alibaba Cloud Model Studio Qwen TTS VC models. Use when creating cloned voices from sample audio and synthesizing text with cloned timbre.
version: 1.0.0
---

Category: provider

# Model Studio Qwen TTS Voice Clone

Use voice cloning models to replicate timbre from enrollment audio samples.

## Critical model names

Use one of these exact model strings:
- `qwen3-tts-vc-2026-01-22`
- `qwen3-tts-vc-realtime-2026-01-15`

## Prerequisites

- Install SDK in a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Normalized interface (tts.voice_clone)

### Request
- `text` (string, required)
- `voice_sample` (string | bytes, required) enrollment sample
- `voice_name` (string, optional)
- `stream` (bool, optional)

### Response
- `audio_url` (string) or streaming PCM chunks
- `voice_id` (string)
- `request_id` (string)

## Operational guidance

- Use clean speech samples with low background noise.
- Respect consent and policy requirements for cloned voices.
- Persist generated `voice_id` and reuse for future synthesis requests.

## Local helper script

Prepare a normalized request JSON and validate response schema:

```bash
.venv/bin/python skills/ai/audio/aliyun-qwen-tts-voice-clone/scripts/prepare_voice_clone_request.py \
  --text "Welcome to this voice-clone demo" \
  --voice-sample "https://example.com/voice-sample.wav"
```

## Output location

- Default output: `output/ai-audio-tts-voice-clone/audio/`
- Override base dir with `OUTPUT_DIR`.

## Validation

```bash
mkdir -p output/aliyun-qwen-tts-voice-clone
for f in skills/ai/audio/aliyun-qwen-tts-voice-clone/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-qwen-tts-voice-clone/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-qwen-tts-voice-clone/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-qwen-tts-voice-clone/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Workflow

1) Confirm user intent, region, identifiers, and whether the operation is read-only or mutating.
2) Run one minimal read-only query first to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.

## References

- `references/sources.md`
