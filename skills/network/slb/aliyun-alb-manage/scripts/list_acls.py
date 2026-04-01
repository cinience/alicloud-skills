#!/usr/bin/env python3
"""List ALB access control lists (ACLs)."""

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


def iter_acls(client: Alb20200616Client, acl_ids: list[str] | None = None,
              acl_names: list[str] | None = None):
    """Yield all ACLs with optional filters."""
    next_token: str | None = None
    while True:
        req = alb_models.ListAclsRequest(
            max_results=100,
            next_token=next_token,
            acl_ids=acl_ids,
            acl_names=acl_names,
        )
        resp = client.list_acls(req)
        for acl in resp.body.acls or []:
            yield acl
        next_token = resp.body.next_token
        if not next_token:
            break


def main() -> int:
    parser = argparse.ArgumentParser(description="List ALB ACLs")
    parser.add_argument("--region", required=True, help="Region ID")
    parser.add_argument("--acl-ids", nargs="+", help="Filter by ACL IDs")
    parser.add_argument("--acl-names", nargs="+", help="Filter by ACL names")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)
    acls = list(iter_acls(client, acl_ids=args.acl_ids, acl_names=args.acl_names))

    if args.json:
        output = json.dumps(
            [a.to_map() for a in acls], indent=2, ensure_ascii=False, default=str
        )
    else:
        header = (
            f"{'AclId':<30} {'AclName':<30} "
            f"{'AddressIPVersion':<18} {'AclStatus':<12} {'CreateTime'}"
        )
        sep = "-" * len(header)
        lines = [header, sep]
        for a in acls:
            lines.append(
                f"{a.acl_id or '-':<30} "
                f"{(a.acl_name or '-'):<30} "
                f"{(a.address_ipversion or '-'):<18} "
                f"{(a.acl_status or '-'):<12} "
                f"{a.create_time or '-'}"
            )
        lines.append(sep)
        lines.append(f"Total: {len(acls)} ACL(s)")
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
