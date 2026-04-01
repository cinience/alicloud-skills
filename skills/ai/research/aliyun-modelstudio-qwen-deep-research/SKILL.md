---
name: aliyun-modelstudio-qwen-deep-research
description: Use when a task needs Alibaba Cloud Model Studio Qwen Deep Research models to plan multi-step investigation, run iterative web research, and produce structured reports with citations or evidence summaries.
version: 1.0.0
---

Category: provider

# Model Studio Qwen Deep Research

## Validation

```bash
mkdir -p output/aliyun-modelstudio-qwen-deep-research
python -m py_compile skills/ai/research/aliyun-modelstudio-qwen-deep-research/scripts/prepare_deep_research_request.py && echo "py_compile_ok" > output/aliyun-modelstudio-qwen-deep-research/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-modelstudio-qwen-deep-research/validate.txt` is generated.

## Output And Evidence

- Save research goals, confirmation answers, normalized request payloads, and final report snapshots under `output/aliyun-modelstudio-qwen-deep-research/`.
- Keep the exact model, region, and `enable_feedback` setting with each saved run.

Use this skill when the user wants a deep, multi-stage research workflow rather than a single chat completion.

## Critical model names

Use one of these exact model strings:
- `qwen-deep-research`
- `qwen-deep-research-2025-12-15`

Selection guidance:
- Use `qwen-deep-research` for the current mainline model.
- Use `qwen-deep-research-2025-12-15` when you need the snapshot with MCP tool-calling support and stronger reproducibility.

## Prerequisites

- Install SDK in a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```

- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.
- This model currently applies to the China mainland (Beijing) region and uses its own API shape rather than OpenAI-compatible mode.

## Normalized interface (research.run)

### Request
- `topic` (string, required)
- `model` (string, optional): default `qwen-deep-research`
- `messages` (array<object>, optional)
- `enable_feedback` (bool, optional): default `true`
- `stream` (bool, optional): must be `true`
- `attachments` (array<object>, optional): image URLs and related context

### Response
- `status` (string): stage status such as `thinking`, `researching`, or `finished`
- `text` (string, optional): streamed content chunk
- `report` (string, optional): final structured research report
- `raw` (object, optional)

## Quick start

```bash
python skills/ai/research/aliyun-modelstudio-qwen-deep-research/scripts/prepare_deep_research_request.py \
  --topic "Compare cloud video generation model trade-offs for marketing automation." \
  --disable-feedback
```

## Operational guidance

- Expect streaming output only.
- Keep the initial topic concrete and bounded; broad topics can trigger long iterative search plans.
- If the model asks follow-up questions and you already know the constraints, answer them explicitly to avoid wasted rounds.
- Use the snapshot model when you need stable evaluation runs or MCP tool-calling support.

## Output location

- Default output: `output/aliyun-modelstudio-qwen-deep-research/requests/`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/sources.md`
