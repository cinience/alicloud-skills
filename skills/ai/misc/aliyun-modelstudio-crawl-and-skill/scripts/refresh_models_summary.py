#!/usr/bin/env python3
"""Build a concise summary from the Model Studio models crawl markdown.

Input:
- alicloud-model-studio-models.md (from npx @just-every/crawl)

Outputs:
- output/alicloud-model-studio-models-summary.md
- output/alicloud-model-studio-models.json
"""

from __future__ import annotations

import json
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RAW_MD = ROOT / "alicloud-model-studio-models.md"
OUTPUT_DIR = ROOT / "output"

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
MODEL_ID_RE = re.compile(r"[?&]modelId=([^&]+)")
BOLD_RE = re.compile(r"\*\*([^*]{2,50})\*\*")

STOPWORDS = {
    "中国内地",
    "全球",
    "国际",
    "美国部署模式",
    "旗舰模型",
    "最大上下文长度",
    "最低输入价格",
    "最低输出价格",
    "每百万 Token",
    "Token数",
    "Token 数",
    "Token",
    "输入价格",
    "输出价格",
}


def main() -> None:
    if not RAW_MD.exists():
        raise SystemExit(f"Missing input: {RAW_MD}")

    lines = RAW_MD.read_text(encoding="utf-8", errors="ignore").splitlines()

    items = []
    seen_ids = set()
    for line in lines:
        for _, url in LINK_RE.findall(line):
            match = MODEL_ID_RE.search(url)
            if not match:
                continue
            model_id = urllib.parse.unquote(match.group(1).strip())
            if model_id in seen_ids:
                continue
            seen_ids.add(model_id)
            raw = line.strip()
            # Try to extract a short description from the line (before the first link separator).
            desc = raw.split("|", 1)[0].strip()
            desc = re.sub(r"\[.*?\]\(.*?\)", "", desc).strip()
            items.append(
                {
                    "model_id": model_id,
                    "url": url.strip(),
                    "desc": desc,
                    "raw": raw,
                }
            )

    # Add bold model names as additional candidates (no model_id).
    seen_names = set()
    for line in lines:
        for name in BOLD_RE.findall(line):
            name = name.strip()
            if not name or name in STOPWORDS:
                continue
            if any(w in name for w in ("元", "Token", "价格")):
                continue
            if name.isdigit():
                continue
            if name in seen_names:
                continue
            seen_names.add(name)
            items.append({"model_id": None, "url": None, "desc": name, "raw": line.strip()})

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT_DIR / "alicloud-model-studio-models.json"
    md_path = OUTPUT_DIR / "alicloud-model-studio-models-summary.md"

    json_path.write_text(json.dumps({"count": len(items), "models": items}, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = ["# Model Studio 模型清单（简表）", "", f"- 总数: {len(items)}", ""]
    for item in items:
        if item.get("model_id"):
            label = item.get("desc") or item.get("model_id")
            md_lines.append(f"- `{item['model_id']}` {label} ({item['url']})")
        else:
            md_lines.append(f"- {item.get('desc')}")
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"Saved: {md_path}")
    print(f"Saved: {json_path}")


if __name__ == "__main__":
    main()
