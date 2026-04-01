# ALB Access Log Analysis

Source: [ALB Access Logs](https://help.aliyun.com/zh/slb/application-load-balancer/user-guide/access-logs)

> **Run log queries using the `aliyun-sls-log-query` skill.**
> Set `SLS_PROJECT` and `SLS_LOGSTORE` to the ALB access log project/logstore.
> Obtain from `GetLoadBalancerAttribute` → `AccessLogConfig.LogProject` / `AccessLogConfig.LogStore`.

## Log Fields

Log topic: `alb_layer7_access_log`

### Request

| Field | Type | Description |
|---|---|---|
| `request_method` | string | HTTP method |
| `request_uri` | string | Request URI |
| `request_length` | int | Total request length (startline + headers + body), bytes |
| `scheme` | string | `HTTP` or `HTTPS` |
| `server_protocol` | string | HTTP protocol version (`HTTP/1.0`, `HTTP/1.1`) |
| `host` | string | Domain or IP — from request params, then Host header, then backend IP |
| `http_host` | string | Host header value |
| `http_referer` | string | Referer header |
| `http_user_agent` | string | User-Agent header |
| `http_x_forwarded_for` | string | X-Forwarded-For header |
| `http_x_real_ip` | string | X-Real-IP header |
| `slb_headers` | string | Custom headers (requires feature enablement, default 1 KB, max 4 KB) |

### Client

| Field | Type | Description |
|---|---|---|
| `client_ip` | string | Client IP. With "real client source IP" enabled, shows the real client IP; otherwise shows previous hop |
| `client_port` | int | Client port |
| `tcpinfo_rtt` | int | Client TCP RTT, **microseconds** |

### ALB Instance

| Field | Type | Description |
|---|---|---|
| `app_lb_id` | string | ALB instance ID |
| `vip_addr` | string | Virtual IP address |
| `slb_vport` | int | Listener port |

### TLS

| Field | Type | Description |
|---|---|---|
| `ssl_protocol` | string | TLS version (e.g. `TLSv1.2`) |
| `ssl_cipher` | string | TLS cipher suite (e.g. `ECDHE-RSA-AES128-GCM-SHA256`) |

### Response & Timing

| Field | Type | Description |
|---|---|---|
| `status` | int | Status code returned by ALB to client |
| `upstream_status` | int | Status code returned by backend |
| `upstream_addr` | string | Backend server IP:port |
| `body_bytes_sent` | int | HTTP body bytes sent to client |
| `request_time` | float | Total request duration (first packet received → response sent), **seconds** |
| `read_request_time` | int | Time ALB spent reading the request, **milliseconds** |
| `upstream_response_time` | float | Time from ALB connecting to backend through receiving data and closing, **seconds** |
| `write_response_time` | int | ALB response write time, **milliseconds** |

### Tracing

| Field | Type | Description |
|---|---|---|
| `slb_xtrace` | string | Trace link TraceId |
| `xtrace_type` | string | Trace type (currently only `Zipkin`) |

### Meta

| Field | Type | Description |
|---|---|---|
| `time` | string | Log timestamp, `YYYY-MM-DDThh:mm:ssZ` |
| `__topic__` | string | Always `alb_layer7_access_log` |

## SLS Query Templates

### 5xx error distribution

```sql
status >= 500 | SELECT status, upstream_status, count(*) AS cnt
  GROUP BY status, upstream_status ORDER BY cnt DESC LIMIT 20
```

### 4xx error distribution

```sql
status >= 400 AND status < 500 | SELECT status, request_uri, count(*) AS cnt
  GROUP BY status, request_uri ORDER BY cnt DESC LIMIT 20
```

### 502 errors with backend detail

```sql
status:502 | SELECT upstream_addr, upstream_status, count(*) AS cnt
  GROUP BY upstream_addr, upstream_status ORDER BY cnt DESC
```

### Slow requests Top 20 (by upstream_response_time)

```sql
* | SELECT request_uri, upstream_addr,
    avg(upstream_response_time) AS avg_rt,
    max(upstream_response_time) AS max_rt,
    count(*) AS cnt
  GROUP BY request_uri, upstream_addr
  ORDER BY avg_rt DESC LIMIT 20
```

### Latency breakdown (read / upstream / write)

```sql
* | SELECT
    avg(read_request_time) AS avg_read_ms,
    avg(upstream_response_time * 1000) AS avg_upstream_ms,
    avg(write_response_time) AS avg_write_ms,
    avg(request_time * 1000) AS avg_total_ms
```

### Top client IPs

```sql
* | SELECT client_ip, count(*) AS cnt
  GROUP BY client_ip ORDER BY cnt DESC LIMIT 20
```

### Traffic by URI path

```sql
* | SELECT request_uri, count(*) AS pv,
    sum(body_bytes_sent) AS total_bytes
  GROUP BY request_uri ORDER BY pv DESC LIMIT 20
```

### Backend server error rate

```sql
* | SELECT upstream_addr,
    count_if(upstream_status >= 500) AS err_5xx,
    count(*) AS total,
    round(count_if(upstream_status >= 500) * 100.0 / count(*), 2) AS err_rate
  GROUP BY upstream_addr ORDER BY err_rate DESC LIMIT 20
```

### Request volume trend (per minute)

```sql
* | SELECT date_trunc('minute', __time__) AS t, count(*) AS qps
  GROUP BY t ORDER BY t
```

### Requests for a specific backend server

```sql
upstream_addr:172.16.0.x | SELECT time, client_ip, request_uri,
    status, upstream_status, request_time, upstream_response_time
  ORDER BY time DESC LIMIT 100
```

### High-RTT clients

```sql
* | SELECT client_ip, avg(tcpinfo_rtt / 1000.0) AS avg_rtt_ms, count(*) AS cnt
  GROUP BY client_ip HAVING avg_rtt_ms > 100
  ORDER BY avg_rtt_ms DESC LIMIT 20
```
