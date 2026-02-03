#!/usr/bin/env python3
"""Fetch Alibaba Cloud product list from OpenAPI metadata endpoints.

Downloads:
  https://api.aliyun.com/meta/v1/products.json?language=EN_US

Optional env vars:
  - OPENAPI_META_LANGUAGE (default: EN_US)
  - OUTPUT_DIR (default: output)
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def fetch_json(url: str) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            payload = resp.read().decode("utf-8")
    except urllib.error.URLError as exc:
        print(f"Failed to fetch {url}: {exc}", file=sys.stderr)
        sys.exit(1)
    return json.loads(payload)


def main() -> None:
    language = os.getenv("OPENAPI_META_LANGUAGE", "EN_US")
    url = f"https://api.aliyun.com/meta/v1/products.json?language={language}"

    data = fetch_json(url)

    output_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "product-scan" / "openapi-meta"
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_file = output_dir / "products.json"
    raw_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    if isinstance(data, list):
        products = data
    else:
        products = data.get("products") or data.get("Products") or []
    normalized = []
    for product in products:
        product_code = product.get("code") or product.get("product") or product.get("Product")
        versions = product.get("versions") or product.get("Versions") or []
        normalized.append({"product_code": product_code, "versions": versions})

    normalized_file = output_dir / "products_normalized.json"
    normalized_file.write_text(
        json.dumps({"language": language, "products": normalized}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Saved: {raw_file}")
    print(f"Saved: {normalized_file}")


if __name__ == "__main__":
    main()
