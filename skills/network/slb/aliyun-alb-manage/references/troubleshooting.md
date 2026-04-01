# ALB Troubleshooting Guide

Source: [ALB FAQ](https://help.aliyun.com/zh/slb/application-load-balancer/support/faq-about-alb), [Status Code Reference](https://help.aliyun.com/zh/slb/application-load-balancer/support/alb-exception-status-code-description), [Health Check Troubleshooting](https://help.aliyun.com/zh/slb/application-load-balancer/support/how-do-i-troubleshoot-health-check-errors)

## 1. Cannot Access Service Through ALB

Diagnostic checklist:

1. **Verify CNAME** — ALB DNS names cannot be accessed directly; custom domain must CNAME to ALB DNS name. Verify with `nslookup` or `dig`.
2. **Check network type** — Private (Intranet) ALB only works within VPC; switch to Internet + bind EIP for public access.
3. **Check ICP filing** — Domains must be ICP-filed for China mainland public access (403 or connection reset otherwise). If ICP was done at another provider, transfer filing to Alibaba Cloud is also required.
4. **Check listeners / forwarding rules** — Verify port, protocol, domain/path matching.
5. **Check health status** — Unhealthy backends prevent proper forwarding. See Section 3 below.
6. **Verify backend directly** — `curl -I http://<backend-IP>:<port>` from the server.
7. **Check security groups** — Ensure listener port and source IPs are allowed.

## 2. High Latency Through ALB

1. Enable access logs, analyze `request_time` and `upstream_response_time`.
2. If `upstream_response_time` is high → backend processing is slow (check app performance, DB, CPU/memory).
3. If `request_time` >> `upstream_response_time` → network issue between client and ALB (use ping/MTR).
4. Cross-region: use Global Accelerator (GA) to reduce latency.

## 3. Health Check Failures

### 3.1 First-time configuration failures

| Cause | Fix |
|---|---|
| Health check parameter misconfiguration | Compare with default parameters as baseline |
| Port/path mismatch | Probe from backend: `curl -X $METHOD -H "Host: $DOMAIN" -I http://$IP:$PORT$PATH` |
| Status code mismatch | Backend returns a valid code (e.g. 302) not in the expected list → update health check success codes |

### 3.2 Previously working, now failing

| Cause | Diagnostic | Fix |
|---|---|---|
| Security software / iptables blocking | `iptables -nL` on backend ECS | Remove blocking rule: `iptables -t filter -D INPUT -s 100.64.0.0/10 -j DROP` |
| Routing misconfiguration (pre-upgrade ALB) | `route -n` — look for 100.64.0.0/10 pointing to wrong gateway | `route del -net 100.64.0.0/10` |
| Backend overloaded | Check CPU/memory/IO on backend | Address resource bottleneck |

### 3.3 ALB health check source IPs

- **Upgraded ALB instances**: use private addresses from the ALB's VSwitch subnet (Local IP).
- **Pre-upgrade ALB instances**: use `100.64.0.0/10` range. Must NOT be blocked by security groups or iptables.

### 3.4 API-based diagnosis

```
1. GetListenerHealthStatus(ListenerId) → NonNormalServers list with ReasonCode
2. ListServerGroupServers(ServerGroupId) → confirm backend IP/port/weight
3. Probe from backend ECS: curl -v http://127.0.0.1:{port}{health_check_path}
```

### 3.5 Health check passes but requests return 502

Health checks use lightweight probes that may succeed while actual requests fail under heavy backend load. Check backend resource utilization.

### 3.6 All backends fail health check

ALB still attempts to forward requests per the scheduling algorithm to minimize business impact. Check logs and health check configuration.

## 4. HTTP Status Codes — ALB Error Reference

Key diagnostic principle: always compare `status` (ALB-returned) vs `upstream_status` (backend-returned) in access logs. When they match, the issue originates from the backend, not ALB.

### 4xx Client Errors

| Code | Cause | Resolution |
|---|---|---|
| **400** | Malformed request; HTTP sent to HTTPS port; request header > 32 KB; incomplete request transmission | Fix client request format; check protocol match; reduce header size |
| **405** | ALB blocks TRACE method; other methods depend on backend support | Use alternative method; verify backend supports the method |
| **408** | Client too slow sending data (default timeout 60s); poor network quality; ALB bandwidth throttling | Check `request_time` and `tcpinfo_rtt` in access logs; increase timeout; check Cloud Monitor bandwidth metrics |
| **414** | URI > 32 KB (ALB limit, not adjustable) | Shorten URI or use POST body (supports up to 50 GB) |
| **463** | Request routing loop — ALB detects duplicate `ALICLOUD-ALB-TRACE` header | Backend is redirecting back to ALB; fix backend config or network architecture |
| **499** | Client closed connection before receiving response | Poor network; backend too slow (`upstream_response_time`); client timeout too short |

### 5xx Server Errors

**500 Internal Server Error**

| Scenario | Diagnostic |
|---|---|
| Backend returns 500 | `upstream_status` = `500` in access logs → investigate backend |
| Backend abnormally closes connection before completing response | Packet capture on backend |

**502 Bad Gateway**

| Scenario | Diagnostic |
|---|---|
| Backend returns 502 directly | `upstream_status` = `502` → backend issue |
| Backend returns other codes (504, 444) but ALB shows 502 | Compare `status` vs `upstream_status` in logs |
| TCP communication failure with backend | Check service status, port listening, TCP handshake |
| Backend backlog full (new connections dropped) | `netstat -s \| grep -i listen` → check for `drop` counts |
| Client packet exceeds backend MTU | Small health check packets succeed but larger packets fail |
| Malformed response or illegal HTTP headers from backend | Packet capture on backend |
| Backend not processing requests in time | Check backend logs, CPU, memory |

**503 Service Temporarily Unavailable**

| Scenario | Diagnostic |
|---|---|
| Backend returns 503 | `upstream_status` = `503` → backend issue |
| ALB rate limiting triggered | `upstream_status` = `-` (request never reached backend); response header `ALB-QPS-Limited: Limited` confirms throttling; check Cloud Monitor "requests per second" metric |
| Direct IP access / DNS anomaly | Traffic concentrates on few IPs → access via ALB domain name with proper CNAME |
| No backends configured or all weights = 0 | Ensure at least one backend with non-zero weight |

**504 Gateway Timeout**

| Scenario | Diagnostic |
|---|---|
| Backend returns 504 | `upstream_status` = `504` → backend issue |
| ALB-to-backend connection timeout | Default 5s, not modifiable; packet capture to find root cause |
| Backend response timeout | Default 60s; check `upstream_response_time` in access logs |

### SLS log query for status code analysis

Use `aliyun-sls-log-query` skill:

```sql
-- Top error status codes with upstream correlation
status >= 400 | SELECT status, upstream_status, count(*) AS cnt
  GROUP BY status, upstream_status ORDER BY cnt DESC LIMIT 20

-- 502 errors with backend detail
status:502 | SELECT upstream_addr, upstream_status, count(*) AS cnt
  GROUP BY upstream_addr, upstream_status ORDER BY cnt DESC
```

## 5. Certificate & HTTPS Issues

| Issue | Resolution |
|---|---|
| Certificate expired | Check validity in SSL Certificate Service console; replace with new certificate |
| Certificate-domain mismatch | Check SNI config with `ListListenerCertificates`; wildcard certs (`*.example.com`) match same-level subdomains only |
| Wildcard cert doesn't match | Only one `*` allowed, must be leftmost; `*.example.com` does NOT match `test.test.example.com`; `*` matches 0-9, letters, hyphens only (no underscores) |
| Cannot upload cert directly to ALB | Upload to SSL Certificate Service console first; ALB references certs from there |
| Browser shows old cert after update | Likely WAF 2.0 transparent integration — force sync by toggling WAF traffic redirection |
| CA mutual auth not working | Only Standard and WAF Enhanced editions support CA mutual auth; Basic edition does not |

## 6. Forwarding Rule Conflicts

```
ListRules(ListenerId) → check all rules' Priority and Conditions
```

- Same listener: Priority values must be unique.
- When conditions overlap, lower Priority value (higher precedence) matches first.
- Check host + path combinations for unintended overlaps.

## 7. ACL Access Control Issues

```
GetListenerAttribute(ListenerId) → AclConfig { AclType, AclRelations }
ListAclEntries(AclId) → check IP entries
```

- `AclType: White` (whitelist): only listed IPs can access.
- `AclType: Black` (blacklist): listed IPs are denied.
- Verify the client's real IP is (or is not) in the ACL list.

## 8. ALB Request Limits

| Parameter | Limit | Adjustable |
|---|---|---|
| URI length | 32 KB max | No |
| Request header | 32 KB max | No |
| Custom header in access logs | 1 KB default, 4 KB max | Via account manager |
| POST body | 50 GB max | — |
| Keep-alive requests per connection | 100 (HTTP); 1000 (HTTPS + HTTP/2.0) | No |
| QUIC Client Hello | ≥ 1024 bytes | Pad with null characters |

Exceeding URI or header limits returns **400** or **414**.

## 9. WAF Integration Notes

| Architecture | Behavior |
|---|---|
| WAF 2.0 transparent | Request → WAF → ALB (two gateways); requires syncing timeouts and certificates on both sides |
| WAF 3.0 service-based | Request → ALB → WAF inspection (single gateway); no sync issues |

- Recommended: WAF 3.0 service-based (WAF Enhanced ALB edition).
- After releasing WAF 2.0, manually enable `X-Forwarded-Proto` header in ALB listener to avoid protocol detection issues (e.g. infinite redirects).

## 10. EIP & Bandwidth

| Issue | Resolution |
|---|---|
| How to increase ALB public bandwidth | Default 400 Mbps per instance (dual AZ); purchase shared bandwidth package and add ALB-bound EIPs |
| EIP traffic unevenly distributed | Domain resolved to single EIP instead of ALB DNS name; front-end proxy using IPHash; clients caching DNS A records |
| Supported EIP types | Pay-as-you-go with usage-based billing only; BGP multi-line, BGP Premium, BGP DDoS Enhanced; subscription and fixed-bandwidth EIPs not supported |
| Private ALB → public | Change network type from Intranet to Internet (binds EIP, incurs public network fees) |
