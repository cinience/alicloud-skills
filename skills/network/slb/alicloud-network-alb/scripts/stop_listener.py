#!/usr/bin/env python3
"""Stop an ALB listener.

Examples:
    python stop_listener.py --region cn-hangzhou --listener-id lsn-xxx
    python stop_listener.py --region cn-hangzhou --listener-id lsn-xxx --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Stop an ALB listener")
    parser.add_argument("--region", required=True, help="Region ID")
    parser.add_argument("--listener-id", required=True, help="Listener ID (lsn-xxx)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")

    args = parser.parse_args()

    client = create_client(args.region)
    try:
        resp = client.stop_listener(alb_models.StopListenerRequest(
            listener_id=args.listener_id,
        ))
        result = {"job_id": resp.body.job_id, "request_id": resp.body.request_id}
    except Exception as e:
        print(f"Error stopping listener: {e}", file=sys.stderr)
        return 1

    if args.json:
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        output = f"Listener {args.listener_id} stopped.\n  Job ID: {result['job_id']}"

    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
