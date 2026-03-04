#!/usr/bin/env python3
"""List IP entries in an ALB access control list (ACL)."""

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


def iter_acl_entries(client: Alb20200616Client, acl_id: str):
    """Yield all entries in an ACL."""
    next_token: str | None = None
    while True:
        req = alb_models.ListAclEntriesRequest(
            acl_id=acl_id,
            max_results=100,
            next_token=next_token,
        )
        resp = client.list_acl_entries(req)
        for entry in resp.body.acl_entries or []:
            yield entry
        next_token = resp.body.next_token
        if not next_token:
            break


def main() -> int:
    parser = argparse.ArgumentParser(description="List entries in an ALB ACL")
    parser.add_argument("--region", required=True, help="Region ID")
    parser.add_argument("--acl-id", required=True, help="ACL ID, e.g. acl-xxx")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)
    entries = list(iter_acl_entries(client, args.acl_id))

    if args.json:
        output = json.dumps(
            [e.to_map() for e in entries], indent=2, ensure_ascii=False, default=str
        )
    else:
        header = f"{'Entry (CIDR)':<45} {'Description'}"
        sep = "-" * len(header)
        lines = [header, sep]
        for e in entries:
            lines.append(
                f"{e.entry or '-':<45} "
                f"{e.description or '-'}"
            )
        lines.append(sep)
        lines.append(f"Total: {len(entries)} entry(ies) in {args.acl_id}")
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
