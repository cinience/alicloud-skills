#!/usr/bin/env python3
"""Prepare a minimal request payload for Qwen ASR Realtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_PAYLOAD = {
    "model": "qwen3-asr-flash-realtime",
    "input_audio": {
        "format": "pcm",
        "sample_rate": 16000,
        "channels": 1,
    },
    "language_hints": ["zh", "en"],
    "chunk_ms": 100,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="output/aliyun-qwen-asr-realtime/request.json",
        help="Path to write the sample request payload.",
    )
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(DEFAULT_PAYLOAD, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
