#!/usr/bin/env python3
"""List DevOps pipelines by organization."""

from __future__ import annotations

import argparse
import json
import os

try:
    from ._devops_client import create_client
except ImportError:
    from _devops_client import create_client


def _to_table(pipelines: list[dict], org_id: str) -> str:
    header = f"{'PipelineId':<14} {'PipelineName':<42} {'GroupId':<12} {'CreatorAccountId'}"
    sep = "-" * len(header)
    lines = [header, sep]
    for p in pipelines:
        lines.append(
            f"{str(p.get('pipelineId', '-')):<14} "
            f"{str(p.get('pipelineName', '-')):<42} "
            f"{str(p.get('groupId', '-')):<12} "
            f"{str(p.get('creatorAccountId', '-'))}"
        )
    lines.append(sep)
    lines.append(f"Total: {len(pipelines)} pipeline(s) in organization {org_id}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="List DevOps pipelines")
    parser.add_argument("--organization-id", required=True)
    parser.add_argument("--region", default=os.getenv("ALICLOUD_REGION_ID", "cn-hangzhou"))
    parser.add_argument("--pipeline-name")
    parser.add_argument("--status-list", help="comma-separated status values")
    parser.add_argument("--max-results", type=int, default=20)
    parser.add_argument("--next-token")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    client, devops_models = create_client(args.region)
    req = devops_models.ListPipelinesRequest(
        pipeline_name=args.pipeline_name,
        status_list=args.status_list,
        max_results=args.max_results,
        next_token=args.next_token,
    )
    resp = client.list_pipelines(args.organization_id, req)
    body = resp.body.to_map() if resp.body else {}
    pipelines = body.get("pipelines") or []

    output = json.dumps(body, ensure_ascii=False, indent=2) if args.json else _to_table(pipelines, args.organization_id)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + ("\n" if not output.endswith("\n") else ""))
        print(f"Output written to {args.output}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
