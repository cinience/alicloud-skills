# SLS Troubleshooting Query Templates

## Top errors by status

```
status:5* | SELECT status, count(*) AS total GROUP BY status ORDER BY total DESC LIMIT 20
```

## Top error messages

```
level:error | SELECT message, count(*) AS total GROUP BY message ORDER BY total DESC LIMIT 20
```

## Top trace IDs with errors

```
level:error AND trace_id:* | SELECT trace_id, count(*) AS total GROUP BY trace_id ORDER BY total DESC LIMIT 20
```

## Slow requests (adjust field names)

```
* | SELECT request_path, avg(latency_ms) AS p50, max(latency_ms) AS max_ms GROUP BY request_path ORDER BY max_ms DESC LIMIT 20
```

## Timeout keywords

```
message:*timeout* | SELECT message, count(*) AS total GROUP BY message ORDER BY total DESC LIMIT 20
```
