#!/usr/bin/env python3
"""Prepare a minimal request payload for Wan video editing models."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_PAYLOAD = {
    "model": "wanx2.1-vace-plus",
    "prompt": "Apply a cinematic cool-tone grade and keep the subject identity stable.",
    "video_url": "https://example.com/input.mp4",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="output/aliyun-wan-edit/request.json",
    )
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(DEFAULT_PAYLOAD, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
