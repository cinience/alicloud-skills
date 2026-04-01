---
name: aliyun-qwen-tts-voice-design
description: Use when designing custom voices with Alibaba Cloud Model Studio Qwen TTS VD models. Use when creating custom synthetic voices from text descriptions and using them for speech synthesis.
version: 1.0.0
---

Category: provider

# Model Studio Qwen TTS Voice Design

Use voice design models to create controllable synthetic voices from natural language descriptions.

## Critical model names

Use one of these exact model strings:
- `qwen3-tts-vd-2026-01-26`
- `qwen3-tts-vd-realtime-2026-01-15`

## Prerequisites

- Install SDK in a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Normalized interface (tts.voice_design)

### Request
- `voice_prompt` (string, required) target voice description
- `text` (string, required)
- `stream` (bool, optional)

### Response
- `audio_url` (string) or streaming PCM chunks
- `voice_id` (string)
- `request_id` (string)

## Operational guidance

- Write voice prompts with tone, pace, emotion, and timbre constraints.
- Build a reusable voice prompt library for product consistency.
- Validate generated voice in short utterances before long scripts.

## Local helper script

Prepare a normalized request JSON and validate response schema:

```bash
.venv/bin/python skills/ai/audio/aliyun-qwen-tts-voice-design/scripts/prepare_voice_design_request.py \
  --voice-prompt "A warm female host voice, clear articulation, medium pace" \
  --text "This is a voice-design demo"
```

## Output location

- Default output: `output/ai-audio-tts-voice-design/audio/`
- Override base dir with `OUTPUT_DIR`.

## Validation

```bash
mkdir -p output/aliyun-qwen-tts-voice-design
for f in skills/ai/audio/aliyun-qwen-tts-voice-design/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-qwen-tts-voice-design/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-qwen-tts-voice-design/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-qwen-tts-voice-design/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Workflow

1) Confirm user intent, region, identifiers, and whether the operation is read-only or mutating.
2) Run one minimal read-only query first to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.

## References

- `references/sources.md`
