#!/usr/bin/env python3
"""Merge product outputs from ticket system, support service, and BSS OpenAPI."""

from __future__ import annotations

import json
import os
from pathlib import Path


BASE_DIR = Path(os.getenv("OUTPUT_DIR", "output")) / "product-scan"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_ticket(data: dict) -> list[dict]:
    results: list[dict] = []
    directories = data.get("Data") or []
    for directory in directories:
        directory_name = directory.get("DirectoryName")
        directory_id = directory.get("DirectoryId")
        product_list = directory.get("ProductList") or []
        for product in product_list:
            results.append(
                {
                    "source": "ticket-system",
                    "product_name": product.get("ProductName"),
                    "product_id": product.get("ProductId"),
                    "directory_name": directory_name,
                    "directory_id": directory_id,
                }
            )
    return results


def normalize_support(data: dict) -> list[dict]:
    results: list[dict] = []
    products = data.get("DataParsed") or []
    for product in products:
        results.append(
            {
                "source": "support-service",
                "product_name": product.get("ProductName") or product.get("productName"),
                "product_code": product.get("ProductCode") or product.get("productCode"),
            }
        )
    return results


def normalize_bss(data: dict) -> list[dict]:
    results: list[dict] = []
    products = data.get("Products") or []
    for product in products:
        results.append(
            {
                "source": "bssopenapi",
                "product_name": product.get("ProductName"),
                "product_code": product.get("ProductCode"),
                "product_type": product.get("ProductType"),
                "subscription_type": product.get("SubscriptionType"),
            }
        )
    return results


def normalize_key(item: dict) -> str:
    product_code = item.get("product_code")
    product_name = item.get("product_name")
    if product_code:
        return str(product_code).strip().lower()
    if product_name:
        return str(product_name).strip().lower()
    return ""


def main() -> None:
    ticket_data = load_json(BASE_DIR / "ticket-system" / "products.json")
    support_data = load_json(BASE_DIR / "support-service" / "products.json")
    bss_data = load_json(BASE_DIR / "bssopenapi" / "products.json")

    merged = normalize_ticket(ticket_data) + normalize_support(support_data) + normalize_bss(bss_data)

    deduped: dict[str, dict] = {}
    for item in merged:
        key = normalize_key(item)
        if not key:
            key = f"{item.get('source','unknown')}:{len(deduped)}"
        if key not in deduped:
            deduped[key] = item
            deduped[key]["sources"] = [item.get("source")]
            continue
        existing = deduped[key]
        sources = existing.get("sources", [])
        if item.get("source") not in sources:
            sources.append(item.get("source"))
        for field, value in item.items():
            if field in ("source", "sources"):
                continue
            if not existing.get(field) and value:
                existing[field] = value

    out = {
        "counts": {
            "ticket-system": len(normalize_ticket(ticket_data)),
            "support-service": len(normalize_support(support_data)),
            "bssopenapi": len(normalize_bss(bss_data)),
            "merged_unique": len(deduped),
        },
        "products": sorted(deduped.values(), key=lambda x: (x.get("product_name") or "")),
    }

    BASE_DIR.mkdir(parents=True, exist_ok=True)
    out_file = BASE_DIR / "merged_products.json"
    out_file.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        "# 产品汇总", "",
        f"- 工单系统: {out['counts']['ticket-system']}",
        f"- 支持与服务: {out['counts']['support-service']}",
        f"- 费用与成本: {out['counts']['bssopenapi']}",
        f"- 去重后: {out['counts']['merged_unique']}",
        "",
        "| 产品名 | 产品Code | 来源 |", "| --- | --- | --- |",
    ]
    for item in out["products"]:
        name = item.get("product_name") or ""
        code = item.get("product_code") or ""
        sources = ", ".join(item.get("sources", []))
        md_lines.append(f"| {name} | {code} | {sources} |")

    md_file = BASE_DIR / "merged_products.md"
    md_file.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Saved: {out_file}")
    print(f"Saved: {md_file}")


if __name__ == "__main__":
    main()
