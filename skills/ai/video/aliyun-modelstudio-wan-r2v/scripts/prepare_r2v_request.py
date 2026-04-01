#!/usr/bin/env python3
"""Prepare and validate normalized request/response for Wan R2V."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare video.generate_reference request and validate response shape")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--reference-video", required=True)
    parser.add_argument("--reference-image")
    parser.add_argument("--duration", type=float)
    parser.add_argument("--fps", type=float)
    parser.add_argument("--size")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output", default="output/ai-video-wan-r2v/request.json")
    parser.add_argument("--validate-response", help="Path to JSON response file")
    args = parser.parse_args()

    req = {
        "prompt": args.prompt,
        "reference_video": args.reference_video,
    }
    if args.reference_image:
        req["reference_image"] = args.reference_image
    if args.duration is not None:
        req["duration"] = args.duration
    if args.fps is not None:
        req["fps"] = args.fps
    if args.size:
        req["size"] = args.size
    if args.seed is not None:
        req["seed"] = args.seed

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(req, ensure_ascii=False, indent=2), encoding="utf-8")

    result = {"ok": True, "request_path": str(out)}

    if args.validate_response:
        resp = _load_json(args.validate_response)
        if "video_url" not in resp and "task_id" not in resp:
            print(json.dumps({"ok": False, "error": "missing video_url and task_id"}, ensure_ascii=False))
            sys.exit(1)
        result["response_valid"] = True

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
