#!/usr/bin/env python3
"""Stop a PTS scene and optionally poll until it is not running."""

from __future__ import annotations

import argparse
import json
import os
import time

try:
    from ._pts_client import create_client
except ImportError:
    from _pts_client import create_client


RUNNING_STATES = {"RUNNING", "DEBUGGING", "WAITSTART"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Stop a PTS scene")
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--region", default=os.getenv("ALICLOUD_REGION_ID", "cn-hangzhou"))
    parser.add_argument("--wait", action="store_true", help="Poll status after stop")
    parser.add_argument("--poll-interval", type=float, default=3.0)
    parser.add_argument("--max-wait", type=int, default=120)
    parser.add_argument("--output", help="Write JSON output to file")
    args = parser.parse_args()

    client, pts_models = create_client(args.region)
    stop_resp = client.stop_pts_scene(pts_models.StopPtsSceneRequest(scene_id=args.scene_id))
    stop_body = stop_resp.body.to_map() if stop_resp.body else {}

    result: dict[str, object] = {
        "region": args.region,
        "scene_id": args.scene_id,
        "stop_response": stop_body,
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
            if status and status not in RUNNING_STATES:
                break
            time.sleep(args.poll_interval)

        result["status_polling"] = {
            "timed_out": final_status in RUNNING_STATES or final_status is None,
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
