#!/usr/bin/env python3
"""Execute the article illustration workflow end-to-end."""

from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
from pathlib import Path


SMALL_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wn8n9sAAAAASUVORK5CYII="
)


def run_command(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=True)


def parse_prompt_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    current_key: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if ":" in raw and not raw.startswith("- "):
            key, _, value = raw.partition(":")
            current_key = key.strip()
            data[current_key] = value.strip()
            continue
        if current_key and raw.strip():
            data[current_key] = f"{data[current_key]}\n{raw.strip()}".strip()
    return data


def render_mock_image(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(base64.b64decode(SMALL_PNG_BASE64))


def render_qwen_image(repo_root: Path, prompt_path: Path, output_path: Path) -> dict[str, str]:
    prompt_data = parse_prompt_file(prompt_path)
    request = {
        "prompt": prompt_data.get("Prompt") or prompt_data.get("Visual Goal") or "illustration",
        "negative_prompt": prompt_data.get("Negative Prompt") or "blurry, low quality",
        "size": prompt_data.get("ASPECT") or "1024*1024",
        "style": prompt_data.get("Style"),
    }
    request_path = output_path.with_suffix(".request.json")
    request_path.parent.mkdir(parents=True, exist_ok=True)
    request_path.write_text(json.dumps(request, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    cmd = [
        sys.executable,
        "skills/ai/image/aliyun-qwen-image/scripts/generate_image.py",
        "--file",
        str(request_path),
        "--output",
        str(output_path),
        "--print-response",
    ]
    result = run_command(cmd, repo_root)
    response = json.loads(result.stdout.strip()) if result.stdout.strip() else {}
    return {"request_path": str(request_path), "response": response}


def write_article(source_path: Path, article_path: Path, image_paths: list[Path]) -> None:
    content = source_path.read_text(encoding="utf-8").rstrip() + "\n\n"
    image_block = "\n".join(f"![illustration]({path.as_posix()})" for path in image_paths)
    article_path.write_text(content + image_block + "\n", encoding="utf-8")


def write_delivery_report(path: Path, topic_slug: str, source_path: Path, image_paths: list[Path], backend: str) -> None:
    lines = [
        "# Delivery Report",
        "",
        f"- Topic Slug: {topic_slug}",
        f"- Source File: {source_path.name}",
        "- Final Article: article.with-images.md",
        f"- Prompt Files: {len(image_paths)}",
        f"- Images: {len(image_paths)}",
        "- Edited Images: 0",
        f"- Notes: backend={backend}",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the article illustration workflow")
    parser.add_argument("--source", required=True, help="Path to source Markdown article")
    parser.add_argument("--output-dir", required=True, help="Workflow output directory")
    parser.add_argument(
        "--generation-backend",
        default="mock",
        choices=["mock", "qwen-image"],
        help="Generation backend to use",
    )
    parser.add_argument(
        "--edit-backend",
        default="none",
        choices=["none", "qwen-image-edit"],
        help="Edit backend to record for future repair steps",
    )
    parser.add_argument("--project-path", help="Project-level EXTEND.md override")
    parser.add_argument("--user-path", help="User-level EXTEND.md override")
    parser.add_argument("--topic-slug", default="article-illustration", help="Topic slug for reporting")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    source_path = Path(args.source)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    copied_source = output_dir / "source.md"
    copied_source.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")

    preferences_output = output_dir / "preferences.json"
    load_preferences_cmd = [
        sys.executable,
        str(Path(__file__).with_name("load_preferences.py")),
        "--output",
        str(preferences_output),
    ]
    if args.project_path:
        load_preferences_cmd.extend(["--project-path", args.project_path])
    if args.user_path:
        load_preferences_cmd.extend(["--user-path", args.user_path])
    run_command(load_preferences_cmd, repo_root)

    run_command(
        [
            sys.executable,
            str(Path(__file__).with_name("build_outline.py")),
            "--output-dir",
            str(output_dir),
        ],
        repo_root,
    )

    prompts_dir = output_dir / "prompts"
    images_dir = output_dir / "images"
    prompt_files = sorted(prompts_dir.glob("*.md"))
    render_results: list[dict[str, object]] = []
    written_images: list[Path] = []

    for prompt_file in prompt_files:
        image_name = prompt_file.stem + ".png"
        image_path = images_dir / image_name
        if args.generation_backend == "mock":
            render_mock_image(image_path)
            render_results.append({
                "prompt_file": str(prompt_file.relative_to(output_dir)),
                "image_file": str(image_path.relative_to(output_dir)),
                "backend": "mock",
            })
        else:
            backend_result = render_qwen_image(repo_root, prompt_file, image_path)
            render_results.append({
                "prompt_file": str(prompt_file.relative_to(output_dir)),
                "image_file": str(image_path.relative_to(output_dir)),
                "backend": "qwen-image",
                "request_path": backend_result["request_path"],
                "response": backend_result["response"],
            })
        written_images.append(Path("images") / image_path.name)

    article_path = output_dir / "article.with-images.md"
    write_article(copied_source, article_path, written_images)

    report_path = output_dir / "delivery-report.md"
    write_delivery_report(report_path, args.topic_slug, copied_source, written_images, args.generation_backend)

    evidence_path = output_dir / "workflow-run.json"
    evidence = {
        "topic_slug": args.topic_slug,
        "generation_backend": args.generation_backend,
        "edit_backend": args.edit_backend,
        "source": str(copied_source),
        "article": str(article_path),
        "render_results": render_results,
    }
    evidence_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    run_command(
        [
            sys.executable,
            str(Path(__file__).with_name("collect_evidence.py")),
            "--workflow-dir",
            str(output_dir),
            "--output",
            str(output_dir / "artifacts.json"),
        ],
        repo_root,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
