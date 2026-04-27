#!/usr/bin/env python3
"""Executable smoke test for the content article illustrator solution skill."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
SKILL_DIR = REPO_ROOT / "skills" / "solutions" / "aliyun-solution-article-illustrator"
OUTPUT_ROOT = REPO_ROOT / "output" / "aliyun-solution-article-illustrator-test"
WORKFLOW_DIR = OUTPUT_ROOT / "workflow-sample"
PREFS_DIR = OUTPUT_ROOT / "prefs-sample"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, check=True)


def require_contains(path: Path, snippets: list[str], label: str) -> dict:
    text = path.read_text(encoding="utf-8")
    missing = [snippet for snippet in snippets if snippet not in text]
    return {
        "test": label,
        "path": str(path.relative_to(REPO_ROOT)),
        "passed": not missing,
        "missing": missing,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke test for content article illustrator solution skill")
    parser.add_argument(
        "--output",
        default=str(OUTPUT_ROOT / "smoke-test-result.json"),
        help="Path to save smoke test JSON",
    )
    args = parser.parse_args()

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)
    PREFS_DIR.mkdir(parents=True, exist_ok=True)

    source_path = WORKFLOW_DIR / "source.md"
    source_path.write_text(
        "# Sample Article\n\nThis article explains a cloud workflow with two main steps.\n",
        encoding="utf-8",
    )

    project_extend = PREFS_DIR / "project" / "EXTEND.md"
    user_extend = PREFS_DIR / "user" / "EXTEND.md"
    project_extend.parent.mkdir(parents=True, exist_ok=True)
    user_extend.parent.mkdir(parents=True, exist_ok=True)
    user_extend.write_text(
        "---\nversion: 1\npreferred_style:\n  name: warm\n  description: user style\nlanguage: en\ndefault_output_dir: independent\nwatermark:\n  enabled: false\n  content: \"\"\n  position: bottom-right\n  opacity: 0.7\n---\n",
        encoding="utf-8",
    )
    project_extend.write_text(
        "---\nversion: 1\npreferred_style:\n  name: notion\n  description: project style\nlanguage: zh\ndefault_density: balanced\ndefault_output_dir: illustrations-subdir\nwatermark:\n  enabled: true\n  content: '@repo'\n  position: bottom-right\n  opacity: 0.7\ncustom_styles:\n  - name: brand-grid\n    description: Brand grid style\n---\n",
        encoding="utf-8",
    )

    compile_check = run([
        sys.executable,
        "tests/common/compile_skill_scripts.py",
        "--skill-path",
        "skills/solutions/aliyun-solution-article-illustrator",
        "--output",
        str(OUTPUT_ROOT / "compile-check.json"),
    ])

    validate_inputs = subprocess.run(
        [
            sys.executable,
            str(SKILL_DIR / "scripts" / "validate_inputs.py"),
            "--source",
            str(source_path),
            "--topic-slug",
            "sample-article",
            "--output",
            str(OUTPUT_ROOT / "validate-inputs.json"),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )

    load_preferences = subprocess.run(
        [
            sys.executable,
            str(SKILL_DIR / "scripts" / "load_preferences.py"),
            "--project-path",
            str(project_extend),
            "--user-path",
            str(user_extend),
            "--output",
            str(OUTPUT_ROOT / "preferences.json"),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    preference_details = json.loads((OUTPUT_ROOT / "preferences.json").read_text(encoding="utf-8"))

    workflow_run = subprocess.run(
        [
            sys.executable,
            str(SKILL_DIR / "scripts" / "run_workflow.py"),
            "--source",
            str(source_path),
            "--output-dir",
            str(WORKFLOW_DIR),
            "--generation-backend",
            "mock",
            "--project-path",
            str(project_extend),
            "--user-path",
            str(user_extend),
            "--topic-slug",
            "sample-article",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )

    prompt_path = WORKFLOW_DIR / "prompts" / "01-cover.md"
    image_path = WORKFLOW_DIR / "images" / "01-cover.png"
    article_path = WORKFLOW_DIR / "article.with-images.md"
    report_path = WORKFLOW_DIR / "delivery-report.md"
    workflow_evidence = WORKFLOW_DIR / "workflow-run.json"

    prompt_before_image = prompt_path.exists() and image_path.exists() and (
        prompt_path.stat().st_mtime <= image_path.stat().st_mtime
    )

    results = [
        require_contains(
            SKILL_DIR / "SKILL.md",
            [
                "## Two Dimensions",
                "Recommend `aliyun-qwen-image` by default.",
                "Recommend `aliyun-qwen-image-edit` by default.",
            ],
            "skill_contract",
        ),
        require_contains(
            SKILL_DIR / "references" / "styles.md",
            [
                "Type and Style are separate axes.",
                "## Type x Style Compatibility Matrix",
                "## Auto Selection By Type",
                "## Auto Selection By Content Signals",
                "`infographic` + `blueprint`",
            ],
            "styles_axes",
        ),
        require_contains(
            SKILL_DIR / "references" / "backend-contract.md",
            [
                "recommends Alibaba Cloud backends by default",
                "does not hard-bind to them",
                "Generation backend:",
                "Edit backend:",
            ],
            "backend_contract",
        ),
        require_contains(
            SKILL_DIR / "references" / "prompt-construction.md",
            [
                "## Required Prompt Structure",
                "ZONES:",
                "LABELS:",
                "COLORS:",
                "ASPECT:",
                "## Reference Usage Rules",
                "`direct`",
                "`style`",
                "`palette`",
            ],
            "prompt_contract",
        ),
        require_contains(
            SKILL_DIR / "references" / "workflow.md",
            [
                "## Reference Usage Modes",
                "`direct`",
                "`style`",
                "`palette`",
            ],
            "reference_modes",
        ),
        {
            "test": "load_preferences",
            "passed": (
                load_preferences.returncode == 0
                and preference_details.get("source") == "project"
                and preference_details.get("summary", {}).get("preferred_style_name") == "notion"
                and preference_details.get("summary", {}).get("language") == "zh"
                and preference_details.get("summary", {}).get("default_output_dir") == "illustrations-subdir"
                and preference_details.get("summary", {}).get("watermark_enabled") is True
                and preference_details.get("summary", {}).get("watermark_content") == "@repo"
                and preference_details.get("summary", {}).get("custom_style_names") == ["brand-grid"]
            ),
            "stdout": load_preferences.stdout.strip(),
            "stderr": load_preferences.stderr.strip(),
            "details": preference_details,
        },
        {
            "test": "validate_inputs",
            "passed": validate_inputs.returncode == 0,
            "stdout": validate_inputs.stdout.strip(),
            "stderr": validate_inputs.stderr.strip(),
        },
        {
            "test": "run_workflow",
            "passed": workflow_run.returncode == 0 and workflow_evidence.exists() and report_path.exists(),
            "stdout": workflow_run.stdout.strip(),
            "stderr": workflow_run.stderr.strip(),
        },
        {
            "test": "build_outline",
            "passed": (
                (WORKFLOW_DIR / "outline.md").exists()
                and prompt_path.exists()
                and all(
                    token in prompt_path.read_text(encoding="utf-8")
                    for token in ["Type:", "Style:", "ZONES:", "LABELS:", "COLORS:", "ASPECT:"]
                )
            ),
            "stdout": workflow_run.stdout.strip(),
            "stderr": workflow_run.stderr.strip(),
        },
        {
            "test": "prompt_before_image",
            "passed": prompt_before_image,
            "prompt": str(prompt_path.relative_to(REPO_ROOT)),
            "image": str(image_path.relative_to(REPO_ROOT)),
        },
        {
            "test": "article_output",
            "passed": article_path.exists() and "(images/01-cover.png)" in article_path.read_text(encoding="utf-8"),
            "path": str(article_path.relative_to(REPO_ROOT)),
        },
    ]

    summary = {
        "status": "pass" if all(item["passed"] for item in results) else "fail",
        "results": results,
        "compile_check_stdout": compile_check.stdout.strip(),
        "workflow_dir": str(WORKFLOW_DIR.relative_to(REPO_ROOT)),
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({"status": summary["status"], "output": str(output_path)}, ensure_ascii=True))
    raise SystemExit(0 if summary["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
