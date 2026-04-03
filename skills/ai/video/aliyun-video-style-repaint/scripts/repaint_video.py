"""Video Style Repaint via DashScope HTTP API.

Transforms video into artistic styles (manga, comics, 3D cartoon, ink painting, etc.).
Usage:
    python repaint_video.py --video-url https://example.com/video.mp4
    python repaint_video.py --video-url https://example.com/video.mp4 --style 3 --fps 25
    python repaint_video.py --video-url https://example.com/video.mp4 --style 7 --min-len 540 --use-sr
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
MODEL = "video-style-transform"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/aliyun-video-style-repaint/videos")

STYLE_NAMES = {
    0: "Japanese Manga",
    1: "American Comics",
    2: "Fresh Comics",
    3: "3D Cartoon",
    4: "Chinese Cartoon",
    5: "Paper Art",
    6: "Simple Illustration",
    7: "Chinese Ink Painting",
}


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
    style: int = 0,
    video_fps: int = 15,
    animate_emotion: bool = True,
    min_len: int = 720,
    use_sr: bool = False,
) -> str:
    """Submit an async video style repaint task. Returns task_id."""
    payload: dict = {
        "model": MODEL,
        "input": {
            "video_url": video_url,
        },
        "parameters": {
            "style": style,
            "video_fps": video_fps,
            "animate_emotion": animate_emotion,
            "min_len": min_len,
            "use_SR": use_sr,
        },
    }

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
        if status in ("SUCCEEDED", "FAILED", "CANCELED", "SUSPENDED"):
            return data
        time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="Video Style Repaint")
    parser.add_argument("--video-url", required=True, help="Input video URL")
    parser.add_argument("--style", type=int, default=0, choices=range(8),
                        metavar="0-7",
                        help="Style ID: 0=Japanese Manga, 1=American Comics, "
                             "2=Fresh Comics, 3=3D Cartoon, 4=Chinese Cartoon, "
                             "5=Paper Art, 6=Simple Illustration, 7=Chinese Ink Painting")
    parser.add_argument("--fps", type=int, default=15,
                        help="Output video frame rate, range [15, 25]")
    parser.add_argument("--no-animate-emotion", action="store_true",
                        help="Disable facial expression optimization")
    parser.add_argument("--min-len", type=int, default=720, choices=[540, 720],
                        help="Output short-side pixels (540 or 720)")
    parser.add_argument("--use-sr", action="store_true",
                        help="Enable super-resolution enhancement")
    parser.add_argument("--output", default=OUTPUT_DIR, help="Output directory")
    args = parser.parse_args()

    if not API_KEY:
        print("Error: DASHSCOPE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    style_name = STYLE_NAMES.get(args.style, f"style-{args.style}")
    print(f"Creating style repaint task (style={args.style} [{style_name}], fps={args.fps})...")
    task_id = create_task(
        video_url=args.video_url,
        style=args.style,
        video_fps=args.fps,
        animate_emotion=not args.no_animate_emotion,
        min_len=args.min_len,
        use_sr=args.use_sr,
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
        video_url = result["output"].get("output_video_url", "")
        print(f"Video URL: {video_url}")
    else:
        print(f"Task {status}: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    print(f"Result saved to {out_path}")


if __name__ == "__main__":
    main()
