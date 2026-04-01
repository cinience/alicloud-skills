#!/usr/bin/env python3
"""Create an ALB (Application Load Balancer) instance.

Examples:
    # Internet-facing ALB in two zones
    python create_load_balancer.py --region cn-hangzhou --name my-alb \\
        --vpc-id vpc-xxx --address-type Internet \\
        --zone cn-hangzhou-h:vsw-aaa --zone cn-hangzhou-i:vsw-bbb

    # Internal ALB
    python create_load_balancer.py --region cn-hangzhou --name my-alb \\
        --vpc-id vpc-xxx --address-type Intranet \\
        --zone cn-hangzhou-h:vsw-aaa --zone cn-hangzhou-i:vsw-bbb

    # Standard edition with deletion protection
    python create_load_balancer.py --region cn-hangzhou --name my-alb \\
        --vpc-id vpc-xxx --address-type Internet --edition Standard \\
        --deletion-protection \\
        --zone cn-hangzhou-h:vsw-aaa --zone cn-hangzhou-i:vsw-bbb

    # Dry run
    python create_load_balancer.py --region cn-hangzhou --name my-alb \\
        --vpc-id vpc-xxx --address-type Internet \\
        --zone cn-hangzhou-h:vsw-aaa --zone cn-hangzhou-i:vsw-bbb \\
        --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

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


def parse_zone(spec: str) -> dict[str, str]:
    """Parse zone spec: zone_id:vswitch_id[:eip_allocation_id]."""
    parts = spec.split(":")
    if len(parts) < 2:
        raise ValueError(
            f"Invalid zone spec '{spec}'. "
            "Format: zone_id:vswitch_id  e.g. cn-hangzhou-h:vsw-xxx"
        )
    result: dict[str, str] = {"zone_id": parts[0], "v_switch_id": parts[1]}
    if len(parts) >= 3 and parts[2]:
        result["allocation_id"] = parts[2]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create an ALB instance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Zone spec format: zone_id:vswitch_id[:eip_allocation_id]

Examples:
  %(prog)s --region cn-hangzhou --name my-alb \\
      --vpc-id vpc-xxx --address-type Internet \\
      --zone cn-hangzhou-h:vsw-aaa --zone cn-hangzhou-i:vsw-bbb
        """,
    )
    parser.add_argument("--region", required=True, help="Region ID")
    parser.add_argument("--name", required=True, help="Load balancer name")
    parser.add_argument("--vpc-id", required=True, help="VPC ID")
    parser.add_argument(
        "--address-type", required=True, choices=["Internet", "Intranet"],
        help="Network type",
    )
    parser.add_argument(
        "--zone", required=True, action="append", dest="zones",
        help="Zone mapping: zone_id:vswitch_id[:eip_allocation_id] (at least 2 zones)",
    )
    parser.add_argument(
        "--edition", default="Standard",
        choices=["Basic", "Standard", "StandardWithWaf"],
        help="ALB edition (default: Standard)",
    )
    parser.add_argument(
        "--address-ip-version", default="IPv4",
        choices=["IPv4", "DualStack"],
        help="IP version (default: IPv4)",
    )
    parser.add_argument(
        "--pay-type", default="PostPay",
        choices=["PostPay"],
        help="Billing type (default: PostPay)",
    )
    parser.add_argument("--deletion-protection", action="store_true", help="Enable deletion protection")
    parser.add_argument("--resource-group-id", help="Resource group ID")
    parser.add_argument("--dry-run", action="store_true", help="Print request without executing")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")

    args = parser.parse_args()

    try:
        parsed_zones = [parse_zone(z) for z in args.zones]
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if len(parsed_zones) < 2:
        print("Error: at least 2 zones are required for ALB.", file=sys.stderr)
        return 1

    if args.dry_run:
        request: dict[str, Any] = {
            "load_balancer_name": args.name,
            "vpc_id": args.vpc_id,
            "address_type": args.address_type,
            "load_balancer_edition": args.edition,
            "address_ip_version": args.address_ip_version,
            "pay_type": args.pay_type,
            "deletion_protection_enabled": args.deletion_protection,
            "zone_mappings": parsed_zones,
        }
        output = json.dumps(request, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(output + "\n", encoding="utf-8")
            print(f"Dry-run request written to {args.output}")
        else:
            print("Dry-run mode - would create ALB:")
            print(output)
        return 0

    client = create_client(args.region)

    zone_mappings = [
        alb_models.CreateLoadBalancerRequestZoneMappings(
            zone_id=z["zone_id"],
            v_switch_id=z["v_switch_id"],
            **({"allocation_id": z["allocation_id"]} if "allocation_id" in z else {}),
        )
        for z in parsed_zones
    ]

    req = alb_models.CreateLoadBalancerRequest(
        load_balancer_name=args.name,
        vpc_id=args.vpc_id,
        address_type=args.address_type,
        load_balancer_edition=args.edition,
        address_ip_version=args.address_ip_version,
        load_balancer_billing_config=alb_models.CreateLoadBalancerRequestLoadBalancerBillingConfig(
            pay_type=args.pay_type,
        ),
        zone_mappings=zone_mappings,
        deletion_protection_enabled=args.deletion_protection,
    )

    if args.resource_group_id:
        req.resource_group_id = args.resource_group_id

    try:
        resp = client.create_load_balancer(req)
        result = {
            "load_balancer_id": resp.body.load_balancer_id,
            "request_id": resp.body.request_id,
        }
    except Exception as e:
        print(f"Error creating ALB: {e}", file=sys.stderr)
        return 1

    if args.json:
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        output = (
            f"ALB created successfully:\n"
            f"  Load Balancer ID: {result['load_balancer_id']}\n"
            f"  Note: ALB creation is async. Use get_instance_status.py to check status."
        )

    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
