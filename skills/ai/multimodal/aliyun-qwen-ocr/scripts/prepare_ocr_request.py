#!/usr/bin/env python3
"""Prepare a normalized request for Model Studio Qwen OCR."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--model", default="qwen-vl-ocr")
    parser.add_argument("--prompt")
    parser.add_argument("--task")
    parser.add_argument("--task-config")
    parser.add_argument("--enable-rotate", action="store_true")
    parser.add_argument("--min-pixels", type=int)
    parser.add_argument("--max-pixels", type=int)
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--temperature", type=float)
    parser.add_argument(
        "--output",
        default="output/aliyun-qwen-ocr/request.json",
    )
    args = parser.parse_args()

    content_item = {
        "type": "image_url",
        "image_url": {
            "url": args.image,
        },
    }
    if args.min_pixels is not None:
        content_item["min_pixels"] = args.min_pixels
    if args.max_pixels is not None:
        content_item["max_pixels"] = args.max_pixels
    if args.enable_rotate:
        content_item["enable_rotate"] = True

    message = {
        "role": "user",
        "content": [content_item],
    }
    if args.prompt:
        message["content"].append({"type": "text", "text": args.prompt})

    payload = {
        "model": args.model,
        "messages": [message],
    }
    if args.max_tokens is not None:
        payload["max_tokens"] = args.max_tokens
    if args.temperature is not None:
        payload["temperature"] = args.temperature
    if args.task:
        payload["ocr_options"] = {"task": args.task}
        if args.task_config:
            payload["ocr_options"]["task_config"] = json.loads(args.task_config)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "request_path": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
