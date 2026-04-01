---
name: aliyun-dashvector-search
description: Use when building vector retrieval with DashVector using the Python SDK. Use when creating collections, upserting docs, and running similarity search with filters in Claude Code/Codex.
version: 1.0.0
---

Category: provider

# DashVector Vector Search

Use DashVector to manage collections and perform vector similarity search with optional filters and sparse vectors.

## Prerequisites

- Install SDK (recommended in a venv to avoid PEP 668 limits):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashvector
```
- Provide credentials and endpoint via environment variables:
  - `DASHVECTOR_API_KEY`
  - `DASHVECTOR_ENDPOINT` (cluster endpoint)

## Normalized operations

### Create collection
- `name` (str)
- `dimension` (int)
- `metric` (str: `cosine` | `dotproduct` | `euclidean`)
- `fields_schema` (optional dict of field types)

### Upsert docs
- `docs` list of `{id, vector, fields}` or tuples
- Supports `sparse_vector` and multi-vector collections

### Query docs
- `vector` or `id` (one required; if both empty, only filter is applied)
- `topk` (int)
- `filter` (SQL-like where clause)
- `output_fields` (list of field names)
- `include_vector` (bool)

## Quickstart (Python SDK)

```python
import os
import dashvector
from dashvector import Doc

client = dashvector.Client(
    api_key=os.getenv("DASHVECTOR_API_KEY"),
    endpoint=os.getenv("DASHVECTOR_ENDPOINT"),
)

# 1) Create a collection
ret = client.create(
    name="docs",
    dimension=768,
    metric="cosine",
    fields_schema={"title": str, "source": str, "chunk": int},
)
assert ret

# 2) Upsert docs
collection = client.get(name="docs")
ret = collection.upsert(
    [
        Doc(id="1", vector=[0.01] * 768, fields={"title": "Intro", "source": "kb", "chunk": 0}),
        Doc(id="2", vector=[0.02] * 768, fields={"title": "FAQ", "source": "kb", "chunk": 1}),
    ]
)
assert ret

# 3) Query
ret = collection.query(
    vector=[0.01] * 768,
    topk=5,
    filter="source = 'kb' AND chunk >= 0",
    output_fields=["title", "source", "chunk"],
    include_vector=False,
)
for doc in ret:
    print(doc.id, doc.fields)
```

## Script quickstart

```bash
python skills/ai/search/aliyun-dashvector-search/scripts/quickstart.py
```

Environment variables:

- `DASHVECTOR_API_KEY`
- `DASHVECTOR_ENDPOINT`
- `DASHVECTOR_COLLECTION` (optional)
- `DASHVECTOR_DIMENSION` (optional)

Optional args: `--collection`, `--dimension`, `--topk`, `--filter`.

## Notes for Claude Code/Codex

- Prefer `upsert` for idempotent ingestion.
- Keep `dimension` aligned to your embedding model output size.
- Use filters to enforce tenant or dataset scoping.
- If using sparse vectors, pass `sparse_vector={token_id: weight, ...}` when upserting/querying.

## Error handling

- 401/403: invalid `DASHVECTOR_API_KEY`
- 400: invalid collection schema or dimension mismatch
- 429/5xx: retry with exponential backoff

## Validation

```bash
mkdir -p output/aliyun-dashvector-search
for f in skills/ai/search/aliyun-dashvector-search/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-dashvector-search/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-dashvector-search/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-dashvector-search/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Workflow

1) Confirm user intent, region, identifiers, and whether the operation is read-only or mutating.
2) Run one minimal read-only query first to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.

## References

- DashVector Python SDK: `Client.create`, `Collection.upsert`, `Collection.query`

- Source list: `references/sources.md`
