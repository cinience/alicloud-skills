#!/usr/bin/env python3
"""Generate or edit images using DashScope (wan2.7-image) from a normalized request.

Usage:
  python scripts/generate_image.py --request '{"prompt":"a cat in a garden","size":"2K"}'
  python scripts/generate_image.py --file request.json --output output/aliyun-wan-image/images/cat.png
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


MODEL_NAME = "wan2.7-image"
DEFAULT_SIZE = "2K"


def load_request(args: argparse.Namespace) -> dict[str, Any]:
    if args.request:
        return json.loads(args.request)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    raise ValueError("Either --request or --file must be provided")


def _get_field(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    getter = getattr(obj, "get", None)
    if callable(getter):
        try:
            return getter(key, default)
        except TypeError:
            value = getter(key)
            return default if value is None else value
    try:
        return obj[key]
    except Exception:
        return getattr(obj, key, default)


def call_generate(req: dict[str, Any]) -> dict[str, Any]:
    prompt = req.get("prompt")
    if not prompt:
        raise ValueError("prompt is required")

    messages = [{"role": "user", "content": [{"text": prompt}]}]

    # Add reference images
    ref_images = req.get("reference_images") or []
    if req.get("reference_image"):
        ref_images = [req["reference_image"]] + ref_images
    for img in ref_images:
        messages[0]["content"].append({"image": img})

    params: dict[str, Any] = {
        "model": req.get("model", MODEL_NAME),
        "messages": messages,
        "size": req.get("size", DEFAULT_SIZE),
        "n": req.get("n", 1),
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
        "watermark": req.get("watermark", False),
    }

    if req.get("seed") is not None:
        params["seed"] = req["seed"]
    if req.get("enable_sequential"):
        params["enable_sequential"] = True
    if req.get("thinking_mode") is not None:
        params["thinking_mode"] = req["thinking_mode"]
    if req.get("bbox_list"):
        params["bbox_list"] = req["bbox_list"]
    if req.get("color_palette"):
        params["color_palette"] = req["color_palette"]

    response = ImageGeneration.call(**params)

    output = _get_field(response, "output", response.output if hasattr(response, "output") else None)
    choices = _get_field(output, "choices", [])
    if not choices:
        raise RuntimeError(f"No choices returned by DashScope: {response}")

    message = _get_field(choices[0], "message", {})
    content = _get_field(message, "content", [])
    image_urls = []
    for item in content:
        if isinstance(item, dict) and item.get("image"):
            image_urls.append(item["image"])

    if not image_urls:
        raise RuntimeError("No image URL returned by DashScope")

    usage = _get_field(response, "usage", response.usage if hasattr(response, "usage") else {})
    return {
        "image_urls": image_urls,
        "image_count": _get_field(usage, "image_count"),
        "size": _get_field(usage, "size"),
        "seed": req.get("seed"),
    }


def download_image(image_url: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(image_url) as response:
        output_path.write_bytes(response.read())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate/edit images with wan2.7-image")
    parser.add_argument("--request", help="Inline JSON request string")
    parser.add_argument("--file", help="Path to JSON request file")
    default_output_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "aliyun-wan-image" / "images"
    parser.add_argument(
        "--output",
        default=str(default_output_dir / "output.png"),
        help="Output image path (for first image; others get _N suffix)",
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
        sys.exit(1)

    req = load_request(args)
    result = call_generate(req)

    output_path = Path(args.output)
    for i, url in enumerate(result["image_urls"]):
        if i == 0:
            path = output_path
        else:
            path = output_path.with_stem(f"{output_path.stem}_{i}")
        download_image(url, path)
        print(f"Saved: {path}")

    if args.print_response:
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
