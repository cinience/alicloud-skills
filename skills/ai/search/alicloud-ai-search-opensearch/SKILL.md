---
name: alicloud-ai-search-opensearch
description: Use OpenSearch vector search edition via the Python SDK (ha3engine) to push documents and run HA/SQL searches. Ideal for RAG and vector retrieval pipelines in Claude Code/Codex.
---

Category: provider

# OpenSearch Vector Search Edition

Use the ha3engine SDK to push documents and execute HA/SQL searches. This skill focuses on API/SDK usage only (no console steps).

## Prerequisites

- Install SDK (recommended in a venv to avoid PEP 668 limits):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install alibabacloud-ha3engine
```
- Provide connection config via environment variables:
  - `OPENSEARCH_ENDPOINT` (API domain)
  - `OPENSEARCH_INSTANCE_ID`
  - `OPENSEARCH_USERNAME`
  - `OPENSEARCH_PASSWORD`
  - `OPENSEARCH_DATASOURCE` (data source name)
  - `OPENSEARCH_PK_FIELD` (primary key field name)

## Quickstart (push + search)

```python
import os
from alibabacloud_ha3engine import models, client
from Tea.exceptions import TeaException, RetryError

cfg = models.Config(
    endpoint=os.getenv("OPENSEARCH_ENDPOINT"),
    instance_id=os.getenv("OPENSEARCH_INSTANCE_ID"),
    protocol="http",
    access_user_name=os.getenv("OPENSEARCH_USERNAME"),
    access_pass_word=os.getenv("OPENSEARCH_PASSWORD"),
)
ha3 = client.Client(cfg)

def push_docs():
    data_source = os.getenv("OPENSEARCH_DATASOURCE")
    pk_field = os.getenv("OPENSEARCH_PK_FIELD", "id")

    documents = [
        {"fields": {"id": 1, "title": "hello", "content": "world"}, "cmd": "add"},
        {"fields": {"id": 2, "title": "faq", "content": "vector search"}, "cmd": "add"},
    ]
    req = models.PushDocumentsRequestModel({}, documents)
    return ha3.push_documents(data_source, pk_field, req)


def search_ha():
    # HA query example. Replace cluster/table names as needed.
    query_str = (
        "config=hit:5,format:json,qrs_chain:search"
        "&&query=title:hello"
        "&&cluster=general"
    )
    ha_query = models.SearchQuery(query=query_str)
    req = models.SearchRequestModel({}, ha_query)
    return ha3.search(req)

try:
    print(push_docs().body)
    print(search_ha())
except (TeaException, RetryError) as e:
    print(e)
```

## Script quickstart

```bash
python skills/ai/search/alicloud-ai-search-opensearch/scripts/quickstart.py
```

Environment variables:

- `OPENSEARCH_ENDPOINT`
- `OPENSEARCH_INSTANCE_ID`
- `OPENSEARCH_USERNAME`
- `OPENSEARCH_PASSWORD`
- `OPENSEARCH_DATASOURCE`
- `OPENSEARCH_PK_FIELD` (optional, default `id`)
- `OPENSEARCH_CLUSTER` (optional, default `general`)

Optional args: `--cluster`, `--hit`, `--query`.

## SQL-style search

```python
from alibabacloud_ha3engine import models

sql = "select * from <indexTableName>&&kvpair=trace:INFO;formatType:json"
sql_query = models.SearchQuery(sql=sql)
req = models.SearchRequestModel({}, sql_query)
resp = ha3.search(req)
print(resp)
```

## Notes for Claude Code/Codex

- Use `push_documents` for add/delete updates.
- Large query strings (>30KB) should use the RESTful search API.
- HA queries are fast and flexible for vector + keyword retrieval; SQL is helpful for structured data.

## Error handling

- Auth errors: verify username/password and instance access.
- 4xx on push: check schema fields and `pk_field` alignment.
- 5xx: retry with backoff.

## References

- SDK package: `alibabacloud-ha3engine`
- Demos: data push and HA/SQL search demos in OpenSearch docs

- Source list: `references/sources.md`
