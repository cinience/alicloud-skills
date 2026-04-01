# ESA Rule Expression - Scenario Examples

Practical examples for common ESA rule expression scenarios.

## Static Resource Caching

```bash
# Cache all images (single extension)
--Rule '(http.request.uri.path.extension eq "jpg")'

# Cache multiple static resource types
--Rule '(http.request.uri.path.extension in {"js" "css" "png" "jpg" "gif" "ico" "woff2" "svg" "webp"})'

# Cache specific file
--Rule '(http.request.uri.path.full_file_name eq "index.html")'

# Cache all HTML pages
--Rule '(ends_with(http.request.uri, ".html"))'
```

## URL Path Matching

```bash
# Match URL prefix (API path)
--Rule '(starts_with(http.request.uri, "/api/"))'

# Match URL suffix
--Rule '(ends_with(http.request.uri, ".json"))'

# Match URL containing substring (MUST start with /)
--Rule '(http.request.uri contains "/test")'
--Rule '(http.request.uri.path contains "/dynamic")'

# Exclude admin path from caching
--Rule '(not starts_with(http.request.uri, "/admin/"))'

# Exclude multiple paths
--Rule '(not starts_with(http.request.uri, "/admin/") and not starts_with(http.request.uri, "/internal/"))'
```

## Domain / Host Matching

```bash
# Match specific hostname
--Rule '(http.host eq "static.example.com")'

# Match multiple domains
--Rule '(http.host in {"cdn1.example.com" "cdn2.example.com" "cdn3.example.com"})'

# Match domain suffix (e.g. all .cn domains) - requires standard plan
--Rule '(ends_with(http.host, ".cn"))'

# Match domain prefix
--Rule '(starts_with(http.host, "api."))'

# Exclude specific domain
--Rule '(http.host ne "internal.example.com")'
```

## Geo / IP Matching

```bash
# Match by country
--Rule '(ip.geoip.country eq "CN")'

# Match multiple countries
--Rule '(ip.geoip.country in {"CN" "JP" "KR"})'

# Match by continent (Asia)
--Rule '(ip.geoip.continent eq "AS")'

# Match by AS number
--Rule '(ip.geoip.asnum eq 45104)'

# Match IPv6 traffic
--Rule '(ip.src.version eq "IPv6")'
```

## Request Method Matching

```bash
# Match GET requests only
--Rule '(http.request.method eq "GET")'

# Match POST requests
--Rule '(http.request.method eq "POST")'

# Match non-GET requests
--Rule '(http.request.method ne "GET")'
```

## Header / Cookie / Query Matching

```bash
# Match if authorization header exists
--Rule '(exists(http.request.headers["authorization"]))'

# Match if specific cookie exists
--Rule '(exists(http.request.cookies["session"]))'

# Match if query parameter exists
--Rule '(exists(http.request.uri.args["nocache"]))'

# Match by cookie length
--Rule '(len(http.request.cookies["session"]) gt 1024)'

# Match if no authorization header (unauthenticated)
--Rule '(not exists(http.request.headers["authorization"]))'
```

## Combined Conditions

```bash
# Specific domain + static resources
--Rule '(http.host eq "www.example.com" and http.request.uri.path.extension in {"js" "css" "png"})'

# Specific domain + path prefix
--Rule '(http.host eq "www.example.com" and starts_with(http.request.uri, "/static/"))'

# Static resources but exclude admin
--Rule '(http.request.uri.path.extension in {"js" "css" "png" "jpg"} and not starts_with(http.request.uri, "/admin/"))'

# GET requests from China to HTML pages
--Rule '(http.request.method eq "GET" and ip.geoip.country eq "CN" and ends_with(http.request.uri, ".html"))'

# HTTPS only + specific domain
--Rule '(ssl eq true and http.host eq "secure.example.com")'
```

## OR Conditions (Multiple Rule Groups)

```bash
# Match either domain
--Rule '(http.host eq "a.example.com") or (http.host eq "b.example.com")'

# Match API path OR static resources
--Rule '(starts_with(http.request.uri, "/api/")) or (http.request.uri.path.extension in {"js" "css" "png"})'

# Match China OR Japan traffic
--Rule '(ip.geoip.country eq "CN") or (ip.geoip.country eq "JP")'
```

## Case-Insensitive Matching

```bash
# Case-insensitive URL match (use lower() wrapper)
--Rule '(lower(http.request.uri) eq "/readme.html")'

# Case-insensitive host match
--Rule '(lower(http.host) eq "www.example.com")'
```

## Regex Examples (Standard Plan and Above)

```bash
# Match versioned API paths
--Rule '(http.request.uri matches "^/api/v[0-9]+")'

# Match image files by extension
--Rule '(http.request.uri matches "\\.(jpg|png|gif|webp)$")'

# Match subdomains pattern
--Rule '(http.host matches "^(www|blog|docs)\\.example\\.com$")'
```
