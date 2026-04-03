#!/usr/bin/env python3
"""List VSwitches in a single region."""

from __future__ import annotations

import argparse
import json
import os

from alibabacloud_vpc20160428.client import Client as Vpc20160428Client
from alibabacloud_vpc20160428 import models as vpc_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Vpc20160428Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"vpc.{region_id}.aliyuncs.com",
    )
    ak = os.getenv("ALICLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALICLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    token = os.getenv("ALICLOUD_SECURITY_TOKEN") or os.getenv("ALIBABA_CLOUD_SECURITY_TOKEN")
    if not ak or not sk:
        raise RuntimeError("ALICLOUD_ACCESS_KEY_ID and ALICLOUD_ACCESS_KEY_SECRET must be set")
    config.access_key_id = ak
    config.access_key_secret = sk
    if token:
        config.security_token = token
    return Vpc20160428Client(config)


def iter_vswitches(client: Vpc20160428Client, region_id: str, *,
                   vpc_id: str | None = None,
                   vswitch_id: str | None = None,
                   zone_id: str | None = None,
                   vswitch_name: str | None = None,
                   is_default: bool | None = None):
    """Yield VSwitches using PageNumber-based pagination with optional filters."""
    page_number = 1
    page_size = 50
    while True:
        req = vpc_models.DescribeVSwitchesRequest(
            region_id=region_id,
            page_number=page_number,
            page_size=page_size,
            vpc_id=vpc_id,
            v_switch_id=vswitch_id,
            zone_id=zone_id,
            v_switch_name=vswitch_name,
            is_default=is_default,
        )
        resp = client.describe_vswitches(req)
        for vs in resp.body.v_switches.v_switch:
            yield vs
        total = resp.body.total_count
        if page_number * page_size >= total:
            break
        page_number += 1


def main() -> int:
    parser = argparse.ArgumentParser(description="List VSwitches in a region")
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--vpc-id", help="Filter by VPC ID")
    parser.add_argument("--vswitch-id", help="Filter by VSwitch ID")
    parser.add_argument("--zone-id", help="Filter by zone ID")
    parser.add_argument("--vswitch-name", help="Filter by VSwitch name")
    parser.add_argument("--is-default", action="store_true", default=None, help="Only show default VSwitch")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)

    vswitches = list(iter_vswitches(
        client, args.region,
        vpc_id=args.vpc_id,
        vswitch_id=args.vswitch_id,
        zone_id=args.zone_id,
        vswitch_name=args.vswitch_name,
        is_default=args.is_default,
    ))

    if args.json:
        output = json.dumps(
            [vs.to_map() for vs in vswitches], indent=2, ensure_ascii=False, default=str
        )
    else:
        header = f"{'VSwitchId':<25} {'VSwitchName':<25} {'CidrBlock':<20} {'ZoneId':<18} {'VpcId':<25} {'Status'}"
        sep = "-" * len(header)
        lines = [header, sep]

        for vs in vswitches:
            lines.append(
                f"{vs.v_switch_id or '-':<25} "
                f"{(vs.v_switch_name or '-'):<25} "
                f"{(vs.cidr_block or '-'):<20} "
                f"{(vs.zone_id or '-'):<18} "
                f"{(vs.vpc_id or '-'):<25} "
                f"{vs.status or '-'}"
            )

        lines.append(sep)
        lines.append(f"Total: {len(vswitches)} VSwitch(es) in {args.region}")
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
