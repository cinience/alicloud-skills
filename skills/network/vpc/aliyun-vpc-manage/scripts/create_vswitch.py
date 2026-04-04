#!/usr/bin/env python3
"""Create a VSwitch in a VPC."""

from __future__ import annotations

import argparse
import json
import os
import time

from alibabacloud_vpc20160428.client import Client as Vpc20160428Client
from alibabacloud_vpc20160428 import models as vpc_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Vpc20160428Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"vpc.{region_id}.aliyuncs.com",
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
    return Vpc20160428Client(config)


def wait_vswitch_available(client: Vpc20160428Client, region_id: str, vswitch_id: str,
                           timeout: int = 60, interval: int = 3) -> str:
    """Poll until VSwitch status is Available. Returns final status."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = client.describe_vswitches(vpc_models.DescribeVSwitchesRequest(
            region_id=region_id,
            v_switch_id=vswitch_id,
        ))
        for vs in resp.body.v_switches.v_switch:
            if vs.v_switch_id == vswitch_id:
                if vs.status == "Available":
                    return vs.status
                break
        time.sleep(interval)
    return "Timeout"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a VSwitch in a VPC")
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--vpc-id", required=True, help="VPC ID to create VSwitch in")
    parser.add_argument("--zone-id", required=True, help="Availability zone ID, e.g. cn-hangzhou-h")
    parser.add_argument("--cidr-block", required=True, help="VSwitch CIDR block, e.g. 172.16.0.0/24")
    parser.add_argument("--vswitch-name", help="VSwitch display name")
    parser.add_argument("--description", help="VSwitch description")
    parser.add_argument("--no-wait", action="store_true", help="Do not wait for VSwitch to become Available")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)

    req = vpc_models.CreateVSwitchRequest(
        region_id=args.region,
        vpc_id=args.vpc_id,
        zone_id=args.zone_id,
        cidr_block=args.cidr_block,
        v_switch_name=args.vswitch_name,
        description=args.description,
    )
    resp = client.create_vswitch(req)
    vswitch_id = resp.body.v_switch_id

    result = {
        "VSwitchId": vswitch_id,
        "VpcId": args.vpc_id,
        "ZoneId": args.zone_id,
        "RegionId": args.region,
        "CidrBlock": args.cidr_block,
        "VSwitchName": args.vswitch_name,
        "RequestId": resp.body.request_id,
    }

    if not args.no_wait:
        status = wait_vswitch_available(client, args.region, vswitch_id)
        result["Status"] = status
        if status != "Available":
            print(f"Warning: VSwitch {vswitch_id} did not reach Available status (got: {status})")
    else:
        result["Status"] = "Pending (not waited)"

    output = json.dumps(result, indent=2, ensure_ascii=False, default=str)

    if args.output:
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(f"VSwitch {vswitch_id} created. Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
