#!/usr/bin/env python3
"""Join merged product list with OpenAPI meta API counts."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> None:
    base_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "product-scan"
    merged_file = base_dir / "merged_products.json"
    api_summary_file = base_dir / "openapi-meta" / "apis" / "summary.json"

    if not merged_file.exists():
        print("Missing merged_products.json. Run merge_product_sources.py first.", file=sys.stderr)
        sys.exit(1)
    if not api_summary_file.exists():
        print("Missing api summary. Run apis_from_openapi_meta.py first.", file=sys.stderr)
        sys.exit(1)

    merged = json.loads(merged_file.read_text(encoding="utf-8"))
    summary = json.loads(api_summary_file.read_text(encoding="utf-8"))

    api_counts = {}
    for item in summary.get("items") or []:
        key = item.get("product_code")
        if not key:
            continue
        api_counts.setdefault(key, 0)
        api_counts[key] += int(item.get("api_count") or 0)

    items = []
    for product in merged.get("products") or []:
        code = product.get("product_code") or ""
        api_count = api_counts.get(code, 0)
        entry = dict(product)
        entry["api_count"] = api_count
        items.append(entry)

    out_file = base_dir / "products_with_api_counts.json"
    out_file.write_text(
        json.dumps({"items": items, "api_counts": api_counts}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    md_lines = [
        "# 产品 + API 统计", "",
        "| 产品名 | 产品Code | API 数量 | 来源 |", "| --- | --- | --- | --- |",
    ]
    for item in items:
        name = item.get("product_name") or ""
        code = item.get("product_code") or ""
        count = item.get("api_count") or 0
        sources = ", ".join(item.get("sources") or [])
        md_lines.append(f"| {name} | {code} | {count} | {sources} |")

    md_file = base_dir / "products_with_api_counts.md"
    md_file.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Saved: {out_file}")
    print(f"Saved: {md_file}")


if __name__ == "__main__":
    main()
