#!/usr/bin/env python3
"""Prepare and validate normalized request/response for Qwen Image Edit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare image.edit request and validate response shape")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--mask")
    parser.add_argument("--size", default="1024*1024")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output", default="output/ai-image-qwen-image-edit/request.json")
    parser.add_argument("--validate-response", help="Path to JSON response file")
    args = parser.parse_args()

    req = {
        "prompt": args.prompt,
        "image": args.image,
        "size": args.size,
    }
    if args.mask:
        req["mask"] = args.mask
    if args.seed is not None:
        req["seed"] = args.seed

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(req, ensure_ascii=False, indent=2), encoding="utf-8")

    result = {"ok": True, "request_path": str(out)}

    if args.validate_response:
        resp = _load_json(args.validate_response)
        missing = [k for k in ["image_url"] if k not in resp]
        if missing:
            result = {"ok": False, "error": f"missing keys: {missing}"}
            print(json.dumps(result, ensure_ascii=False))
            sys.exit(1)
        result["response_valid"] = True

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
