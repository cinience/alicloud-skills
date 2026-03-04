#!/usr/bin/env python3
"""List ALB forwarding rules for a listener or load balancer."""

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


def iter_rules(client: Alb20200616Client, listener_ids: list[str] | None = None,
               lb_ids: list[str] | None = None):
    """Yield all forwarding rules with optional filters."""
    next_token: str | None = None
    while True:
        req = alb_models.ListRulesRequest(
            listener_ids=listener_ids,
            load_balancer_ids=lb_ids,
            max_results=100,
            next_token=next_token,
        )
        resp = client.list_rules(req)
        for rule in resp.body.rules or []:
            yield rule
        next_token = resp.body.next_token
        if not next_token:
            break


def summarize_conditions(rule) -> str:
    """Build a short description of rule match conditions."""
    parts: list[str] = []
    for cond in rule.rule_conditions or []:
        ctype = cond.type or ""
        if ctype == "Host" and cond.host_config:
            parts.append("Host(" + ",".join(cond.host_config.values or []) + ")")
        elif ctype == "Path" and cond.path_config:
            parts.append("Path(" + ",".join(cond.path_config.values or []) + ")")
        elif ctype == "Header" and cond.header_config:
            key = cond.header_config.key or ""
            values = cond.header_config.values or []
            parts.append(f"Header({key}={','.join(values)})")
        elif ctype == "Method" and cond.method_config:
            parts.append("Method(" + ",".join(cond.method_config.values or []) + ")")
        elif ctype == "QueryString" and cond.query_string_config:
            qs = cond.query_string_config.values or []
            qs_str = "&".join(f"{v.key}={v.value}" for v in qs if v.key)
            parts.append(f"QS({qs_str})")
        elif ctype == "Cookie" and cond.cookie_config:
            cookies = cond.cookie_config.values or []
            ck_str = ",".join(f"{c.key}={c.value}" for c in cookies if c.key)
            parts.append(f"Cookie({ck_str})")
        elif ctype == "SourceIp" and cond.source_ip_config:
            parts.append("SrcIP(" + ",".join(cond.source_ip_config.values or []) + ")")
        else:
            parts.append(ctype)
    return " & ".join(parts) if parts else "(default)"


def summarize_actions(rule) -> str:
    """Build a short description of rule actions."""
    parts: list[str] = []
    for act in rule.rule_actions or []:
        atype = act.type or ""
        if atype == "ForwardGroup" and act.forward_group_config:
            sgcs = act.forward_group_config.server_group_tuples or []
            sg_ids = [s.server_group_id for s in sgcs if s.server_group_id]
            parts.append("→ " + ",".join(sg_ids))
        elif atype == "Redirect" and act.redirect_config:
            rc = act.redirect_config
            target = f"{rc.protocol or ''}:{rc.port or ''}" if rc.protocol else str(rc.port or "")
            parts.append(f"Redirect({target})")
        elif atype == "FixedResponse" and act.fixed_response_config:
            parts.append(f"FixedResponse({act.fixed_response_config.http_code or ''})")
        elif atype == "Rewrite" and act.rewrite_config:
            rw = act.rewrite_config
            parts.append(f"Rewrite({rw.host or ''}{rw.path or ''})")
        elif atype == "InsertHeader" and act.insert_header_config:
            ih = act.insert_header_config
            parts.append(f"InsertHeader({ih.key or ''})")
        elif atype == "TrafficMirror":
            parts.append("TrafficMirror")
        elif atype == "TrafficLimit":
            parts.append("TrafficLimit")
        elif atype == "CORS":
            parts.append("CORS")
        else:
            parts.append(atype)
    return " ".join(parts) if parts else "-"


def main() -> int:
    parser = argparse.ArgumentParser(description="List ALB forwarding rules")
    parser.add_argument("--region", required=True, help="Region ID")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--listener-id", help="Filter by listener ID")
    group.add_argument("--lb-id", help="Filter by load balancer ID")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)
    listener_ids = [args.listener_id] if args.listener_id else None
    lb_ids = [args.lb_id] if args.lb_id else None
    rules = list(iter_rules(client, listener_ids=listener_ids, lb_ids=lb_ids))

    if args.json:
        output = json.dumps(
            [r.to_map() for r in rules], indent=2, ensure_ascii=False, default=str
        )
    else:
        header = (
            f"{'RuleId':<35} {'ListenerId':<35} {'Priority':<10} "
            f"{'Conditions':<35} {'Actions'}"
        )
        sep = "-" * len(header)
        lines = [header, sep]
        for r in sorted(rules, key=lambda x: (x.listener_id or "", x.priority or 0)):
            lines.append(
                f"{r.rule_id or '-':<35} "
                f"{r.listener_id or '-':<35} "
                f"{str(r.priority or '-'):<10} "
                f"{summarize_conditions(r):<35} "
                f"{summarize_actions(r)}"
            )
        lines.append(sep)
        lines.append(f"Total: {len(rules)} rule(s)")
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
