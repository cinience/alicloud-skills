---
name: aliyun-qvq-test
description: Minimal visual reasoning smoke test for Model Studio QVQ.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Goals

- Validate that the QVQ skill includes the visual reasoning models and sample payload.

## Prerequisites

- Target skill: `skills/ai/multimodal/aliyun-qvq`

## Recommended check

```bash
python skills/ai/multimodal/aliyun-qvq/scripts/prepare_qvq_request.py \
  --output output/aliyun-qvq/request.json
```
