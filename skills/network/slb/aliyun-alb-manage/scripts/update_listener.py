#!/usr/bin/env python3
"""Update ALB listener attributes such as description, default action, certificates, timeouts, and security policy.

Examples:
    # Update listener description
    python update_listener.py --region cn-hangzhou --listener-id lsn-xxx \\
        --description "Production HTTP listener"

    # Change default forwarding target
    python update_listener.py --region cn-hangzhou --listener-id lsn-xxx \\
        --forward-server-groups sgp-new

    # Update certificates for HTTPS listener
    python update_listener.py --region cn-hangzhou --listener-id lsn-xxx \\
        --certificate-ids cert-xxx

    # Update security policy
    python update_listener.py --region cn-hangzhou --listener-id lsn-xxx \\
        --security-policy-id tls_cipher_policy_1_2

    # Update timeouts
    python update_listener.py --region cn-hangzhou --listener-id lsn-xxx \\
        --idle-timeout 60 --request-timeout 120

    # Enable/disable gzip or HTTP/2
    python update_listener.py --region cn-hangzhou --listener-id lsn-xxx \\
        --gzip-enabled true --http2-enabled true

    # Dry run
    python update_listener.py --region cn-hangzhou --listener-id lsn-xxx \\
        --description "test" --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from alibabacloud_alb20200616.client import Client as Alb20200616Client
from alibabacloud_alb20200616 import models as alb_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Alb20200616Client:
    """Create ALB client with credentials from environment."""
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


def parse_bool(value: str) -> bool:
    """Parse a boolean string value."""
    return value.lower() in ("true", "1", "yes")


def build_request(args: argparse.Namespace) -> dict[str, Any]:
    """Build the UpdateListenerAttribute request structure."""
    request: dict[str, Any] = {"listener_id": args.listener_id}
    has_update = False

    if args.description is not None:
        request["listener_description"] = args.description
        has_update = True

    if args.idle_timeout is not None:
        request["idle_timeout"] = args.idle_timeout
        has_update = True

    if args.request_timeout is not None:
        request["request_timeout"] = args.request_timeout
        has_update = True

    if args.security_policy_id is not None:
        request["security_policy_id"] = args.security_policy_id
        has_update = True

    if args.gzip_enabled is not None:
        request["gzip_enabled"] = parse_bool(args.gzip_enabled)
        has_update = True

    if args.http2_enabled is not None:
        request["http2_enabled"] = parse_bool(args.http2_enabled)
        has_update = True

    if args.certificate_ids:
        request["certificates"] = [{"certificate_id": cid} for cid in args.certificate_ids]
        has_update = True

    if args.forward_server_groups:
        request["default_actions"] = [{
            "type": "ForwardGroup",
            "forward_group_config": {
                "server_group_tuples": [
                    {"server_group_id": sg_id}
                    for sg_id in args.forward_server_groups
                ],
            },
        }]
        has_update = True

    if not has_update:
        raise ValueError(
            "Nothing to update. Specify at least one of: --description, --idle-timeout, "
            "--request-timeout, --security-policy-id, --gzip-enabled, --http2-enabled, "
            "--certificate-ids, --forward-server-groups"
        )

    return request


def execute_update(client: Alb20200616Client, request: dict[str, Any]) -> dict[str, Any]:
    """Execute the UpdateListenerAttribute API call."""
    req = alb_models.UpdateListenerAttributeRequest(listener_id=request["listener_id"])

    if "listener_description" in request:
        req.listener_description = request["listener_description"]

    if "idle_timeout" in request:
        req.idle_timeout = request["idle_timeout"]

    if "request_timeout" in request:
        req.request_timeout = request["request_timeout"]

    if "security_policy_id" in request:
        req.security_policy_id = request["security_policy_id"]

    if "gzip_enabled" in request:
        req.gzip_enabled = request["gzip_enabled"]

    if "http2_enabled" in request:
        req.http_2enabled = request["http2_enabled"]

    if "certificates" in request:
        req.certificates = [
            alb_models.UpdateListenerAttributeRequestCertificates(certificate_id=c["certificate_id"])
            for c in request["certificates"]
        ]

    if "default_actions" in request:
        actions = []
        for a in request["default_actions"]:
            tuples = [
                alb_models.UpdateListenerAttributeRequestDefaultActionsForwardGroupConfigServerGroupTuples(
                    server_group_id=t["server_group_id"],
                )
                for t in a["forward_group_config"]["server_group_tuples"]
            ]
            actions.append(alb_models.UpdateListenerAttributeRequestDefaultActions(
                type="ForwardGroup",
                forward_group_config=alb_models.UpdateListenerAttributeRequestDefaultActionsForwardGroupConfig(
                    server_group_tuples=tuples,
                ),
            ))
        req.default_actions = actions

    resp = client.update_listener_attribute(req)
    return {
        "job_id": resp.body.job_id,
        "request_id": resp.body.request_id,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update ALB listener attributes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update description
  %(prog)s --region cn-hangzhou --listener-id lsn-xxx \\
      --description "Updated listener"

  # Change forwarding target
  %(prog)s --region cn-hangzhou --listener-id lsn-xxx \\
      --forward-server-groups sgp-new

  # Update security and timeouts
  %(prog)s --region cn-hangzhou --listener-id lsn-xxx \\
      --security-policy-id tls_cipher_policy_1_2 \\
      --idle-timeout 60 --request-timeout 120
        """,
    )
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--listener-id", required=True, help="Listener ID to update (lsn-xxx)")

    # Attribute updates
    parser.add_argument("--description", help="New listener description")
    parser.add_argument("--idle-timeout", type=int, help="Idle timeout in seconds (1-60)")
    parser.add_argument("--request-timeout", type=int, help="Request timeout in seconds (1-180)")
    parser.add_argument("--security-policy-id", help="TLS security policy ID")
    parser.add_argument("--gzip-enabled", help="Enable gzip compression (true/false)")
    parser.add_argument("--http2-enabled", help="Enable HTTP/2 for HTTPS listener (true/false)")

    # Certificate updates
    parser.add_argument("--certificate-ids", nargs="+", help="Certificate IDs for HTTPS/QUIC")

    # Default action updates
    parser.add_argument("--forward-server-groups", nargs="+", help="Server group IDs for default forwarding action")

    # Other options
    parser.add_argument("--dry-run", action="store_true", help="Validate and print request without executing")
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

    client = create_client(args.region)
    try:
        result = execute_update(client, request)
    except Exception as e:
        print(f"Error updating listener: {e}", file=sys.stderr)
        return 1

    if args.json:
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        output = f"Listener updated successfully:\n  Job ID: {result['job_id']}"

    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
