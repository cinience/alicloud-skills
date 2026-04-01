#!/usr/bin/env python3
"""Prepare a normalized request for Qwen Deep Research."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare research.run request")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--model", default="qwen-deep-research")
    parser.add_argument("--disable-feedback", action="store_true")
    parser.add_argument("--image", action="append", default=[])
    parser.add_argument("--output", default="output/aliyun-modelstudio-qwen-deep-research/requests/request.json")
    args = parser.parse_args()

    content: list[dict[str, str]] = [{"text": args.topic}]
    for image in args.image:
        content.insert(0, {"image": image})

    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": content}],
        "parameters": {
            "enable_feedback": not args.disable_feedback,
        },
        "stream": True,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "request_path": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
