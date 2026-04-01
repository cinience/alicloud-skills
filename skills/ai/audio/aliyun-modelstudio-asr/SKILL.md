---
name: aliyun-modelstudio-asr
description: Transcribe non-realtime speech with Alibaba Cloud Model Studio Qwen ASR models (`qwen3-asr-flash`, `qwen-audio-asr`, `qwen3-asr-flash-filetrans`). Use when converting recorded audio files to text, generating transcripts with timestamps, or documenting DashScope/OpenAI-compatible ASR request and response fields.
version: 1.0.0
---

Category: provider

# Model Studio Qwen ASR (Non-Realtime)

## Validation

```bash
mkdir -p output/aliyun-modelstudio-asr
python -m py_compile skills/ai/audio/aliyun-modelstudio-asr/scripts/transcribe_audio.py && echo "py_compile_ok" > output/aliyun-modelstudio-asr/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-modelstudio-asr/validate.txt` is generated.

## Output And Evidence

- Store transcripts and API responses under `output/aliyun-modelstudio-asr/`.
- Keep one command log or sample response per run.

Use Qwen ASR for recorded audio transcription (non-realtime), including short audio sync calls and long audio async jobs.

## Critical model names

Use one of these exact model strings:
- `qwen3-asr-flash`
- `qwen3-asr-flash-2026-02-10`
- `qwen-audio-asr`
- `qwen3-asr-flash-filetrans`
- `qwen3-asr-flash-filetrans-2025-11-17`

Selection guidance:
- Use `qwen3-asr-flash`, `qwen3-asr-flash-2026-02-10`, or `qwen-audio-asr` for short/normal recordings (sync).
- Use `qwen3-asr-flash-filetrans` or `qwen3-asr-flash-filetrans-2025-11-17` for long-file transcription (async task workflow).

## Prerequisites

- Install SDK dependencies (script uses Python stdlib only):

```bash
python3 -m venv .venv
. .venv/bin/activate
```

- Set `DASHSCOPE_API_KEY` in environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Normalized interface (asr.transcribe)

### Request
- `audio` (string, required): public URL or local file path.
- `model` (string, optional): default `qwen3-asr-flash`.
- `language_hints` (array<string>, optional): e.g. `zh`, `en`.
- `sample_rate` (number, optional)
- `vocabulary_id` (string, optional)
- `disfluency_removal_enabled` (bool, optional)
- `timestamp_granularities` (array<string>, optional): e.g. `sentence`.
- `async` (bool, optional): default false for sync models, true for `qwen3-asr-flash-filetrans`.

### Response
- `text` (string): normalized transcript text.
- `task_id` (string, optional): present for async submission.
- `status` (string): `SUCCEEDED` or submission status.
- `raw` (object): original API response.

## Quick start (official HTTP API)

Sync transcription (OpenAI-compatible protocol):

```bash
curl -sS --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "qwen3-asr-flash",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
            }
          }
        ]
      }
    ],
    "stream": false,
    "asr_options": {
      "enable_itn": false
    }
  }'
```

Async long-file transcription (DashScope protocol):

```bash
curl -sS --location 'https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'X-DashScope-Async: enable' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "qwen3-asr-flash-filetrans",
    "input": {
      "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
    }
  }'
```

Poll task result:

```bash
curl -sS --location "https://dashscope.aliyuncs.com/api/v1/tasks/<task_id>" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## Local helper script

Use the bundled script for URL/local-file input and optional async polling:

```bash
python skills/ai/audio/aliyun-modelstudio-asr/scripts/transcribe_audio.py \
  --audio "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3" \
  --model qwen3-asr-flash \
  --language-hints zh,en \
  --print-response
```

Long-file mode:

```bash
python skills/ai/audio/aliyun-modelstudio-asr/scripts/transcribe_audio.py \
  --audio "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3" \
  --model qwen3-asr-flash-filetrans \
  --async \
  --wait
```

## Operational guidance

- For local files, use `input_audio.data` (data URI) when direct URL is unavailable.
- Keep `language_hints` minimal to reduce recognition ambiguity.
- For async tasks, use 5-20s polling interval with max retry guard.
- Save normalized outputs under `output/aliyun-modelstudio-asr/transcripts/`.

## Output location

- Default output: `output/aliyun-modelstudio-asr/transcripts/`
- Override base dir with `OUTPUT_DIR`.

## Workflow

1) Confirm user intent, region, identifiers, and whether the operation is read-only or mutating.
2) Run one minimal read-only query first to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.

## References

- `references/api_reference.md`
- `references/sources.md`
- Realtime synthesis is provided by `skills/ai/audio/aliyun-modelstudio-tts-realtime/`.
