# Edge KV — 边缘键值存储参考文档

ESA Edge KV 是分布式边缘键值存储服务，可在 Edge Routine 中读写数据，也可通过 OpenAPI 管理。适用于边缘配置分发、特征标记、A/B 测试等场景。

## 核心概念

- **Namespace（存储空间）**: KV 数据的隔离容器，每个账号可创建多个 namespace
- **Key**: 键名，最大 512 字符，不允许包含空格和反斜杠
- **Value**: 值，标准 API 最大 2MB，高容量 API 最大 25MB
- **TTL**: 可选的过期时间，支持绝对时间戳（Expiration）或相对秒数（ExpirationTtl）

## 限制

| 限制项 | 值 |
|--------|-----|
| Key 最大长度 | 512 字符 |
| 单个 Value 最大 (PutKv/BatchPutKv) | 2 MB |
| 单个 Value 最大 (PutKvWithHighCapacity) | 25 MB |
| 批量请求体最大 (BatchPutKvWithHighCapacity/BatchDeleteKvWithHighCapacity) | 100 MB |
| BatchDeleteKv 单次最多删除 | 10,000 个键 |
| 单个 Namespace 最大容量 | 1 GB |
| ListKvs 分页限制 | PageNumber × PageSize ≤ 50,000 |

## API 列表

### Namespace 管理

| API | 描述 | 关键参数 |
|-----|------|----------|
| `CreateKvNamespace` | 创建 KV 存储空间 | `Namespace`(必填, string), `Description`(可选) |
| `DeleteKvNamespace` | 删除 KV 存储空间 | `Namespace`(必填, string) |
| `GetKvNamespace` | 查询单个 namespace 信息 | `Namespace`(必填, string) |
| `GetKvAccount` | 查询账户 KV 使用信息及所有 namespace | 无参数 |
| `DescribeKvAccountStatus` | 查询 Edge KV 是否已开通 | 无参数 |

### 单键操作

| API | 描述 | 关键参数 |
|-----|------|----------|
| `PutKv` | 写入键值对 (≤2MB) | `Namespace`(必填), `Key`(必填), `Value`(body, 必填), `Expiration`(可选, Unix时间戳), `ExpirationTtl`(可选, 秒), `Base64`(可选, bool) |
| `PutKvWithHighCapacity` | 写入大容量键值对 (≤25MB) | 同 PutKv，但需通过 SDK body 方式 |
| `GetKv` | 读取键的值 | `Namespace`(必填), `Key`(必填), `Base64`(可选, bool) |
| `GetKvDetail` | 读取键值及 TTL | `Namespace`(必填), `Key`(必填) |
| `DeleteKv` | 删除键值对 | `Namespace`(必填), `Key`(必填) |

### 批量操作

| API | 描述 | 关键参数 |
|-----|------|----------|
| `BatchPutKv` | 批量写入键值对 (≤2MB) | `Namespace`(必填), body 为 JSON 数组 `[{Key, Value, Expiration?, ExpirationTtl?}]` |
| `BatchPutKvWithHighCapacity` | 批量写入大容量 (≤100MB) | 同上，通过 SDK body 方式 |
| `BatchDeleteKv` | 批量删除键值对 (≤10000个) | `Namespace`(必填), body 为 JSON 数组 `["key1", "key2", ...]` |
| `BatchDeleteKvWithHighCapacity` | 批量删除大容量 (≤100MB) | 同上，通过 SDK body 方式 |
| `ListKvs` | 列出 namespace 中所有键 | `Namespace`(必填), `Prefix`(可选), `PageNumber`(可选), `PageSize`(可选, 默认20, 最大100) |

## Python SDK 用法

### 安装

```bash
pip install alibabacloud_esa20240910 alibabacloud_tea_openapi alibabacloud_credentials
```

### Namespace 管理

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


# 创建 namespace
def create_namespace(name: str, description: str = ""):
    client = create_client()
    request = esa_models.CreateKvNamespaceRequest(
        namespace=name,
        description=description,
    )
    return client.create_kv_namespace(request)


# 列出所有 namespace（通过 GetKvAccount）
def list_namespaces():
    client = create_client()
    request = esa_models.GetKvAccountRequest()
    resp = client.get_kv_account(request)
    return resp.body


# 删除 namespace
def delete_namespace(name: str):
    client = create_client()
    request = esa_models.DeleteKvNamespaceRequest(namespace=name)
    return client.delete_kv_namespace(request)
```

### 键值操作

```python
# 写入键值对
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


# 读取键的值
def get_kv(namespace: str, key: str):
    client = create_client()
    request = esa_models.GetKvRequest(
        namespace=namespace,
        key=key,
    )
    return client.get_kv(request)


# 删除键值对
def delete_kv(namespace: str, key: str):
    client = create_client()
    request = esa_models.DeleteKvRequest(
        namespace=namespace,
        key=key,
    )
    return client.delete_kv(request)


# 列出键
def list_kvs(namespace: str, prefix: str = None):
    client = create_client()
    request = esa_models.ListKvsRequest(
        namespace=namespace,
        prefix=prefix,
    )
    return client.list_kvs(request)
```

### 批量操作

```python
import json

# 批量写入
def batch_put_kv(namespace: str, items: list):
    """items: [{"Key": "k1", "Value": "v1", "ExpirationTtl": 3600}, ...]"""
    client = create_client()
    request = esa_models.BatchPutKvRequest(
        namespace=namespace,
    )
    # body 为 JSON 字符串
    request.body = json.dumps(items).encode("utf-8")
    return client.batch_put_kv(request)


# 批量删除
def batch_delete_kv(namespace: str, keys: list):
    """keys: ["key1", "key2", ...]"""
    client = create_client()
    request = esa_models.BatchDeleteKvRequest(
        namespace=namespace,
    )
    request.body = json.dumps(keys).encode("utf-8")
    return client.batch_delete_kv(request)
```

## Edge Routine 中使用 KV

在 Edge Routine 代码中，需要通过 `new EdgeKV({namespace: "..."})` 创建实例来访问 KV 存储（没有全局实例，每次需显式创建）：

```javascript
export default {
  async fetch(request) {
    const kv = new EdgeKV({ namespace: "my-namespace" });

    // 写入
    await kv.put("key1", "value1");

    // 读取
    const value = await kv.get("key1");

    // 删除
    await kv.delete("key1");

    return new Response(value || "not found");
  },
};
```

## 常见工作流

### 1. 初始化 KV 存储

```
DescribeKvAccountStatus → (未开通则需先开通)
CreateKvNamespace → PutKv / BatchPutKv → ListKvs 验证
```

### 2. 配置分发（边缘配置热更新）

```
1. 通过 OpenAPI 写入配置: PutKv(namespace="config", key="feature-flags", value=json)
2. Edge Routine 读取配置: new EdgeKV({namespace: "config"}).get("feature-flags")
3. 更新配置只需再次 PutKv，边缘节点自动同步
```

### 3. 数据清理

```
ListKvs(prefix="temp-") → 筛选需要删除的键 → BatchDeleteKv
```

## 常见错误码

| HTTP | 错误码 | 说明 |
|------|--------|------|
| 400 | InvalidNameSpace.Malformed | namespace 名称无效（如空字符串） |
| 400 | InvalidKey.Malformed | Key 名称无效（如空字符串） |
| 400 | InvalidKey.ExceedsMaximum | Key 长度超过 512 字节 |
| 400 | InvalidValue.ExceedsMaximum | Value 超过 2MB (或 25MB) |
| 404 | InvalidNameSpace.NotFound | namespace 不存在 |
| 404 | InvalidKey.NotFound | Key 不存在 |
| 406 | InvalidNameSpace.Duplicate | namespace 已存在 |
| 406 | InvalidNameSpace.QuotaFull | namespace 数量超限 |
| 403 | InvalidKey.ExceedsCapacity | namespace 容量已满 |
| 429 | TooQuickRequests | 修改/删除操作过于频繁 |
