---
name: alicloud-ai-multimodal-qwen-ocr-test
description: Minimal OCR smoke test for Model Studio Qwen OCR.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/multimodal/alicloud-ai-multimodal-qwen-ocr`

## Executable Example

```bash
.venv/bin/python skills/ai/multimodal/alicloud-ai-multimodal-qwen-ocr/scripts/prepare_ocr_request.py \
  --image "https://example.com/invoice.png" \
  --task key_information_extraction \
  --task-config '{"keys":["seller_name","invoice_date","amount"]}'
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/alicloud-ai-multimodal-qwen-ocr/request.json`.

