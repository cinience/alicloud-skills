"""HappyHorse 1.0 Reference-to-Video generation via DashScope HTTP API.

Use 1-9 reference images, with prompt referring to them as character1, character2, ... in order.

Usage:
    python r2v_happyhorse.py --reference-image https://example.com/girl.jpg \
        --prompt "character1 walking through a forest" --duration 5

    python r2v_happyhorse.py \
        --reference-image https://example.com/girl.jpg \
        --reference-image https://example.com/fan.jpg \
        --reference-image https://example.com/earring.jpg \
        --prompt "character1 holds character2 and wears character3" \
        --resolution 720P --ratio 16:9 --duration 5
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
MODEL = "happyhorse-1.0-r2v"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/aliyun-happyhorse-r2v/videos")


def _headers(async_mode: bool = True) -> dict:
    h = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    if async_mode:
        h["X-DashScope-Async"] = "enable"
    return h


def create_task(
    reference_images: list[str],
    prompt: str,
    resolution: str = "1080P",
    ratio: str = "16:9",
    duration: int = 5,
    watermark: bool = True,
    seed: int | None = None,
) -> str:
    """Submit an async r2v task. Returns task_id."""
    if not 1 <= len(reference_images) <= 9:
        raise ValueError("reference_images must contain 1 to 9 URLs")
    media = [{"type": "reference_image", "url": url} for url in reference_images]
    payload: dict = {
        "model": MODEL,
        "input": {"prompt": prompt, "media": media},
        "parameters": {
            "resolution": resolution,
            "ratio": ratio,
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
    parser = argparse.ArgumentParser(description="HappyHorse 1.0 Reference-to-Video")
    parser.add_argument(
        "--reference-image",
        action="append",
        required=True,
        help="Reference image URL (repeat 1-9 times; order maps to character1..N)",
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Text prompt referencing characters as character1, character2, ...",
    )
    parser.add_argument("--resolution", default="1080P", choices=["720P", "1080P"])
    parser.add_argument(
        "--ratio",
        default="16:9",
        choices=["16:9", "9:16", "1:1", "4:3", "3:4"],
    )
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

    print(
        f"Creating r2v task with model={MODEL} and {len(args.reference_image)} reference image(s)..."
    )
    task_id = create_task(
        reference_images=args.reference_image,
        prompt=args.prompt,
        resolution=args.resolution,
        ratio=args.ratio,
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
