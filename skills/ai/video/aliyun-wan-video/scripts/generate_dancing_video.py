#!/usr/bin/env python3
"""Generate a dancing video: first create an image, then animate it.

Usage:
  python scripts/generate_dancing_video.py --prompt "亚洲美女在跳舞" --output output/dancing_video.mp4
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
    from dashscope.aigc.image_generation import ImageGeneration
    from dashscope import VideoSynthesis
except ImportError:
    print("Error: dashscope is not installed. Run: pip install dashscope", file=sys.stderr)
    sys.exit(1)


IMAGE_MODEL = "qwen-image-max"
VIDEO_MODEL = "wan2.6-i2v-flash"
DEFAULT_IMAGE_SIZE = "1024*1024"
DEFAULT_VIDEO_SIZE = "1280*720"
DEFAULT_FPS = 24
DEFAULT_DURATION = 5


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


def generate_image(prompt: str, size: str = DEFAULT_IMAGE_SIZE) -> dict[str, Any]:
    """Generate an image of an Asian beauty."""
    print(f"Step 1: Generating image with prompt: {prompt}")
    
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    
    response = ImageGeneration.call(
        model=IMAGE_MODEL,
        messages=messages,
        size=size,
        api_key=os.getenv("DASHSCOPE_API_KEY"),
    )
    
    content = response.output["choices"][0]["message"]["content"]
    image_url = None
    for item in content:
        if isinstance(item, dict) and item.get("image"):
            image_url = item["image"]
            break
    
    if not image_url:
        raise RuntimeError("No image URL returned by DashScope")
    
    print(f"  Image generated: {image_url}")
    return {"image_url": image_url}


def generate_video(image_url: str, prompt: str, duration: int = DEFAULT_DURATION, 
                   fps: int = DEFAULT_FPS, size: str = DEFAULT_VIDEO_SIZE) -> dict[str, Any]:
    """Generate a dancing video from the image."""
    print(f"Step 2: Generating video from image...")
    print(f"  Video prompt: {prompt}")
    print(f"  Duration: {duration}s, FPS: {fps}, Size: {size}")
    
    payload = {
        "model": VIDEO_MODEL,
        "prompt": prompt,
        "duration": duration,
        "fps": fps,
        "size": size,
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
        "img_url": image_url,
    }
    
    task = VideoSynthesis.async_call(**payload)
    
    print("  Waiting for video generation (this may take 2-5 minutes)...")
    poll_interval = 10
    timeout_s = 600
    start = time.time()
    
    while True:
        final = VideoSynthesis.wait(task)
        output = getattr(final, "output", None) or {}
        status = output.get("status")
        if status in ("SUCCEEDED", "FAILED") or output.get("video_url"):
            break
        if time.time() - start > timeout_s:
            raise TimeoutError(f"Video generation timed out after {timeout_s}s")
        print(f"  Still processing... ({int(time.time() - start)}s elapsed)")
        time.sleep(poll_interval)
    
    output = getattr(final, "output", None) or {}
    video_url = output.get("video_url")
    if not video_url:
        results = output.get("results") or []
        if results and isinstance(results, list):
            video_url = results[0].get("url")
    
    if not video_url:
        raise RuntimeError("No video URL returned by DashScope")
    
    print(f"  Video generated: {video_url}")
    return {"video_url": video_url, "duration": output.get("duration"), "fps": output.get("fps")}


def download_file(url: str, output_path: Path) -> None:
    """Download a file from URL."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading to: {output_path}")
    with urllib.request.urlopen(url) as response:
        output_path.write_bytes(response.read())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a dancing video (image + animation)")
    parser.add_argument("--prompt", required=True, help="Prompt for the dancing video")
    parser.add_argument("--image-prompt", help="Optional separate prompt for the base image")
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION, help="Video duration in seconds")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help="Video FPS")
    parser.add_argument("--output", help="Output video path")
    parser.add_argument("--save-image", action="store_true", help="Also save the generated image")
    parser.add_argument("--print-response", action="store_true", help="Print response JSON")
    args = parser.parse_args()
    
    _load_env()
    _load_dashscope_api_key_from_credentials()
    
    if not os.environ.get("DASHSCOPE_API_KEY"):
        print("Error: DASHSCOPE_API_KEY is not set.", file=sys.stderr)
        print("Configure via environment variable, .env file, or ~/.alibabacloud/credentials", file=sys.stderr)
        sys.exit(1)
    
    # Default image prompt if not specified
    image_prompt = args.image_prompt or args.prompt
    if not args.image_prompt:
        # Enhance the prompt for image generation if user didn't specify
        image_prompt = f"一位美丽的亚洲女性，专业摄影，高质量，{args.prompt}"
    
    output_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "ai-video-wan-video" / "videos"
    output_path = Path(args.output) if args.output else output_dir / "dancing_video.mp4"
    image_output_path = output_path.with_name(output_path.stem + "_reference.png")
    
    try:
        # Step 1: Generate image
        image_result = generate_image(image_prompt)
        
        # Save image if requested
        if args.save_image:
            download_file(image_result["image_url"], image_output_path)
            print(f"Image saved to: {image_output_path}")
        
        # Step 2: Generate video
        video_result = generate_video(
            image_result["image_url"],
            args.prompt,
            duration=args.duration,
            fps=args.fps,
        )
        
        # Download video
        download_file(video_result["video_url"], output_path)
        print(f"\nVideo saved to: {output_path}")
        
        if args.print_response:
            print(json.dumps({
                "image": image_result,
                "video": video_result,
                "output_path": str(output_path),
            }, ensure_ascii=False, indent=2))
        
        print("\nDone!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
