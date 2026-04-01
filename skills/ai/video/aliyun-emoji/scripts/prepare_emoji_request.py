#!/usr/bin/env python3
"""Prepare normalized requests for Emoji detect/generate flows."""

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
    parser.add_argument("--face-bbox")
    parser.add_argument("--ext-bbox-face")
    parser.add_argument("--template-id")
    parser.add_argument("--detect-only", action="store_true")
    parser.add_argument("--output", default="output/aliyun-emoji/request.json")
    args = parser.parse_args()

    if args.detect_only:
        payload = {
            "model": "emoji-detect-v1",
            "input": {"image_url": args.image_url},
        }
    else:
        if not args.face_bbox or not args.ext_bbox_face or not args.template_id:
            raise SystemExit("--face-bbox, --ext-bbox-face, and --template-id are required unless --detect-only is set")
        payload = {
            "model": "emoji-v1",
            "input": {
                "image_url": args.image_url,
                "face_bbox": parse_bbox(args.face_bbox),
                "ext_bbox_face": parse_bbox(args.ext_bbox_face),
                "template_id": args.template_id,
            },
        }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "request_path": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
