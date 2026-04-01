#!/usr/bin/env python3
"""Fetch CDN OpenAPI metadata API list and save artifacts to output/."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import urllib.request

DEFAULT_PRODUCT_CODE = "cdn"
DEFAULT_VERSION = "2018-05-10"
OUTPUT_DIR = pathlib.Path("output/aliyun-cdn-manage")


def fetch_json(url: str, timeout: int) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "codex-skill"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_api_names(payload: dict) -> list[str]:
    raw_apis = payload.get("apis", {})
    if isinstance(raw_apis, dict):
        return sorted(raw_apis.keys())
    if isinstance(raw_apis, list):
        names = []
        for item in raw_apis:
            if isinstance(item, dict):
                name = item.get("name") or item.get("apiName")
                if name:
                    names.append(name)
            elif isinstance(item, str):
                names.append(item)
        return sorted(set(names))
    return []


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product-code", default=DEFAULT_PRODUCT_CODE)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    args = parser.parse_args()

    timeout = int(os.getenv("OPENAPI_META_TIMEOUT", "20"))
    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    url = (
        f"https://api.aliyun.com/meta/v1/products/{args.product_code}"
        f"/versions/{args.version}/api-docs.json"
    )
    payload = fetch_json(url, timeout)
    api_names = parse_api_names(payload)

    json_file = output_dir / f"{args.product_code}_{args.version}_api_docs.json"
    md_file = output_dir / f"{args.product_code}_{args.version}_api_list.md"

    json_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        f"# {args.product_code} {args.version} API List",
        "",
        f"- Source: {url}",
        f"- API count: {len(api_names)}",
        "",
    ]
    lines.extend([f"- `{name}`" for name in api_names])
    md_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Saved: {json_file}")
    print(f"Saved: {md_file}")


if __name__ == "__main__":
    main()
