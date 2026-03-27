#!/usr/bin/env python3
"""Prepare a minimal request payload for Model Studio multimodal embedding."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", action="append", default=[])
    parser.add_argument("--image", action="append", default=[])
    parser.add_argument("--video", action="append", default=[])
    parser.add_argument("--model", default="qwen3-vl-embedding")
    parser.add_argument("--dimension", type=int)
    parser.add_argument(
        "--output",
        default="output/alicloud-ai-search-multimodal-embedding/request.json",
    )
    args = parser.parse_args()

    contents: list[dict[str, str]] = []
    for text in args.text:
        contents.append({"text": text})
    for image in args.image:
        contents.append({"image": image})
    for video in args.video:
        contents.append({"video": video})
    if not contents:
        contents.append({"text": "Alibaba Cloud multimodal embedding"})

    payload = {
        "model": args.model,
        "input": {
            "contents": contents,
        },
    }
    if args.dimension is not None:
        payload["dimension"] = args.dimension

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "request_path": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
