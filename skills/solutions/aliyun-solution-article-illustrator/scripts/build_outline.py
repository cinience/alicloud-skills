#!/usr/bin/env python3
"""Create a minimal outline and prompt skeleton for article illustration."""

from __future__ import annotations

import argparse
from pathlib import Path


OUTLINE_TEXT = """# Illustration Outline

## Illustration 1

- Position: introduction
- Purpose: establish the article topic
- Visual Content: a cover illustration derived from the article theme
- Prompt File: prompts/01-cover.md
- Image File: images/01-cover.png
- Edited: no
"""


PROMPT_TEXT = """Title: Cover Illustration
Target Section: introduction
Type: scene
Style: notion
Visual Goal: establish the article topic
References:
Layout: centered editorial cover
ZONES:
- Zone 1: central concept illustration for the article theme
- Zone 2: simple background support shapes
LABELS:
- Term 1: cloud workflow
- Term 2: two main steps
COLORS:
- Primary: blue for core system concept
- Accent: orange for emphasis
STYLE NOTES: clean editorial illustration with light line work
ASPECT: 1024*1024
Prompt: create a clear editorial illustration based on the article introduction and the structured zones above
Negative Prompt: blurry, low quality, watermark
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, help="Workflow output directory")
    args = parser.parse_args()

    root = Path(args.output_dir)
    prompts = root / "prompts"
    images = root / "images"
    edits = root / "edits"
    for path in (root, prompts, images, edits):
        path.mkdir(parents=True, exist_ok=True)

    (root / "outline.md").write_text(OUTLINE_TEXT, encoding="utf-8")
    (prompts / "01-cover.md").write_text(PROMPT_TEXT, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
