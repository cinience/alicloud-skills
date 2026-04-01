---
name: aliyun-qwen-text-embedding
description: Use when text embeddings are needed from Alibaba Cloud Model Studio models for semantic search, retrieval-augmented generation, clustering, or offline vectorization pipelines.
version: 1.0.0
---

Category: provider

# Model Studio Text Embedding

## Validation

```bash
mkdir -p output/aliyun-qwen-text-embedding
python -m py_compile skills/ai/search/aliyun-qwen-text-embedding/scripts/prepare_embedding_request.py && echo "py_compile_ok" > output/aliyun-qwen-text-embedding/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-qwen-text-embedding/validate.txt` is generated.

## Critical model names

Use one of these exact model strings as needed:
- `text-embedding-v4`
- `text-embedding-v3`
- `text-embedding-v2`
- `text-embedding-v1`
- `qwen3-embedding-8b`
- `qwen3-embedding-4b`
- `qwen3-embedding-0.6b`

## Quick start

```bash
python skills/ai/search/aliyun-qwen-text-embedding/scripts/prepare_embedding_request.py \
  --text "Alibaba Cloud Model Studio" \
  --output output/aliyun-qwen-text-embedding/request.json
```

## Notes

- Pair this skill with `skills/ai/search/aliyun-dashvector-search/` or other vector-store skills.
- For image or multimodal embeddings, add dedicated multimodal embedding coverage separately.

## References

- `references/sources.md`
