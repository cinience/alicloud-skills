#!/usr/bin/env python3
"""Generate an image using Z-Image Turbo (z-image-turbo) via DashScope API.

Usage:
  python scripts/generate_image.py --request '{"prompt":"a cat","size":"1024*1024"}'
  python scripts/generate_image.py --file request.json --output output/ai-image-zimage-turbo/images/cat.png
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
DEFAULT_SIZE = "1024*1024"
MODEL_NAME = "z-image-turbo"


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
    import configparser

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


def load_request(args: argparse.Namespace) -> dict[str, Any]:
    if args.request:
        return json.loads(args.request)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    raise ValueError("Either --request or --file must be provided")


def _build_payload(req: dict[str, Any]) -> dict[str, Any]:
    prompt = req.get("prompt")
    if not prompt:
        raise ValueError("prompt is required")

    messages = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]

    parameters: dict[str, Any] = {}
    size = req.get("size") or DEFAULT_SIZE
    if size:
        parameters["size"] = size
    if req.get("seed") is not None:
        parameters["seed"] = req.get("seed")
    if req.get("prompt_extend") is not None:
        parameters["prompt_extend"] = bool(req.get("prompt_extend"))

    payload: dict[str, Any] = {
        "model": MODEL_NAME,
        "input": {"messages": messages},
    }
    if parameters:
        payload["parameters"] = parameters
    return payload


def _post_json(url: str, api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as response:
        body = response.read().decode("utf-8")
    return json.loads(body)


def _extract_image_url(resp: dict[str, Any]) -> str:
    choices = (((resp.get("output") or {}).get("choices")) or [])
    if not choices:
        raise RuntimeError("No choices returned by DashScope")
    content = (choices[0].get("message") or {}).get("content") or []
    for item in content:
        if isinstance(item, dict) and item.get("image"):
            return item["image"]
    raise RuntimeError("No image URL returned by DashScope")


def _extract_text_field(content: list[dict[str, Any]], key: str) -> str | None:
    for item in content:
        if isinstance(item, dict) and item.get(key):
            return item.get(key)
    return None


def call_generate(req: dict[str, Any]) -> dict[str, Any]:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY is not set")

    base_url = req.get("base_url") or os.getenv("DASHSCOPE_BASE_URL") or DEFAULT_BASE_URL
    payload = _build_payload(req)
    resp = _post_json(base_url, api_key, payload)

    output = resp.get("output") or {}
    choices = output.get("choices") or []
    content = (choices[0].get("message") or {}).get("content") if choices else []

    image_url = _extract_image_url(resp)
    return {
        "image_url": image_url,
        "width": (resp.get("usage") or {}).get("width"),
        "height": (resp.get("usage") or {}).get("height"),
        "prompt": req.get("prompt"),
        "rewritten_prompt": _extract_text_field(content, "text"),
        "reasoning": _extract_text_field(content, "reasoning_content"),
        "request_id": resp.get("request_id"),
    }


def download_image(image_url: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(image_url) as response:
        output_path.write_bytes(response.read())


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate image with z-image-turbo")
    parser.add_argument("--request", help="Inline JSON request string")
    parser.add_argument("--file", help="Path to JSON request file")
    default_output_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "ai-image-zimage-turbo" / "images"
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
        print("Example credentials:\n  [default]\n  dashscope_api_key=your_key_here", file=sys.stderr)
        return 1

    req = load_request(args)
    result = call_generate(req)
    download_image(result["image_url"], Path(args.output))

    if args.print_response:
        print(json.dumps(result, ensure_ascii=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
