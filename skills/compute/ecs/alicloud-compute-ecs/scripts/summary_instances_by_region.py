#!/usr/bin/env python3
"""Summarize ECS instance counts by region (and optionally by status)."""

from __future__ import annotations

import argparse
import os
from collections import Counter

from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_ecs20140526 import models as ecs_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Ecs20140526Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"ecs.{region_id}.aliyuncs.com",
    )
    ak = os.getenv("ALICLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALICLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if ak and sk:
        config.access_key_id = ak
        config.access_key_secret = sk
    return Ecs20140526Client(config)


def list_regions() -> list[str]:
    client = create_client("cn-hangzhou")
    resp = client.describe_regions(ecs_models.DescribeRegionsRequest())
    return [r.region_id for r in resp.body.regions.region]


def iter_instances(client: Ecs20140526Client, region_id: str):
    page_number = 1
    page_size = 100
    while True:
        resp = client.describe_instances(ecs_models.DescribeInstancesRequest(
            region_id=region_id,
            page_number=page_number,
            page_size=page_size,
        ))
        for inst in resp.body.instances.instance:
            yield inst
        total = resp.body.total_count
        if page_number * page_size >= total:
            break
        page_number += 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--by-status", action="store_true", help="Break down by instance status")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    counter: Counter[str] = Counter()
    for region_id in list_regions():
        client = create_client(region_id)
        for inst in iter_instances(client, region_id):
            key = f"{region_id}\t{inst.status}" if args.by_status else region_id
            counter[key] += 1

    lines = []
    if args.by_status:
        lines.append("region_id\tstatus\tcount")
        for key, cnt in sorted(counter.items()):
            region_id, status = key.split("\t", 1)
            lines.append(f"{region_id}\t{status}\t{cnt}")
    else:
        lines.append("region_id\tcount")
        for region_id, cnt in sorted(counter.items()):
            lines.append(f"{region_id}\t{cnt}")

    output = "\n".join(lines) if lines else "No ECS instances found."
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
