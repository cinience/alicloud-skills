#!/usr/bin/env python3
"""Get ALB instance status with overview (tree) or detail (JSON) view."""

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


# ---------------------------------------------------------------------------
# Pagination helpers
# ---------------------------------------------------------------------------

def list_all_listeners(client: Alb20200616Client, lb_id: str) -> list:
    """Fetch all listeners for a given ALB instance."""
    listeners: list = []
    next_token: str | None = None
    while True:
        req = alb_models.ListListenersRequest(
            load_balancer_ids=[lb_id],
            max_results=100,
            next_token=next_token,
        )
        resp = client.list_listeners(req)
        listeners.extend(resp.body.listeners or [])
        next_token = resp.body.next_token
        if not next_token:
            break
    return listeners


def list_all_rules(client: Alb20200616Client, listener_id: str) -> list:
    """Fetch all forwarding rules for a listener."""
    rules: list = []
    next_token: str | None = None
    while True:
        req = alb_models.ListRulesRequest(
            listener_ids=[listener_id],
            max_results=100,
            next_token=next_token,
        )
        resp = client.list_rules(req)
        rules.extend(resp.body.rules or [])
        next_token = resp.body.next_token
        if not next_token:
            break
    return rules


# ---------------------------------------------------------------------------
# Tree rendering helpers
# ---------------------------------------------------------------------------

def _format_zone(zm) -> str:
    """Format a single ZoneMapping entry."""
    zone_id = zm.zone_id or "?"
    vsw = zm.v_switch_id or "?"
    # Extract the first load balancer address if available
    addr = "-"
    if zm.load_balancer_addresses:
        first = zm.load_balancer_addresses[0]
        addr = first.address or first.ipv_6address or "-"
    status_tag = ""
    if hasattr(zm, "status") and zm.status and zm.status != "Active":
        status_tag = f" ({zm.status})"
    return f"Zone {zone_id} (vsw: {vsw}) → {addr}{status_tag}"


def _summarize_conditions(rule) -> str:
    """Build a short description of rule match conditions."""
    parts: list[str] = []
    for cond in rule.rule_conditions or []:
        ctype = cond.type or ""
        if ctype == "Host" and cond.host_config:
            values = cond.host_config.values or []
            parts.append(",".join(values))
        elif ctype == "Path" and cond.path_config:
            values = cond.path_config.values or []
            parts.append(",".join(values))
        elif ctype == "Header" and cond.header_config:
            key = cond.header_config.key or ""
            values = cond.header_config.values or []
            parts.append(f"Header({key}={','.join(values)})")
        elif ctype == "Method" and cond.method_config:
            values = cond.method_config.values or []
            parts.append(f"Method({','.join(values)})")
        elif ctype == "QueryString" and cond.query_string_config:
            qs = cond.query_string_config.values or []
            qs_str = "&".join(f"{v.key}={v.value}" for v in qs if v.key)
            parts.append(f"QS({qs_str})")
        elif ctype == "Cookie" and cond.cookie_config:
            cookies = cond.cookie_config.values or []
            ck_str = ",".join(f"{c.key}={c.value}" for c in cookies if c.key)
            parts.append(f"Cookie({ck_str})")
        elif ctype == "SourceIp" and cond.source_ip_config:
            values = cond.source_ip_config.values or []
            parts.append(f"SrcIP({','.join(values)})")
        else:
            parts.append(ctype)
    return " & ".join(parts) if parts else "match-all"


def _summarize_actions(rule) -> str:
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
            parts.append(f"Redirect {target}")
        elif atype == "FixedResponse" and act.fixed_response_config:
            fc = act.fixed_response_config
            parts.append(f"FixedResponse({fc.http_code or ''})")
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


def build_overview(client: Alb20200616Client, lb_id: str) -> str:
    """Build an ASCII tree view of the ALB instance."""
    # 1. Get instance attributes
    attr_resp = client.get_load_balancer_attribute(
        alb_models.GetLoadBalancerAttributeRequest(load_balancer_id=lb_id)
    )
    lb = attr_resp.body
    lines: list[str] = []

    name = lb.load_balancer_name or ""
    status = lb.load_balancer_status or "?"
    edition = lb.load_balancer_edition or ""
    addr_type = lb.address_type or ""
    edition_tag = f" ({edition})" if edition else ""
    addr_tag = f" [{addr_type}]" if addr_type else ""
    lines.append(f"ALB: {lb.load_balancer_id} ({name}) [{status}]{edition_tag}{addr_tag}")

    # 2. Zone mappings
    zones = lb.zone_mappings or []
    listeners = list_all_listeners(client, lb_id)
    total_children = len(zones) + len(listeners)
    child_idx = 0

    for zm in zones:
        child_idx += 1
        is_last_child = child_idx == total_children
        prefix = "└── " if is_last_child else "├── "
        lines.append(prefix + _format_zone(zm))

    # 3. Listeners & their rules
    for listener in listeners:
        child_idx += 1
        is_last_listener = child_idx == total_children
        l_prefix = "└── " if is_last_listener else "├── "
        l_cont = "    " if is_last_listener else "│   "

        lid = listener.listener_id or "?"
        proto = listener.listener_protocol or "?"
        port = listener.listener_port or "?"
        lstatus = listener.listener_status or "?"
        lines.append(f"{l_prefix}Listener: {lid} ({proto}:{port}) [{lstatus}]")

        # Fetch rules
        rules = list_all_rules(client, lid)

        # Separate default action from non-default rules
        default_rules = [r for r in rules if r.priority and r.priority >= 99999]
        custom_rules = [r for r in rules if not r.priority or r.priority < 99999]
        custom_rules.sort(key=lambda r: r.priority or 0)

        all_rule_items = custom_rules + default_rules
        for ri, rule in enumerate(all_rule_items):
            is_last_rule = ri == len(all_rule_items) - 1
            r_prefix = l_cont + ("└── " if is_last_rule else "├── ")

            if rule.priority and rule.priority >= 99999:
                # Default action
                actions = _summarize_actions(rule)
                lines.append(f"{r_prefix}DefaultAction {actions}")
            else:
                priority = rule.priority or "?"
                conds = _summarize_conditions(rule)
                actions = _summarize_actions(rule)
                rule_id = rule.rule_id or ""
                lines.append(f"{r_prefix}Rule: {rule_id} (Priority:{priority}, {conds}) {actions}")

    return "\n".join(lines)


def build_detail(client: Alb20200616Client, lb_id: str) -> str:
    """Return full GetLoadBalancerAttribute response as formatted JSON."""
    resp = client.get_load_balancer_attribute(
        alb_models.GetLoadBalancerAttributeRequest(load_balancer_id=lb_id)
    )
    return json.dumps(resp.body.to_map(), indent=2, ensure_ascii=False, default=str)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Get ALB instance status")
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--lb-id", required=True, help="LoadBalancer ID, e.g. alb-xxx")
    parser.add_argument(
        "--view",
        choices=["overview", "detail"],
        default="overview",
        help="View mode: overview (tree) or detail (full JSON). Default: overview",
    )
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)

    if args.view == "detail":
        output = build_detail(client, args.lb_id)
    else:
        output = build_overview(client, args.lb_id)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
