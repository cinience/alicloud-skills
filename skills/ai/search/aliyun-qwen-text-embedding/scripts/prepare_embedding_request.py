#!/usr/bin/env python3
"""Prepare a minimal request payload for Model Studio text embedding."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default="Alibaba Cloud Model Studio")
    parser.add_argument("--model", default="text-embedding-v4")
    parser.add_argument(
        "--output",
        default="output/aliyun-qwen-text-embedding/request.json",
    )
    args = parser.parse_args()

    payload = {
        "model": args.model,
        "input": {
            "texts": [args.text],
        },
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
