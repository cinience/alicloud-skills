---
name: alicloud-ai-search-milvus
description: Use AliCloud Milvus (serverless) with PyMilvus to create collections, insert vectors, and run filtered similarity search. Optimized for Claude Code/Codex vector retrieval flows.
---

Category: provider

# AliCloud Milvus (Serverless) via PyMilvus

This skill uses standard PyMilvus APIs to connect to AliCloud Milvus and run vector search.

## Prerequisites

- Install SDK (recommended in a venv to avoid PEP 668 limits):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pymilvus
```
- Provide connection via environment variables:
  - `MILVUS_URI` (e.g. `http://<host>:19530`)
  - `MILVUS_TOKEN` (`<username>:<password>`)
  - `MILVUS_DB` (default: `default`)

## Quickstart (Python)

```python
import os
from pymilvus import MilvusClient

client = MilvusClient(
    uri=os.getenv("MILVUS_URI"),
    token=os.getenv("MILVUS_TOKEN"),
    db_name=os.getenv("MILVUS_DB", "default"),
)

# 1) Create a collection
client.create_collection(
    collection_name="docs",
    dimension=768,
)

# 2) Insert data
items = [
    {"id": 1, "vector": [0.01] * 768, "source": "kb", "chunk": 0},
    {"id": 2, "vector": [0.02] * 768, "source": "kb", "chunk": 1},
]
client.insert(collection_name="docs", data=items)

# 3) Search
query_vectors = [[0.01] * 768]
res = client.search(
    collection_name="docs",
    data=query_vectors,
    limit=5,
    filter='source == "kb" and chunk >= 0',
    output_fields=["source", "chunk"],
)
print(res)
```

## Script quickstart

```bash
python skills/ai/search/alicloud-ai-search-milvus/scripts/quickstart.py
```

Environment variables:

- `MILVUS_URI`
- `MILVUS_TOKEN`
- `MILVUS_DB` (optional)
- `MILVUS_COLLECTION` (optional)
- `MILVUS_DIMENSION` (optional)

Optional args: `--collection`, `--dimension`, `--limit`, `--filter`.

## Notes for Claude Code/Codex

- Insert is async; wait a few seconds before searching newly inserted data.
- Keep vector `dimension` aligned with your embedding model.
- Use filters to enforce tenant scoping or dataset partitions.

## Error handling

- Auth errors: check `MILVUS_TOKEN` and instance permissions.
- Dimension mismatch: ensure all vectors match collection dimension.
- Network errors: verify VPC/public access settings on the instance.

## References

- PyMilvus `MilvusClient` examples for AliCloud Milvus

- Source list: `references/sources.md`
