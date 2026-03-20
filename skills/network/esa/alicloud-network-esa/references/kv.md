# Edge KV — Edge Key-Value Storage Reference

ESA Edge KV is a distributed edge key-value storage service, readable and writable in Edge Routine, also manageable via OpenAPI. Suitable for edge configuration distribution, feature flags, A/B testing, and other scenarios.

## Core Concepts

- **Namespace (Storage Space)**: Isolation container for KV data, each account can create multiple namespaces
- **Key**: Key name, max 512 characters, cannot contain spaces or backslashes
- **Value**: Value, standard API max 2MB, high capacity API max 25MB
- **TTL**: Optional expiration time, supports absolute timestamp (Expiration) or relative seconds (ExpirationTtl)

## Limits

| Limit Item | Value |
|------------|-------|
| Max Key length | 512 characters |
| Single Value max (PutKv/BatchPutKv) | 2 MB |
| Single Value max (PutKvWithHighCapacity) | 25 MB |
| Batch request body max (BatchPutKvWithHighCapacity/BatchDeleteKvWithHighCapacity) | 100 MB |
| BatchDeleteKv max keys per request | 10,000 |
| Single Namespace max capacity | 1 GB |
| ListKvs pagination limit | PageNumber × PageSize ≤ 50,000 |

## API List

### Namespace Management

| API | Description | Key Parameters |
|-----|-------------|----------------|
| `CreateKvNamespace` | Create KV storage space | `Namespace`(required, string), `Description`(optional) |
| `DeleteKvNamespace` | Delete KV storage space | `Namespace`(required, string) |
| `GetKvNamespace` | Query single namespace info | `Namespace`(required, string) |
| `GetKvAccount` | Query account KV usage info and all namespaces | No parameters |
| `DescribeKvAccountStatus` | Query if Edge KV is enabled | No parameters |

### Single Key Operations

| API | Description | Key Parameters |
|-----|-------------|----------------|
| `PutKv` | Write key-value pair (≤2MB) | `Namespace`(required), `Key`(required), `Value`(body, required), `Expiration`(optional, Unix timestamp), `ExpirationTtl`(optional, seconds), `Base64`(optional, bool) |
| `PutKvWithHighCapacity` | Write large capacity key-value pair (≤25MB) | Same as PutKv, but via SDK body method |
| `GetKv` | Read key's value | `Namespace`(required), `Key`(required), `Base64`(optional, bool) |
| `GetKvDetail` | Read key-value and TTL | `Namespace`(required), `Key`(required) |
| `DeleteKv` | Delete key-value pair | `Namespace`(required), `Key`(required) |

### Batch Operations

| API | Description | Key Parameters |
|-----|-------------|----------------|
| `BatchPutKv` | Batch write key-value pairs (≤2MB) | `Namespace`(required), body is JSON array `[{Key, Value, Expiration?, ExpirationTtl?}]` |
| `BatchPutKvWithHighCapacity` | Batch write large capacity (≤100MB) | Same as above, via SDK body method |
| `BatchDeleteKv` | Batch delete key-value pairs (≤10000) | `Namespace`(required), body is JSON array `["key1", "key2", ...]` |
| `BatchDeleteKvWithHighCapacity` | Batch delete large capacity (≤100MB) | Same as above, via SDK body method |
| `ListKvs` | List all keys in namespace | `Namespace`(required), `Prefix`(optional), `PageNumber`(optional), `PageSize`(optional, default 20, max 100) |

## Python SDK Usage

### Installation

```bash
pip install alibabacloud_esa20240910 alibabacloud_tea_openapi alibabacloud_credentials
```

### Namespace Management

```python
from alibabacloud_esa20240910.client import Client as Esa20240910Client
from alibabacloud_esa20240910 import models as esa_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str = "cn-hangzhou") -> Esa20240910Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint="esa.cn-hangzhou.aliyuncs.com",
    )
    return Esa20240910Client(config)


# Create namespace
def create_namespace(name: str, description: str = ""):
    client = create_client()
    request = esa_models.CreateKvNamespaceRequest(
        namespace=name,
        description=description,
    )
    return client.create_kv_namespace(request)


# List all namespaces (via GetKvAccount)
def list_namespaces():
    client = create_client()
    request = esa_models.GetKvAccountRequest()
    resp = client.get_kv_account(request)
    return resp.body


# Delete namespace
def delete_namespace(name: str):
    client = create_client()
    request = esa_models.DeleteKvNamespaceRequest(namespace=name)
    return client.delete_kv_namespace(request)
```

### Key-Value Operations

```python
# Write key-value pair
def put_kv(namespace: str, key: str, value: str, ttl: int = None):
    client = create_client()
    request = esa_models.PutKvRequest(
        namespace=namespace,
        key=key,
        value=value,
    )
    if ttl:
        request.expiration_ttl = ttl
    return client.put_kv(request)


# Read key's value
def get_kv(namespace: str, key: str):
    client = create_client()
    request = esa_models.GetKvRequest(
        namespace=namespace,
        key=key,
    )
    return client.get_kv(request)


# Delete key-value pair
def delete_kv(namespace: str, key: str):
    client = create_client()
    request = esa_models.DeleteKvRequest(
        namespace=namespace,
        key=key,
    )
    return client.delete_kv(request)


# List keys
def list_kvs(namespace: str, prefix: str = None):
    client = create_client()
    request = esa_models.ListKvsRequest(
        namespace=namespace,
        prefix=prefix,
    )
    return client.list_kvs(request)
```

### Batch Operations

```python
import json

# Batch write
def batch_put_kv(namespace: str, items: list):
    """items: [{"Key": "k1", "Value": "v1", "ExpirationTtl": 3600}, ...]"""
    client = create_client()
    request = esa_models.BatchPutKvRequest(
        namespace=namespace,
    )
    # body is JSON string
    request.body = json.dumps(items).encode("utf-8")
    return client.batch_put_kv(request)


# Batch delete
def batch_delete_kv(namespace: str, keys: list):
    """keys: ["key1", "key2", ...]"""
    client = create_client()
    request = esa_models.BatchDeleteKvRequest(
        namespace=namespace,
    )
    request.body = json.dumps(keys).encode("utf-8")
    return client.batch_delete_kv(request)
```

## Using KV in Edge Routine

In Edge Routine code, you need to create an instance via `new EdgeKV({namespace: "..."})` to access KV storage (no global instance, must be explicitly created each time):

```javascript
export default {
  async fetch(request) {
    const kv = new EdgeKV({ namespace: "my-namespace" });

    // Write
    await kv.put("key1", "value1");

    // Read
    const value = await kv.get("key1");

    // Delete
    await kv.delete("key1");

    return new Response(value || "not found");
  },
};
```

## Common Workflows

### 1. Initialize KV Storage

```
DescribeKvAccountStatus → (Enable if not enabled)
CreateKvNamespace → PutKv / BatchPutKv → ListKvs verify
```

### 2. Configuration Distribution (Edge Config Hot Update)

```
1. Write config via OpenAPI: PutKv(namespace="config", key="feature-flags", value=json)
2. Edge Routine reads config: new EdgeKV({namespace: "config"}).get("feature-flags")
3. Update config by calling PutKv again, edge nodes sync automatically
```

### 3. Data Cleanup

```
ListKvs(prefix="temp-") → Filter keys to delete → BatchDeleteKv
```

## Common Error Codes

| HTTP | Error Code | Description |
|------|------------|-------------|
| 400 | InvalidNameSpace.Malformed | Invalid namespace name (e.g. empty string) |
| 400 | InvalidKey.Malformed | Invalid key name (e.g. empty string) |
| 400 | InvalidKey.ExceedsMaximum | Key length exceeds 512 bytes |
| 400 | InvalidValue.ExceedsMaximum | Value exceeds 2MB (or 25MB) |
| 404 | InvalidNameSpace.NotFound | Namespace does not exist |
| 404 | InvalidKey.NotFound | Key does not exist |
| 406 | InvalidNameSpace.Duplicate | Namespace already exists |
| 406 | InvalidNameSpace.QuotaFull | Namespace quota exceeded |
| 403 | InvalidKey.ExceedsCapacity | Namespace capacity full |
| 429 | TooQuickRequests | Modify/delete operations too frequent |
