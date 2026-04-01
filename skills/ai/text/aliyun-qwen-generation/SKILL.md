---
name: aliyun-qwen-generation
description: Use when generating or reasoning over text with Alibaba Cloud Model Studio Qwen flagship text models (`qwen3-max`, `qwen3.5-plus`, `qwen3.5-flash`, snapshots, and compatible open-source variants). Use when building chat, agent, tool-calling, or long-context text generation workflows on Model Studio.
version: 1.0.0
---

Category: provider

# Model Studio Qwen Text Generation

## Validation

```bash
mkdir -p output/aliyun-qwen-generation
python -m py_compile skills/ai/text/aliyun-qwen-generation/scripts/prepare_generation_request.py && echo "py_compile_ok" > output/aliyun-qwen-generation/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-qwen-generation/validate.txt` is generated.

## Output And Evidence

- Save prompt templates, normalized request payloads, and response summaries under `output/aliyun-qwen-generation/`.
- Keep one reproducible request example with model name, region, and key parameters.

Use this skill for general text generation, reasoning, tool-calling, and long-context chat on Alibaba Cloud Model Studio.

## Critical model names

Prefer the current flagship families:
- `qwen3-max`
- `qwen3-max-2026-01-23`
- `qwen3.5-plus`
- `qwen3.5-plus-2026-02-15`
- `qwen3.5-flash`
- `qwen3.5-flash-2026-02-23`

Common related variants listed in the official model catalog:
- `qwen3.5-397b-a17b`
- `qwen3.5-122b-a10b`
- `qwen3.5-35b-a3b`
- `qwen3.5-27b`

## Prerequisites

- Install SDK in a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```

- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Normalized interface (text.generate)

### Request
- `messages` (array<object>, required): standard chat turns.
- `model` (string, optional): default `qwen3.5-plus`.
- `temperature` (number, optional)
- `top_p` (number, optional)
- `max_tokens` (int, optional)
- `enable_thinking` (bool, optional)
- `tools` (array<object>, optional)
- `response_format` (object, optional)
- `stream` (bool, optional)

### Response
- `text` (string): assistant output.
- `finish_reason` (string, optional)
- `usage` (object, optional)
- `raw` (object, optional)

## Quick start (OpenAI-compatible endpoint)

```bash
curl -sS https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5-plus",
    "messages": [
      {"role": "system", "content": "You are a concise assistant."},
      {"role": "user", "content": "Summarize why object storage helps media pipelines."}
    ],
    "stream": false
  }'
```

## Local helper script

```bash
python skills/ai/text/aliyun-qwen-generation/scripts/prepare_generation_request.py \
  --prompt "Draft a concise architecture summary for a media ingestion pipeline." \
  --model qwen3.5-plus
```

## Operational guidance

- Use snapshot IDs when reproducibility matters.
- Prefer `qwen3.5-flash` for lower-latency simple tasks and `qwen3-max` for harder multi-step tasks.
- Keep tool schemas minimal and explicit when enabling tool calls.
- For multimodal input, route to dedicated VL or Omni skills unless the task is primarily text-centric.

## Output location

- Default output: `output/aliyun-qwen-generation/requests/`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/sources.md`
