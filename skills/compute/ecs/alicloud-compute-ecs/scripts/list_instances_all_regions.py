#!/usr/bin/env python3
"""List ECS instances across all regions.

Outputs TSV by default. Use --json for JSON output.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Iterable

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


def iter_instances(client: Ecs20140526Client, region_id: str) -> Iterable[ecs_models.DescribeInstancesResponseBodyInstancesInstance]:
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


def to_record(region_id: str, inst) -> dict:
    return {
        "region_id": region_id,
        "instance_id": inst.instance_id,
        "instance_name": inst.instance_name,
        "status": inst.status,
        "instance_type": inst.instance_type,
        "cpu": inst.cpu,
        "memory_gib": inst.memory,
        "zone_id": inst.zone_id,
        "vpc_id": (inst.vpc_attributes.vpc_id if inst.vpc_attributes else None),
        "vswitch_id": (inst.vpc_attributes.v_switch_id if inst.vpc_attributes else None),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Output JSON array")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    records = []
    for region_id in list_regions():
        client = create_client(region_id)
        for inst in iter_instances(client, region_id):
            records.append(to_record(region_id, inst))

    if args.json:
        output = json.dumps(records, ensure_ascii=False, indent=2)
    else:
        lines = [
            "region_id\tinstance_id\tinstance_name\tstatus\tinstance_type\tcpu\tmemory_gib\tzone_id\tvpc_id\tvswitch_id"
        ]
        for r in records:
            lines.append(
                "\t".join(
                    [
                        str(r.get("region_id") or ""),
                        str(r.get("instance_id") or ""),
                        str(r.get("instance_name") or ""),
                        str(r.get("status") or ""),
                        str(r.get("instance_type") or ""),
                        str(r.get("cpu") or ""),
                        str(r.get("memory_gib") or ""),
                        str(r.get("zone_id") or ""),
                        str(r.get("vpc_id") or ""),
                        str(r.get("vswitch_id") or ""),
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
