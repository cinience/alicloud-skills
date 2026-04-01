#!/usr/bin/env python3
"""Compare merged product list with existing skills."""

from __future__ import annotations

import json
import os
from pathlib import Path


BASE_DIR = Path(os.getenv("OUTPUT_DIR", "output")) / "product-scan"
SKILLS_DIR = Path("skills")


def read_skill_text(path: Path) -> str:
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return ""
    return content.lower()


def load_skills() -> list[dict]:
    skills = []
    for skill_file in SKILLS_DIR.rglob("SKILL.md"):
        text = read_skill_text(skill_file)
        rel = skill_file.relative_to(SKILLS_DIR)
        skills.append({"path": str(rel), "text": text})
    return skills


def product_matches_skills(product: dict, skills: list[dict]) -> list[str]:
    name = (product.get("product_name") or "").strip().lower()
    code = (product.get("product_code") or "").strip().lower()
    tokens = []
    if name and len(name) >= 2:
        tokens.append(name)
    if code and len(code) >= 2:
        tokens.append(code)

    matched = []
    for skill in skills:
        text = skill["text"]
        if any(token in text for token in tokens):
            matched.append(skill["path"])
    return matched


def main() -> None:
    merged_file = BASE_DIR / "merged_products.json"
    if not merged_file.exists():
        raise SystemExit("Missing merged_products.json. Run merge_product_sources.py first.")

    merged = json.loads(merged_file.read_text(encoding="utf-8"))
    products = merged.get("products") or []

    skills = load_skills()

    results = []
    uncovered = []
    for product in products:
        matches = product_matches_skills(product, skills)
        entry = {
            "product_name": product.get("product_name"),
            "product_code": product.get("product_code"),
            "sources": product.get("sources"),
            "matched_skills": matches,
        }
        results.append(entry)
        if not matches:
            uncovered.append(entry)

    out = {
        "total_products": len(products),
        "covered": len(products) - len(uncovered),
        "uncovered": len(uncovered),
        "items": results,
        "uncovered_items": uncovered,
    }

    out_file = BASE_DIR / "skill_gap.json"
    out_file.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        "# 产品覆盖分析", "",
        f"- 产品总数: {out['total_products']}",
        f"- 已覆盖: {out['covered']}",
        f"- 未覆盖: {out['uncovered']}",
        "",
        "## 未覆盖产品", "",
        "| 产品名 | 产品Code | 来源 |", "| --- | --- | --- |",
    ]
    for item in uncovered:
        name = item.get("product_name") or ""
        code = item.get("product_code") or ""
        sources = ", ".join(item.get("sources") or [])
        md_lines.append(f"| {name} | {code} | {sources} |")

    md_file = BASE_DIR / "skill_gap.md"
    md_file.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Saved: {out_file}")
    print(f"Saved: {md_file}")


if __name__ == "__main__":
    main()
