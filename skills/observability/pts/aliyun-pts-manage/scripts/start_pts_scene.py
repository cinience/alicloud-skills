#!/usr/bin/env python3
"""Start a PTS scene and optionally poll running status."""

from __future__ import annotations

import argparse
import json
import os
import time

try:
    from ._pts_client import create_client
except ImportError:
    from _pts_client import create_client


RUNNING_STATES = {"RUNNING", "DEBUGGING"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Start a PTS scene")
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--region", default=os.getenv("ALICLOUD_REGION_ID", "cn-hangzhou"))
    parser.add_argument("--wait", action="store_true", help="Poll running status after start")
    parser.add_argument("--poll-interval", type=float, default=3.0)
    parser.add_argument("--max-wait", type=int, default=120)
    parser.add_argument("--output", help="Write JSON output to file")
    args = parser.parse_args()

    client, pts_models = create_client(args.region)
    start_resp = client.start_pts_scene(pts_models.StartPtsSceneRequest(scene_id=args.scene_id))
    start_body = start_resp.body.to_map() if start_resp.body else {}

    result: dict[str, object] = {
        "region": args.region,
        "scene_id": args.scene_id,
        "start_response": start_body,
    }

    if args.wait:
        deadline = time.time() + args.max_wait
        polls: list[dict] = []
        final_status = None

        while time.time() < deadline:
            status_resp = client.get_pts_scene_running_status(
                pts_models.GetPtsSceneRunningStatusRequest(scene_id=args.scene_id)
            )
            status_body = status_resp.body.to_map() if status_resp.body else {}
            polls.append(status_body)
            status = str(status_body.get("Status", "")).upper()
            final_status = status
            if status in RUNNING_STATES:
                break
            time.sleep(args.poll_interval)

        result["status_polling"] = {
            "timed_out": final_status not in RUNNING_STATES,
            "final_status": final_status,
            "attempts": len(polls),
            "polls": polls,
        }

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Output written to {args.output}")
    else:
        print(output)

    if args.wait:
        sp = result.get("status_polling", {})
        if isinstance(sp, dict) and sp.get("timed_out"):
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
