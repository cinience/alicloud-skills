#!/usr/bin/env python3
"""Get SSH port from sshd_config via SWAS RunCommand."""

from __future__ import annotations

import argparse
import os
from alibabacloud_swas_open20200601.client import Client as SwasClient
from alibabacloud_swas_open20200601 import models as swas_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> SwasClient:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"swas.{region_id}.aliyuncs.com",
    )
    ak = os.getenv("ALICLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALICLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if ak and sk:
        config.access_key_id = ak
        config.access_key_secret = sk
    return SwasClient(config)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True)
    parser.add_argument("--instance-id", required=True)
    args = parser.parse_args()

    script = """#!/bin/bash
set -e
PORT=$(grep -E '^Port ' /etc/ssh/sshd_config | tail -n 1 | awk '{print $2}')
if [ -z "$PORT" ]; then
  PORT=22
fi
echo $PORT
"""

    client = create_client(args.region)
    resp = client.run_command(swas_models.RunCommandRequest(
        region_id=args.region,
        instance_id=args.instance_id,
        name="get-ssh-port",
        type="RunShellScript",
        command_content=script,
    ))
    print("InvokeId:", resp.body.invoke_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
