#!/usr/bin/env python3
"""Prepare normalized requests for AnimateAnyone detect/template/generate flows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-url")
    parser.add_argument("--video-url")
    parser.add_argument("--template-id")
    parser.add_argument("--detect-only", action="store_true")
    parser.add_argument("--template-only", action="store_true")
    parser.add_argument("--use-ref-img-bg", action="store_true")
    parser.add_argument("--output", default="output/alicloud-ai-video-animate-anyone/request.json")
    args = parser.parse_args()

    if args.detect_only:
        if not args.image_url:
            raise SystemExit("--image-url is required for --detect-only")
        payload = {
            "model": "animate-anyone-detect-gen2",
            "input": {"image_url": args.image_url},
        }
    elif args.template_only:
        if not args.video_url:
            raise SystemExit("--video-url is required for --template-only")
        payload = {
            "model": "animate-anyone-template-gen2",
            "input": {"video_url": args.video_url},
        }
    else:
        if not args.image_url or not args.template_id:
            raise SystemExit("--image-url and --template-id are required for generation")
        payload = {
            "model": "animate-anyone-gen2",
            "input": {
                "image_url": args.image_url,
                "template_id": args.template_id,
            },
            "parameters": {
                "use_ref_img_bg": args.use_ref_img_bg,
            },
        }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "request_path": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
