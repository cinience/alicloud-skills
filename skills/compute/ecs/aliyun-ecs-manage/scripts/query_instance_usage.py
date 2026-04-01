#!/usr/bin/env python3
"""Query ECS resource usage metrics for one instance via CloudMonitor (CMS).

Default namespace is `acs_ecs_dashboard`, with 5-minute period and 1-hour window.
Outputs JSON by default; use --summary-only for compact output.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from statistics import fmean
from typing import Any

from alibabacloud_cms20190101 import models as cms_models
from alibabacloud_cms20190101.client import Client as CmsClient
from alibabacloud_tea_openapi import models as open_api_models


DEFAULT_METRICS = [
    "CPUUtilization",
    "memory_usedutilization",
    "InternetInRate",
    "InternetOutRate",
    "IntranetInRate",
    "IntranetOutRate",
]


def create_client(region_id: str) -> CmsClient:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint="metrics.aliyuncs.com",
    )
    ak = os.getenv("ALICLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALICLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    token = os.getenv("ALICLOUD_SECURITY_TOKEN") or os.getenv("ALIBABA_CLOUD_SECURITY_TOKEN")
    if ak and sk:
        config.access_key_id = ak
        config.access_key_secret = sk
        if token:
            config.security_token = token
    return CmsClient(config)


def parse_datapoints(raw: str) -> list[dict[str, Any]]:
    try:
        data = json.loads(raw or "[]")
    except json.JSONDecodeError:
        return []
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        return []

    out = [x for x in data if isinstance(x, dict)]
    out.sort(key=lambda x: int(x.get("timestamp") or x.get("Timestamp") or 0))
    return out


def pick_value(point: dict[str, Any]) -> float | None:
    for key in ("Average", "Value", "Maximum", "Minimum"):
        val = point.get(key)
        if val is None:
            continue
        try:
            return float(val)
        except (TypeError, ValueError):
            continue
    return None


def summarize(points: list[dict[str, Any]]) -> dict[str, Any]:
    values = [v for v in (pick_value(p) for p in points) if v is not None]
    if not values:
        return {"points": 0}
    return {
        "points": len(values),
        "avg": round(fmean(values), 3),
        "max": round(max(values), 3),
        "min": round(min(values), 3),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--region-id", default=os.getenv("ALICLOUD_REGION_ID", "cn-hangzhou"))
    parser.add_argument("--hours", type=float, default=1.0, help="Lookback window in hours")
    parser.add_argument("--period", type=int, default=300, help="Metric period in seconds")
    parser.add_argument("--namespace", default="acs_ecs_dashboard")
    parser.add_argument(
        "--metrics",
        default=",".join(DEFAULT_METRICS),
        help="Comma-separated metric names",
    )
    parser.add_argument("--summary-only", action="store_true", help="Output summary only")
    parser.add_argument("--output", help="Write JSON output to file")
    args = parser.parse_args()

    end = datetime.now(timezone.utc).replace(microsecond=0)
    start = end - timedelta(hours=args.hours)
    start_time = start.isoformat().replace("+00:00", "Z")
    end_time = end.isoformat().replace("+00:00", "Z")

    metrics = [m.strip() for m in args.metrics.split(",") if m.strip()]
    client = create_client(args.region_id)

    result: dict[str, Any] = {
        "instance_id": args.instance_id,
        "region_id": args.region_id,
        "namespace": args.namespace,
        "window_utc": {
            "start": start_time,
            "end": end_time,
            "period_sec": args.period,
        },
        "metrics": {},
    }

    for metric in metrics:
        req = cms_models.DescribeMetricListRequest(
            namespace=args.namespace,
            metric_name=metric,
            dimensions=json.dumps({"instanceId": args.instance_id}),
            start_time=start_time,
            end_time=end_time,
            period=str(args.period),
        )

        try:
            resp = client.describe_metric_list(req)
            points = parse_datapoints(resp.body.datapoints or "[]")
            payload: dict[str, Any] = {"summary": summarize(points)}
            if not args.summary_only:
                payload["datapoints"] = points
            result["metrics"][metric] = payload
        except Exception as exc:  # noqa: BLE001
            result["metrics"][metric] = {"error": str(exc)}

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
