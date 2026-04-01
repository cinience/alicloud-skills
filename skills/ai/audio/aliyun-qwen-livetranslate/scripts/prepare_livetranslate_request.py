#!/usr/bin/env python3
"""Prepare a minimal request payload for Qwen LiveTranslate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-language", default="zh")
    parser.add_argument("--target-language", default="en")
    parser.add_argument(
        "--output",
        default="output/aliyun-qwen-livetranslate/request.json",
    )
    args = parser.parse_args()

    payload = {
        "model": "qwen3-livetranslate-flash",
        "source_language": args.source_language,
        "target_language": args.target_language,
        "audio": {
            "format": "pcm",
            "sample_rate": 16000,
            "channels": 1,
        },
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
