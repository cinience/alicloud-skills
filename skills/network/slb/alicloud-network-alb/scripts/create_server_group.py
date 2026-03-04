#!/usr/bin/env python3
"""Create ALB server group with health check and sticky session configuration."""

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


def build_health_check_config(args: argparse.Namespace) -> alb_models.CreateServerGroupRequestHealthCheckConfig | None:
    """Build health check config from CLI arguments."""
    if args.health_check_disabled:
        return alb_models.CreateServerGroupRequestHealthCheckConfig(
            health_check_enabled=False,
        )

    return alb_models.CreateServerGroupRequestHealthCheckConfig(
        health_check_enabled=True,
        health_check_protocol=args.health_check_protocol or "HTTP",
        health_check_method=args.health_check_method or "HEAD",
        health_check_path=args.health_check_path or "/",
        health_check_host=args.health_check_host,
        health_check_http_version=args.health_check_http_version or "HTTP1.1",
        health_check_interval=args.health_check_interval or 5,
        health_check_timeout=args.health_check_timeout or 3,
        healthy_threshold=args.healthy_threshold or 3,
        unhealthy_threshold=args.unhealthy_threshold or 3,
        health_check_codes=args.health_check_codes or ["http_2xx"],
    )


def build_sticky_session_config(args: argparse.Namespace) -> alb_models.CreateServerGroupRequestStickySessionConfig:
    """Build sticky session config from CLI arguments.

    ALB API requires StickySessionConfig to be present even when disabled.
    """
    if not args.sticky_session_enabled:
        return alb_models.CreateServerGroupRequestStickySessionConfig(
            sticky_session_enabled=False,
        )

    return alb_models.CreateServerGroupRequestStickySessionConfig(
        sticky_session_enabled=True,
        sticky_session_type=args.sticky_session_type or "Server",
        cookie=args.sticky_session_cookie,
        cookie_timeout=args.sticky_session_timeout,
    )


def create_server_group(client: Alb20200616Client, args: argparse.Namespace) -> dict[str, Any]:
    """Create server group and return result."""
    health_check_config = build_health_check_config(args)
    sticky_session_config = build_sticky_session_config(args)

    req = alb_models.CreateServerGroupRequest(
        server_group_name=args.name,
        vpc_id=args.vpc_id,
        protocol=args.protocol or "HTTP",
        scheduler=args.scheduler or "Wrr",
        server_group_type=args.server_group_type or "Instance",
    )

    if health_check_config:
        req.health_check_config = health_check_config

    # ALB API requires StickySessionConfig to always be present
    req.sticky_session_config = sticky_session_config

    if args.connection_drain_timeout is not None:
        req.connection_drain_config = alb_models.CreateServerGroupRequestConnectionDrainConfig(
            connection_drain_enabled=args.connection_drain_timeout > 0,
            connection_drain_timeout=max(0, args.connection_drain_timeout),
        )

    resp = client.create_server_group(req)
    return {
        "server_group_id": resp.body.server_group_id,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create ALB server group",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic HTTP server group
  python create_server_group.py --region cn-hangzhou --name my-sg \\
    --vpc-id vpc-xxx --protocol HTTP

  # With health check customization
  python create_server_group.py --region cn-hangzhou --name my-sg \\
    --vpc-id vpc-xxx --protocol HTTP \\
    --health-check-path /health --health-check-interval 10

  # With sticky sessions
  python create_server_group.py --region cn-hangzhou --name my-sg \\
    --vpc-id vpc-xxx --protocol HTTP \\
    --sticky-session-enabled --sticky-session-type Server --sticky-session-cookie SERVERID

  # Disable health check (not recommended for production)
  python create_server_group.py --region cn-hangzhou --name my-sg \\
    --vpc-id vpc-xxx --health-check-disabled
        """,
    )

    # Required
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-hangzhou")
    parser.add_argument("--name", required=True, help="Server group name")
    parser.add_argument("--vpc-id", required=True, help="VPC ID")

    # Basic config
    parser.add_argument("--protocol", choices=["HTTP", "HTTPS", "GRPC"], default="HTTP", help="Protocol (default: HTTP)")
    parser.add_argument("--scheduler", choices=["Wrr", "Wlc", "Sch", "Uch"], default="Wrr", help="Scheduling algorithm (default: Wrr)")
    parser.add_argument("--server-group-type", choices=["Instance", "Ip"], default="Instance", help="Server group type (default: Instance)")

    # Health check options
    parser.add_argument("--health-check-disabled", action="store_true", help="Disable health check")
    parser.add_argument("--health-check-protocol", choices=["HTTP", "HTTPS", "TCP"], default="HTTP", help="Health check protocol")
    parser.add_argument("--health-check-method", choices=["HEAD", "GET"], default="HEAD", help="Health check method")
    parser.add_argument("--health-check-path", default="/", help="Health check path (default: /)")
    parser.add_argument("--health-check-host", help="Health check host header")
    parser.add_argument("--health-check-http-version", choices=["HTTP1.0", "HTTP1.1"], default="HTTP1.1", help="Health check HTTP version (default: HTTP1.1)")
    parser.add_argument("--health-check-interval", type=int, default=5, help="Check interval in seconds (default: 5)")
    parser.add_argument("--health-check-timeout", type=int, default=3, help="Check timeout in seconds (default: 3)")
    parser.add_argument("--healthy-threshold", type=int, default=3, help="Healthy threshold (default: 3)")
    parser.add_argument("--unhealthy-threshold", type=int, default=3, help="Unhealthy threshold (default: 3)")
    parser.add_argument("--health-check-codes", nargs="+", default=["http_2xx"], help="Expected status codes (default: http_2xx)")

    # Sticky session options
    parser.add_argument("--sticky-session-enabled", action="store_true", help="Enable sticky sessions")
    parser.add_argument("--sticky-session-type", choices=["Server", "Insert"], help="Sticky session type")
    parser.add_argument("--sticky-session-cookie", help="Cookie name for Server type")
    parser.add_argument("--sticky-session-timeout", type=int, help="Cookie timeout for Insert type (seconds)")

    # Connection draining
    parser.add_argument("--connection-drain-timeout", type=int, default=300, help="Connection drain timeout in seconds (default: 300, 0 to disable)")

    # Output
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--dry-run", action="store_true", help="Print request without executing")

    args = parser.parse_args()

    try:
        if args.dry_run:
            print("Dry run - would create server group with:")
            print(f"  Name: {args.name}")
            print(f"  VPC: {args.vpc_id}")
            print(f"  Protocol: {args.protocol}")
            print(f"  Scheduler: {args.scheduler}")
            print(f"  Health check: {'disabled' if args.health_check_disabled else 'enabled'}")
            if args.sticky_session_enabled:
                print(f"  Sticky session: enabled (type={args.sticky_session_type})")
            return 0

        client = create_client(args.region)
        result = create_server_group(client, args)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Server group created: {result['server_group_id']}")

        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
