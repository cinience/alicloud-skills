#!/usr/bin/env python3
"""Prepare and optionally validate a CosyVoice design enrollment request."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare CosyVoice voice design request")
    parser.add_argument("--target-model", default="cosyvoice-v3.5-plus")
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--voice-prompt", required=True)
    parser.add_argument("--preview-text", required=True)
    parser.add_argument("--language-hint", default="zh")
    parser.add_argument("--sample-rate", type=int, default=24000)
    parser.add_argument("--response-format", default="wav")
    parser.add_argument(
        "--output",
        default="output/aliyun-cosyvoice-voice-design/request.json",
    )
    parser.add_argument("--validate-response", help="Path to a JSON response to validate")
    args = parser.parse_args()

    request = {
        "model": "voice-enrollment",
        "input": {
            "action": "create_voice",
            "target_model": args.target_model,
            "voice_prompt": args.voice_prompt,
            "preview_text": args.preview_text,
            "prefix": args.prefix,
            "language_hints": [args.language_hint],
        },
        "parameters": {
            "sample_rate": args.sample_rate,
            "response_format": args.response_format,
        },
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")

    result = {"ok": True, "request_path": str(out)}
    if args.validate_response:
        response = _load_json(args.validate_response)
        voice_id = ((response.get("output") or {}).get("voice_id"))
        if not voice_id:
            print(json.dumps({"ok": False, "error": "missing output.voice_id"}, ensure_ascii=False))
            sys.exit(1)
        result["response_valid"] = True

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
