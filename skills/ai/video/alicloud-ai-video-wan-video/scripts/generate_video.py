#!/usr/bin/env python3
"""Generate a video using DashScope (wan2.6-i2v-flash) from a normalized request.

Usage:
  python scripts/generate_video.py --request '{"prompt":"...","reference_image":"./ref.png"}'
  python scripts/generate_video.py --file request.json --output output/ai-video-wan-video/videos/output.mp4
"""

from __future__ import annotations

import argparse
import configparser
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

try:
    from dashscope import VideoSynthesis
except ImportError:
    print("Error: dashscope is not installed. Run: pip install dashscope", file=sys.stderr)
    sys.exit(1)


MODEL_NAME = "wan2.6-i2v-flash"
DEFAULT_SIZE = "1280*720"
DEFAULT_FPS = 24
DEFAULT_DURATION = 4


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


def load_request(args: argparse.Namespace) -> dict[str, Any]:
    if args.request:
        return json.loads(args.request)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    raise ValueError("Either --request or --file must be provided")


def resolve_reference_image(value: str) -> Any:
    if value.startswith("http://") or value.startswith("https://"):
        return value
    path = Path(value)
    if path.exists():
        return str(path)
    return value


def call_generate(req: dict[str, Any]) -> dict[str, Any]:
    prompt = req.get("prompt")
    if not prompt:
        raise ValueError("prompt is required")

    reference_image = req.get("reference_image")
    if not reference_image:
        raise ValueError("reference_image is required for wan2.6-i2v-flash")

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "negative_prompt": req.get("negative_prompt"),
        "duration": req.get("duration", DEFAULT_DURATION),
        "fps": req.get("fps", DEFAULT_FPS),
        "size": req.get("size", DEFAULT_SIZE),
        "seed": req.get("seed"),
        "motion_strength": req.get("motion_strength"),
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
        "img_url": resolve_reference_image(reference_image),
    }

    task = VideoSynthesis.async_call(**payload)

    timeout_s = req.get("timeout_s", 600)
    poll_interval = req.get("poll_interval_s", 5)
    start = time.time()

    while True:
        final = VideoSynthesis.wait(task)
        output = getattr(final, "output", None) or {}
        status = output.get("status")
        if status in ("SUCCEEDED", "FAILED") or output.get("video_url"):
            break
        if time.time() - start > timeout_s:
            raise TimeoutError(f"Video generation timed out after {timeout_s}s")
        time.sleep(poll_interval)

    output = getattr(final, "output", None) or {}
    video_url = output.get("video_url")
    if not video_url:
        results = output.get("results") or []
        if results and isinstance(results, list):
            video_url = results[0].get("url")

    if not video_url:
        raise RuntimeError("No video URL returned by DashScope")

    return {
        "video_url": video_url,
        "duration": output.get("duration"),
        "fps": output.get("fps"),
        "seed": output.get("seed"),
    }


def download_video(video_url: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(video_url) as response:
        output_path.write_bytes(response.read())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate video with wan2.6-i2v-flash")
    parser.add_argument("--request", help="Inline JSON request string")
    parser.add_argument("--file", help="Path to JSON request file")
    default_output_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "ai-video-wan-video" / "videos"
    parser.add_argument(
        "--output",
        default=str(default_output_dir / "output.mp4"),
        help="Output video path",
    )
    parser.add_argument("--print-response", action="store_true", help="Print normalized response JSON")
    args = parser.parse_args()

    _load_env()
    _load_dashscope_api_key_from_credentials()
    if not os.environ.get("DASHSCOPE_API_KEY"):
        print(
            "Error: DASHSCOPE_API_KEY is not set. Configure it via env/.env or ~/.alibabacloud/credentials.",
            file=sys.stderr,
        )
        print("Example .env:\n  DASHSCOPE_API_KEY=your_key_here", file=sys.stderr)
        print(
            "Example credentials:\n  [default]\n  dashscope_api_key=your_key_here",
            file=sys.stderr,
        )
        sys.exit(1)

    req = load_request(args)
    result = call_generate(req)
    download_video(result["video_url"], Path(args.output))

    if args.print_response:
        print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
