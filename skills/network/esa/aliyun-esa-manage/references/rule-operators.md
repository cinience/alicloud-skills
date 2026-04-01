# ESA Rule Expression - Operators

Complete list of operators available in ESA rule expressions.

## Forbidden Operator Formats (CRITICAL)

These formats are **ABSOLUTELY FORBIDDEN** and will cause errors:

| Forbidden Format | Why | Correct Alternative |
|------------------|-----|---------------------|
| `not...eq` | Invalid syntax | Use `ne` |
| `not...ne` | Invalid syntax | Use `eq` |
| `not in` | Wrong position | Use `not...in` (not before field) |
| `not contains` | Wrong position | Use `not...contains` (not before field) |
| `not matches` | Wrong position | Use `not...matches` (not before field) |
| `field ends_with "value"` | Wrong syntax | Use `ends_with(field, "value")` |
| `field starts_with "value"` | Wrong syntax | Use `starts_with(field, "value")` |

**Correct negation patterns:**
```
# Negating equality
WRONG:  not http.host eq "a.com"
RIGHT:  http.host ne "a.com"

# Negating set membership
WRONG:  http.host not in {"a.com" "b.com"}
RIGHT:  not http.host in {"a.com" "b.com"}

# Negating contains
WRONG:  http.request.uri not contains "/test"
RIGHT:  not http.request.uri contains "/test"
```

## String Comparison (Infix Style)

Syntax: `(field operator "value")`

| Operator | Description | Syntax | Example |
|----------|-------------|--------|---------|
| `eq` | Equal to | `(field eq "value")` | `(http.host eq "www.example.com")` |
| `ne` | Not equal to | `(field ne "value")` | `(http.host ne "test.example.com")` |
| `contains` | Contains substring | `(field contains "value")` | `(http.request.uri contains "/test")` |
| `in` | In a set of values | `(field in {"v1" "v2"})` | `(http.host in {"a.com" "b.com"})` |
| `matches` | Regex match (PCRE) | `(field matches "regex")` | `(http.request.uri matches "^/api/v[0-9]+")` |

**Important notes:**
- `in` uses **space-separated** values in braces, NOT comma-separated: `{"a" "b" "c"}`
- `matches` requires **standard plan or above**; basic plan returns `RuleRegexQuotaCheckFailed`
- `contains` works with `http.request.uri` and `http.host`. When matching URI, include the path separator (e.g. `"/test"` not `"test"`)

## String Comparison (Function Style)

Syntax: `(function(field, "value"))`

| Operator | Description | Syntax | Example |
|----------|-------------|--------|---------|
| `starts_with` | Starts with prefix | `(starts_with(field, "value"))` | `(starts_with(http.request.uri, "/api/"))` |
| `ends_with` | Ends with suffix | `(ends_with(field, "value"))` | `(ends_with(http.request.uri, ".html"))` |

**Critical:** `starts_with` and `ends_with` **MUST** use function-call syntax. Infix syntax like `(field ends_with "value")` will cause `CompileRuleError`.

## Numeric Comparison (Infix Style)

Syntax: `(field operator number)`

| Operator | Description | Syntax | Example |
|----------|-------------|--------|---------|
| `eq` | Equal to | `(field eq num)` | `(ip.geoip.asnum eq 45104)` |
| `ne` | Not equal to | `(field ne num)` | `(ip.geoip.asnum ne 45104)` |
| `lt` | Less than | `(field lt num)` | `(ip.geoip.asnum lt 45104)` |
| `le` | Less than or equal | `(field le num)` | `(ip.geoip.asnum le 45104)` |
| `gt` | Greater than | `(field gt num)` | `(ip.geoip.asnum gt 45104)` |
| `ge` | Greater than or equal | `(field ge num)` | `(ip.geoip.asnum ge 45104)` |

## Length Check (Function Style)

Syntax: `(len(field) operator number)`

| Operator | Description | Syntax | Example |
|----------|-------------|--------|---------|
| `len eq` | Length equals | `(len(field) eq num)` | `(len(http.cookie) eq 100)` |
| `len gt` | Length greater than | `(len(field) gt num)` | `(len(http.cookie) gt 1024)` |
| `len lt` | Length less than | `(len(field) lt num)` | `(len(http.request.uri) lt 2048)` |

## Existence Check (Function Style)

| Operator | Description | Syntax | Example |
|----------|-------------|--------|---------|
| `exists` | Field exists | `(exists(field))` | `(exists(http.request.headers["authorization"]))` |
| `not exists` | Field not exists | `(not exists(field))` | `(not exists(http.request.headers["authorization"]))` |

## Transformation (Function Style)

| Function | Description | Syntax | Example |
|----------|-------------|--------|---------|
| `lower` | Convert to lowercase | `lower(field)` | `(lower(http.request.uri) contains "api")` |

Use `lower()` for case-insensitive matching by wrapping the field.

## Negation

Any expression can be negated with `not`:

| Operator | Syntax | Example |
|----------|--------|---------|
| `not` | `(not expr)` | `(not http.host contains "test")` |
| `not...contains` | `(not field contains "value")` | `(not http.host contains "staging")` |
| `not...in` | `(not field in {...})` | `(not http.host in {"a.com" "b.com"})` |
| `not...matches` | `(not field matches "regex")` | `(not http.request.uri matches "^/internal")` |
| `not starts_with` | `(not starts_with(field, "v"))` | `(not starts_with(http.request.uri, "/admin"))` |
| `not ends_with` | `(not ends_with(field, "v"))` | `(not ends_with(http.request.uri, ".json"))` |

## Logical Operators

| Operator | Description | Syntax | Example |
|----------|-------------|--------|---------|
| `and` | Both conditions | `(expr1 and expr2)` | `(http.host eq "a.com" and starts_with(http.request.uri, "/api"))` |
| `or` | Either condition | `(expr1) or (expr2)` | `(http.host eq "a.com") or (http.host eq "b.com")` |

**Nesting rules:**
- Max nesting depth: **2 levels**
- `and` conditions go inside the same parentheses: `(A and B and C)`
- `or` conditions separate parenthesized groups: `(A) or (B) or (C)`
- Mixed: `(A and B) or (C and D)`

## Plan Limitations

| Plan | eq/ne/in/starts_with/ends_with | contains | matches (regex) |
|------|-------------------------------|----------|----------------|
| Basic | Supported | Supported | **Not supported** |
| Standard | Supported | Supported | Supported |
| Enterprise | Supported | Supported | Supported |

## Common CompileRuleError causes

1. Using `ends_with`/`starts_with` as infix operators instead of function syntax
2. Using `wildcard` (not a valid ESA operator)
3. Using `contains` with URI but missing path separator (use `"/test"` not `"test"`)
4. Using unsupported match fields for the specific rule type
5. Missing parentheses around the expression
6. Using comma-separated values in `in` instead of space-separated
