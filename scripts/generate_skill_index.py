#!/usr/bin/env python3
"""Generate skill index tables for README files."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
README_FILES = [
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "README.zh-TW.md",
]

BEGIN = "<!-- SKILL_INDEX_BEGIN -->"
END = "<!-- SKILL_INDEX_END -->"


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = {}
    for line in parts[1].splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip()
    return fm


def category_from_path(skill_path: Path) -> str:
    # skill_path is .../skills/<a>/<b>/<skill>/SKILL.md
    rel = skill_path.relative_to(SKILLS_DIR)
    parts = rel.parts
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"
    return parts[0]


def collect_skills() -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        name = fm.get("name", skill_md.parent.name)
        category = category_from_path(skill_md)
        path = str(skill_md.parent.relative_to(ROOT))
        rows.append((category, name, path))
    rows.sort(key=lambda x: (x[0], x[1]))
    return rows


def render_table(rows: list[tuple[str, str, str]]) -> str:
    lines = ["| Category | Skill | Path |", "| --- | --- | --- |"]
    for category, name, path in rows:
        lines.append(f"| {category} | {name} | `{path}` |")
    return "\n".join(lines)


def update_readme(path: Path, table: str) -> None:
    text = path.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        raise RuntimeError(f"Missing skill index markers in {path}")
    pattern = re.compile(
        re.escape(BEGIN) + r".*?" + re.escape(END),
        flags=re.S,
    )
    replacement = f"{BEGIN}\n{table}\n{END}"
    new_text = pattern.sub(replacement, text)
    path.write_text(new_text, encoding="utf-8")


def main() -> None:
    rows = collect_skills()
    table = render_table(rows)
    for readme in README_FILES:
        update_readme(readme, table)


if __name__ == "__main__":
    main()
