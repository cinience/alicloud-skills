#!/usr/bin/env python3
"""Prepare a minimal request payload for Model Studio rerank."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="cloud vector database")
    parser.add_argument("--model", default="gte-rerank-v2")
    parser.add_argument(
        "--output",
        default="output/aliyun-modelstudio-rerank/request.json",
    )
    args = parser.parse_args()

    payload = {
        "model": args.model,
        "input": {
            "query": args.query,
            "documents": [
                "Alibaba Cloud DashVector supports vector retrieval.",
                "This paragraph is unrelated to vector search.",
            ],
        },
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
