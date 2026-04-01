#!/usr/bin/env python3
"""Prepare a minimal request payload for QVQ visual reasoning."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_PAYLOAD = {
    "model": "qvq-plus",
    "prompt": "Read the chart carefully and explain the trend.",
    "image": "https://example.com/chart.png",
    "max_tokens": 1024,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="output/aliyun-qvq/request.json",
    )
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(DEFAULT_PAYLOAD, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
