"""Wan 2.7 Video Editing via DashScope HTTP API.

Supports: style transfer, instruction-based editing with optional reference images.
Usage:
    python edit_video.py --video https://example.com/input.mp4 --prompt "convert to clay style"
    python edit_video.py --video input.mp4 --ref-image hat.jpg --prompt "wear the hat from reference"
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
MODEL = "wan2.7-videoedit"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/aliyun-wan-videoedit/videos")


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
    ratio: str | None = None,
    duration: int = 0,
    audio_setting: str | None = None,
    prompt_extend: bool = True,
    watermark: bool = False,
    seed: int | None = None,
) -> str:
    """Submit an async video editing task. Returns task_id."""
    payload: dict = {
        "model": MODEL,
        "input": {"prompt": prompt, "media": media},
        "parameters": {
            "resolution": resolution,
            "prompt_extend": prompt_extend,
            "watermark": watermark,
        },
    }
    if negative_prompt:
        payload["input"]["negative_prompt"] = negative_prompt
    if ratio:
        payload["parameters"]["ratio"] = ratio
    if duration:
        payload["parameters"]["duration"] = duration
    if audio_setting:
        payload["parameters"]["audio_setting"] = audio_setting
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
    if not args.video:
        raise ValueError("--video is required")
    media = [{"type": "video", "url": args.video}]
    for img in args.ref_image or []:
        media.append({"type": "reference_image", "url": img})
    return media


def main() -> None:
    parser = argparse.ArgumentParser(description="Wan 2.7 Video Editing")
    parser.add_argument("--video", required=True, help="Input video URL")
    parser.add_argument("--ref-image", action="append", help="Reference image URL (up to 3)")
    parser.add_argument("--prompt", default="", help="Editing instruction")
    parser.add_argument("--negative-prompt", default=None)
    parser.add_argument("--resolution", default="1080P", choices=["720P", "1080P"])
    parser.add_argument("--ratio", default=None, choices=["16:9", "9:16", "1:1", "4:3", "3:4"])
    parser.add_argument("--duration", type=int, default=0, help="Truncate to N seconds (2-10, 0=keep original)")
    parser.add_argument("--audio-setting", default=None, choices=["auto", "origin"])
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--no-prompt-extend", action="store_true")
    parser.add_argument("--watermark", action="store_true")
    parser.add_argument("--output", default=OUTPUT_DIR, help="Output directory")
    args = parser.parse_args()

    if not API_KEY:
        print("Error: DASHSCOPE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if args.ref_image and len(args.ref_image) > 3:
        print("Error: maximum 3 reference images allowed", file=sys.stderr)
        sys.exit(1)

    media = _build_media(args)
    print(f"Creating video edit task with {len(media)} media input(s)...")
    task_id = create_task(
        media=media,
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        resolution=args.resolution,
        ratio=args.ratio,
        duration=args.duration,
        audio_setting=args.audio_setting,
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
