---
name: aliyun-modelstudio-multimodal-embedding
description: Use when multimodal embeddings are needed from Alibaba Cloud Model Studio models such as `qwen3-vl-embedding` for image, video, and text retrieval, cross-modal search, clustering, or offline vectorization pipelines.
version: 1.0.0
---

Category: provider

# Model Studio Multimodal Embedding

## Validation

```bash
mkdir -p output/aliyun-modelstudio-multimodal-embedding
python -m py_compile skills/ai/search/aliyun-modelstudio-multimodal-embedding/scripts/prepare_multimodal_embedding_request.py && echo "py_compile_ok" > output/aliyun-modelstudio-multimodal-embedding/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-modelstudio-multimodal-embedding/validate.txt` is generated.

## Output And Evidence

- Save normalized request payloads, selected dimensions, and sample input references under `output/aliyun-modelstudio-multimodal-embedding/`.
- Record the exact model, modality mix, and output vector dimension for reproducibility.

Use this skill when the task needs text, image, or video embeddings from Model Studio for retrieval or similarity workflows.

## Critical model names

Use one of these exact model strings as needed:
- `qwen3-vl-embedding`
- `qwen2.5-vl-embedding`
- `tongyi-embedding-vision-plus-2026-03-06`

Selection guidance:
- Prefer `qwen3-vl-embedding` for the newest multimodal embedding path.
- Use `qwen2.5-vl-embedding` when you need compatibility with an older deployed pipeline.

## Prerequisites

- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.
- Pair this skill with a vector store such as DashVector, OpenSearch, or Milvus when building retrieval systems.

## Normalized interface (embedding.multimodal)

### Request
- `model` (string, optional): default `qwen3-vl-embedding`
- `texts` (array<string>, optional)
- `images` (array<string>, optional): public URLs or local paths uploaded by your client layer
- `videos` (array<string>, optional): public URLs where supported
- `dimension` (int, optional): e.g. `2560`, `2048`, `1536`, `1024`, `768`, `512`, `256` for `qwen3-vl-embedding`

### Response
- `embeddings` (array<object>)
- `dimension` (int)
- `usage` (object, optional)

## Quick start

```bash
python skills/ai/search/aliyun-modelstudio-multimodal-embedding/scripts/prepare_multimodal_embedding_request.py \
  --text "A cat sitting on a red chair" \
  --image "https://example.com/cat.jpg" \
  --dimension 1024
```

## Operational guidance

- Keep `input.contents` as an array; malformed shapes are a common 400 cause.
- Pin the output dimension to match your index schema before writing vectors.
- Use the same model and dimension across one vector index to avoid mixed-vector incompatibility.
- For large image or video batches, stage files in object storage and reference stable URLs.

## Output location

- Default output: `output/aliyun-modelstudio-multimodal-embedding/request.json`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/sources.md`
