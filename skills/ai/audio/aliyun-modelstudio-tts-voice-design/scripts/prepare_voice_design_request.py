#!/usr/bin/env python3
"""Prepare and validate normalized request/response for Qwen TTS voice design."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare tts.voice_design request and validate response shape")
    parser.add_argument("--voice-prompt", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--output", default="output/ai-audio-tts-voice-design/request.json")
    parser.add_argument("--validate-response", help="Path to JSON response file")
    args = parser.parse_args()

    req = {
        "voice_prompt": args.voice_prompt,
        "text": args.text,
        "stream": bool(args.stream),
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(req, ensure_ascii=False, indent=2), encoding="utf-8")

    result = {"ok": True, "request_path": str(out)}

    if args.validate_response:
        resp = _load_json(args.validate_response)
        if "audio_url" not in resp and "audio_base64_pcm" not in resp:
            print(json.dumps({"ok": False, "error": "missing audio_url/audio_base64_pcm"}, ensure_ascii=False))
            sys.exit(1)
        result["response_valid"] = True

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
