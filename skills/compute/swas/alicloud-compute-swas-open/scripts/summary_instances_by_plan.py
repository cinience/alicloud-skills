#!/usr/bin/env python3
"""Summarize SWAS instances by plan across all regions."""

from __future__ import annotations

import argparse
import os
from collections import Counter

from alibabacloud_swas_open20200601.client import Client as SwasClient
from alibabacloud_swas_open20200601 import models as swas_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> SwasClient:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"swas.{region_id}.aliyuncs.com",
    )
    ak = os.getenv("ALICLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALICLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if ak and sk:
        config.access_key_id = ak
        config.access_key_secret = sk
    return SwasClient(config)


def list_regions() -> list[str]:
    client = create_client("cn-hangzhou")
    resp = client.list_regions(swas_models.ListRegionsRequest())
    return [r.region_id for r in resp.body.regions]


def list_instances(region_id: str):
    client = create_client(region_id)
    resp = client.list_instances(swas_models.ListInstancesRequest(region_id=region_id))
    return resp.body.instances or []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    counter: Counter[str] = Counter()
    for region_id in list_regions():
        for inst in list_instances(region_id):
            plan = getattr(inst, "plan_name", None) or getattr(inst, "plan_id", None) or "(unknown)"
            counter[plan] += 1

    lines = ["plan\tcount"]
    for plan, cnt in sorted(counter.items()):
        lines.append(f"{plan}\t{cnt}")

    output = "\n".join(lines) if len(lines) > 1 else "No SWAS instances found."
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
