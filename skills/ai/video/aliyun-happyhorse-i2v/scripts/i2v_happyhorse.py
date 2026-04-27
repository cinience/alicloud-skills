"""HappyHorse 1.0 Image-to-Video (first-frame) generation via DashScope HTTP API.

Usage:
    python i2v_happyhorse.py --first-frame https://example.com/img.jpg --prompt "a cat running"
    python i2v_happyhorse.py --first-frame img.jpg --duration 10 --resolution 720P
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
MODEL = "happyhorse-1.0-i2v"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/aliyun-happyhorse-i2v/videos")


def _headers(async_mode: bool = True) -> dict:
    h = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    if async_mode:
        h["X-DashScope-Async"] = "enable"
    return h


def create_task(
    first_frame_url: str,
    prompt: str = "",
    resolution: str = "1080P",
    duration: int = 5,
    watermark: bool = True,
    seed: int | None = None,
) -> str:
    """Submit an async i2v task. Returns task_id."""
    media = [{"type": "first_frame", "url": first_frame_url}]
    payload: dict = {
        "model": MODEL,
        "input": {"prompt": prompt, "media": media},
        "parameters": {
            "resolution": resolution,
            "duration": duration,
            "watermark": watermark,
        },
    }
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


def main() -> None:
    parser = argparse.ArgumentParser(description="HappyHorse 1.0 Image-to-Video (first-frame)")
    parser.add_argument("--first-frame", required=True, help="First frame image URL")
    parser.add_argument("--prompt", default="", help="Text prompt")
    parser.add_argument("--resolution", default="1080P", choices=["720P", "1080P"])
    parser.add_argument("--duration", type=int, default=5, help="Video duration 3-15s")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument(
        "--no-watermark",
        action="store_true",
        help="Disable the default 'Happy Horse' watermark",
    )
    parser.add_argument("--output", default=OUTPUT_DIR, help="Output directory")
    args = parser.parse_args()

    if not API_KEY:
        print("Error: DASHSCOPE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    print(f"Creating i2v task with model={MODEL}...")
    task_id = create_task(
        first_frame_url=args.first_frame,
        prompt=args.prompt,
        resolution=args.resolution,
        duration=args.duration,
        watermark=not args.no_watermark,
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
