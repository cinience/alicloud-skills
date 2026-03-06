#!/usr/bin/env python3
"""Load EXTEND.md preferences with project-first fallback."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_PROJECT_PATH = ".alicloud-skills/alicloud-solution-content-article-illustrator/EXTEND.md"
DEFAULT_USER_PATH = "~/.alicloud-skills/alicloud-solution-content-article-illustrator/EXTEND.md"


def parse_scalar(value: str):
    text = value.strip()
    if text in {"null", "None", "~"}:
        return None
    if text in {"true", "false"}:
        return text == "true"
    if text.isdigit():
        return int(text)
    try:
        return float(text)
    except ValueError:
        pass
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    if text.startswith("'") and text.endswith("'"):
        return text[1:-1]
    return text


def parse_frontmatter(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    data: dict = {}
    stack: list[tuple[int, object]] = [(-1, data)]

    for idx, raw in enumerate(lines[1:], start=1):
        line = raw.rstrip()
        if line.strip() == "---":
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        current = stack[-1][1]

        if stripped.startswith("- "):
            item_text = stripped[2:].strip()
            if not isinstance(current, list):
                continue
            if item_text == "":
                child_dict: dict = {}
                current.append(child_dict)
                stack.append((indent, child_dict))
                continue
            if ":" in item_text:
                key, _, value = item_text.partition(":")
                child_dict = {key.strip(): parse_scalar(value.strip()) if value.strip() else {}}
                current.append(child_dict)
                if value.strip() == "":
                    stack.append((indent, child_dict[key.strip()]))
                else:
                    stack.append((indent, child_dict))
                continue
            current.append(parse_scalar(item_text))
            continue

        if ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()

        if value == "":
            next_nonempty = ""
            for candidate in lines[idx + 1:]:
                if candidate.strip():
                    next_nonempty = candidate.strip()
                    break
            if next_nonempty.startswith("- "):
                child_list: list = []
                if isinstance(current, dict):
                    current[key] = child_list
                    stack.append((indent, child_list))
            else:
                child_dict = {}
                if isinstance(current, dict):
                    current[key] = child_dict
                    stack.append((indent, child_dict))
            continue

        if isinstance(current, dict):
            current[key] = parse_scalar(value)

    return data


def collect_custom_style_names(preferences: dict) -> list[str]:
    custom_styles = preferences.get("custom_styles")
    if not isinstance(custom_styles, list):
        return []
    names: list[str] = []
    for item in custom_styles:
        if isinstance(item, dict) and isinstance(item.get("name"), str):
            names.append(item["name"])
    return names


def summarize(preferences: dict) -> dict:
    watermark = preferences.get("watermark", {}) if isinstance(preferences.get("watermark"), dict) else {}
    preferred_style = (
        preferences.get("preferred_style", {})
        if isinstance(preferences.get("preferred_style"), dict)
        else {}
    )
    return {
        "version": preferences.get("version"),
        "default_type": preferences.get("default_type"),
        "default_density": preferences.get("default_density"),
        "language": preferences.get("language"),
        "default_output_dir": preferences.get("default_output_dir"),
        "watermark_enabled": watermark.get("enabled"),
        "watermark_content": watermark.get("content"),
        "watermark_position": watermark.get("position"),
        "watermark_opacity": watermark.get("opacity"),
        "preferred_style_name": preferred_style.get("name"),
        "preferred_style_description": preferred_style.get("description"),
        "custom_style_names": collect_custom_style_names(preferences),
    }


def resolve_preferences(project_path: Path, user_path: Path) -> tuple[str, Path | None]:
    if project_path.is_file():
        return "project", project_path
    if user_path.is_file():
        return "user", user_path
    return "none", None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-path", default=DEFAULT_PROJECT_PATH, help="Project-level EXTEND.md path")
    parser.add_argument("--user-path", default=DEFAULT_USER_PATH, help="User-level EXTEND.md path")
    parser.add_argument("--output", required=True, help="Path to JSON output file")
    args = parser.parse_args()

    project_path = Path(args.project_path).expanduser()
    user_path = Path(args.user_path).expanduser()
    source, selected_path = resolve_preferences(project_path, user_path)

    payload = {
        "source": source,
        "project_path": str(project_path),
        "user_path": str(user_path),
        "selected_path": str(selected_path) if selected_path else None,
        "preferences": {},
        "summary": {},
        "status": "pass",
    }

    if selected_path is not None:
        preferences = parse_frontmatter(selected_path.read_text(encoding="utf-8"))
        payload["preferences"] = preferences
        payload["summary"] = summarize(preferences)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
