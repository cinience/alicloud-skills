---
name: aliyun-modelstudio-qvq
description: Use when visual reasoning is needed with Alibaba Cloud Model Studio QVQ models, including step-by-step image reasoning, chart analysis, and visually grounded problem solving.
version: 1.0.0
---

Category: provider

# Model Studio QVQ Visual Reasoning

## Validation

```bash
mkdir -p output/aliyun-modelstudio-qvq
python -m py_compile skills/ai/multimodal/aliyun-modelstudio-qvq/scripts/prepare_qvq_request.py && echo "py_compile_ok" > output/aliyun-modelstudio-qvq/validate.txt
```

Pass criteria: command exits 0 and `output/alicloud-ai-multimodal-qwen-vqv/validate.txt` is generated.

## Critical model names

Use one of these exact model strings:
- `qvq-plus`
- `qvq-max`

## Typical use

- Mathematical reasoning from screenshots
- Diagram and chart reasoning
- Visually grounded multi-step problem solving

## Quick start

```bash
python skills/ai/multimodal/aliyun-modelstudio-qvq/scripts/prepare_qvq_request.py \
  --output output/aliyun-modelstudio-qvq/request.json
```

## Notes

- Use `skills/ai/multimodal/aliyun-modelstudio-qwen-vl/` for standard image understanding.
- Use QVQ when the task explicitly needs stronger reasoning over visual evidence.

## References

- `references/sources.md`
