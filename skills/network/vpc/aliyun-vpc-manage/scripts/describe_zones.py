#!/usr/bin/env python3
"""List available zones in a region (uses ECS DescribeZones API)."""

from __future__ import annotations

import argparse
import json
import os

from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_ecs20140526 import models as ecs_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Ecs20140526Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"ecs.{region_id}.aliyuncs.com",
    )
    ak = os.getenv("ALIBABACLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID") or os.getenv("ALICLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALIBABACLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET") or os.getenv("ALICLOUD_ACCESS_KEY_SECRET")
    token = os.getenv("ALIBABACLOUD_SECURITY_TOKEN") or os.getenv("ALIBABA_CLOUD_SECURITY_TOKEN") or os.getenv("ALICLOUD_SECURITY_TOKEN")
    if not ak or not sk:
        raise RuntimeError("ALIBABACLOUD_ACCESS_KEY_ID and ALIBABACLOUD_ACCESS_KEY_SECRET must be set (ALIBABA_CLOUD_* and ALICLOUD_* aliases are also accepted)")
    config.access_key_id = ak
    config.access_key_secret = sk
    if token:
        config.security_token = token
    return Ecs20140526Client(config)


def main() -> int:
    parser = argparse.ArgumentParser(description="List available zones in a region")
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)

    resp = client.describe_zones(ecs_models.DescribeZonesRequest(
        region_id=args.region,
    ))

    zones = resp.body.zones.zone

    if args.json:
        output = json.dumps(
            [{"ZoneId": z.zone_id, "LocalName": z.local_name} for z in zones],
            indent=2, ensure_ascii=False, default=str,
        )
    else:
        header = f"{'ZoneId':<25} {'LocalName'}"
        sep = "-" * 60
        lines = [header, sep]

        for z in zones:
            lines.append(f"{z.zone_id or '-':<25} {z.local_name or '-'}")

        lines.append(sep)
        lines.append(f"Total: {len(zones)} zone(s) in {args.region}")
        output = "\n".join(lines)

    if args.output:
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
