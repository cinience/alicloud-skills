#!/usr/bin/env python3
"""Create a VPC in a region."""

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


def wait_vpc_available(client: Vpc20160428Client, region_id: str, vpc_id: str,
                       timeout: int = 60, interval: int = 3) -> str:
    """Poll until VPC status is Available. Returns final status."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = client.describe_vpcs(vpc_models.DescribeVpcsRequest(
            region_id=region_id,
            vpc_id=vpc_id,
        ))
        for v in resp.body.vpcs.vpc:
            if v.vpc_id == vpc_id:
                if v.status == "Available":
                    return v.status
                break
        time.sleep(interval)
    return "Timeout"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a VPC")
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--cidr-block", default="172.16.0.0/12", help="VPC CIDR block (default: 172.16.0.0/12)")
    parser.add_argument("--vpc-name", help="VPC display name")
    parser.add_argument("--description", help="VPC description")
    parser.add_argument("--no-wait", action="store_true", help="Do not wait for VPC to become Available")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)

    req = vpc_models.CreateVpcRequest(
        region_id=args.region,
        cidr_block=args.cidr_block,
        vpc_name=args.vpc_name,
        description=args.description,
    )
    resp = client.create_vpc(req)
    vpc_id = resp.body.vpc_id

    result = {
        "VpcId": vpc_id,
        "RegionId": args.region,
        "CidrBlock": args.cidr_block,
        "VpcName": args.vpc_name,
        "RequestId": resp.body.request_id,
    }

    if not args.no_wait:
        status = wait_vpc_available(client, args.region, vpc_id)
        result["Status"] = status
        if status != "Available":
            print(f"Warning: VPC {vpc_id} did not reach Available status (got: {status})")
    else:
        result["Status"] = "Pending (not waited)"

    output = json.dumps(result, indent=2, ensure_ascii=False, default=str)

    if args.output:
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(f"VPC {vpc_id} created. Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
