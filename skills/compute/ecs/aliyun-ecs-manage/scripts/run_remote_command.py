#!/usr/bin/env python3
"""Run a remote command on one ECS instance via Cloud Assistant (RunCommand).

This utility submits a command, polls invocation results, decodes stdout,
and outputs JSON for reproducible evidence.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import time
from typing import Any

from alibabacloud_ecs20140526 import models as ecs_models
from alibabacloud_ecs20140526.client import Client as EcsClient
from alibabacloud_tea_openapi import models as open_api_models


FINAL_STATES = {"Finished", "Failed", "Stopped", "Terminated", "Timeout"}


def create_client(region_id: str) -> EcsClient:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"ecs.{region_id}.aliyuncs.com",
    )
    ak = os.getenv("ALICLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALICLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    token = os.getenv("ALICLOUD_SECURITY_TOKEN") or os.getenv("ALIBABA_CLOUD_SECURITY_TOKEN")
    if ak and sk:
        config.access_key_id = ak
        config.access_key_secret = sk
        if token:
            config.security_token = token
    return EcsClient(config)


def safe_b64decode(content: str | None) -> str:
    if not content:
        return ""
    try:
        return base64.b64decode(content).decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return ""


def to_result_payload(item: Any) -> dict[str, Any]:
    return {
        "invoke_record_status": getattr(item, "invoke_record_status", None),
        "exit_code": getattr(item, "exit_code", None),
        "finished_time": getattr(item, "finished_time", None),
        "start_time": getattr(item, "start_time", None),
        "instance_id": getattr(item, "instance_id", None),
        "stdout": safe_b64decode(getattr(item, "output", None)),
        "stderr": getattr(item, "error_info", None),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--command", required=True, help="Shell command text, e.g. 'ps -ef'")
    parser.add_argument("--region-id", default=os.getenv("ALICLOUD_REGION_ID", "cn-hangzhou"))
    parser.add_argument("--name", default="codex-remote-command")
    parser.add_argument("--command-type", default="RunShellScript", choices=["RunShellScript", "RunPowerShellScript"])
    parser.add_argument("--timeout", type=int, default=120, help="RunCommand timeout seconds")
    parser.add_argument("--poll-interval", type=float, default=2.0)
    parser.add_argument("--max-wait", type=int, default=180, help="Max polling wait seconds")
    parser.add_argument("--output", help="Write JSON output to file")
    args = parser.parse_args()

    client = create_client(args.region_id)

    run_req = ecs_models.RunCommandRequest(
        region_id=args.region_id,
        type=args.command_type,
        command_content=args.command,
        instance_id=[args.instance_id],
        name=args.name,
        timeout=args.timeout,
    )
    run_resp = client.run_command(run_req)
    invoke_id = run_resp.body.invoke_id

    poll_req = ecs_models.DescribeInvocationResultsRequest(
        region_id=args.region_id,
        invoke_id=invoke_id,
        instance_id=args.instance_id,
    )

    deadline = time.time() + args.max_wait
    final_payload: dict[str, Any] | None = None
    while time.time() < deadline:
        poll_resp = client.describe_invocation_results(poll_req)
        invocation = getattr(poll_resp.body, "invocation", None)
        inv_results = getattr(invocation, "invocation_results", None) if invocation else None
        items = getattr(inv_results, "invocation_result", None) if inv_results else None
        if items:
            item = items[0]
            status = getattr(item, "invoke_record_status", "")
            if status in FINAL_STATES:
                final_payload = to_result_payload(item)
                break
        time.sleep(args.poll_interval)

    result = {
        "region_id": args.region_id,
        "instance_id": args.instance_id,
        "invoke_id": invoke_id,
        "command": args.command,
        "command_type": args.command_type,
        "timed_out": final_payload is None,
        "result": final_payload,
    }

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)

    if final_payload is None:
        return 2
    status = final_payload.get("invoke_record_status")
    return 0 if status == "Finished" else 1


if __name__ == "__main__":
    raise SystemExit(main())
