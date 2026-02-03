#!/usr/bin/env python3
"""Summarize ECS instance counts by security group across all regions."""

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
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    counter: Counter[str] = Counter()
    for region_id in list_regions():
        client = create_client(region_id)
        for inst in iter_instances(client, region_id):
            group_ids = []
            if inst.security_group_ids and inst.security_group_ids.security_group_id:
                group_ids = inst.security_group_ids.security_group_id
            if not group_ids:
                counter["(none)"] += 1
                continue
            for sg in group_ids:
                counter[sg] += 1

    lines = ["security_group_id\tcount"]
    for sg_id, cnt in sorted(counter.items()):
        lines.append(f"{sg_id}\t{cnt}")

    output = "\n".join(lines) if len(lines) > 1 else "No ECS instances found."
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
