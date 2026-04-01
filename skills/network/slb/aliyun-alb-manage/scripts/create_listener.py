#!/usr/bin/env python3
"""Create ALB listener with support for HTTP/HTTPS/QUIC and various default actions."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any

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


def build_default_action(args: argparse.Namespace) -> alb_models.CreateListenerRequestDefaultActions:
    """Build default action from CLI arguments."""
    action_type = args.action_type

    if action_type == "ForwardGroup":
        if not args.forward_server_groups:
            raise ValueError("--forward-server-groups required for ForwardGroup action")
        tuples = [
            alb_models.CreateListenerRequestDefaultActionsForwardGroupConfigServerGroupTuples(
                server_group_id=sg_id,
            )
            for sg_id in args.forward_server_groups
        ]
        return alb_models.CreateListenerRequestDefaultActions(
            type="ForwardGroup",
            forward_group_config=alb_models.CreateListenerRequestDefaultActionsForwardGroupConfig(
                server_group_tuples=tuples,
            ),
        )

    elif action_type == "Redirect":
        if not args.redirect_protocol and not args.redirect_port:
            raise ValueError("--redirect-protocol or --redirect-port required for Redirect action")
        return alb_models.CreateListenerRequestDefaultActions(
            type="Redirect",
            redirect_config=alb_models.CreateListenerRequestDefaultActionsRedirectConfig(
                protocol=args.redirect_protocol,
                port=str(args.redirect_port) if args.redirect_port else None,
                http_redirect_code=str(args.redirect_code) if args.redirect_code else "301",
            ),
        )

    elif action_type == "FixedResponse":
        if not args.fixed_response_code:
            raise ValueError("--fixed-response-code required for FixedResponse action")
        return alb_models.CreateListenerRequestDefaultActions(
            type="FixedResponse",
            fixed_response_config=alb_models.CreateListenerRequestDefaultActionsFixedResponseConfig(
                http_code=str(args.fixed_response_code),
                content=args.fixed_response_content or "",
                content_type=args.fixed_response_content_type or "text/plain",
            ),
        )

    else:
        raise ValueError(f"Unsupported action type: {action_type}")


def build_certificates(args: argparse.Namespace) -> list | None:
    """Build certificate list for HTTPS/QUIC listeners."""
    if args.protocol not in ("HTTPS", "QUIC"):
        return None
    if not args.certificate_ids:
        raise ValueError(f"--certificate-ids required for {args.protocol} listener")
    return [
        alb_models.CreateListenerRequestCertificates(certificate_id=cert_id)
        for cert_id in args.certificate_ids
    ]


def create_listener(client: Alb20200616Client, args: argparse.Namespace) -> dict[str, Any]:
    """Create listener and return result."""
    action = build_default_action(args)
    certificates = build_certificates(args)

    req = alb_models.CreateListenerRequest(
        load_balancer_id=args.load_balancer_id,
        listener_protocol=args.protocol,
        listener_port=args.port,
        default_actions=[action],
        listener_description=args.description,
    )

    if certificates:
        req.certificates = certificates

    if args.security_policy_id:
        req.security_policy_id = args.security_policy_id

    if args.http2_enabled is not None and args.protocol == "HTTPS":
        req.http_2enabled = args.http2_enabled

    if args.idle_timeout:
        req.idle_timeout = args.idle_timeout

    if args.request_timeout:
        req.request_timeout = args.request_timeout

    resp = client.create_listener(req)
    return {
        "listener_id": resp.body.listener_id,
        "job_id": resp.body.job_id,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create ALB listener",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # HTTP listener forwarding to server group
  python create_listener.py --region cn-hangzhou --lb-id alb-xxx \\
    --protocol HTTP --port 80 --action-type ForwardGroup \\
    --forward-server-groups sgp-xxx

  # HTTPS listener with certificate
  python create_listener.py --region cn-hangzhou --lb-id alb-xxx \\
    --protocol HTTPS --port 443 --action-type ForwardGroup \\
    --forward-server-groups sgp-xxx --certificate-ids cert-xxx

  # HTTP to HTTPS redirect
  python create_listener.py --region cn-hangzhou --lb-id alb-xxx \\
    --protocol HTTP --port 80 --action-type Redirect \\
    --redirect-protocol HTTPS --redirect-port 443

  # QUIC listener
  python create_listener.py --region cn-hangzhou --lb-id alb-xxx \\
    --protocol QUIC --port 443 --forward-server-groups sgp-xxx \\
    --certificate-ids cert-xxx
        """,
    )

    # Required
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--lb-id", required=True, dest="load_balancer_id", help="Load balancer ID")
    parser.add_argument("--protocol", required=True, choices=["HTTP", "HTTPS", "QUIC"], help="Listener protocol")
    parser.add_argument("--port", required=True, type=int, help="Listener port")

    # Action type
    parser.add_argument("--action-type", required=True, choices=["ForwardGroup", "Redirect", "FixedResponse"], help="Default action type")

    # ForwardGroup action options
    parser.add_argument("--forward-server-groups", nargs="+", help="Server group IDs for forwarding")

    # Redirect action options
    parser.add_argument("--redirect-protocol", choices=["HTTP", "HTTPS"], help="Target protocol for redirect")
    parser.add_argument("--redirect-port", type=int, help="Target port for redirect")
    parser.add_argument("--redirect-code", type=int, default=301, help="HTTP redirect code (default: 301)")

    # FixedResponse action options
    parser.add_argument("--fixed-response-code", type=int, help="HTTP status code for fixed response")
    parser.add_argument("--fixed-response-content", help="Response body content")
    parser.add_argument("--fixed-response-content-type", default="text/plain", help="Content type (default: text/plain)")

    # HTTPS/QUIC options
    parser.add_argument("--certificate-ids", nargs="+", help="Certificate IDs for HTTPS/QUIC")
    parser.add_argument("--security-policy-id", help="TLS security policy ID")
    parser.add_argument("--http2-enabled", type=lambda x: x.lower() == "true", help="Enable HTTP/2 (HTTPS only)")

    # General options
    parser.add_argument("--description", help="Listener description")
    parser.add_argument("--idle-timeout", type=int, help="Idle timeout in seconds")
    parser.add_argument("--request-timeout", type=int, help="Request timeout in seconds")

    # Output
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--dry-run", action="store_true", help="Print request without executing")

    args = parser.parse_args()

    try:
        action = build_default_action(args)
        certificates = build_certificates(args)

        if args.dry_run:
            print("Dry run - would create listener with:")
            print(f"  LoadBalancerId: {args.load_balancer_id}")
            print(f"  Protocol: {args.protocol}")
            print(f"  Port: {args.port}")
            print(f"  Action: {args.action_type}")
            if certificates:
                print(f"  Certificates: {args.certificate_ids}")
            return 0

        client = create_client(args.region)
        result = create_listener(client, args)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Listener created: {result['listener_id']}")
            print(f"Job ID: {result['job_id']}")
            print(f"Note: Listener creation is async. Use get_listener_attribute.py to check status.")

        return 0

    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"API Error: {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
