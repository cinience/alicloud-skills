#!/usr/bin/env python3
"""List backend servers in an ALB server group."""

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


def iter_servers(client: Alb20200616Client, sg_id: str):
    """Yield all servers in a server group."""
    next_token: str | None = None
    while True:
        req = alb_models.ListServerGroupServersRequest(
            server_group_id=sg_id,
            max_results=100,
            next_token=next_token,
        )
        resp = client.list_server_group_servers(req)
        for srv in resp.body.servers or []:
            yield srv
        next_token = resp.body.next_token
        if not next_token:
            break


def main() -> int:
    parser = argparse.ArgumentParser(description="List servers in an ALB server group")
    parser.add_argument("--region", required=True, help="Region ID")
    parser.add_argument("--sg-id", required=True, help="Server group ID, e.g. sgp-xxx")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)
    servers = list(iter_servers(client, args.sg_id))

    if args.json:
        output = json.dumps(
            [s.to_map() for s in servers], indent=2, ensure_ascii=False, default=str
        )
    else:
        header = (
            f"{'ServerId':<25} {'ServerType':<12} {'ServerIp':<18} "
            f"{'Port':<8} {'Weight':<8} {'Status':<12} {'Description'}"
        )
        sep = "-" * len(header)
        lines = [header, sep]
        for s in servers:
            lines.append(
                f"{s.server_id or '-':<25} "
                f"{(s.server_type or '-'):<12} "
                f"{(s.server_ip or '-'):<18} "
                f"{str(s.port or '-'):<8} "
                f"{str(s.weight if s.weight is not None else '-'):<8} "
                f"{(s.status or '-'):<12} "
                f"{s.description or '-'}"
            )
        lines.append(sep)
        lines.append(f"Total: {len(servers)} server(s) in {args.sg_id}")
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
