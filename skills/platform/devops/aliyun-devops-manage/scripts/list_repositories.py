#!/usr/bin/env python3
"""List DevOps code repositories by organization."""

from __future__ import annotations

import argparse
import json
import os

try:
    from ._devops_client import create_client
except ImportError:
    from _devops_client import create_client


def _to_table(repositories: list[dict], org_id: str) -> str:
    header = f"{'Id':<12} {'Name':<32} {'PathWithNamespace':<42} {'Visibility':<10} {'UpdatedAt'}"
    sep = "-" * len(header)
    lines = [header, sep]
    for r in repositories:
        lines.append(
            f"{str(r.get('Id', '-')):<12} "
            f"{str(r.get('name', '-')):<32} "
            f"{str(r.get('pathWithNamespace', '-')):<42} "
            f"{str(r.get('visibilityLevel', '-')):<10} "
            f"{str(r.get('updatedAt', '-'))}"
        )
    lines.append(sep)
    lines.append(f"Total: {len(repositories)} repository item(s) in organization {org_id}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="List DevOps repositories")
    parser.add_argument("--organization-id", required=True)
    parser.add_argument("--region", default=os.getenv("ALICLOUD_REGION_ID", "cn-hangzhou"))
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--per-page", type=int, default=20)
    parser.add_argument("--search")
    parser.add_argument("--sort", choices=["asc", "desc"])
    parser.add_argument("--order-by")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    client, devops_models = create_client(args.region)
    req = devops_models.ListRepositoriesRequest(
        organization_id=args.organization_id,
        page=args.page,
        per_page=args.per_page,
        search=args.search,
        sort=args.sort,
        order_by=args.order_by,
    )
    resp = client.list_repositories(req)
    body = resp.body.to_map() if resp.body else {}
    repositories = body.get("result") or []

    output = json.dumps(body, ensure_ascii=False, indent=2) if args.json else _to_table(repositories, args.organization_id)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + ("\n" if not output.endswith("\n") else ""))
        print(f"Output written to {args.output}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
