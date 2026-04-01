#!/usr/bin/env python3
"""Summarize ESA sites by plan type.

Outputs TSV by default. Use --json for JSON output.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter

from alibabacloud_esa20240910.client import Client as Esa20240910Client
from alibabacloud_esa20240910 import models as esa_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client() -> Esa20240910Client:
    config = open_api_models.Config(
        region_id="cn-hangzhou",
        endpoint="esa.cn-hangzhou.aliyuncs.com",
    )
    ak = os.getenv("ALICLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALICLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    token = os.getenv("ALICLOUD_SECURITY_TOKEN") or os.getenv("ALIBABA_CLOUD_SECURITY_TOKEN")
    if ak and sk:
        config.access_key_id = ak
        config.access_key_secret = sk
        if token:
            config.security_token = token
    return Esa20240910Client(config)


def iter_sites(client: Esa20240910Client):
    page_number = 1
    page_size = 50
    while True:
        resp = client.list_sites(esa_models.ListSitesRequest(
            page_number=page_number,
            page_size=page_size,
        ))
        for site in resp.body.sites:
            yield site
        total = resp.body.total_count
        if page_number * page_size >= total:
            break
        page_number += 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize ESA sites by plan")
    parser.add_argument("--by-status", action="store_true", help="Further break down by status")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client()

    if args.by_status:
        counter: Counter = Counter()
        for site in iter_sites(client):
            key = (site.plan_name or "unknown", site.status or "unknown")
            counter[key] += 1
        records = [
            {"plan_name": k[0], "status": k[1], "count": v}
            for k, v in sorted(counter.items())
        ]
        header = "plan_name\tstatus\tcount"
        keys = ["plan_name", "status", "count"]
    else:
        counter = Counter()
        for site in iter_sites(client):
            counter[site.plan_name or "unknown"] += 1
        records = [
            {"plan_name": k, "count": v}
            for k, v in sorted(counter.items())
        ]
        header = "plan_name\tcount"
        keys = ["plan_name", "count"]

    if args.json:
        output = json.dumps(records, ensure_ascii=False, indent=2)
    else:
        lines = [header]
        for r in records:
            lines.append("\t".join(str(r.get(k) or "") for k in keys))
        output = "\n".join(lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
