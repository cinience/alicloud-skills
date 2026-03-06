#!/usr/bin/env python3
"""Validate minimal inputs for the article illustrator workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Path to source Markdown article")
    parser.add_argument("--topic-slug", required=True, help="Output topic slug")
    parser.add_argument("--output", required=True, help="Path to JSON output file")
    args = parser.parse_args()

    source = Path(args.source)
    payload = {
        "source_exists": source.is_file(),
        "source_suffix": source.suffix,
        "topic_slug": args.topic_slug,
        "valid_topic_slug": bool(args.topic_slug) and "/" not in args.topic_slug and " " not in args.topic_slug,
        "status": "pass",
    }
    if not payload["source_exists"] or payload["source_suffix"].lower() != ".md" or not payload["valid_topic_slug"]:
        payload["status"] = "fail"

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
