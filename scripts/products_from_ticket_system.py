#!/usr/bin/env python3
"""Fetch products via Ticket System ListProducts API.

Requires:
  - ALIBABACLOUD_ACCESS_KEY_ID (preferred; also accepts ALIBABA_CLOUD_ACCESS_KEY_ID / ALICLOUD_ACCESS_KEY_ID)
  - ALIBABACLOUD_ACCESS_KEY_SECRET (preferred; also accepts ALIBABA_CLOUD_ACCESS_KEY_SECRET / ALICLOUD_ACCESS_KEY_SECRET)
  - TICKET_ENDPOINT (e.g. <product_code>.<region>.aliyuncs.com)
Optional:
  - ALIBABACLOUD_SECURITY_TOKEN / ALIBABA_CLOUD_SECURITY_TOKEN / ALICLOUD_SECURITY_TOKEN (STS session token)
  - TICKET_VERSION (default: 2021-06-10)
  - TICKET_LANGUAGE (zh|en|jp)
  - TICKET_NAME (fuzzy name filter)
  - OUTPUT_DIR (default: output)
"""

import json
import os
import sys
from pathlib import Path


def get_env(*names: str, default: str | None = None) -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    if default is not None:
        return default
    print(f"Missing env var: {' / '.join(names)}", file=sys.stderr)
    sys.exit(1)


def get_optional_env(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def main() -> None:
    try:
        from aliyunsdkcore.client import AcsClient
        from aliyunsdkcore.request import CommonRequest
    except Exception:
        print("Missing SDK. Install: pip install aliyun-python-sdk-core", file=sys.stderr)
        sys.exit(1)

    access_key_id = get_env(
        "ALIBABACLOUD_ACCESS_KEY_ID",
        "ALIBABA_CLOUD_ACCESS_KEY_ID",
        "ALICLOUD_ACCESS_KEY_ID",
    )
    access_key_secret = get_env(
        "ALIBABACLOUD_ACCESS_KEY_SECRET",
        "ALIBABA_CLOUD_ACCESS_KEY_SECRET",
        "ALICLOUD_ACCESS_KEY_SECRET",
    )
    security_token = get_optional_env(
        "ALIBABACLOUD_SECURITY_TOKEN",
        "ALIBABA_CLOUD_SECURITY_TOKEN",
        "ALICLOUD_SECURITY_TOKEN",
    )
    endpoint = get_env("TICKET_ENDPOINT")
    version = os.getenv("TICKET_VERSION", "2021-06-10")

    client = AcsClient(access_key_id, access_key_secret, "cn-hangzhou", security_token)

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
