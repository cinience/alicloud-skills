"""HappyHorse 1.0 Video Editing via DashScope HTTP API.

Edit a single video with optional reference images (0-5) and a text instruction.

Usage:
    python edit_happyhorse.py \
        --video https://example.com/input.mp4 \
        --prompt "switch character outfit to a striped sweater"

    python edit_happyhorse.py \
        --video https://example.com/input.mp4 \
        --reference-image https://example.com/sweater.webp \
        --prompt "dress the character in the sweater from the reference" \
        --resolution 720P --audio-setting origin
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
MODEL = "happyhorse-1.0-video-edit"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/aliyun-happyhorse-videoedit/videos")


def _headers(async_mode: bool = True) -> dict:
    h = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    if async_mode:
        h["X-DashScope-Async"] = "enable"
    return h


def create_task(
    video_url: str,
    prompt: str,
    reference_images: list[str] | None = None,
    resolution: str = "1080P",
    audio_setting: str | None = None,
    watermark: bool = True,
    seed: int | None = None,
) -> str:
    """Submit an async video-edit task. Returns task_id."""
    reference_images = reference_images or []
    if len(reference_images) > 5:
        raise ValueError("At most 5 reference images are allowed")

    media: list[dict] = [{"type": "video", "url": video_url}]
    for url in reference_images:
        media.append({"type": "reference_image", "url": url})

    payload: dict = {
        "model": MODEL,
        "input": {"prompt": prompt, "media": media},
        "parameters": {
            "resolution": resolution,
            "watermark": watermark,
        },
    }
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


def main() -> None:
    parser = argparse.ArgumentParser(description="HappyHorse 1.0 Video Editing")
    parser.add_argument("--video", required=True, help="Input video URL (the only video)")
    parser.add_argument(
        "--reference-image",
        action="append",
        default=[],
        help="Reference image URL (repeat 0-5 times)",
    )
    parser.add_argument("--prompt", required=True, help="Edit instruction prompt")
    parser.add_argument("--resolution", default="1080P", choices=["720P", "1080P"])
    parser.add_argument(
        "--audio-setting",
        default=None,
        choices=["auto", "origin"],
        help="auto (default) or origin to keep input video audio",
    )
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
        f"Creating video-edit task with model={MODEL} and {len(args.reference_image)} reference image(s)..."
    )
    task_id = create_task(
        video_url=args.video,
        prompt=args.prompt,
        reference_images=args.reference_image,
        resolution=args.resolution,
        audio_setting=args.audio_setting,
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
