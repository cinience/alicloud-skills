---
name: aliyun-qwen-rerank
description: Use when reranking search candidates is needed with Alibaba Cloud Model Studio rerank models, including hybrid retrieval, top-k refinement, and multilingual relevance sorting.
version: 1.0.0
---

Category: provider

# Model Studio Rerank

## Validation

```bash
mkdir -p output/aliyun-qwen-rerank
python -m py_compile skills/ai/search/aliyun-qwen-rerank/scripts/prepare_rerank_request.py && echo "py_compile_ok" > output/aliyun-qwen-rerank/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-qwen-rerank/validate.txt` is generated.

## Critical model names

Use one of these exact model strings:
- `gte-rerank-v2`
- `gte-rerank`
- `gte-multilingual-rerank`
- `qwen3-reranker-8b`
- `qwen3-reranker-4b`
- `qwen3-reranker-0.6b`

## Quick start

```bash
python skills/ai/search/aliyun-qwen-rerank/scripts/prepare_rerank_request.py \
  --query "cloud vector database" \
  --output output/aliyun-qwen-rerank/request.json
```

## Notes

- Use after embedding/vector retrieval to reorder candidates.
- Prefer multilingual rerankers when query/document languages differ.

## References

- `references/sources.md`
