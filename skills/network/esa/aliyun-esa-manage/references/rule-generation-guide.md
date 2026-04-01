# ESA Rule Expression - Generation Guide

This guide provides detailed rules for generating correct ESA rule expressions from natural language requirements.

## Operator Usage Rules (CRITICAL)

### Forbidden Operator Formats

These formats will cause errors - **NEVER USE THEM**:

| Forbidden Format | Correct Alternative |
|------------------|---------------------|
| `not...eq` | Use `ne` instead |
| `not...ne` | Use `eq` instead |
| `not in` | Use `not...in` (with space) |
| `not contains` | Use `not...contains` (with space) |
| `not matches` | Use `not...matches` (with space) |

### Operator Selection by User Expression

| User Expression | Operator | Example |
|-----------------|----------|---------|
| "equals/is/为" | `eq` | `http.host eq "example.com"` |
| "not equals/is not/不等于" | `ne` | `http.host ne "test.com"` |
| "contains the following/包含以下各项" | `in` + set | `http.host in {"a.com" "b.com"}` |
| "does not contain the following/不包含以下各项" | `not...in` + set | `not http.host in {"a.com" "b.com"}` |
| "contains/包含" (substring) | `contains` | `http.request.uri contains "/test"` |
| "does not contain/不包含" (substring) | `not...contains` | `not http.request.uri contains "/test"` |
| "starts with/以...开头" | `starts_with` | `starts_with(http.request.uri, "/api")` |
| "does not start with/不以...开头" | `not starts_with` | `not starts_with(http.request.uri, "/api")` |
| "ends with/以...结尾" | `ends_with` | `ends_with(http.request.uri, ".html")` |
| "does not end with/不以...结尾" | `not ends_with` | `not ends_with(http.request.uri, ".html")` |

## Rule Type Recognition

### Priority 1: Explicit Context

If user mentions rule type explicitly ("cache rule", "HTTPS rule", "version management"), use that type.

### Priority 2: Keywords Inference

| Keywords | Rule Type |
|----------|-----------|
| cache, 缓存, expire, ttl | Cache Rules |
| compress, 压缩, gzip, brotli | Compression Rules |
| HTTPS, SSL/TLS, certificate | HTTPS Rules |
| redirect, 重定向, 301, 302 | Redirect Rules |
| request header, 请求头 | Request Header Modification |
| response header, 响应头 | Response Header Modification |
| rewrite, 重写, url rewrite | URL Rewrite Rules |
| load balance, 负载均衡 | Load Balancing Rules |
| version, 版本, A/B test, 灰度 | Version Management |
| origin, 回源 | Origin Rules |

### Priority 3: Default

If unable to determine, default to **Node Rules** (most versatile).

## Rule Type Field Restrictions

| Rule Type | Allowed Fields |
|-----------|---------------|
| Node Rules | All common fields |
| Load Balancing | Node fields + `ip.src.region_code` + `http.request.timestamp.sec` |
| HTTPS Rules | Only `http.host` (only `eq`/`ne` supported) |
| Version Management | Node fields, but no `in_list`/`not in_list`; `matches` quota-limited |

## URI Field Selection Rule

Choose the correct URI field based on match value format:

| Match Value Format | Use Field |
|-------------------|-----------|
| Starts with `http://` or `https://` (full URL) | `http.request.full_uri` |
| Starts with `/` (path only) | `http.request.uri` |
| Path without protocol | `http.request.uri` |

**Examples:**
```
# Full URL matching
http.request.full_uri eq "http://example.com/api/v1/users"

# Path only matching
http.request.uri eq "/api/v1/users"
http.request.uri contains "/test"
```

**IMPORTANT**: When using `contains` with `http.request.uri`, the value **MUST start with `/`**:
- CORRECT: `http.request.uri contains "/test"`
- WRONG: `http.request.uri contains "test"` (will cause `CompileRuleError`)

## Value Types and Literals

| Type | Format | Example |
|------|--------|---------|
| String | Double quotes, escape `\\` `\"` | `"example.com"` |
| Integer | No quotes | `30`, `45104` |
| Boolean | Direct use | `ssl`, `not ssl` |
| IP | Single or CIDR | `192.168.1.1`, `192.168.0.0/24` |
| Set | Space-separated in braces | `{"a.com" "b.com" "c.com"}` |
| Object | Subscript access | `http.request.headers["x-header"]` |

## Special Values

- **Match all requests**: Return `true` (boolean, not string)
- **HTTP version values**: `HTTP/1.0`, `HTTP/1.1`, `HTTP/2.0`, `HTTP/3.0`
- **`ip.geoip.asnum`**: Integer, no quotes

## Logical Operators

- **Priority**: `not` > `and` > `or`
- **Use parentheses** to eliminate ambiguity
- **Max nesting**: 2 levels

**Combination examples:**
```
# AND combination
(http.host eq "example.com" and starts_with(http.request.uri, "/api"))

# OR combination
(http.host eq "a.com") or (http.host eq "b.com")

# Complex combination
(http.request.uri contains "/test" and ip.geoip.country eq "CN")

# Negation with set
(http.host contains "example.com") and (not http.host in {"sub1.example.com" "sub2.example.com"})
```

## Error Examples and Corrections

### Error 1: Using `not...eq`

```
# Input: Requests that are NOT m3u8 files
# WRONG: (not http.request.uri.path.extension eq "m3u8")
# CORRECT: http.request.uri.path.extension ne "m3u8"
```

### Error 2: Using `not in` (wrong syntax)

```
# Input: Exclude jpg and png files
# WRONG: http.request.uri.path.extension not in {"jpg" "png"}
# CORRECT: not http.request.uri.path.extension in {"jpg" "png"}
```

### Error 3: Using `not contains` (wrong syntax)

```
# Input: User-Agent not containing "bot"
# WRONG: http.user_agent not contains "bot"
# CORRECT: not http.user_agent contains "bot"
```

## Generation Flow

1. **Preprocess input**: Extract match conditions, ignore configuration operations
2. **Check "match all"**: If "all requests", return `true`
3. **Identify rule type**: Determine type by keywords and context
4. **Filter allowed fields**: Based on rule type
5. **Select field and operator**: Based on user expression and field support
6. **Apply URI field rule**: Choose `http.request.uri` or `http.request.full_uri`
7. **Type matching**: String with quotes, integer without quotes
8. **Combine expression**: Use parentheses, prefer function-style for prefix/suffix
9. **Error check**: Field range, operator restrictions, type constraints

## Final Checklist

Before output, verify:

1. ✅ Correct operator format (no `not...eq`, `not in`, `not contains`)
2. ✅ Correct field names and syntax
3. ✅ Correct value types (strings quoted, integers unquoted)
4. ✅ Correct set syntax `{value1 value2}`
5. ✅ Correct parentheses grouping and logical operators
6. ✅ Correct URI field selection based on value format
