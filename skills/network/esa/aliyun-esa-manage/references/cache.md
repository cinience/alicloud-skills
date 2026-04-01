# ESA Cache

Cache rules for ESA sites.

## Cache Rules

Cache rules control how content is cached at ESA edge nodes.

### Common operations

- Create: `CreateCacheRule`
- List: `ListCacheRules`
- Query: `GetCacheRule`
- Update: `UpdateCacheRule`
- Delete: `DeleteCacheRule`

### Rule types

- `global`: Site-wide default cache configuration
- `rule`: Conditional rule with match expression

### CreateCacheRule parameters

Parameters are **flat** (not a nested JSON object). Key parameters:

Required:
- `SiteId`: Site ID (Long)
- `Rule`: Match condition expression (String). **For rule expression syntax, see `rule-generation-guide.md` and related rule reference files in this directory.**

Optional:
- `RuleName`: Rule name (not required for `global` type)
- `RuleEnable`: `on` / `off` (not required for `global` type)
- `EdgeCacheMode`: Edge cache mode
  - `follow_origin`: Follow origin cache policy (default)
  - `no_cache`: Do not cache
  - `override_origin`: Override origin cache policy
  - `follow_origin_bypass`: Follow origin if exists, otherwise no cache
- `EdgeCacheTtl`: Edge cache TTL in seconds (e.g. 864000 = 10 days)
- `BrowserCacheMode`: Browser cache mode (`no_cache`, `follow_origin`, `override_origin`)
- `BrowserCacheTtl`: Browser cache TTL in seconds
- `QueryStringMode`: Query string handling (`ignore_all`, `exclude_query_string`, `reserve_all`, `include_query_string`)
- `BypassCache`: Bypass cache mode (`cache_all`, `bypass_all`)
- `ServeStale`: Serve stale cache when origin unavailable (`on`/`off`)
- `SortQueryStringForCache`: Sort query string for cache key (`on`/`off`)

### Rule expression syntax

**See rule expression reference files in this directory for complete documentation:**
- `rule-generation-guide.md` - Generation guide from natural language
- `rule-match-fields.md` - All match fields (HTTP, IP/Geo, Map fields)
- `rule-operators.md` - All operators (string/numeric comparison, function-style, negation, logical)
- `rule-examples.md` - Scenario examples and common mistakes

Quick reminder for cache rules:
- Parameters are **flat** (not a nested JSON `Rule` object).
- `ends_with`/`starts_with` use **function-call syntax**: `(ends_with(http.request.uri, ".html"))`.
- `matches` (regex) requires standard plan or above.

### Cache TTL options

- Override origin: set `EdgeCacheMode` to `override_origin` + `EdgeCacheTtl` in seconds
- Follow origin: set `EdgeCacheMode` to `follow_origin`
- Browser cache: set `BrowserCacheMode` + `BrowserCacheTtl`
- Common TTL values: 3600 (1h), 86400 (1d), 604800 (7d), 864000 (10d), 2592000 (30d)

## Tiered Cache

Multi-level cache architecture configuration.

- `GetTieredCache`: Get current tiered cache config
- `UpdateTieredCache`: Update tiered cache config

Cache architecture modes:
- `edge_regional`: Regional edge caching
- `edge_smart`: Smart edge caching

## Cache Tag

Cache tag configuration for granular cache control.

- `GetCacheTag`: Get cache tag config
- `UpdateCacheTag`: Update cache tag config

## References

- CreateCacheRule: https://help.aliyun.com/zh/esa/developer-reference/api-esa-2024-09-10-createcacherule
- ListCacheRules: https://help.aliyun.com/zh/esa/developer-reference/api-esa-2024-09-10-listcacherules
