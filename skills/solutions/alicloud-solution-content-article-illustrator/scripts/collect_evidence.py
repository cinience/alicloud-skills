#!/usr/bin/env python3
"""Collect a simple artifact listing for the article illustrator workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-dir", required=True, help="Workflow output directory")
    parser.add_argument("--output", required=True, help="Path to JSON evidence file")
    args = parser.parse_args()

    root = Path(args.workflow_dir)
    files = sorted(str(path.relative_to(root)) for path in root.rglob("*") if path.is_file())
    payload = {
        "workflow_dir": str(root),
        "files": files,
        "status": "pass" if root.is_dir() else "fail",
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
