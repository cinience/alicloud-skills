---
name: aliyun-qwen-ocr
description: Use when OCR-specialized extraction is needed with Alibaba Cloud Model Studio Qwen OCR models (`qwen-vl-ocr`, `qwen-vl-ocr-latest`, and snapshots), including document parsing, table parsing, multilingual OCR, formula recognition, and key information extraction.
version: 1.0.0
---

Category: provider

# Model Studio Qwen OCR

## Validation

```bash
mkdir -p output/aliyun-qwen-ocr
python -m py_compile skills/ai/multimodal/aliyun-qwen-ocr/scripts/prepare_ocr_request.py && echo "py_compile_ok" > output/aliyun-qwen-ocr/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-qwen-ocr/validate.txt` is generated.

## Output And Evidence

- Save request payloads, selected OCR task name, and normalized output expectations under `output/aliyun-qwen-ocr/`.
- Keep the exact model, image source, and task configuration with each saved run.

Use Qwen OCR when the task is primarily text extraction or document structure parsing rather than broad visual reasoning.

## Critical model names

Use one of these exact model strings:
- `qwen-vl-ocr`
- `qwen-vl-ocr-latest`
- `qwen-vl-ocr-2025-11-20`
- `qwen-vl-ocr-2025-08-28`
- `qwen-vl-ocr-2025-04-13`
- `qwen-vl-ocr-2024-10-28`

Selection guidance:
- Use `qwen-vl-ocr` for the stable channel.
- Use `qwen-vl-ocr-latest` only when you explicitly want the newest OCR behavior.
- Pin `qwen-vl-ocr-2025-11-20` when you need reproducible document parsing based on the Qwen3-VL OCR upgrade.

## Prerequisites

- Install dependencies (recommended in a venv):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install requests
```

- Set `DASHSCOPE_API_KEY` in environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Normalized interface (ocr.extract)

### Request
- `image` (string, required): HTTPS URL, local path, or `data:` URL.
- `model` (string, optional): default `qwen-vl-ocr`.
- `prompt` (string, optional): use when you want custom extraction instructions.
- `task` (string, optional): built-in OCR task.
- `task_config` (object, optional): configuration for built-in task such as extraction fields.
- `enable_rotate` (bool, optional): default `false`.
- `min_pixels` (int, optional)
- `max_pixels` (int, optional)
- `max_tokens` (int, optional)
- `temperature` (float, optional): recommended to keep near default/low values.

### Response
- `text` (string): extracted text or structured markdown/html-style output.
- `model` (string)
- `usage` (object, optional)

## Built-in OCR tasks

Use one of these values in `task`:
- `text_recognition`
- `key_information_extraction`
- `document_parsing`
- `table_parsing`
- `formula_recognition`
- `multi_lan`
- `advanced_recognition`

## Quick start

Custom prompt:

```bash
python skills/ai/multimodal/aliyun-qwen-ocr/scripts/prepare_ocr_request.py \
  --image "https://example.com/invoice.png" \
  --prompt "Extract seller name, invoice date, amount, and tax number in JSON."
```

Built-in task:

```bash
python skills/ai/multimodal/aliyun-qwen-ocr/scripts/prepare_ocr_request.py \
  --image "https://example.com/table.png" \
  --task table_parsing \
  --model qwen-vl-ocr-2025-11-20
```

## Operational guidance

- Prefer built-in OCR tasks for standard parsing jobs because they use official task prompts.
- For critical business fields, add downstream validation rules after OCR.
- `qwen-vl-ocr` and older snapshots default to `4096` max output tokens unless higher limits are approved by Alibaba Cloud; `qwen-vl-ocr-2025-11-20` follows the model maximum.
- Increase `max_pixels` only when small text is missed; this raises token cost.

## Output location

- Default output: `output/aliyun-qwen-ocr/request.json`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/api_reference.md`
- `references/sources.md`
