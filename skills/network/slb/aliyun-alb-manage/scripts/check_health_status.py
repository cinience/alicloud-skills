#!/usr/bin/env python3
"""Check ALB listener health status and report unhealthy backends."""

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


def _get_all_health_status(client: Alb20200616Client, listener_id: str):
    """Fetch all health status pages for a listener."""
    all_status = []
    all_rule_status = []
    next_token: str | None = None
    while True:
        req = alb_models.GetListenerHealthStatusRequest(
            listener_id=listener_id,
            include_rule=True,
            max_results=30,
            next_token=next_token,
        )
        resp = client.get_listener_health_status(req)
        all_status.extend(resp.body.listener_health_status or [])
        all_rule_status.extend(resp.body.rule_health_status or [])
        next_token = resp.body.next_token
        if not next_token:
            break
    return all_status, all_rule_status


def _format_unhealthy_servers(non_normal, indent: str = "    ") -> list[str]:
    """Format unhealthy server entries."""
    lines: list[str] = []
    for srv in non_normal:
        server_ip = srv.server_ip or "?"
        port = srv.port or "?"
        status = srv.status or "?"
        reason_str = ""
        if srv.reason:
            reason_code = srv.reason.reason_code or ""
            actual = srv.reason.actual_response or ""
            expected = srv.reason.expected_response or ""
            reason_str = reason_code
            if actual or expected:
                reason_str += f" (expected:{expected}, actual:{actual})"
        line = f"{indent}- {server_ip}:{port} [{status}]"
        if reason_str:
            line += f" {reason_str}"
        lines.append(line)
    return lines


def check_listener_health(client: Alb20200616Client, listener_id: str) -> list[str]:
    """Check health status for a single listener, return formatted lines."""
    lines: list[str] = []

    health_status, rule_health_status = _get_all_health_status(client, listener_id)

    if not health_status:
        lines.append("  (No health status data available)")
        return lines

    for lhs in health_status:
        for sg_info in lhs.server_group_infos or []:
            sg_id = sg_info.server_group_id or "?"

            # health_check_enabled is a str: "on" means enabled
            hc_enabled = sg_info.health_check_enabled
            if hc_enabled is not None and hc_enabled != "on":
                lines.append(f"  ServerGroup: {sg_id}")
                lines.append("    ⏸️  Health check disabled")
                continue

            non_normal = sg_info.non_normal_servers or []
            if not non_normal:
                lines.append(f"  ServerGroup: {sg_id}")
                lines.append("    ✅ All backends healthy")
            else:
                lines.append(f"  ServerGroup: {sg_id}")
                lines.append(f"    ⚠️  Unhealthy backends detected ({len(non_normal)}):")
                lines.extend(_format_unhealthy_servers(non_normal))

    # Rule-level health status
    if rule_health_status:
        lines.append("")
        lines.append("  Rule-level health status:")
        for rhs in rule_health_status:
            rule_id = rhs.rule_id or "?"
            for sg_info in rhs.server_group_infos or []:
                sg_id = sg_info.server_group_id or "?"
                hc_enabled = sg_info.health_check_enabled
                if hc_enabled is not None and hc_enabled != "on":
                    lines.append(f"    Rule {rule_id} → ServerGroup {sg_id}: health check disabled")
                    continue
                non_normal = sg_info.non_normal_servers or []
                if not non_normal:
                    lines.append(f"    Rule {rule_id} → ServerGroup {sg_id}: all healthy")
                else:
                    lines.append(f"    Rule {rule_id} → ServerGroup {sg_id}: {len(non_normal)} unhealthy")
                    lines.extend(_format_unhealthy_servers(non_normal, indent="      "))

    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Check ALB listener health status")
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--lb-id", required=True, help="LoadBalancer ID, e.g. alb-xxx")
    parser.add_argument("--listener-id", help="Specific listener ID. If omitted, checks all listeners.")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)

    # Determine which listeners to check
    if args.listener_id:
        listener_ids = [args.listener_id]
    else:
        listeners = list_all_listeners(client, args.lb_id)
        listener_ids = [ls.listener_id for ls in listeners if ls.listener_id]

    if args.json:
        # JSON mode: collect raw health status data for all listeners
        result = []
        for lid in listener_ids:
            health_status, rule_health_status = _get_all_health_status(client, lid)
            entry = {
                "listener_id": lid,
                "listener_health_status": [s.to_map() for s in health_status],
                "rule_health_status": [r.to_map() for r in rule_health_status],
            }
            result.append(entry)
        output = json.dumps(result, indent=2, ensure_ascii=False, default=str)
    else:
        lines: list[str] = []
        if args.listener_id:
            lines.append(f"Listener: {args.listener_id}")
            lines.extend(check_listener_health(client, args.listener_id))
        else:
            if not listener_ids:
                lines.append(f"No listeners found for ALB {args.lb_id}")
            else:
                lines.append(f"Health check for ALB: {args.lb_id} ({len(listener_ids)} listener(s))")
                lines.append("")
                for ls in listeners:
                    lid = ls.listener_id or "?"
                    proto = ls.listener_protocol or "?"
                    port = ls.listener_port or "?"
                    lstatus = ls.listener_status or "?"
                    lines.append(f"Listener: {lid} ({proto}:{port}) [{lstatus}]")
                    lines.extend(check_listener_health(client, lid))
                    lines.append("")
        output = "\n".join(lines).rstrip()
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
