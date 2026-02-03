#!/usr/bin/env python3
"""Fetch products via Ticket System ListProducts API.

Requires:
  - ALICLOUD_ACCESS_KEY_ID
  - ALICLOUD_ACCESS_KEY_SECRET
  - TICKET_ENDPOINT (e.g. <product_code>.<region>.aliyuncs.com)
Optional:
  - TICKET_VERSION (default: 2021-06-10)
  - TICKET_LANGUAGE (zh|en|jp)
  - TICKET_NAME (fuzzy name filter)
  - OUTPUT_DIR (default: output)
"""

import json
import os
import sys
from pathlib import Path


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if not value:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def main() -> None:
    try:
        from aliyunsdkcore.client import AcsClient
        from aliyunsdkcore.request import CommonRequest
    except Exception:
        print("Missing SDK. Install: pip install aliyun-python-sdk-core", file=sys.stderr)
        sys.exit(1)

    access_key_id = get_env("ALICLOUD_ACCESS_KEY_ID")
    access_key_secret = get_env("ALICLOUD_ACCESS_KEY_SECRET")
    endpoint = get_env("TICKET_ENDPOINT")
    version = os.getenv("TICKET_VERSION", "2021-06-10")

    client = AcsClient(access_key_id, access_key_secret, "cn-hangzhou")

    request = CommonRequest()
    request.set_domain(endpoint)
    request.set_version(version)
    request.set_action_name("ListProducts")
    request.set_method("GET")

    name = os.getenv("TICKET_NAME")
    language = os.getenv("TICKET_LANGUAGE")
    if name:
        request.add_query_param("Name", name)
    if language:
        request.add_query_param("Language", language)

    response = client.do_action_with_exception(request)
    data = json.loads(response.decode("utf-8"))

    output_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "product-scan" / "ticket-system"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / "products.json"
    out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()
