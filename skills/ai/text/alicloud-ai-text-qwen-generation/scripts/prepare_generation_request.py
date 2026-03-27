#!/usr/bin/env python3
"""Prepare a normalized request for Model Studio text generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare text.generate request")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", default="qwen3.5-plus")
    parser.add_argument("--system", default="You are a concise Alibaba Cloud Model Studio assistant.")
    parser.add_argument("--temperature", type=float)
    parser.add_argument("--top-p", dest="top_p", type=float)
    parser.add_argument("--max-tokens", dest="max_tokens", type=int)
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--output", default="output/alicloud-ai-text-qwen-generation/requests/request.json")
    args = parser.parse_args()

    payload = {
        "model": args.model,
        "messages": [
            {"role": "system", "content": args.system},
            {"role": "user", "content": args.prompt},
        ],
        "stream": args.stream,
    }
    if args.temperature is not None:
        payload["temperature"] = args.temperature
    if args.top_p is not None:
        payload["top_p"] = args.top_p
    if args.max_tokens is not None:
        payload["max_tokens"] = args.max_tokens

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "request_path": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
