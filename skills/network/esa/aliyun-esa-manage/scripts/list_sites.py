#!/usr/bin/env python3
"""List all ESA sites.

Outputs TSV by default. Use --json for JSON output.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Iterable

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


def iter_sites(client: Esa20240910Client) -> Iterable:
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


def to_record(site) -> dict:
    return {
        "site_id": site.site_id,
        "site_name": site.site_name,
        "status": site.status,
        "access_type": site.access_type,
        "plan_name": site.plan_name,
        "coverage": site.coverage,
        "cname_zone": getattr(site, "cname_zone", None),
        "create_time": site.create_time,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="List all ESA sites")
    parser.add_argument("--json", action="store_true", help="Output JSON array")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client()
    records = [to_record(site) for site in iter_sites(client)]

    if args.json:
        output = json.dumps(records, ensure_ascii=False, indent=2)
    else:
        lines = [
            "site_id\tsite_name\tstatus\taccess_type\tplan_name\tcoverage\tcname_zone\tcreate_time"
        ]
        for r in records:
            lines.append(
                "\t".join(
                    str(r.get(k) or "")
                    for k in [
                        "site_id", "site_name", "status", "access_type",
                        "plan_name", "coverage", "cname_zone", "create_time",
                    ]
                )
            )
        output = "\n".join(lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
