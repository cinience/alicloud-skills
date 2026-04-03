"""Wan 2.2 Animate Move generation via DashScope HTTP API.

Transfers actions/expressions from a reference video onto a character image.
Usage:
    python generate_animate_move.py --image-url https://example.com/person.jpg --video-url https://example.com/dance.mp4
    python generate_animate_move.py --image-url https://example.com/person.jpg --video-url https://example.com/dance.mp4 --mode wan-pro
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
MODEL = "wan2.2-animate-move"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/aliyun-wan-animate-move/videos")


def _headers(async_mode: bool = True) -> dict:
    h = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    if async_mode:
        h["X-DashScope-Async"] = "enable"
    return h


def create_task(
    image_url: str,
    video_url: str,
    mode: str = "wan-std",
    watermark: bool = False,
    check_image: bool = True,
) -> str:
    """Submit an async animate-move task. Returns task_id."""
    payload: dict = {
        "model": MODEL,
        "input": {
            "image_url": image_url,
            "video_url": video_url,
            "watermark": watermark,
        },
        "parameters": {
            "mode": mode,
            "check_image": check_image,
        },
    }

    resp = requests.post(
        f"{BASE_URL}/services/aigc/image2video/video-synthesis",
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Wan 2.2 Animate Move")
    parser.add_argument("--image-url", required=True, help="Character image URL")
    parser.add_argument("--video-url", required=True, help="Reference motion video URL")
    parser.add_argument("--mode", default="wan-std", choices=["wan-std", "wan-pro"],
                        help="Service mode: wan-std (fast) or wan-pro (quality)")
    parser.add_argument("--watermark", action="store_true", help="Add AI watermark")
    parser.add_argument("--no-check-image", action="store_true",
                        help="Skip image detection")
    parser.add_argument("--output", default=OUTPUT_DIR, help="Output directory")
    args = parser.parse_args()

    if not API_KEY:
        print("Error: DASHSCOPE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    print(f"Creating animate-move task (mode={args.mode})...")
    task_id = create_task(
        image_url=args.image_url,
        video_url=args.video_url,
        mode=args.mode,
        watermark=args.watermark,
        check_image=not args.no_check_image,
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
