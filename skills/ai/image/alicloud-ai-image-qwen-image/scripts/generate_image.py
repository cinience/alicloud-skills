#!/usr/bin/env python3
"""Generate an image using DashScope (qwen-image-max) from a normalized request.

Usage:
  python scripts/generate_image.py --request '{"prompt":"a cat","size":"1024*1024"}'
  python scripts/generate_image.py --file request.json --output output/ai-image-qwen-image/images/cat.png
"""

from __future__ import annotations

import argparse
import configparser
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any



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

try:
    from dashscope.aigc.image_generation import ImageGeneration
except ImportError:
    print("Error: dashscope is not installed. Run: pip install dashscope", file=sys.stderr)
    sys.exit(1)


MODEL_NAME = "qwen-image-max"
DEFAULT_SIZE = "1024*1024"


def load_request(args: argparse.Namespace) -> dict[str, Any]:
    if args.request:
        return json.loads(args.request)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    raise ValueError("Either --request or --file must be provided")


def resolve_reference_image(value: str) -> Any:
    if value.startswith("http://") or value.startswith("https://"):
        return value
    path = Path(value)
    if path.exists():
        return path.read_bytes()
    return value


def call_generate(req: dict[str, Any]) -> dict[str, Any]:
    prompt = req.get("prompt")
    if not prompt:
        raise ValueError("prompt is required")

    messages = [{"role": "user", "content": [{"text": prompt}]}]
    reference_image = req.get("reference_image")
    if reference_image:
        messages[0]["content"].insert(0, {"image": resolve_reference_image(reference_image)})

    response = ImageGeneration.call(
        model=MODEL_NAME,
        messages=messages,
        size=req.get("size", DEFAULT_SIZE),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        negative_prompt=req.get("negative_prompt"),
        style=req.get("style"),
        seed=req.get("seed"),
    )

    content = response.output["choices"][0]["message"]["content"]
    image_url = None
    for item in content:
        if isinstance(item, dict) and item.get("image"):
            image_url = item["image"]
            break

    if not image_url:
        raise RuntimeError("No image URL returned by DashScope")

    return {
        "image_url": image_url,
        "width": response.usage.get("width"),
        "height": response.usage.get("height"),
        "seed": req.get("seed"),
    }


def download_image(image_url: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(image_url) as response:
        output_path.write_bytes(response.read())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate image with qwen-image-max")
    parser.add_argument("--request", help="Inline JSON request string")
    parser.add_argument("--file", help="Path to JSON request file")
    default_output_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "ai-image-qwen-image" / "images"
    parser.add_argument(
        "--output",
        default=str(default_output_dir / "output.png"),
        help="Output image path",
    )
    parser.add_argument("--print-response", action="store_true", help="Print normalized response JSON")
    args = parser.parse_args()

    _load_env()
    _load_dashscope_api_key_from_credentials()
    if not os.environ.get("DASHSCOPE_API_KEY"):
        print(
            "Error: DASHSCOPE_API_KEY is not set. Configure it via env/.env or ~/.alibabacloud/credentials.",
            file=sys.stderr,
        )
        print("Example .env:\n  DASHSCOPE_API_KEY=your_key_here", file=sys.stderr)
        print(
            "Example credentials:\n  [default]\n  dashscope_api_key=your_key_here",
            file=sys.stderr,
        )
        sys.exit(1)

    req = load_request(args)
    result = call_generate(req)
    download_image(result["image_url"], Path(args.output))

    if args.print_response:
        print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
