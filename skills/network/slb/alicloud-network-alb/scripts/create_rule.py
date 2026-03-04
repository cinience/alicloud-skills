#!/usr/bin/env python3
"""Create ALB forwarding rule with flexible conditions and actions.

Supports common patterns like blocking HTTP methods, host-based routing,
path-based routing, and fixed responses.

Examples:
    # Block DELETE method with 405 response
    python create_rule.py --region cn-hangzhou --listener-id lsn-xxx \\
        --name "block-delete" --priority 10 \\
        --condition-method DELETE \\
        --action-fixed-response 405 "Method Not Allowed"

    # Host-based routing to server group
    python create_rule.py --region cn-hangzhou --listener-id lsn-xxx \\
        --name "api-route" --priority 20 \\
        --condition-host "api.example.com" \\
        --action-forward-to sgp-xxx

    # Path-based routing with multiple conditions
    python create_rule.py --region cn-hangzhou --listener-id lsn-xxx \\
        --name "api-v1-route" --priority 30 \\
        --condition-host "api.example.com" \\
        --condition-path "/v1/*" \\
        --action-forward-to sgp-xxx

    # HTTP to HTTPS redirect
    python create_rule.py --region cn-hangzhou --listener-id lsn-xxx \\
        --name "force-https" --priority 5 \\
        --action-redirect https 443

    # Dry run - validate without creating
    python create_rule.py --region cn-hangzhou --listener-id lsn-xxx \\
        --name "test" --priority 100 \\
        --condition-method POST \\
        --action-fixed-response 200 "OK" \\
        --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


def create_client(region_id: str):
    """Create ALB client with credentials from environment."""
    from alibabacloud_alb20200616.client import Client as Alb20200616Client
    from alibabacloud_alb20200616 import models as alb_models
    from alibabacloud_tea_openapi import models as open_api_models

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


def parse_conditions(args: argparse.Namespace) -> list[dict]:
    """Parse condition arguments into ALB condition structures."""
    conditions: list[dict] = []

    if args.condition_method:
        conditions.append({
            "type": "Method",
            "method_config": {"values": args.condition_method.split(",")},
        })

    if args.condition_host:
        conditions.append({
            "type": "Host",
            "host_config": {"values": args.condition_host.split(",")},
        })

    if args.condition_path:
        conditions.append({
            "type": "Path",
            "path_config": {"values": args.condition_path.split(",")},
        })

    if args.condition_header:
        for header in args.condition_header:
            # Format: "X-Api-Key: value1,value2" or "X-Api-Key=value1,value2"
            if ":" in header:
                key, values = header.split(":", 1)
            elif "=" in header:
                key, values = header.split("=", 1)
            else:
                key, values = header, ""
            conditions.append({
                "type": "Header",
                "header_config": {
                    "key": key.strip(),
                    "values": [v.strip() for v in values.split(",") if v.strip()],
                },
            })

    if args.condition_query:
        for query in args.condition_query:
            # Format: "version=1.0,2.0"
            if "=" in query:
                key, values = query.split("=", 1)
            else:
                key, values = query, ""
            conditions.append({
                "type": "QueryString",
                "query_string_config": {
                    "values": [{"key": key.strip(), "value": v.strip()}
                               for v in values.split(",") if v.strip()],
                },
            })

    if args.condition_cookie:
        for cookie in args.condition_cookie:
            # Format: "session=abc,def"
            if "=" in cookie:
                key, values = cookie.split("=", 1)
            else:
                key, values = cookie, ""
            conditions.append({
                "type": "Cookie",
                "cookie_config": {
                    "values": [{"key": key.strip(), "value": v.strip()}
                               for v in values.split(",") if v.strip()],
                },
            })

    if args.condition_source_ip:
        conditions.append({
            "type": "SourceIp",
            "source_ip_config": {"values": args.condition_source_ip.split(",")},
        })

    return conditions


def parse_actions(args: argparse.Namespace) -> list[dict]:
    """Parse action arguments into ALB action structures."""
    actions: list[dict] = []
    order = 1

    if args.action_forward_to:
        actions.append({
            "type": "ForwardGroup",
            "order": order,
            "forward_group_config": {
                "server_group_tuples": [
                    {"server_group_id": sg_id.strip()}
                    for sg_id in args.action_forward_to.split(",")
                ],
            },
        })
        order += 1

    if args.action_redirect:
        # Format: "https 443" or "https" or "443"
        parts = args.action_redirect.split()
        protocol = None
        port = None
        for part in parts:
            if part.lower() in ("http", "https"):
                protocol = part.upper()
            elif part.isdigit():
                port = part
        actions.append({
            "type": "Redirect",
            "order": order,
            "redirect_config": {
                **({"protocol": protocol} if protocol else {}),
                **({"port": port} if port else {}),
                "http_redirect_code": args.action_redirect_code,
            },
        })
        order += 1

    if args.action_fixed_response:
        code, *content_parts = args.action_fixed_response.split(None, 1)
        content = content_parts[0] if content_parts else ""
        actions.append({
            "type": "FixedResponse",
            "order": order,
            "fixed_response_config": {
                "http_code": code,
                "content": content,
                **({"content_type": args.action_fixed_response_type} if args.action_fixed_response_type else {}),
            },
        })
        order += 1

    if args.action_rewrite:
        # Format: "host=/new-host" or "path=/new-path" or both
        config: dict[str, str] = {}
        for part in args.action_rewrite.split():
            if "=" in part:
                key, value = part.split("=", 1)
                if key == "host":
                    config["host"] = value
                elif key == "path":
                    config["path"] = value
        if config:
            actions.append({
                "type": "Rewrite",
                "order": order,
                "rewrite_config": config,
            })
            order += 1

    if args.action_insert_header:
        for header in args.action_insert_header:
            # Format: "X-Custom-Header: value" or "X-Custom-Header=value"
            if ":" in header:
                key, value = header.split(":", 1)
            elif "=" in header:
                key, value = header.split("=", 1)
            else:
                key, value = header, ""
            actions.append({
                "type": "InsertHeader",
                "order": order,
                "insert_header_config": {
                    "key": key.strip(),
                    "value": value.strip(),
                },
            })
            order += 1

    return actions


def build_request(args: argparse.Namespace) -> dict[str, Any]:
    """Build the CreateRule request structure."""
    conditions = parse_conditions(args)
    actions = parse_actions(args)

    if not conditions and not args.allow_no_conditions:
        raise ValueError(
            "No conditions specified. Use --condition-* options or --allow-no-conditions "
            "to create a catch-all rule."
        )

    if not actions:
        raise ValueError("No actions specified. Use --action-* options.")

    request: dict[str, Any] = {
        "listener_id": args.listener_id,
        "rule_name": args.name,
        "priority": args.priority,
        "rule_conditions": conditions,
        "rule_actions": actions,
    }

    return request


def execute_create(client, request: dict[str, Any]) -> dict[str, Any]:
    """Execute the CreateRule API call."""
    from alibabacloud_alb20200616 import models as alb_models

    # Convert dict to model objects
    conditions = []
    for c in request["rule_conditions"]:
        cond = alb_models.CreateRuleRequestRuleConditions(type=c["type"])
        if "host_config" in c:
            cond.host_config = alb_models.CreateRuleRequestRuleConditionsHostConfig(**c["host_config"])
        elif "path_config" in c:
            cond.path_config = alb_models.CreateRuleRequestRuleConditionsPathConfig(**c["path_config"])
        elif "method_config" in c:
            cond.method_config = alb_models.CreateRuleRequestRuleConditionsMethodConfig(**c["method_config"])
        elif "header_config" in c:
            cond.header_config = alb_models.CreateRuleRequestRuleConditionsHeaderConfig(**c["header_config"])
        elif "query_string_config" in c:
            values = [alb_models.CreateRuleRequestRuleConditionsQueryStringConfigValues(**v)
                      for v in c["query_string_config"]["values"]]
            cond.query_string_config = alb_models.CreateRuleRequestRuleConditionsQueryStringConfig(values=values)
        elif "cookie_config" in c:
            values = [alb_models.CreateRuleRequestRuleConditionsCookieConfigValues(**v)
                      for v in c["cookie_config"]["values"]]
            cond.cookie_config = alb_models.CreateRuleRequestRuleConditionsCookieConfig(values=values)
        elif "source_ip_config" in c:
            cond.source_ip_config = alb_models.CreateRuleRequestRuleConditionsSourceIpConfig(**c["source_ip_config"])
        conditions.append(cond)

    actions = []
    for a in request["rule_actions"]:
        act = alb_models.CreateRuleRequestRuleActions(type=a["type"], order=a["order"])
        if "forward_group_config" in a:
            tuples = [alb_models.CreateRuleRequestRuleActionsForwardGroupConfigServerGroupTuples(**t)
                      for t in a["forward_group_config"]["server_group_tuples"]]
            act.forward_group_config = alb_models.CreateRuleRequestRuleActionsForwardGroupConfig(
                server_group_tuples=tuples
            )
        elif "redirect_config" in a:
            act.redirect_config = alb_models.CreateRuleRequestRuleActionsRedirectConfig(**a["redirect_config"])
        elif "fixed_response_config" in a:
            act.fixed_response_config = alb_models.CreateRuleRequestRuleActionsFixedResponseConfig(
                **a["fixed_response_config"]
            )
        elif "rewrite_config" in a:
            act.rewrite_config = alb_models.CreateRuleRequestRuleActionsRewriteConfig(**a["rewrite_config"])
        elif "insert_header_config" in a:
            act.insert_header_config = alb_models.CreateRuleRequestRuleActionsInsertHeaderConfig(
                **a["insert_header_config"]
            )
        actions.append(act)

    req = alb_models.CreateRuleRequest(
        listener_id=request["listener_id"],
        rule_name=request["rule_name"],
        priority=request["priority"],
        rule_conditions=conditions,
        rule_actions=actions,
    )

    resp = client.create_rule(req)
    return {
        "rule_id": resp.body.rule_id,
        "job_id": resp.body.job_id,
        "request_id": resp.body.request_id,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create ALB forwarding rule",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Block DELETE method
  %(prog)s --region cn-hangzhou --listener-id lsn-xxx \\
      --name "block-delete" --priority 10 \\
      --condition-method DELETE \\
      --action-fixed-response 405 "Method Not Allowed"

  # Route by host
  %(prog)s --region cn-hangzhou --listener-id lsn-xxx \\
      --name "api-route" --priority 20 \\
      --condition-host "api.example.com" \\
      --action-forward-to sgp-xxx

  # HTTP to HTTPS redirect
  %(prog)s --region cn-hangzhou --listener-id lsn-xxx \\
      --name "force-https" --priority 5 \\
      --action-redirect https 443
        """,
    )
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--listener-id", required=True, help="Listener ID (lsn-xxx)")
    parser.add_argument("--name", required=True, help="Rule name")
    parser.add_argument("--priority", type=int, required=True, help="Rule priority (1-10000, lower = higher priority)")

    # Condition options
    cond_group = parser.add_argument_group("Conditions (at least one required)")
    cond_group.add_argument("--condition-method", help="HTTP method(s), comma-separated: GET,POST,DELETE")
    cond_group.add_argument("--condition-host", help="Host(s), comma-separated: api.example.com,*.example.com")
    cond_group.add_argument("--condition-path", help="Path(s), comma-separated: /api/*,/v1/*")
    cond_group.add_argument("--condition-header", action="append", help="Header condition: 'X-Api-Key: value1,value2'")
    cond_group.add_argument("--condition-query", action="append", help="Query string condition: 'version=1.0,2.0'")
    cond_group.add_argument("--condition-cookie", action="append", help="Cookie condition: 'session=abc,def'")
    cond_group.add_argument("--condition-source-ip", help="Source IP(s), comma-separated: 10.0.0.0/8,192.168.1.1")
    cond_group.add_argument("--allow-no-conditions", action="store_true", help="Allow creating a catch-all rule")

    # Action options
    act_group = parser.add_argument_group("Actions (at least one required)")
    act_group.add_argument("--action-forward-to", help="Forward to server group ID(s), comma-separated")
    act_group.add_argument("--action-redirect", help="Redirect: 'https 443' or 'https' or '443'")
    act_group.add_argument("--action-redirect-code", default="301", help="Redirect HTTP code (default: 301)")
    act_group.add_argument("--action-fixed-response", help="Fixed response: '404 Not Found'")
    act_group.add_argument("--action-fixed-response-type", help="Content-Type for fixed response")
    act_group.add_argument("--action-rewrite", help="Rewrite: 'host=newhost' or 'path=/newpath' or 'host=newhost path=/new'")
    act_group.add_argument("--action-insert-header", action="append", help="Insert header: 'X-Custom: value'")

    # Other options
    parser.add_argument("--dry-run", action="store_true", help="Validate and print request without creating")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")

    args = parser.parse_args()

    try:
        request = build_request(args)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.dry_run:
        output = json.dumps(request, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(output + "\n", encoding="utf-8")
            print(f"Dry-run request written to {args.output}")
        else:
            print("Dry-run mode - request structure:")
            print(output)
        return 0

    # Execute the create
    client = create_client(args.region)
    try:
        result = execute_create(client, request)
    except Exception as e:
        print(f"Error creating rule: {e}", file=sys.stderr)
        return 1

    # Output
    if args.json:
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        output = f"Rule created successfully:\n  Rule ID: {result['rule_id']}\n  Job ID: {result['job_id']}"

    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
