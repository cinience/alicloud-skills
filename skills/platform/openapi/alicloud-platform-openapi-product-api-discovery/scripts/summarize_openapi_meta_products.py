#!/usr/bin/env python3
"""Summarize OpenAPI meta products by category/group."""

from __future__ import annotations

import json
import os
from collections import defaultdict
from pathlib import Path


def main() -> None:
    base_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "product-scan" / "openapi-meta"
    products_file = base_dir / "products.json"
    if not products_file.exists():
        raise SystemExit("Missing products.json. Run products_from_openapi_meta.py first.")

    data = json.loads(products_file.read_text(encoding="utf-8"))
    products = data if isinstance(data, list) else data.get("products") or data.get("Products") or []

    by_category2 = defaultdict(list)
    by_category1 = defaultdict(list)
    by_group = defaultdict(list)

    for product in products:
        code = product.get("code") or ""
        name = product.get("name") or ""
        category2 = product.get("category2Name") or "Uncategorized"
        category1 = product.get("categoryName") or "Uncategorized"
        group = product.get("group") or "Uncategorized"
        entry = {"code": code, "name": name}
        by_category2[category2].append(entry)
        by_category1[category1].append(entry)
        by_group[group].append(entry)

    def write_section(title: str, mapping: dict[str, list[dict]], lines: list[str]) -> None:
        lines.append(f"## {title}")
        lines.append("")
        for key in sorted(mapping.keys()):
            lines.append(f"### {key} ({len(mapping[key])})")
            lines.append("")
            lines.append("| 产品Code | 产品名 |")
            lines.append("| --- | --- |")
            for item in sorted(mapping[key], key=lambda x: x.get("code") or ""):
                lines.append(f"| {item.get('code','')} | {item.get('name','')} |")
            lines.append("")

    md_lines = ["# OpenAPI 产品分类汇总", "", f"产品总数: {len(products)}", ""]
    write_section("二级类目 (category2Name)", by_category2, md_lines)
    write_section("一级类目 (categoryName)", by_category1, md_lines)
    write_section("集团/业务线 (group)", by_group, md_lines)

    out_file = base_dir / "products_summary.md"
    out_file.write_text("\n".join(md_lines), encoding="utf-8")

    json_file = base_dir / "products_summary.json"
    json_file.write_text(
        json.dumps(
            {
                "total": len(products),
                "by_category2": by_category2,
                "by_category1": by_category1,
                "by_group": by_group,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Saved: {out_file}")
    print(f"Saved: {json_file}")


if __name__ == "__main__":
    main()
