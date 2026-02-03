#!/usr/bin/env python3
"""Fix SSH access for SWAS instances.

- Ensures authorized_keys contains the provided public key
- Ensures PermitRootLogin and PubkeyAuthentication are enabled
- Restarts ssh service
- Optionally sets Port in sshd_config

This script uses SWAS RunCommand to execute on the instance.
"""

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


def build_script(pub_key: str, user: str, port: str | None) -> str:
    port_block = ""
    if port:
        port_block = f"""
if ! grep -q '^Port' $SSHD_CONFIG; then
  echo 'Port {port}' >> $SSHD_CONFIG
else
  sed -i 's/^Port.*/Port {port}/' $SSHD_CONFIG
fi
"""

    return f"""#!/bin/bash
set -e
USER_NAME="{user}"
HOME_DIR=$(getent passwd "$USER_NAME" | cut -d: -f6)
if [ -z "$HOME_DIR" ]; then
  echo "User $USER_NAME not found"
  exit 1
fi

mkdir -p "$HOME_DIR/.ssh"
chmod 700 "$HOME_DIR/.ssh"
if ! grep -qF '{pub_key}' "$HOME_DIR/.ssh/authorized_keys" 2>/dev/null; then
  echo '{pub_key}' >> "$HOME_DIR/.ssh/authorized_keys"
fi
chmod 600 "$HOME_DIR/.ssh/authorized_keys"
chown -R "$USER_NAME":"$USER_NAME" "$HOME_DIR/.ssh"

SSHD_CONFIG=/etc/ssh/sshd_config
if ! grep -q '^PermitRootLogin' $SSHD_CONFIG; then
  echo 'PermitRootLogin yes' >> $SSHD_CONFIG
else
  sed -i 's/^PermitRootLogin.*/PermitRootLogin yes/' $SSHD_CONFIG
fi
if ! grep -q '^PubkeyAuthentication' $SSHD_CONFIG; then
  echo 'PubkeyAuthentication yes' >> $SSHD_CONFIG
else
  sed -i 's/^PubkeyAuthentication.*/PubkeyAuthentication yes/' $SSHD_CONFIG
fi
{port_block}

if systemctl list-unit-files | grep -q '^ssh\\.service'; then
  systemctl restart ssh
elif systemctl list-unit-files | grep -q '^sshd\\.service'; then
  systemctl restart sshd
elif command -v service >/dev/null 2>&1; then
  service ssh restart || service sshd restart
elif [ -x /etc/init.d/ssh ]; then
  /etc/init.d/ssh restart
elif [ -x /etc/init.d/sshd ]; then
  /etc/init.d/sshd restart
else
  echo "No ssh service found"
  exit 1
fi
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True)
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--user", default="root")
    parser.add_argument("--port", help="Set SSH port in sshd_config")
    parser.add_argument("--pubkey", default="~/.ssh/id_ed25519.pub")
    args = parser.parse_args()

    pubkey_path = os.path.expanduser(args.pubkey)
    with open(pubkey_path, "r", encoding="utf-8") as f:
        pub_key = f.read().strip()

    script = build_script(pub_key, args.user, args.port)
    client = create_client(args.region)
    resp = client.run_command(swas_models.RunCommandRequest(
        region_id=args.region,
        instance_id=args.instance_id,
        name="fix-ssh-access",
        type="RunShellScript",
        command_content=script,
    ))
    print("InvokeId:", resp.body.invoke_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
