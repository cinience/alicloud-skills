#!/usr/bin/env python3
"""Prepare a normalized request for Model Studio Aishi (PixVerse) video generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_media(values: list[str]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for value in values:
        if "=" not in value:
            raise ValueError(f"Invalid media value: {value}. Expected type=url format.")
        media_type, url = value.split("=", 1)
        items.append({"type": media_type, "url": url})
    return items


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt")
    parser.add_argument("--media", action="append", default=[])
    parser.add_argument("--size")
    parser.add_argument("--resolution")
    parser.add_argument("--duration", type=int, required=True)
    parser.add_argument("--audio", action="store_true")
    parser.add_argument("--watermark", action="store_true")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output", default="output/aliyun-modelstudio-aishi-generation/request.json")
    args = parser.parse_args()

    payload: dict[str, object] = {
        "model": args.model,
        "input": {},
        "parameters": {
            "duration": args.duration,
            "audio": args.audio,
            "watermark": args.watermark,
        },
    }

    if args.prompt:
        payload["input"]["prompt"] = args.prompt
    media = parse_media(args.media)
    if media:
        payload["input"]["media"] = media
    if args.size:
        payload["parameters"]["size"] = args.size
    if args.resolution:
        payload["parameters"]["resolution"] = args.resolution
    if args.seed is not None:
        payload["parameters"]["seed"] = args.seed

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "request_path": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
