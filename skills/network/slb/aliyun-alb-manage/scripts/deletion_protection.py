#!/usr/bin/env python3
"""Enable or disable deletion protection for an ALB instance.

Examples:
    # Enable deletion protection
    python deletion_protection.py --region cn-hangzhou --resource-id alb-xxx --enable

    # Disable deletion protection (required before deleting an ALB)
    python deletion_protection.py --region cn-hangzhou --resource-id alb-xxx --disable

    # JSON output
    python deletion_protection.py --region cn-hangzhou --resource-id alb-xxx --enable --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Enable or disable ALB deletion protection")
    parser.add_argument("--region", required=True, help="Region ID")
    parser.add_argument("--resource-id", required=True, help="ALB instance ID (alb-xxx)")

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--enable", action="store_true", help="Enable deletion protection")
    action.add_argument("--disable", action="store_true", help="Disable deletion protection")

    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")

    args = parser.parse_args()

    client = create_client(args.region)

    try:
        if args.enable:
            resp = client.enable_deletion_protection(alb_models.EnableDeletionProtectionRequest(
                resource_id=args.resource_id,
            ))
            action_desc = "enabled"
        else:
            resp = client.disable_deletion_protection(alb_models.DisableDeletionProtectionRequest(
                resource_id=args.resource_id,
            ))
            action_desc = "disabled"

        result = {"request_id": resp.body.request_id, "action": action_desc}
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        output = f"Deletion protection {action_desc} for {args.resource_id}."

    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
