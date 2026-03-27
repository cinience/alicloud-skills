#!/usr/bin/env python3
"""Prepare a normalized request for Model Studio VideoRetalk."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-url", required=True)
    parser.add_argument("--audio-url", required=True)
    parser.add_argument("--ref-image-url")
    parser.add_argument("--video-extension", action="store_true")
    parser.add_argument("--query-face-threshold", type=int)
    parser.add_argument("--output", default="output/alicloud-ai-video-retalk/request.json")
    args = parser.parse_args()

    payload: dict[str, object] = {
        "model": "videoretalk",
        "input": {
            "video_url": args.video_url,
            "audio_url": args.audio_url,
        },
        "parameters": {
            "video_extension": args.video_extension,
        },
    }
    if args.ref_image_url:
        payload["input"]["ref_image_url"] = args.ref_image_url
    if args.query_face_threshold is not None:
        payload["parameters"]["query_face_threshold"] = args.query_face_threshold

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "request_path": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
