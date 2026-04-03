"""Wan 2.7 Image-to-Video generation via DashScope HTTP API.

Supports: first-frame, first+last frame, video continuation, audio-driven.
Usage:
    python generate_i2v.py --first-frame https://example.com/img.jpg --prompt "a cat running"
    python generate_i2v.py --first-frame img.jpg --last-frame img2.jpg --duration 10
    python generate_i2v.py --first-clip clip.mp4 --duration 15
    python generate_i2v.py --first-frame face.jpg --driving-audio speech.mp3
"""

import argparse
import json
import os
import sys
import time

import requests

API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
BASE_URL = os.getenv(
    "DASHSCOPE_BASE_URL",
    "https://dashscope.aliyuncs.com/api/v1",
)
MODEL = "wan2.7-i2v"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/aliyun-wan-i2v/videos")


def _headers(async_mode: bool = True) -> dict:
    h = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    if async_mode:
        h["X-DashScope-Async"] = "enable"
    return h


def create_task(
    media: list[dict],
    prompt: str = "",
    negative_prompt: str | None = None,
    resolution: str = "1080P",
    duration: int = 5,
    prompt_extend: bool = True,
    watermark: bool = False,
    seed: int | None = None,
) -> str:
    """Submit an async i2v task. Returns task_id."""
    payload: dict = {
        "model": MODEL,
        "input": {"prompt": prompt, "media": media},
        "parameters": {
            "resolution": resolution,
            "duration": duration,
            "prompt_extend": prompt_extend,
            "watermark": watermark,
        },
    }
    if negative_prompt:
        payload["input"]["negative_prompt"] = negative_prompt
    if seed is not None:
        payload["parameters"]["seed"] = seed

    resp = requests.post(
        f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
        headers=_headers(async_mode=True),
        json=payload,
    )
    resp.raise_for_status()
    data = resp.json()
    if "output" not in data or "task_id" not in data["output"]:
        raise RuntimeError(f"Unexpected response: {json.dumps(data, ensure_ascii=False)}")
    return data["output"]["task_id"]


def poll_task(task_id: str, interval: int = 15) -> dict:
    """Poll until terminal status. Returns full response."""
    while True:
        resp = requests.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
        )
        resp.raise_for_status()
        data = resp.json()
        status = data["output"]["task_status"]
        print(f"  status: {status}")
        if status in ("SUCCEEDED", "FAILED", "CANCELED"):
            return data
        time.sleep(interval)


def _build_media(args: argparse.Namespace) -> list[dict]:
    media = []
    if args.first_frame:
        media.append({"type": "first_frame", "url": args.first_frame})
    if args.last_frame:
        media.append({"type": "last_frame", "url": args.last_frame})
    if args.driving_audio:
        media.append({"type": "driving_audio", "url": args.driving_audio})
    if args.first_clip:
        media.append({"type": "first_clip", "url": args.first_clip})
    if not media:
        raise ValueError("At least one media input is required (--first-frame, --first-clip, etc.)")
    return media


def main() -> None:
    parser = argparse.ArgumentParser(description="Wan 2.7 Image-to-Video")
    parser.add_argument("--first-frame", help="First frame image URL")
    parser.add_argument("--last-frame", help="Last frame image URL")
    parser.add_argument("--driving-audio", help="Driving audio URL")
    parser.add_argument("--first-clip", help="First clip video URL for continuation")
    parser.add_argument("--prompt", default="", help="Text prompt")
    parser.add_argument("--negative-prompt", default=None)
    parser.add_argument("--resolution", default="1080P", choices=["720P", "1080P"])
    parser.add_argument("--duration", type=int, default=5, help="Video duration 2-15s")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--no-prompt-extend", action="store_true")
    parser.add_argument("--watermark", action="store_true")
    parser.add_argument("--output", default=OUTPUT_DIR, help="Output directory")
    args = parser.parse_args()

    if not API_KEY:
        print("Error: DASHSCOPE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    media = _build_media(args)
    print(f"Creating i2v task with {len(media)} media input(s)...")
    task_id = create_task(
        media=media,
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        resolution=args.resolution,
        duration=args.duration,
        prompt_extend=not args.no_prompt_extend,
        watermark=args.watermark,
        seed=args.seed,
    )
    print(f"Task created: {task_id}")
    print("Polling for result...")

    result = poll_task(task_id)
    os.makedirs(args.output, exist_ok=True)
    out_path = os.path.join(args.output, f"{task_id}.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    status = result["output"]["task_status"]
    if status == "SUCCEEDED":
        video_url = result["output"].get("video_url", "")
        print(f"Video URL: {video_url}")
    else:
        print(f"Task {status}: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    print(f"Result saved to {out_path}")


if __name__ == "__main__":
    main()
