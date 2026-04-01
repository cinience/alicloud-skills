#!/usr/bin/env python3
"""Probe realtime TTS model compatibility and optionally fallback to non-realtime TTS.

Usage:
  .venv/bin/python skills/ai/audio/aliyun-qwen-tts-realtime/scripts/realtime_tts_demo.py \
    --text "hello" --fallback
"""

from __future__ import annotations

import argparse
import configparser
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any

try:
    import dashscope
except ImportError:
    print("Error: dashscope is not installed. Run: pip install dashscope", file=sys.stderr)
    sys.exit(1)

REALTIME_MODEL = "qwen3-tts-instruct-flash-realtime"
FALLBACK_MODEL = "qwen3-tts-instruct-flash"
DEFAULT_VOICE = "Cherry"
DEFAULT_LANGUAGE = "Chinese"


def _find_repo_root(start: Path) -> Path | None:
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    return None


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _load_env() -> None:
    _load_dotenv(Path.cwd() / ".env")
    repo_root = _find_repo_root(Path(__file__).resolve())
    if repo_root:
        _load_dotenv(repo_root / ".env")


def _load_dashscope_api_key_from_credentials() -> None:
    if os.environ.get("DASHSCOPE_API_KEY"):
        return
    credentials_path = Path(os.path.expanduser("~/.alibabacloud/credentials"))
    if not credentials_path.exists():
        return
    config = configparser.ConfigParser()
    try:
        config.read(credentials_path)
    except configparser.Error:
        return
    profile = os.getenv("ALIBABA_CLOUD_PROFILE") or os.getenv("ALICLOUD_PROFILE") or "default"
    if not config.has_section(profile):
        return
    key = config.get(profile, "dashscope_api_key", fallback="").strip()
    if not key:
        key = config.get(profile, "DASHSCOPE_API_KEY", fallback="").strip()
    if key:
        os.environ["DASHSCOPE_API_KEY"] = key


def _download_audio(audio_url: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(audio_url) as response:
        output_path.write_bytes(response.read())


def _probe_realtime(text: str, voice: str, instruction: str | None, language_type: str, base_url: str) -> dict[str, Any]:
    dashscope.base_http_api_url = base_url

    try:
        stream = dashscope.MultiModalConversation.call(
            model=REALTIME_MODEL,
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            text=text,
            voice=voice,
            instruction=instruction,
            language_type=language_type,
            stream=True,
        )
    except Exception as exc:  # pragma: no cover
        return {
            "ok": False,
            "model": REALTIME_MODEL,
            "stage": "call",
            "error": str(exc),
        }

    chunk_count = 0
    statuses: list[dict[str, Any]] = []
    has_audio_chunk = False

    try:
        for chunk in stream:
            chunk_count += 1
            status_code = getattr(chunk, "status_code", None)
            code = getattr(chunk, "code", None)
            message = getattr(chunk, "message", None)
            statuses.append({"status_code": status_code, "code": code, "message": message})

            out = getattr(chunk, "output", None)
            audio = getattr(out, "audio", None) if out is not None else None
            if audio:
                data = audio.get("data") if hasattr(audio, "get") else None
                if data:
                    has_audio_chunk = True

            if isinstance(status_code, int) and status_code >= 400:
                return {
                    "ok": False,
                    "model": REALTIME_MODEL,
                    "stage": "stream",
                    "chunk_count": chunk_count,
                    "statuses": statuses,
                    "error": f"status_code={status_code}, code={code}, message={message}",
                }
    except Exception as exc:
        return {
            "ok": False,
            "model": REALTIME_MODEL,
            "stage": "stream-exception",
            "chunk_count": chunk_count,
            "statuses": statuses,
            "error": str(exc),
        }

    if not has_audio_chunk:
        return {
            "ok": False,
            "model": REALTIME_MODEL,
            "stage": "stream",
            "chunk_count": chunk_count,
            "statuses": statuses,
            "error": "No audio chunks returned.",
        }

    return {
        "ok": True,
        "model": REALTIME_MODEL,
        "stage": "stream",
        "chunk_count": chunk_count,
        "statuses": statuses,
    }


def _fallback_generate(text: str, voice: str, instruction: str | None, language_type: str, base_url: str, output: Path) -> dict[str, Any]:
    dashscope.base_http_api_url = base_url
    response = dashscope.MultiModalConversation.call(
        model=FALLBACK_MODEL,
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text=text,
        voice=voice,
        instruction=instruction,
        language_type=language_type,
        stream=False,
    )

    status_code = getattr(response, "status_code", None)
    if isinstance(status_code, int) and status_code >= 400:
        return {
            "ok": False,
            "model": FALLBACK_MODEL,
            "error": f"status_code={status_code}, code={response.code}, message={response.message}",
        }

    audio = getattr(response.output, "audio", None)
    audio_url = audio.get("url") if audio else None
    if not audio_url:
        return {
            "ok": False,
            "model": FALLBACK_MODEL,
            "error": "Missing audio_url in response.",
        }

    _download_audio(audio_url, output)
    return {
        "ok": True,
        "model": FALLBACK_MODEL,
        "audio_url": audio_url,
        "output": str(output),
        "sample_rate": audio.get("sample_rate") if audio else None,
        "format": audio.get("format") if audio else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe realtime TTS and optionally fallback to non-realtime model")
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--voice", default=DEFAULT_VOICE)
    parser.add_argument("--language-type", default=DEFAULT_LANGUAGE)
    parser.add_argument("--instruction", default="Warm and calm tone, slightly slower pace.")
    parser.add_argument("--base-url", default="https://dashscope.aliyuncs.com/api/v1")
    parser.add_argument("--fallback", action="store_true", help="Fallback to non-realtime model when probe fails")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when realtime probe fails even if fallback succeeds",
    )
    default_output = Path(os.getenv("OUTPUT_DIR", "output")) / "ai-audio-tts-realtime" / "audio" / "fallback-demo.wav"
    parser.add_argument("--output", default=str(default_output), help="Fallback output path")
    args = parser.parse_args()

    _load_env()
    _load_dashscope_api_key_from_credentials()
    if not os.environ.get("DASHSCOPE_API_KEY"):
        print("Error: DASHSCOPE_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    probe = _probe_realtime(
        text=args.text,
        voice=args.voice,
        instruction=args.instruction,
        language_type=args.language_type,
        base_url=args.base_url,
    )

    result: dict[str, Any] = {"realtime_probe": probe}

    if not probe.get("ok") and args.fallback:
        fallback = _fallback_generate(
            text=args.text,
            voice=args.voice,
            instruction=args.instruction,
            language_type=args.language_type,
            base_url=args.base_url,
            output=Path(args.output),
        )
        result["fallback"] = fallback

    print(json.dumps(result, ensure_ascii=False))

    # Exit semantics:
    # - strict: realtime probe must pass
    # - non-strict: probe pass OR fallback pass
    if args.strict:
        if not probe.get("ok"):
            sys.exit(2)
        sys.exit(0)

    if probe.get("ok"):
        sys.exit(0)
    fallback_ok = bool(result.get("fallback", {}).get("ok")) if isinstance(result.get("fallback"), dict) else False
    if fallback_ok:
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
