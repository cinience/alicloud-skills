"""Vidu video generation via DashScope HTTP API.

Supports: text-to-video, image-to-video, keyframe-to-video, reference-to-video.
Usage:
    # Text-to-video
    python generate_vidu_video.py --mode t2v --model vidu/viduq3-turbo_text2video --prompt "A cat running"

    # Image-to-video (first frame)
    python generate_vidu_video.py --mode i2v --model vidu/viduq3-pro_img2video --image https://example.com/img.jpg

    # Keyframe-to-video (first + last frame)
    python generate_vidu_video.py --mode keyframe --model vidu/viduq3-turbo_start-end2video \
        --image https://example.com/first.png --end-image https://example.com/last.png \
        --prompt "A cat jumps from windowsill to sofa"

    # Reference-to-video
    python generate_vidu_video.py --mode ref --model vidu/viduq2_reference2video \
        --image https://example.com/ref1.jpg --image https://example.com/ref2.jpg \
        --prompt "Man playing guitar in a cafe" --size 1280*720
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
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/aliyun-vidu-video/videos")

VALID_MODELS = {
    "t2v": [
        "vidu/viduq3-pro_text2video",
        "vidu/viduq3-turbo_text2video",
        "vidu/viduq2_text2video",
    ],
    "i2v": [
        "vidu/viduq3-pro_img2video",
        "vidu/viduq3-turbo_img2video",
        "vidu/viduq2-pro_img2video",
        "vidu/viduq2-turbo_img2video",
    ],
    "keyframe": [
        "vidu/viduq3-pro_start-end2video",
        "vidu/viduq3-turbo_start-end2video",
        "vidu/viduq2-pro_start-end2video",
        "vidu/viduq2-turbo_start-end2video",
    ],
    "ref": [
        "vidu/viduq2_reference2video",
        "vidu/viduq2-pro_reference2video",
    ],
}

ALL_MODELS = [m for models in VALID_MODELS.values() for m in models]


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }


def create_task(
    model: str,
    prompt: str = "",
    media: list[dict] | None = None,
    resolution: str = "720P",
    size: str | None = None,
    duration: int = 5,
    audio: bool = False,
    watermark: bool = False,
    seed: int | None = None,
) -> str:
    """Submit an async Vidu task. Returns task_id."""
    payload: dict = {
        "model": model,
        "input": {},
        "parameters": {
            "resolution": resolution,
            "duration": duration,
            "watermark": watermark,
        },
    }
    if prompt:
        payload["input"]["prompt"] = prompt
    if media:
        payload["input"]["media"] = media
    if size:
        payload["parameters"]["size"] = size
    if audio:
        payload["parameters"]["audio"] = True
    if seed is not None:
        payload["parameters"]["seed"] = seed

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
    """Build media array from CLI args."""
    media = []
    if args.image:
        for url in args.image:
            media.append({"type": "image", "url": url})
    if args.end_image:
        media.append({"type": "image", "url": args.end_image})
    if args.ref_video:
        for url in args.ref_video:
            media.append({"type": "video", "url": url})
    return media if media else None


def _validate_mode_model(mode: str, model: str) -> None:
    """Validate that the model matches the selected mode."""
    if mode not in VALID_MODELS:
        print(f"Error: unknown mode '{mode}'", file=sys.stderr)
        sys.exit(1)
    if model not in VALID_MODELS[mode]:
        valid = ", ".join(VALID_MODELS[mode])
        print(
            f"Error: model '{model}' is not valid for mode '{mode}'. "
            f"Valid models: {valid}",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Vidu Video Generation")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["t2v", "i2v", "keyframe", "ref"],
        help="Generation mode: t2v (text-to-video), i2v (image-to-video), "
        "keyframe (first+last frame), ref (reference-to-video)",
    )
    parser.add_argument(
        "--model",
        required=True,
        choices=ALL_MODELS,
        help="Model name",
    )
    parser.add_argument("--prompt", default="", help="Text prompt (up to 5000 chars)")
    parser.add_argument(
        "--image",
        action="append",
        help="Image URL (repeatable for reference mode). "
        "For keyframe mode, use this for the first frame.",
    )
    parser.add_argument(
        "--end-image",
        help="Last frame image URL (keyframe mode only)",
    )
    parser.add_argument(
        "--ref-video",
        action="append",
        help="Reference video URL (reference mode with viduq2-pro only, repeatable)",
    )
    parser.add_argument(
        "--resolution",
        default="720P",
        choices=["540P", "720P", "1080P"],
        help="Resolution tier (default: 720P)",
    )
    parser.add_argument("--size", default=None, help="Pixel size WxH, e.g. 1280*720")
    parser.add_argument(
        "--duration", type=int, default=5, help="Video duration in seconds"
    )
    parser.add_argument(
        "--audio", action="store_true", help="Generate audio (Q3 models only)"
    )
    parser.add_argument("--watermark", action="store_true", help="Add watermark")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument(
        "--output", default=OUTPUT_DIR, help="Output directory"
    )
    args = parser.parse_args()

    if not API_KEY:
        print("Error: DASHSCOPE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    _validate_mode_model(args.mode, args.model)

    # Validate mode-specific requirements
    if args.mode == "t2v":
        if not args.prompt:
            print("Error: --prompt is required for text-to-video mode", file=sys.stderr)
            sys.exit(1)
    elif args.mode == "i2v":
        if not args.image or len(args.image) != 1:
            print("Error: exactly one --image is required for image-to-video mode", file=sys.stderr)
            sys.exit(1)
    elif args.mode == "keyframe":
        if not args.image or len(args.image) != 1 or not args.end_image:
            print(
                "Error: --image (first frame) and --end-image (last frame) "
                "are both required for keyframe mode",
                file=sys.stderr,
            )
            sys.exit(1)
        if not args.prompt:
            print("Error: --prompt is required for keyframe mode", file=sys.stderr)
            sys.exit(1)
    elif args.mode == "ref":
        if not args.image:
            print("Error: at least one --image is required for reference mode", file=sys.stderr)
            sys.exit(1)
        if not args.prompt:
            print("Error: --prompt is required for reference mode", file=sys.stderr)
            sys.exit(1)

    media = _build_media(args) if args.mode != "t2v" else None

    print(f"Creating Vidu {args.mode} task with model {args.model}...")
    task_id = create_task(
        model=args.model,
        prompt=args.prompt,
        media=media,
        resolution=args.resolution,
        size=args.size,
        duration=args.duration,
        audio=args.audio,
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
