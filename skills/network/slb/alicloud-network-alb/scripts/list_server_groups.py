#!/usr/bin/env python3
"""List ALB server groups, optionally filtered by VPC or server group IDs."""

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


def iter_server_groups(client: Alb20200616Client, vpc_id: str | None = None,
                       sg_ids: list[str] | None = None):
    """Yield all server groups with optional filters."""
    next_token: str | None = None
    while True:
        req = alb_models.ListServerGroupsRequest(
            max_results=100,
            next_token=next_token,
            vpc_id=vpc_id,
            server_group_ids=sg_ids,
        )
        resp = client.list_server_groups(req)
        for sg in resp.body.server_groups or []:
            yield sg
        next_token = resp.body.next_token
        if not next_token:
            break


def main() -> int:
    parser = argparse.ArgumentParser(description="List ALB server groups")
    parser.add_argument("--region", required=True, help="Region ID")
    parser.add_argument("--vpc-id", help="Filter by VPC ID")
    parser.add_argument("--sg-ids", nargs="+", help="Filter by server group IDs")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)
    groups = list(iter_server_groups(client, vpc_id=args.vpc_id, sg_ids=args.sg_ids))

    if args.json:
        output = json.dumps(
            [g.to_map() for g in groups], indent=2, ensure_ascii=False, default=str
        )
    else:
        header = (
            f"{'ServerGroupId':<35} {'Name':<30} {'Type':<12} "
            f"{'Protocol':<10} {'Scheduler':<12} {'VpcId':<26} {'ServerCount'}"
        )
        sep = "-" * len(header)
        lines = [header, sep]
        for g in groups:
            lines.append(
                f"{g.server_group_id or '-':<35} "
                f"{(g.server_group_name or '-'):<30} "
                f"{(g.server_group_type or '-'):<12} "
                f"{(g.protocol or '-'):<10} "
                f"{(g.scheduler or '-'):<12} "
                f"{(g.vpc_id or '-'):<26} "
                f"{g.server_count if g.server_count is not None else '-'}"
            )
        lines.append(sep)
        lines.append(f"Total: {len(groups)} server group(s)")
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
