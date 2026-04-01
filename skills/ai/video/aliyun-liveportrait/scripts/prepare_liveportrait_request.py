#!/usr/bin/env python3
"""Prepare normalized requests for LivePortrait detect/generate flows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-url", required=True)
    parser.add_argument("--audio-url")
    parser.add_argument("--template-id", choices=["normal", "calm", "active"])
    parser.add_argument("--eye-move-freq", type=float)
    parser.add_argument("--video-fps", type=int)
    parser.add_argument("--mouth-move-strength", type=float)
    parser.add_argument("--paste-back", action="store_true")
    parser.add_argument("--head-move-strength", type=float)
    parser.add_argument("--detect-only", action="store_true")
    parser.add_argument("--output", default="output/aliyun-liveportrait/request.json")
    args = parser.parse_args()

    if args.detect_only:
        payload = {
            "model": "liveportrait-detect",
            "input": {"image_url": args.image_url},
        }
    else:
        if not args.audio_url:
            raise SystemExit("--audio-url is required unless --detect-only is set")
        payload: dict[str, object] = {
            "model": "liveportrait",
            "input": {
                "image_url": args.image_url,
                "audio_url": args.audio_url,
            },
            "parameters": {},
        }
        if args.template_id:
            payload["parameters"]["template_id"] = args.template_id
        if args.eye_move_freq is not None:
            payload["parameters"]["eye_move_freq"] = args.eye_move_freq
        if args.video_fps is not None:
            payload["parameters"]["video_fps"] = args.video_fps
        if args.mouth_move_strength is not None:
            payload["parameters"]["mouth_move_strength"] = args.mouth_move_strength
        if args.paste_back:
            payload["parameters"]["paste_back"] = True
        if args.head_move_strength is not None:
            payload["parameters"]["head_move_strength"] = args.head_move_strength

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "request_path": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
