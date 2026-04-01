#!/usr/bin/env python3
"""List DevOps projects by organization."""

from __future__ import annotations

import argparse
import json
import os

try:
    from ._devops_client import create_client
except ImportError:
    from _devops_client import create_client


def _to_table(projects: list[dict], org_id: str) -> str:
    header = f"{'Identifier':<26} {'Name':<34} {'Type':<18} {'Creator'}"
    sep = "-" * len(header)
    lines = [header, sep]
    for p in projects:
        lines.append(
            f"{str(p.get('identifier', '-')):<26} "
            f"{str(p.get('name', '-')):<34} "
            f"{str(p.get('typeIdentifier', '-')):<18} "
            f"{str(p.get('creator', '-'))}"
        )
    lines.append(sep)
    lines.append(f"Total: {len(projects)} project(s) in organization {org_id}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="List DevOps projects")
    parser.add_argument("--organization-id", required=True)
    parser.add_argument("--region", default=os.getenv("ALICLOUD_REGION_ID", "cn-hangzhou"))
    parser.add_argument("--category", help="Project category (required by API in most cases)")
    parser.add_argument("--scope")
    parser.add_argument("--max-results", type=int, default=20)
    parser.add_argument("--next-token")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    client, devops_models = create_client(args.region)
    req = devops_models.ListProjectsRequest(
        category=args.category or "BizOps",
        scope=args.scope,
        max_results=args.max_results,
        next_token=args.next_token,
    )
    resp = client.list_projects(args.organization_id, req)
    body = resp.body.to_map() if resp.body else {}
    projects = body.get("projects") or []

    output = json.dumps(body, ensure_ascii=False, indent=2) if args.json else _to_table(projects, args.organization_id)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + ("\n" if not output.endswith("\n") else ""))
        print(f"Output written to {args.output}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
