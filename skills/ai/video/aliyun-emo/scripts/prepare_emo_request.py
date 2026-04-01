#!/usr/bin/env python3
"""Prepare a normalized request for Model Studio EMO generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_bbox(value: str) -> list[int]:
    parts = [part.strip() for part in value.split(",") if part.strip()]
    if len(parts) != 4:
        raise ValueError("bbox must have 4 comma-separated integers")
    return [int(part) for part in parts]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-url", required=True)
    parser.add_argument("--audio-url")
    parser.add_argument("--face-bbox")
    parser.add_argument("--ext-bbox")
    parser.add_argument("--style-level", choices=["normal", "calm", "active"])
    parser.add_argument("--detect-only", action="store_true")
    parser.add_argument("--output", default="output/aliyun-emo/request.json")
    args = parser.parse_args()

    if args.detect_only:
        payload = {
            "model": "emo-v1-detect",
            "input": {
                "image_url": args.image_url,
            },
        }
    else:
        if not args.audio_url or not args.face_bbox or not args.ext_bbox:
            raise SystemExit("--audio-url, --face-bbox, and --ext-bbox are required unless --detect-only is set")
        payload = {
            "model": "emo-v1",
            "input": {
                "image_url": args.image_url,
                "audio_url": args.audio_url,
                "face_bbox": parse_bbox(args.face_bbox),
                "ext_bbox": parse_bbox(args.ext_bbox),
            },
            "parameters": {},
        }
        if args.style_level:
            payload["parameters"]["style_level"] = args.style_level

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "request_path": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
