# DescribeSiteTopData API Reference

Query account-level or site-level traffic analysis Top-N ranking data.

Official docs: https://api.aliyun.com/document/ESA/2024-09-10/DescribeSiteTopData

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `SiteId` | string | No | Site ID. Empty = account-level query |
| `StartTime` | string | No | Start time (ISO8601 UTC+0) |
| `EndTime` | string | No | End time (ISO8601 UTC+0) |
| `Interval` | string | No | Time granularity in seconds |
| `Fields` | array | Yes | Query metrics array |
| `Limit` | string | No | Top-N count. Values: `5`, `10`, `150` |

### Fields Structure

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `FieldName` | string | No | Metric name (e.g., `Traffic`, `Request`) |
| `Dimension` | array | No | Dimension array (e.g., `["ClientCountryCode"]`) |

## Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `Data` | array | Top-N data array |
| `StartTime` | string | Query start time |
| `EndTime` | string | Query end time |
| `SamplingRate` | float | Sampling rate (%) |
| `RequestId` | string | Request ID |

### Data Structure

| Parameter | Type | Description |
|-----------|------|-------------|
| `FieldName` | string | Metric name |
| `DimensionName` | string | Dimension name |
| `DetailData` | array | Top-N ranking data |

### DetailData Structure

| Parameter | Type | Description |
|-----------|------|-------------|
| `DimensionValue` | string | Dimension value (e.g., country code) |
| `Value` | any | Metric value |

## Code Examples

### Query top 10 countries by traffic

```python
from alibabacloud_esa20240910.client import Client as EsaClient
from alibabacloud_esa20240910 import models as esa_models
from alibabacloud_tea_openapi import models as open_api_models
from datetime import datetime, timedelta, timezone

def create_client():
    config = open_api_models.Config(
        region_id="cn-hangzhou",
        endpoint="esa.cn-hangzhou.aliyuncs.com",
    )
    return EsaClient(config)

def query_top_countries(site_id: str, limit: int = 10):
    client = create_client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=24)

    resp = client.describe_site_top_data(
        esa_models.DescribeSiteTopDataRequest(
            site_id=site_id,
            start_time=start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end_time=end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            fields=[
                esa_models.DescribeSiteTopDataRequestFields(
                    field_name="Traffic",
                    dimension=["ClientCountryCode"]
                )
            ],
            limit=str(limit)
        )
    )

    return resp.body

# Usage
result = query_top_countries("974351557069296", limit=10)
for item in result.data:
    print(f"Metric: {item.field_name} by {item.dimension_name}")
    for i, rank in enumerate(item.detail_data, 1):
        print(f"  #{i} {rank.dimension_value}: {rank.value} bytes")
```

### Query top hosts by requests

```python
def query_top_hosts(site_id: str):
    client = create_client()

    resp = client.describe_site_top_data(
        esa_models.DescribeSiteTopDataRequest(
            site_id=site_id,
            start_time="2026-03-10T00:00:00Z",
            end_time="2026-03-11T00:00:00Z",
            fields=[
                esa_models.DescribeSiteTopDataRequestFields(
                    field_name="Request",
                    dimension=["Host"]
                )
            ],
            limit="10"
        )
    )

    return resp.body
```

### Query top URLs by traffic

```python
def query_top_urls(site_id: str):
    client = create_client()

    resp = client.describe_site_top_data(
        esa_models.DescribeSiteTopDataRequest(
            site_id=site_id,
            start_time="2026-03-10T00:00:00Z",
            end_time="2026-03-11T00:00:00Z",
            fields=[
                esa_models.DescribeSiteTopDataRequestFields(
                    field_name="Traffic",
                    dimension=["RequestUri"]
                )
            ],
            limit="150"
        )
    )

    return resp.body
```

### Query account-level top sites

```python
def query_top_sites():
    """Query top sites at account level (no SiteId)"""
    client = create_client()

    resp = client.describe_site_top_data(
        esa_models.DescribeSiteTopDataRequest(
            # No site_id = account level
            start_time="2026-03-10T00:00:00Z",
            end_time="2026-03-11T00:00:00Z",
            fields=[
                esa_models.DescribeSiteTopDataRequestFields(
                    field_name="Traffic",
                    dimension=["SiteId"]
                )
            ],
            limit="10"
        )
    )

    return resp.body
```

## Response Example

```json
{
  "Data": [
    {
      "FieldName": "Traffic",
      "DimensionName": "ClientCountryCode",
      "DetailData": [
        {"DimensionValue": "HK", "Value": 9132354},
        {"DimensionValue": "CN", "Value": 703820},
        {"DimensionValue": "CA", "Value": 64679},
        {"DimensionValue": "US", "Value": 33979},
        {"DimensionValue": "SG", "Value": 27666}
      ]
    }
  ],
  "StartTime": "2026-03-10T02:47:00Z",
  "EndTime": "2026-03-11T02:47:00Z",
  "SamplingRate": 100
}
```

## Common Use Cases

| Use Case | FieldName | Dimension |
|----------|-----------|-----------|
| Top countries by traffic | `Traffic` | `ClientCountryCode` |
| Top provinces (China) | `Traffic` | `ClientProvinceCode` |
| Top ISPs | `Traffic` | `ClientISP` |
| Top hosts | `Request` | `Host` |
| Top URLs | `Traffic` | `RequestUri` |
| Top sites (account level) | `Traffic` | `SiteId` |
| Top status codes | `Request` | `Status` |

## Error Codes

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 400 | `InvalidParameter.TimeRange` | Time range exceeds limit |
| 400 | `InvalidEndTime.Mismatch` | EndTime earlier than StartTime |
| 400 | `InvalidParameter.Field` | Invalid field name |
| 400 | `InvalidParameter.Dimension` | Invalid dimension |
| 400 | `InvalidTime.Malformed` | Wrong time format |
| 400 | `TooManyDimensions` | Too many query dimensions |
| 400 | `TooManyRequests` | Rate limited |

## Differences from Time-Series API

| Feature | Time-Series | Top-N |
|---------|-------------|-------|
| Purpose | Trend over time | Ranking at a point |
| Returns | Time-stamped values | Ranked values |
| Limit | N/A | 5, 10, or 150 |
| SummarizedData | Yes | No |
