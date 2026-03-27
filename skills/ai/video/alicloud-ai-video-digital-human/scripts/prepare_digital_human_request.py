#!/usr/bin/env python3
"""Prepare a normalized request for Model Studio digital human generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-url", required=True)
    parser.add_argument("--audio-url")
    parser.add_argument("--resolution", choices=["480P", "720P"])
    parser.add_argument("--scenario", choices=["talk", "sing", "perform"])
    parser.add_argument("--detect-only", action="store_true")
    parser.add_argument("--output", default="output/alicloud-ai-video-digital-human/request.json")
    args = parser.parse_args()

    if args.detect_only:
        payload = {
            "model": "wan2.2-s2v-detect",
            "input": {
                "image_url": args.image_url,
            },
        }
    else:
        if not args.audio_url:
            raise SystemExit("--audio-url is required unless --detect-only is set")
        payload = {
            "model": "wan2.2-s2v",
            "input": {
                "image_url": args.image_url,
                "audio_url": args.audio_url,
            },
            "parameters": {},
        }
        if args.resolution:
            payload["parameters"]["resolution"] = args.resolution
        if args.scenario:
            payload["parameters"]["scenario"] = args.scenario

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "request_path": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
