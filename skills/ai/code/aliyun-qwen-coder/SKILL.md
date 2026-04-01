---
name: aliyun-qwen-coder
description: Use when code generation, repository understanding, or coding-agent tasks need Alibaba Cloud Model Studio Qwen Coder models (`qwen3-coder-next`, `qwen3-coder-plus` and related coder variants).
version: 1.0.0
---

Category: provider

# Model Studio Qwen Coder

## Validation

```bash
mkdir -p output/aliyun-qwen-coder
python -m py_compile skills/ai/code/aliyun-qwen-coder/scripts/prepare_code_request.py && echo "py_compile_ok" > output/aliyun-qwen-coder/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-qwen-coder/validate.txt` is generated.

## Output And Evidence

- Save prompts, repository context summaries, and normalized coding request payloads under `output/aliyun-qwen-coder/`.
- Record the exact model, endpoint mode, and target language/framework for reproducibility.

Use Qwen Coder for coding assistants, code review drafting, repository-level reasoning, patch planning, and tool-using software agents.

## Critical model names

Use one of these exact model strings as appropriate:
- `qwen3-coder-next`
- `qwen3-coder-plus`
- `qwen-coder-plus`
- `qwen2.5-coder-32b-instruct`

## Prerequisites

- Install SDK in a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```

- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.
- Prefer the OpenAI-compatible endpoint when a client does not yet expose the latest coder models in dropdown UI.

## Normalized interface (code.generate)

### Request
- `messages` (array<object>, required)
- `model` (string, optional): default `qwen3-coder-next`
- `repository_summary` (string, optional)
- `files` (array<string>, optional)
- `language` (string, optional)
- `tools` (array<object>, optional)
- `stream` (bool, optional)

### Response
- `text` (string)
- `patch` (string, optional)
- `usage` (object, optional)

## Quick start

```bash
python skills/ai/code/aliyun-qwen-coder/scripts/prepare_code_request.py \
  --task "Refactor request validation into a small helper and add one unit test." \
  --language python
```

## Operational guidance

- Pass only the files relevant to the requested change to reduce noise.
- Use `qwen3-coder-next` for current-generation coding tasks and `qwen3-coder-plus` when you need a stronger but potentially costlier coder.
- For repo-scale changes, include architecture notes and expected test commands.
- Prefer deterministic prompts and pinned model IDs for benchmarking or regression comparison.

## Output location

- Default output: `output/aliyun-qwen-coder/requests/`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/sources.md`
