#!/usr/bin/env python3
"""List ALB instances in a single region."""

from __future__ import annotations

import argparse
import json
import os

from alibabacloud_alb20200616.client import Client as Alb20200616Client
from alibabacloud_alb20200616 import models as alb_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Alb20200616Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"alb.{region_id}.aliyuncs.com",
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
    return Alb20200616Client(config)


def iter_load_balancers(client: Alb20200616Client, *,
                        lb_ids: list[str] | None = None,
                        vpc_id: str | None = None,
                        address_type: str | None = None,
                        status: str | None = None):
    """Yield ALB instances using NextToken-based pagination with optional filters."""
    next_token: str | None = None
    while True:
        req = alb_models.ListLoadBalancersRequest(
            max_results=100,
            next_token=next_token,
            load_balancer_ids=lb_ids,
            vpc_ids=[vpc_id] if vpc_id else None,
            address_type=address_type,
            load_balancer_status=status,
        )
        resp = client.list_load_balancers(req)
        for lb in resp.body.load_balancers or []:
            yield lb
        next_token = resp.body.next_token
        if not next_token:
            break


def main() -> int:
    parser = argparse.ArgumentParser(description="List ALB instances in a region")
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--lb-ids", nargs="+", help="Filter by load balancer IDs")
    parser.add_argument("--vpc-id", help="Filter by VPC ID")
    parser.add_argument("--address-type", choices=["Internet", "Intranet"], help="Filter by address type")
    parser.add_argument("--status", help="Filter by status, e.g. Active, Provisioning")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)

    instances = list(iter_load_balancers(
        client,
        lb_ids=args.lb_ids,
        vpc_id=args.vpc_id,
        address_type=args.address_type,
        status=args.status,
    ))

    if args.json:
        output = json.dumps(
            [lb.to_map() for lb in instances], indent=2, ensure_ascii=False, default=str
        )
    else:
        header = f"{'LoadBalancerId':<30} {'Name':<30} {'AddressType':<12} {'Status':<12} {'VpcId':<25} {'CreateTime'}"
        sep = "-" * len(header)
        lines = [header, sep]

        for lb in instances:
            lines.append(
                f"{lb.load_balancer_id or '-':<30} "
                f"{(lb.load_balancer_name or '-'):<30} "
                f"{(lb.address_type or '-'):<12} "
                f"{(lb.load_balancer_status or '-'):<12} "
                f"{(lb.vpc_id or '-'):<25} "
                f"{lb.create_time or '-'}"
            )

        lines.append(sep)
        lines.append(f"Total: {len(instances)} ALB instance(s) in {args.region}")
        output = "\n".join(lines)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
