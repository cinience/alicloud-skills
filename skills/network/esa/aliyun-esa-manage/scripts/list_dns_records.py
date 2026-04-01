#!/usr/bin/env python3
"""List DNS records for an ESA site.

Only works for NS-connected sites. CNAME sites will return an error.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

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


def iter_records(client: Esa20240910Client, site_id: int, record_type: str | None = None):
    """Iterate over all DNS records for a site with pagination."""
    page_number = 1
    page_size = 100
    while True:
        req = esa_models.ListRecordsRequest(
            site_id=site_id,
            page_number=page_number,
            page_size=page_size,
        )
        if record_type:
            req.type = record_type
        resp = client.list_records(req)
        records = resp.body.records or []
        for rec in records:
            yield rec
        total = resp.body.total_count or 0
        if page_number * page_size >= total:
            break
        page_number += 1


def to_record(rec) -> dict:
    """Convert a record object to a dict."""
    return {
        "record_id": rec.record_id,
        "record_name": rec.record_name,
        "type": rec.type,
        "data": getattr(rec, "data", None) or getattr(rec, "record_data", None),
        "ttl": rec.ttl,
        "proxied": rec.proxied,
        "create_time": rec.create_time,
        "update_time": rec.update_time,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="List DNS records for an ESA site")
    parser.add_argument("--site-id", type=int, required=True, help="ESA site ID")
    parser.add_argument("--type", dest="record_type", help="Filter by record type (e.g., A/AAAA, CNAME)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    client = create_client()

    try:
        records = [to_record(rec) for rec in iter_records(client, args.site_id, args.record_type)]
    except Exception as e:
        if "CnameSiteRecordUnsupport" in str(e):
            print("Error: DNS record APIs are not available for CNAME-connected sites.", file=sys.stderr)
            print("This site uses CNAME access type. Switch to NS access to manage DNS records.", file=sys.stderr)
            return 1
        raise

    if args.json:
        print(json.dumps({"records": records, "total": len(records)}, indent=2, ensure_ascii=False))
    else:
        if not records:
            print("No DNS records found.")
            return 0
        # TSV output
        print("record_name\ttype\tdata\tttl\tproxied")
        for rec in records:
            print(f"{rec['record_name']}\t{rec['type']}\t{rec['data']}\t{rec['ttl']}\t{rec['proxied']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
