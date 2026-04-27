#!/usr/bin/env python3
"""Executable smoke test for alicloud-ai-multimodal-qwen-vl."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def load_analyze_module(repo_root: Path):
    module_path = (
        repo_root
        / "skills/ai/multimodal/alicloud-ai-multimodal-qwen-vl/scripts/analyze_image.py"
    )
    spec = importlib.util.spec_from_file_location("analyze_image", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke test for Qwen VL image understanding skill")
    parser.add_argument(
        "--image",
        required=True,
        help="Image URL or local path for validation",
    )
    parser.add_argument(
        "--prompt",
        default="Describe the image and list 3 visible details.",
        help="Prompt for the model",
    )
    parser.add_argument(
        "--model",
        default="qwen3-vl-plus",
        help="Model name to test",
    )
    parser.add_argument(
        "--output",
        default="output/ai-multimodal-qwen-vl/smoke-test/result.json",
        help="Where to save smoke-test output JSON",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[5]
    mod = load_analyze_module(repo_root)
    mod._load_env()
    mod._load_dashscope_api_key_from_credentials()

    req = {
        "prompt": args.prompt,
        "image": args.image,
        "model": args.model,
        "max_tokens": 512,
        "temperature": 0.2,
    }
    result = mod.call_analyze(req)

    text = result.get("text")
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError("Smoke test failed: empty text in response")
    if result.get("model") != args.model and not str(result.get("model", "")).startswith(args.model):
        raise RuntimeError(
            f"Smoke test failed: unexpected model. expected={args.model} actual={result.get('model')}"
        )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=True, indent=2), encoding="utf-8")

    print(json.dumps({"status": "pass", "output": str(output_path)}, ensure_ascii=True))


if __name__ == "__main__":
    main()
