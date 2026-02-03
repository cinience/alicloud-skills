#!/usr/bin/env python3
"""Analyze Model Studio models summary and suggest skill coverage.

Inputs:
- output/alicloud-model-studio-models.json

Outputs:
- output/alicloud-model-studio-skill-scan.md
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
MODELS_JSON = ROOT / "output" / "alicloud-model-studio-models.json"
OUTPUT_MD = ROOT / "output" / "alicloud-model-studio-skill-scan.md"

KEYWORDS = {
    "image": ["image", "图像", "img", "vision"],
    "video": ["video", "视频", "i2v", "t2v"],
    "audio": ["audio", "语音", "tts", "speech"],
    "asr": ["asr", "语音识别", "转写", "stt"],
    "embedding": ["embedding", "向量", "embed", "rerank"],
    "llm": ["llm", "qwen", "chat", "对话", "文本生成"],
}

KNOWN_SKILLS = {
    "image": "skills/ai/image/alicloud-ai-image-qwen-image",
    "video": "skills/ai/video/alicloud-ai-video-wan-video",
    "audio": "skills/ai/audio/alicloud-ai-audio-tts",
    "embedding": "skills/ai/search/alicloud-ai-search-dashvector",
    "asr": "(missing)",
    "llm": "(missing)",
}


def classify(name: str) -> set[str]:
    name_l = (name or "").lower()
    hits = set()
    for k, words in KEYWORDS.items():
        if any(w in name_l for w in words):
            hits.add(k)
    return hits


def main() -> None:
    if not MODELS_JSON.exists():
        raise SystemExit(f"Missing input: {MODELS_JSON}. Run refresh_models_summary.py first.")

    data = json.loads(MODELS_JSON.read_text(encoding="utf-8"))
    models = data.get("models", [])

    buckets = {k: [] for k in KEYWORDS}
    unknown = []

    for m in models:
        name = m.get("name") or m.get("model_id") or m.get("desc") or ""
        hits = classify(name)
        if not hits:
            unknown.append(m)
            continue
        for h in hits:
            buckets[h].append(m)

    lines = ["# Model Studio 技能覆盖扫描", "", f"- 模型总数: {len(models)}", ""]

    lines.append("## 覆盖建议")
    for k in KEYWORDS:
        lines.append(f"- {k}: {KNOWN_SKILLS.get(k, '(unknown)')}")

    lines.append("")
    lines.append("## 分组统计")
    for k in KEYWORDS:
        lines.append(f"- {k}: {len(buckets[k])}")

    if unknown:
        lines.append("")
        lines.append("## 未分类模型")
        for m in unknown[:50]:
            lines.append(f"- {m.get('name')} | {m.get('url')}")
        if len(unknown) > 50:
            lines.append(f"- ... {len(unknown) - 50} more")

    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
