#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ossutil skill prerequisites and write evidence.")
    parser.add_argument("--check-binary", action="store_true", help="Check ossutil binary availability and version")
    parser.add_argument("--output", default="output/aliyun-oss-ossutil/validate.txt")
    args = parser.parse_args()

    install_doc = Path("skills/storage/oss/aliyun-oss-ossutil/references/install.md")
    skill_doc = Path("skills/storage/oss/aliyun-oss-ossutil/SKILL.md")

    lines = [
        f"install_doc_exists={install_doc.exists()}",
        f"skill_doc_exists={skill_doc.exists()}",
    ]

    if args.check_binary:
        binary = shutil.which("ossutil")
        lines.append(f"ossutil_path={binary or 'NOT_FOUND'}")
        if binary:
            proc = subprocess.run([binary, "--version"], capture_output=True, text=True, check=False)
            lines.append(f"ossutil_version_exit={proc.returncode}")
            lines.append(proc.stdout.strip() or proc.stderr.strip())

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
