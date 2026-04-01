#!/usr/bin/env python3
"""Prepare a normalized request for Model Studio coding models."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare code.generate request")
    parser.add_argument("--task", required=True)
    parser.add_argument("--model", default="qwen3-coder-next")
    parser.add_argument("--language")
    parser.add_argument("--repository-summary")
    parser.add_argument("--file", action="append", dest="files", default=[])
    parser.add_argument("--output", default="output/aliyun-qwen-coder/requests/request.json")
    args = parser.parse_args()

    content = args.task
    if args.repository_summary:
        content = f"Repository summary:\n{args.repository_summary}\n\nTask:\n{content}"

    payload = {
        "model": args.model,
        "messages": [
            {"role": "system", "content": "You are a careful coding assistant."},
            {"role": "user", "content": content},
        ],
    }
    if args.language:
        payload["language"] = args.language
    if args.files:
        payload["files"] = args.files

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "request_path": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
