#!/usr/bin/env python3
"""Fetch products via BssOpenApi QueryProductList API.

Requires:
  - ALIBABACLOUD_ACCESS_KEY_ID (preferred; also accepts ALIBABA_CLOUD_ACCESS_KEY_ID / ALICLOUD_ACCESS_KEY_ID)
  - ALIBABACLOUD_ACCESS_KEY_SECRET (preferred; also accepts ALIBABA_CLOUD_ACCESS_KEY_SECRET / ALICLOUD_ACCESS_KEY_SECRET)
Optional:
  - ALIBABACLOUD_SECURITY_TOKEN / ALIBABA_CLOUD_SECURITY_TOKEN / ALICLOUD_SECURITY_TOKEN (STS session token)
  - BSS_ENDPOINT (default: business.aliyuncs.com)
  - BSS_VERSION (default: 2017-12-14)
  - BSS_PAGE_SIZE (default: 50)
  - OUTPUT_DIR (default: output)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        print(f"Invalid int env var {name}: {value}", file=sys.stderr)
        sys.exit(1)


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

    endpoint = os.getenv("BSS_ENDPOINT", "business.aliyuncs.com")
    version = os.getenv("BSS_VERSION", "2017-12-14")
    page_size = get_int("BSS_PAGE_SIZE", 50)

    client = AcsClient(access_key_id, access_key_secret, "cn-hangzhou", security_token)

    products: list[dict] = []
    page_num = 1
    total_count = None

    while True:
        request = CommonRequest()
        request.set_domain(endpoint)
        request.set_version(version)
        request.set_action_name("QueryProductList")
        request.set_method("GET")
        request.add_query_param("PageNum", page_num)
        request.add_query_param("PageSize", page_size)
        request.add_query_param("QueryTotalCount", True)

        response = client.do_action_with_exception(request)
        payload = json.loads(response.decode("utf-8"))
        data = payload.get("Data") or {}

        if total_count is None:
            total_count = data.get("TotalCount")

        product_list = data.get("ProductList") or {}
        product_items = product_list.get("Product") or []
        if isinstance(product_items, dict):
            product_items = [product_items]

        if not product_items:
            break

        products.extend(product_items)

        if total_count is not None:
            if len(products) >= int(total_count):
                break

        page_num += 1

    output_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "product-scan" / "bssopenapi"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / "products.json"
    out_file.write_text(
        json.dumps({"TotalCount": total_count, "Products": products}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()
