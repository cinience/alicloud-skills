# ESA Rule Expression - Match Fields

Complete list of match fields available in ESA rule expressions.

## Standard Fields (HTTP Request)

| Field | Type | Supported Operators | Example |
|-------|------|---------------------|---------|
| `http.host` | String | `in`, `eq`, `ne`, `contains`, `matches`, `starts_with`, `ends_with`, `in_list` | `http.host in {"example.com"}` |
| `http.cookie` | String | `in`, `eq`, `ne`, `contains`, `matches` | `http.cookie contains "PHPSESSID"` |
| `http.referer` | String | `in`, `eq`, `ne`, `contains`, `matches` | `http.referer contains "google.com"` |
| `http.request.method` | String | `in`, `eq`, `ne` | `http.request.method in {"GET" "POST"}` |
| `http.request.uri` | String | `in`, `eq`, `ne`, `contains`, `matches`, `starts_with`, `ends_with` | `http.request.uri contains "/test"` |
| `http.request.uri.path` | String | `in`, `eq`, `ne`, `contains`, `matches`, `starts_with`, `ends_with` | `starts_with(http.request.uri.path, "/api")` |
| `http.request.uri.path.extension` | String | `in`, `eq`, `ne` | `http.request.uri.path.extension in {"jpg" "png"}` |
| `http.request.uri.path.file_name` | String | `in`, `eq`, `ne` | `http.request.uri.path.file_name eq "index"` |
| `http.request.uri.path.full_file_name` | String | `in`, `eq`, `ne` | `http.request.uri.path.full_file_name eq "index.html"` |
| `http.request.uri.query` | String | `in`, `eq`, `ne`, `contains`, `matches`, `starts_with`, `ends_with` | `http.request.uri.query contains "utm_source"` |
| `http.request.full_uri` | String | `in`, `eq`, `ne`, `contains`, `matches`, `starts_with`, `ends_with` | `http.request.full_uri eq "http://example.com/api"` |
| `http.request.version` | String | `in`, `eq`, `ne` | `http.request.version eq "HTTP/2.0"` |
| `http.request.scheme` | String | `eq` | `http.request.scheme eq "https"` |
| `http.user_agent` | String | `in`, `eq`, `ne`, `contains`, `matches` | `http.user_agent contains "bot"` |
| `http.x_forwarded_for` | String | `in`, `eq`, `ne`, `contains`, `matches` | `http.x_forwarded_for eq "192.168.1.1"` |
| `http.request.body.mime` | String | `eq`, `ne` | `http.request.body.mime eq "application/json"` |
| `http.request.timestamp.sec` | Integer | `eq`, `ne`, `le`, `ge`, `lt`, `gt` | `http.request.timestamp.sec gt 1735019278` |

**HTTP version values**: `HTTP/1.0`, `HTTP/1.1`, `HTTP/2.0`, `HTTP/3.0`

## Map Fields (support key access with `["key"]`)

| Field | Type | Description | Access example |
|-------|------|-------------|---------------|
| `http.request.headers` | Object | Request headers | `http.request.headers["accept"]` |
| `http.request.cookies` | Map | Individual cookies | `http.request.cookies["session"]` |
| `http.request.uri.args` | Map | Query parameters | `http.request.uri.args["page"]` |
| `http.request.body.form` | Map | Form body fields | `http.request.body.form["username"]` |

## IP / Geo Fields

| Field | Type | Supported Operators | Example |
|-------|------|---------------------|---------|
| `ip.src` | IP | `in`, `eq`, `ne`, `in_list` | `ip.src in {192.168.1.1 10.0.0.5}` |
| `ip.geoip.country` | String | `in`, `eq`, `ne` | `ip.geoip.country eq "CN"` |
| `ip.geoip.continent` | String | `in`, `eq`, `ne` | `ip.geoip.continent eq "AS"` |
| `ip.geoip.asnum` | Integer | `in`, `eq`, `ne`, `in_list` | `ip.geoip.asnum eq 45104` |
| `ip.src.isp` | String | `in`, `eq`, `ne` | `ip.src.isp contains "China Telecom"` |
| `ip.src.version` | String | `eq`, `ne` | `ip.src.version eq "IPv4"` |
| `ip.src.subdivision_1_iso_code` | String | `in`, `eq`, `ne` | `ip.src.subdivision_1_iso_code in {"CN-ZJ" "CN-GD"}` |
| `ip.src.region_code` | String | `in`, `eq`, `ne` | `ip.src.region_code eq "us-west-1"` |

**Note**: `ip.geoip.asnum` is an **integer**, do not use quotes.

## Boolean Fields

| Field | Type | Description |
|-------|------|-------------|
| `ssl` | Boolean | Whether the request is HTTPS |

## Extended Fields (advanced, may require specific plan)

| Field | Type | Description |
|-------|------|-------------|
| `ali.ja3_hash` | String | JA3 TLS fingerprint hash |
| `ali.ja4` | String | JA4 TLS fingerprint |
| `ali.js_detection.passed` | Boolean | Whether JS challenge passed |
| `ali.static_resource` | Boolean | Whether request is for a static resource |
| `ali.tls_client_auth.cert_verified` | Boolean | Whether client TLS cert is verified |
| `ali.tls_hash` | String | TLS hash |

## Field selection guidance

| Scenario | Recommended field |
|----------|------------------|
| Match by domain | `http.host` |
| Match URL path or suffix | `http.request.uri` |
| Match file type | `http.request.uri.path.extension` |
| Match specific file | `http.request.uri.path.full_file_name` |
| Match query parameter | `http.request.uri.args["key"]` |
| Match by country | `ip.geoip.country` |
| Match by IP | `ip.src` |
| Match by request method | `http.request.method` |
| Match by header | `http.request.headers["header-name"]` |
| Match by cookie | `http.request.cookies["cookie-name"]` |

## Notes

- Not all fields are available for all rule types. If a field causes `CompileRuleError`, try a related field (e.g. use `http.request.uri` instead of `http.request.uri.path`).
- Map fields accessed with `["key"]` return the value for that key as a string.
- Extended fields (`ali.*`) may require specific plan levels or feature activation.
