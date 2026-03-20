# DescribeSiteTimeSeriesData API Reference

Query account-level or site-level traffic analysis time-series data.

Official docs: https://api.aliyun.com/document/ESA/2024-09-10/DescribeSiteTimeSeriesData

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `SiteId` | string | No | Site ID. Empty = account-level query |
| `StartTime` | string | No | Start time (ISO8601 UTC+0) |
| `EndTime` | string | No | End time (ISO8601 UTC+0) |
| `Interval` | string | No | Time granularity in seconds |
| `Fields` | array | Yes | Query metrics array |

### Fields Structure

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `FieldName` | string | No | Metric name (e.g., `Traffic`, `Request`) |
| `Dimension` | array | No | Dimension array (e.g., `["SiteId"]`) |

## Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `Data` | array | Time-series data array |
| `SummarizedData` | array | Aggregated summary data |
| `StartTime` | string | Query start time |
| `EndTime` | string | Query end time |
| `Interval` | long | Data granularity (seconds) |
| `SamplingRate` | float | Sampling rate (%) |
| `RequestId` | string | Request ID |

### Data Structure

| Parameter | Type | Description |
|-----------|------|-------------|
| `FieldName` | string | Metric name |
| `DimensionName` | string | Dimension name |
| `DimensionValue` | string | Dimension value |
| `DimensionValueAlias` | string | Dimension alias (e.g., site name) |
| `DetailData` | array | Time-series points |

### DetailData Structure

| Parameter | Type | Description |
|-----------|------|-------------|
| `TimeStamp` | string | Time point (ISO8601) |
| `Value` | any | Metric value |

### SummarizedData Structure

| Parameter | Type | Description |
|-----------|------|-------------|
| `FieldName` | string | Metric name |
| `DimensionName` | string | Dimension name |
| `DimensionValue` | string | Dimension value |
| `AggMethod` | string | Aggregation method (`sum`, `avg`) |
| `Value` | any | Aggregated value |

## Time Granularity Rules

| Time Range | Interval | Parameter Value |
|------------|----------|-----------------|
| <= 3 hours | 1 minute | `60` |
| 3-12 hours | 5 minutes | `300` |
| 12 hours - 1 day | 15 minutes | `900` |
| 1-10 days | 1 hour | `3600` |
| 10-31 days | 1 day | `86400` |

**Default**: If `StartTime` and `EndTime` not specified, returns last 24 hours.

**Note**: Large time ranges may use sampling.

## Code Examples

### Query site traffic (hourly)

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

def query_traffic(site_id: str, hours: int = 24):
    client = create_client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)

    resp = client.describe_site_time_series_data(
        esa_models.DescribeSiteTimeSeriesDataRequest(
            site_id=site_id,
            start_time=start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end_time=end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            interval="3600",  # 1 hour
            fields=[
                esa_models.DescribeSiteTimeSeriesDataRequestFields(
                    field_name="Traffic",
                    dimension=["SiteId"]
                )
            ]
        )
    )

    return resp.body

# Usage
result = query_traffic("974351557069296", hours=24)
for item in result.data:
    print(f"Site: {item.dimension_value_alias}")
    for point in item.detail_data:
        print(f"  {point.time_stamp}: {point.value} bytes")
```

### Query multiple metrics

```python
def query_multiple_metrics(site_id: str):
    client = create_client()

    resp = client.describe_site_time_series_data(
        esa_models.DescribeSiteTimeSeriesDataRequest(
            site_id=site_id,
            start_time="2026-03-09T00:00:00Z",
            end_time="2026-03-10T00:00:00Z",
            interval="3600",
            fields=[
                esa_models.DescribeSiteTimeSeriesDataRequestFields(
                    field_name="Traffic",
                    dimension=["ALL"]
                ),
                esa_models.DescribeSiteTimeSeriesDataRequestFields(
                    field_name="Request",
                    dimension=["ALL"]
                ),
                esa_models.DescribeSiteTimeSeriesDataRequestFields(
                    field_name="HitRate",
                    dimension=["ALL"]
                )
            ]
        )
    )

    return resp.body
```

### Query by country

```python
def query_traffic_by_country(site_id: str):
    client = create_client()

    resp = client.describe_site_time_series_data(
        esa_models.DescribeSiteTimeSeriesDataRequest(
            site_id=site_id,
            start_time="2026-03-09T00:00:00Z",
            end_time="2026-03-10T00:00:00Z",
            interval="3600",
            fields=[
                esa_models.DescribeSiteTimeSeriesDataRequestFields(
                    field_name="Traffic",
                    dimension=["ClientCountryCode"]
                )
            ]
        )
    )

    # Group by country
    for item in resp.body.data:
        country = item.dimension_value
        print(f"Country: {country}")
        for point in item.detail_data:
            print(f"  {point.time_stamp}: {point.value}")
```

## Response Example

```json
{
  "Data": [
    {
      "FieldName": "Traffic",
      "DimensionName": "SiteId",
      "DimensionValue": "974351557069296",
      "DimensionValueAlias": "lwcwiki.fun",
      "DetailData": [
        {"TimeStamp": "2026-03-09T16:00:00Z", "Value": 38428},
        {"TimeStamp": "2026-03-09T17:00:00Z", "Value": 1042},
        {"TimeStamp": "2026-03-09T18:00:00Z", "Value": 629}
      ]
    }
  ],
  "SummarizedData": [
    {
      "FieldName": "Traffic",
      "DimensionName": "SiteId",
      "DimensionValue": "974351557069296",
      "DimensionValueAlias": "lwcwiki.fun",
      "AggMethod": "sum",
      "Value": 27317844
    }
  ],
  "StartTime": "2026-03-09T16:00:00Z",
  "EndTime": "2026-03-10T15:59:00Z",
  "Interval": 3600,
  "SamplingRate": 100
}
```

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
