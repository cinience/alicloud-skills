#!/usr/bin/env python3
"""Delete a VPC."""

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Delete a VPC")
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--vpc-id", required=True, help="VPC ID to delete")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)

    req = vpc_models.DeleteVpcRequest(
        region_id=args.region,
        vpc_id=args.vpc_id,
    )
    resp = client.delete_vpc(req)

    result = {
        "Action": "DeleteVpc",
        "VpcId": args.vpc_id,
        "RegionId": args.region,
        "RequestId": resp.body.request_id,
        "Success": True,
    }

    output = json.dumps(result, indent=2, ensure_ascii=False, default=str)

    if args.output:
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(f"VPC {args.vpc_id} deleted. Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
