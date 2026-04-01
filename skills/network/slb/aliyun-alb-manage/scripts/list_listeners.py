#!/usr/bin/env python3
"""List ALB listeners for a given load balancer."""

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


def iter_listeners(client: Alb20200616Client, lb_id: str):
    """Yield all listeners for a load balancer."""
    next_token: str | None = None
    while True:
        req = alb_models.ListListenersRequest(
            load_balancer_ids=[lb_id],
            max_results=100,
            next_token=next_token,
        )
        resp = client.list_listeners(req)
        for listener in resp.body.listeners or []:
            yield listener
        next_token = resp.body.next_token
        if not next_token:
            break


def main() -> int:
    parser = argparse.ArgumentParser(description="List ALB listeners")
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--lb-id", required=True, help="LoadBalancer ID")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)
    listeners = list(iter_listeners(client, args.lb_id))

    if args.json:
        output = json.dumps(
            [l.to_map() for l in listeners], indent=2, ensure_ascii=False, default=str
        )
    else:
        header = (
            f"{'ListenerId':<35} {'Protocol':<10} {'Port':<8} "
            f"{'Status':<14} {'ServerGroupId':<35} {'Description'}"
        )
        sep = "-" * len(header)
        lines = [header, sep]
        for l in listeners:
            # default action server group
            sg_id = "-"
            if l.default_actions:
                for act in l.default_actions:
                    if act.forward_group_config and act.forward_group_config.server_group_tuples:
                        sg_id = act.forward_group_config.server_group_tuples[0].server_group_id or "-"
                        break
            lines.append(
                f"{l.listener_id or '-':<35} "
                f"{l.listener_protocol or '-':<10} "
                f"{str(l.listener_port or '-'):<8} "
                f"{l.listener_status or '-':<14} "
                f"{sg_id:<35} "
                f"{l.listener_description or '-'}"
            )
        lines.append(sep)
        lines.append(f"Total: {len(listeners)} listener(s) for {args.lb_id}")
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
