#!/usr/bin/env python3
"""Generate README skill sections to avoid manual drift.

Updates:
- Included skills section in README.md / README.en.md / README.zh-TW.md
- Skill mapping section in README.en.md
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

README_ZH = ROOT / "README.md"
README_EN = ROOT / "README.en.md"
README_ZH_TW = ROOT / "README.zh-TW.md"

INCLUDED_BEGIN = "<!-- INCLUDED_SKILLS_BEGIN -->"
INCLUDED_END = "<!-- INCLUDED_SKILLS_END -->"
MAPPING_BEGIN = "<!-- SKILL_MAPPING_BEGIN -->"
MAPPING_END = "<!-- SKILL_MAPPING_END -->"

GROUP_ORDER = [
    "ai",
    "storage",
    "compute",
    "database",
    "network",
    "media",
    "observability",
    "backup",
    "data-lake",
    "data-analytics",
    "platform",
    "security",
]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm: dict[str, str] = {}
    for line in parts[1].splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip()
    return fm


def collect_skills() -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        rel = skill_md.parent.relative_to(SKILLS_DIR)
        parts = rel.parts
        if len(parts) < 2:
            continue
        top = parts[0]
        if len(parts) >= 3:
            short_path = f"{parts[1]}/{parts[2]}"
            skill_dir = parts[2]
        else:
            short_path = parts[1]
            skill_dir = parts[1]
        text = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        name = fm.get("name", skill_dir)
        rows.append((top, short_path, name))
    rows.sort(key=lambda x: (x[0], x[1]))
    return rows


def _group_sort_key(group: str) -> tuple[int, str]:
    if group in GROUP_ORDER:
        return (GROUP_ORDER.index(group), group)
    return (len(GROUP_ORDER), group)


def render_included(rows: list[tuple[str, str, str]], language: str) -> str:
    grouped: dict[str, list[str]] = {}
    for top, short_path, _ in rows:
        grouped.setdefault(top, []).append(short_path)

    lines: list[str] = []
    for group in sorted(grouped.keys(), key=_group_sort_key):
        if language == "en":
            lines.append(f"Located in `skills/{group}/`:")
        elif language == "zh-tw":
            lines.append(f"位於 `skills/{group}/`：")
        else:
            lines.append(f"位于 `skills/{group}/`：")
        lines.append("")
        for short in sorted(grouped[group]):
            lines.append(f"- `{short}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _to_display_name(skill_name: str) -> str:
    parts = [p for p in skill_name.split("-") if p.lower() != "alicloud"]
    fixed = {
        "ai": "AI",
        "oss": "OSS",
        "ecs": "ECS",
        "sls": "SLS",
        "kms": "KMS",
        "dns": "DNS",
        "rds": "RDS",
        "pai": "PAI",
        "api": "API",
        "openapi": "OpenAPI",
        "gbi": "GBI",
        "sas": "SAS",
        "bdrc": "BDRC",
        "hbr": "HBR",
        "fc": "FC",
        "dlf": "DLF",
        "tts": "TTS",
        "wan": "Wan",
        "r2v": "R2V",
        "qwen": "Qwen",
    }
    title: list[str] = []
    for p in parts:
        lp = p.lower()
        if lp in fixed:
            title.append(fixed[lp])
        else:
            title.append(p[:1].upper() + p[1:])
    return "Alibaba Cloud " + " ".join(title)


def render_mapping(rows: list[tuple[str, str, str]]) -> str:
    names = sorted({name for _, _, name in rows})
    lines = ["| Skill | Display Name |", "| --- | --- |"]
    for name in names:
        lines.append(f"| `{name}` | {_to_display_name(name)} |")
    return "\n".join(lines) + "\n"


def ensure_markers(text: str, heading: str, begin: str, end: str) -> str:
    if begin in text and end in text:
        return text
    idx = text.find(heading)
    if idx < 0:
        raise RuntimeError(f"Heading not found: {heading}")
    after_heading = text.find("\n", idx)
    if after_heading < 0:
        raise RuntimeError(f"Malformed heading block: {heading}")
    next_heading = text.find("\n## ", after_heading + 1)
    if next_heading < 0:
        next_heading = len(text)
    injected = f"\n\n{begin}\n{end}\n"
    return text[: after_heading + 1] + injected + text[next_heading:]


def replace_marked(text: str, begin: str, end: str, payload: str) -> str:
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), flags=re.S)
    replacement = f"{begin}\n{payload}{end}"
    return pattern.sub(replacement, text)


def update_file(path: Path, heading: str, begin: str, end: str, payload: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = ensure_markers(text, heading, begin, end)
    text = replace_marked(text, begin, end, payload)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    rows = collect_skills()

    update_file(
        README_ZH,
        "## 已包含技能（当前）",
        INCLUDED_BEGIN,
        INCLUDED_END,
        render_included(rows, "zh"),
    )
    update_file(
        README_EN,
        "## Included Skills (current)",
        INCLUDED_BEGIN,
        INCLUDED_END,
        render_included(rows, "en"),
    )
    update_file(
        README_ZH_TW,
        "## 已包含技能（目前）",
        INCLUDED_BEGIN,
        INCLUDED_END,
        render_included(rows, "zh-tw"),
    )
    update_file(
        README_EN,
        "## Skill Mapping (Skill → Display Name)",
        MAPPING_BEGIN,
        MAPPING_END,
        render_mapping(rows),
    )


if __name__ == "__main__":
    main()
