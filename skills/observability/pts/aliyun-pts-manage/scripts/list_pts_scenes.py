#!/usr/bin/env python3
"""List PTS scenes in a region."""

from __future__ import annotations

import argparse
import json
import os

try:
    from ._pts_client import create_client
except ImportError:
    from _pts_client import create_client


def _render_table(scenes: list[dict], region: str, page_number: int, page_size: int) -> str:
    header = f"{'SceneId':<20} {'SceneName':<36} {'Status':<16} {'CreateTime'}"
    sep = "-" * len(header)
    lines = [header, sep]
    for scene in scenes:
        lines.append(
            f"{str(scene.get('SceneId', '-')):<20} "
            f"{str(scene.get('SceneName', '-')):<36} "
            f"{str(scene.get('Status', '-')):<16} "
            f"{str(scene.get('CreateTime', '-'))}"
        )
    lines.append(sep)
    lines.append(
        f"Total page items: {len(scenes)} (region={region}, page_number={page_number}, page_size={page_size})"
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="List PTS scenes")
    parser.add_argument("--region", default=os.getenv("ALICLOUD_REGION_ID", "cn-hangzhou"))
    parser.add_argument("--keyword", help="Search by scene name or scene id")
    parser.add_argument("--page-number", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=10)
    parser.add_argument("--json", action="store_true", help="Output response body JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client, pts_models = create_client(args.region)
    req = pts_models.ListPtsSceneRequest(
        key_word=args.keyword,
        page_number=args.page_number,
        page_size=args.page_size,
    )
    resp = client.list_pts_scene(req)
    body = resp.body.to_map() if resp.body else {}
    scenes = body.get("SceneViewList") or []

    if args.json:
        output = json.dumps(body, ensure_ascii=False, indent=2)
    else:
        output = _render_table(scenes, args.region, args.page_number, args.page_size)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + ("\n" if not output.endswith("\n") else ""))
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
