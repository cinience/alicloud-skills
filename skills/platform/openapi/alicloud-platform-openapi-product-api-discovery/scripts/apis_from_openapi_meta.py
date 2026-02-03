#!/usr/bin/env python3
"""Fetch API list/details from OpenAPI metadata for product/version pairs.

Requires a products list from products_from_openapi_meta.py.

Optional env vars:
  - OPENAPI_META_PRODUCTS_FILE (default: output/product-scan/openapi-meta/products_normalized.json)
  - OPENAPI_META_OUTPUT_DIR (default: output/product-scan/openapi-meta/apis)
  - OPENAPI_META_PRODUCTS (comma-separated product codes to include)
  - OPENAPI_META_VERSIONS (comma-separated versions to include)
  - OPENAPI_META_MAX_PRODUCTS (limit number of products to fetch)
  - OPENAPI_META_SLEEP_SECONDS (default: 0.2)
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def fetch_json(url: str) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            payload = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        print(f"HTTP error {exc.code} for {url}", file=sys.stderr)
        return {}
    except urllib.error.URLError as exc:
        print(f"Failed to fetch {url}: {exc}", file=sys.stderr)
        return {}
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        print(f"Invalid JSON for {url}", file=sys.stderr)
        return {}


def parse_list(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def main() -> None:
    products_file = Path(
        os.getenv(
            "OPENAPI_META_PRODUCTS_FILE",
            "output/product-scan/openapi-meta/products_normalized.json",
        )
    )
    if not products_file.exists():
        print(f"Missing products file: {products_file}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(
        os.getenv("OPENAPI_META_OUTPUT_DIR", "output/product-scan/openapi-meta/apis")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    include_products = parse_list(os.getenv("OPENAPI_META_PRODUCTS"))
    include_versions = parse_list(os.getenv("OPENAPI_META_VERSIONS"))
    max_products = os.getenv("OPENAPI_META_MAX_PRODUCTS")
    sleep_seconds = float(os.getenv("OPENAPI_META_SLEEP_SECONDS", "0.2"))

    data = json.loads(products_file.read_text(encoding="utf-8"))
    products = data.get("products") or []

    summary = []
    processed = 0

    for product in products:
        product_code = product.get("product_code")
        if not product_code:
            continue
        if include_products and product_code not in include_products:
            continue

        versions = product.get("versions") or []
        if include_versions:
            versions = [v for v in versions if v in include_versions]

        for version in versions:
            url = (
                "https://api.aliyun.com/meta/v1/products/"
                f"{product_code}/versions/{version}/api-docs.json"
            )
            payload = fetch_json(url)
            if not payload:
                continue

            api_count = len(payload.get("apis") or [])

            product_dir = output_dir / product_code / version
            product_dir.mkdir(parents=True, exist_ok=True)
            out_file = product_dir / "api-docs.json"
            out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

            summary.append(
                {
                    "product_code": product_code,
                    "version": version,
                    "api_count": api_count,
                    "api_docs_path": str(out_file),
                }
            )
            time.sleep(sleep_seconds)

        processed += 1
        if max_products and processed >= int(max_products):
            break

    summary_file = output_dir / "summary.json"
    summary_file.write_text(json.dumps({"items": summary}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved: {summary_file}")


if __name__ == "__main__":
    main()
