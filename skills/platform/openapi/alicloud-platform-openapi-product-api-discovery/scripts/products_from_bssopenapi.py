#!/usr/bin/env python3
"""Fetch products via BssOpenApi QueryProductList API.

Requires:
  - ALICLOUD_ACCESS_KEY_ID
  - ALICLOUD_ACCESS_KEY_SECRET
Optional:
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


def main() -> None:
    try:
        from aliyunsdkcore.client import AcsClient
        from aliyunsdkcore.request import CommonRequest
    except Exception:
        print("Missing SDK. Install: pip install aliyun-python-sdk-core", file=sys.stderr)
        sys.exit(1)

    access_key_id = os.getenv("ALICLOUD_ACCESS_KEY_ID")
    access_key_secret = os.getenv("ALICLOUD_ACCESS_KEY_SECRET")
    if not access_key_id or not access_key_secret:
        print("Missing ALICLOUD_ACCESS_KEY_ID or ALICLOUD_ACCESS_KEY_SECRET", file=sys.stderr)
        sys.exit(1)

    endpoint = os.getenv("BSS_ENDPOINT", "business.aliyuncs.com")
    version = os.getenv("BSS_VERSION", "2017-12-14")
    page_size = get_int("BSS_PAGE_SIZE", 50)

    client = AcsClient(access_key_id, access_key_secret, "cn-hangzhou")

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
