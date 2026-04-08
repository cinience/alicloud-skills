# Origin Rules — 回源规则配置

Origin Rules 控制 ESA CDN 如何回源到源站，包括回源协议、端口、Host 头和 DNS 记录等。

## 核心概念

- **Origin Rule** 是一条条件匹配 + 回源行为的规则
- 当请求匹配规则条件时，ESA 按规则指定的方式回源，而非使用站点默认源站
- 常用于：为不同子域名指定不同源站、修改回源协议/端口、自定义 Host 头

## API 列表

| 操作 | API | 说明 |
|------|-----|------|
| 创建 | `CreateOriginRule` | 创建回源规则 |
| 查询列表 | `ListOriginRules` | 列出站点下所有回源规则 |
| 查询详情 | `GetOriginRule` | 按 config_id 查询 |
| 更新 | `UpdateOriginRule` | 修改规则 |
| 删除 | `DeleteOriginRule` | 删除规则 |

## 关键参数

### CreateOriginRule

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `site_id` | long | 是 | 站点 ID |
| `rule` | string | 是 | 匹配条件表达式，如 `(http.host eq "sub.example.com")` |
| `origin_scheme` | string | 否 | 回源协议：`http` 或 `https`（默认 `https`） |
| `origin_port` | int | 否 | 回源端口（默认 80/443） |
| `origin_host` | string | 否 | 回源 Host 头 |
| `dns_record` | string | 否 | 回源目标 DNS 记录名 |
| `origin_sni` | string | 否 | HTTPS 回源时的 SNI |

## CDN 代理回源工作流

将子域名通过 ESA CDN 代理到后端服务器的完整流程：

```
1. CreateRecord         → 添加 A 记录 (proxied=true)
2. ApplyCertificate     → 申请免费 SSL 证书
3. CreateOriginRule     → 配置回源协议/端口/DNS记录
4. 验证访问             → curl -sI https://sub.example.com
```

### 步骤详解

#### 1. 创建 DNS 记录

```python
req = esa_models.CreateRecordRequest(
    site_id=SITE_ID,
    record_name='agent.example.com',
    type='A/AAAA',
    data=esa_models.CreateRecordRequestData(value='1.2.3.4'),
    proxied=True,   # 必须开启代理，流量经过 ESA 边缘节点
    ttl=1
)
resp = client.create_record(req)
record_id = resp.body.record_id
```

**注意**: `data` 参数必须使用 `CreateRecordRequestData` 对象，不能传 dict，否则报 `'dict' has no attribute 'validate'`。

#### 2. 申请 SSL 证书

```python
req = esa_models.ApplyCertificateRequest(
    site_id=SITE_ID,
    domains='agent.example.com',
)
resp = client.apply_certificate(req)
# 状态变化: Applying → TOKEN_DEPLOYED → OK
```

#### 3. 创建 Origin Rule

```python
req = esa_models.CreateOriginRuleRequest(
    site_id=SITE_ID,
    rule='(http.host eq "agent.example.com")',
    origin_scheme='http',       # 源站仅支持 HTTP 时必须设置
    origin_port=10112,          # 源站服务端口
    dns_record='agent.example.com',  # ⚠️ 必须是 ESA DNS 记录名
)
resp = client.create_origin_rule(req)
config_id = resp.body.config_id
```

#### 4. 验证

```bash
# 检查 CDN 代理（Server 应为 ESA）
curl -sI https://agent.example.com | head -5

# 直接检查源站（绕过 CDN）
curl -sI http://1.2.3.4:10112 | head -5
```

## 重要坑点

### 1. `dns_record` 必须是 ESA DNS 记录名，不能是原始 IP

```python
# ❌ 错误 — 使用原始 IP 会导致 502 destination_not_found
dns_record='47.117.136.136'

# ✅ 正确 — 使用 ESA DNS 记录名，ESA 内部解析为 A 记录 IP
dns_record='agent.example.com'
```

**原因**: ESA Origin Rule 的 `dns_record` 不是直接指定回源 IP，而是引用 ESA 站点内的 DNS 记录名。ESA 通过该记录名查找对应的 A/AAAA 记录值来确定回源地址。

### 2. `origin_scheme` 默认是 HTTPS

如果源站只监听 HTTP（无 SSL），必须显式设置 `origin_scheme='http'`，否则 ESA 会用 HTTPS 回源导致 502。

```python
# ❌ 不设置 origin_scheme → ESA 默认 HTTPS 回源 → 源站无 SSL → 502
origin_scheme 未设置

# ✅ 显式指定 HTTP 回源
origin_scheme='http'
```

### 3. DNS 记录必须 proxied=True

Origin Rule 仅对经过 ESA 边缘节点的流量生效。如果 DNS 记录 `proxied=False`（DNS only），请求直接到源站 IP，不经过 CDN，Origin Rule 不会被触发。

### 4. Edge Routine Route 优先级高于 Origin Rule

如果某个域名同时绑定了 Edge Routine route 和 Origin Rule，Edge Routine 会拦截请求。要使用 Origin Rule 回源，必须先删除该域名的 Edge Routine route。

```python
# 删除 Edge Routine route
req = esa_models.DeleteRoutineRouteRequest(
    site_id=SITE_ID,
    config_id=ROUTE_CONFIG_ID,
)
client.delete_routine_route(req)
```

### 5. 缓存可能导致旧内容残留

修改 Origin Rule 或切换域名路由后，ESA 边缘节点可能仍缓存旧内容。等待缓存自然过期或通过控制台手动刷新缓存。

## 与 Edge Routine 的对比

| 维度 | Edge Routine | Origin Rule (CDN 代理) |
|------|-------------|----------------------|
| 适用场景 | 静态站点、边缘计算 | 动态服务回源 |
| 流量路径 | 请求在边缘节点处理 | 请求经边缘节点转发到源站 |
| SSL | ESA 边缘终止 | ESA 边缘终止，回源可 HTTP |
| 配置方式 | Routine + Route | DNS 记录 + Origin Rule |
| 优先级 | 高（拦截请求） | 低（仅在无 Route 匹配时生效） |

## 排查清单

当通过 Origin Rule 代理的域名返回异常时：

1. **502 Bad Gateway**
   - 检查 `origin_scheme` 是否与源站一致（HTTP vs HTTPS）
   - 检查 `origin_port` 是否正确
   - 检查源站服务是否运行中

2. **502 destination_not_found**
   - 检查 `dns_record` 是否使用 ESA DNS 记录名（不是 IP）
   - 检查对应的 DNS 记录是否存在

3. **请求仍被 Edge Routine 处理**
   - 检查是否存在匹配该域名的 Edge Routine route
   - 使用 `ListRoutineRoutes` 或 `ListSiteRoutes` 查看

4. **返回旧内容**
   - CDN 缓存未过期，等待或手动刷新
