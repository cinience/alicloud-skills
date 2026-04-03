"""Kling V3 Video Generation via DashScope HTTP API.

Supports: text-to-video, image-to-video, reference-to-video, video editing.
Usage:
    python generate_kling_video.py --prompt "a cat running under moonlight" --aspect-ratio 16:9
    python generate_kling_video.py --first-frame https://example.com/img.jpg --prompt "flower blooming"
    python generate_kling_video.py --model kling/kling-v3-omni-video-generation --prompt "<<<element_1>>> running" --refer img.jpg
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
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/aliyun-kling-video/videos")


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }


def create_task(
    model: str = "kling/kling-v3-video-generation",
    prompt: str = "",
    negative_prompt: str | None = None,
    media: list[dict] | None = None,
    mode: str = "pro",
    aspect_ratio: str | None = None,
    duration: int = 5,
    audio: bool = False,
    watermark: bool = False,
) -> str:
    """Submit an async Kling video task. Returns task_id."""
    payload: dict = {
        "model": model,
        "input": {"prompt": prompt},
        "parameters": {
            "mode": mode,
            "duration": duration,
            "audio": audio,
            "watermark": watermark,
        },
    }
    if negative_prompt:
        payload["input"]["negative_prompt"] = negative_prompt
    if media:
        payload["input"]["media"] = media
    if aspect_ratio:
        payload["parameters"]["aspect_ratio"] = aspect_ratio

    resp = requests.post(
        f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
        headers=_headers(),
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


def _build_media(args: argparse.Namespace) -> list[dict] | None:
    media = []
    if args.first_frame:
        media.append({"type": "first_frame", "url": args.first_frame})
    if args.last_frame:
        media.append({"type": "last_frame", "url": args.last_frame})
    for img in args.refer or []:
        media.append({"type": "refer", "url": img})
    if args.base_video:
        media.append({"type": "base", "url": args.base_video})
    if args.feature_video:
        media.append({"type": "feature", "url": args.feature_video})
    return media if media else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Kling V3 Video Generation")
    parser.add_argument("--model", default="kling/kling-v3-video-generation",
                        choices=["kling/kling-v3-video-generation", "kling/kling-v3-omni-video-generation"])
    parser.add_argument("--prompt", default="", help="Text prompt (max 2500 chars)")
    parser.add_argument("--negative-prompt", default=None)
    parser.add_argument("--first-frame", help="First frame image URL")
    parser.add_argument("--last-frame", help="Last frame image URL")
    parser.add_argument("--refer", action="append", help="Reference image URL (omni model, repeatable)")
    parser.add_argument("--base-video", help="Base video URL for editing (omni model)")
    parser.add_argument("--feature-video", help="Feature reference video URL (omni model)")
    parser.add_argument("--mode", default="pro", choices=["pro", "std"])
    parser.add_argument("--aspect-ratio", default=None, choices=["16:9", "9:16", "1:1"])
    parser.add_argument("--duration", type=int, default=5, help="Video duration 3-15s")
    parser.add_argument("--audio", action="store_true", help="Generate audio")
    parser.add_argument("--watermark", action="store_true")
    parser.add_argument("--output", default=OUTPUT_DIR, help="Output directory")
    args = parser.parse_args()

    if not API_KEY:
        print("Error: DASHSCOPE_API_KEY not set (must be Beijing region)", file=sys.stderr)
        sys.exit(1)

    media = _build_media(args)
    print(f"Creating Kling video task (model={args.model})...")
    task_id = create_task(
        model=args.model,
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        media=media,
        mode=args.mode,
        aspect_ratio=args.aspect_ratio,
        duration=args.duration,
        audio=args.audio,
        watermark=args.watermark,
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
