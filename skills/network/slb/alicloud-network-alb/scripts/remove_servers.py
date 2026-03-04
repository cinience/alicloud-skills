#!/usr/bin/env python3
"""Remove backend servers from an ALB server group.

Examples:
    # Remove a single ECS server
    python remove_servers.py --region cn-hangzhou --sg-id sgp-xxx \\
        --server ecs:i-xxx:8080

    # Remove multiple servers
    python remove_servers.py --region cn-hangzhou --sg-id sgp-xxx \\
        --server ecs:i-xxx:8080 \\
        --server ecs:i-yyy:8080

    # Remove IP-based server
    python remove_servers.py --region cn-hangzhou --sg-id sgp-xxx \\
        --server ip:10.0.1.100:8080

    # Dry run
    python remove_servers.py --region cn-hangzhou --sg-id sgp-xxx \\
        --server ecs:i-xxx:8080 --dry-run
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


SERVER_TYPE_MAP = {
    "ecs": "Ecs",
    "eni": "Eni",
    "eci": "Eci",
    "ip": "Ip",
}


def parse_server(spec: str) -> dict[str, Any]:
    """Parse server spec: type:id:port.

    For IP type: ip:address:port
    """
    parts = spec.split(":")
    if len(parts) < 3:
        raise ValueError(
            f"Invalid server spec '{spec}'. "
            "Format: type:id:port  e.g. ecs:i-xxx:8080"
        )

    raw_type = parts[0].lower()
    server_type = SERVER_TYPE_MAP.get(raw_type)
    if not server_type:
        raise ValueError(
            f"Unknown server type '{raw_type}'. Supported: {', '.join(SERVER_TYPE_MAP.keys())}"
        )

    server: dict[str, Any] = {"server_type": server_type, "port": int(parts[2])}

    if server_type == "Ip":
        server["server_ip"] = parts[1]
    else:
        server["server_id"] = parts[1]

    return server


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove backend servers from ALB server group",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Server spec format: type:id:port
  type: ecs | eni | eci | ip
  id:   instance/ENI/ECI ID, or IP address for 'ip' type
  port: backend port

Examples:
  %(prog)s --region cn-hangzhou --sg-id sgp-xxx --server ecs:i-xxx:8080
  %(prog)s --region cn-hangzhou --sg-id sgp-xxx --server ip:10.0.1.100:8080
        """,
    )
    parser.add_argument("--region", required=True, help="Region ID")
    parser.add_argument("--sg-id", required=True, dest="server_group_id", help="Server group ID")
    parser.add_argument(
        "--server", required=True, action="append", dest="servers",
        help="Server spec: type:id:port",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print request without executing")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")

    args = parser.parse_args()

    try:
        parsed_servers = [parse_server(s) for s in args.servers]
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.dry_run:
        output = json.dumps({
            "server_group_id": args.server_group_id,
            "servers": parsed_servers,
        }, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(output + "\n", encoding="utf-8")
            print(f"Dry-run request written to {args.output}")
        else:
            print("Dry-run mode - would remove servers:")
            print(output)
        return 0

    client = create_client(args.region)

    sdk_servers = []
    for s in parsed_servers:
        srv = alb_models.RemoveServersFromServerGroupRequestServers(
            server_type=s["server_type"],
            port=s["port"],
        )
        if "server_id" in s:
            srv.server_id = s["server_id"]
        if "server_ip" in s:
            srv.server_ip = s["server_ip"]
        sdk_servers.append(srv)

    try:
        resp = client.remove_servers_from_server_group(alb_models.RemoveServersFromServerGroupRequest(
            server_group_id=args.server_group_id,
            servers=sdk_servers,
        ))
        result = {"job_id": resp.body.job_id, "request_id": resp.body.request_id}
    except Exception as e:
        print(f"Error removing servers: {e}", file=sys.stderr)
        return 1

    if args.json:
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        output = f"Servers removed successfully ({len(parsed_servers)} server(s)):\n  Job ID: {result['job_id']}"

    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
