#!/usr/bin/env python3
"""Prepare a minimal request payload for Qwen Omni."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_PAYLOAD = {
    "model": "qwen3-omni-flash",
    "text": "Describe the input briefly and answer in Chinese.",
    "image": "https://example.com/demo.jpg",
    "response_modalities": ["text"],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="output/aliyun-qwen-omni/request.json",
    )
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(DEFAULT_PAYLOAD, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
