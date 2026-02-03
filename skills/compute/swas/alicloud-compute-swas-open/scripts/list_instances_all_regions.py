#!/usr/bin/env python3
"""List SWAS instances across all regions.

Outputs TSV by default. Use --json for JSON output.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

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


def to_record(region_id: str, inst) -> dict:
    return {
        "region_id": region_id,
        "instance_id": inst.instance_id,
        "instance_name": getattr(inst, "instance_name", None),
        "status": getattr(inst, "status", None),
        "public_ip": getattr(inst, "public_ip_address", None),
        "inner_ip": getattr(inst, "inner_ip_address", None),
        "plan_id": getattr(inst, "plan_id", None),
        "plan_name": getattr(inst, "plan_name", None),
        "cpu": getattr(inst, "cpu", None),
        "memory_gib": getattr(inst, "memory", None),
        "zone_id": getattr(inst, "zone_id", None),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Output JSON array")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    records = []
    failed_regions: list[tuple[str, str]] = []
    for region_id in list_regions():
        try:
            instances = list_instances(region_id)
        except Exception as exc:
            failed_regions.append((region_id, str(exc)))
            print(f"Warning: failed to query region {region_id}: {exc}", file=sys.stderr)
            continue
        for inst in instances:
            records.append(to_record(region_id, inst))

    if args.json:
        output = json.dumps(records, ensure_ascii=False, indent=2)
    else:
        lines = [
            "region_id\tinstance_id\tinstance_name\tstatus\tpublic_ip\tinner_ip\tplan_name\tplan_id\tcpu\tmemory_gib\tzone_id"
        ]
        for r in records:
            lines.append(
                "\t".join(
                    [
                        str(r.get("region_id") or ""),
                        str(r.get("instance_id") or ""),
                        str(r.get("instance_name") or ""),
                        str(r.get("status") or ""),
                        str(r.get("public_ip") or ""),
                        str(r.get("inner_ip") or ""),
                        str(r.get("plan_name") or ""),
                        str(r.get("plan_id") or ""),
                        str(r.get("cpu") or ""),
                        str(r.get("memory_gib") or ""),
                        str(r.get("zone_id") or ""),
                    ]
                )
            )
        output = "\n".join(lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)

    if failed_regions:
        print("\nFailed regions:", file=sys.stderr)
        for region_id, err in failed_regions:
            print(f"- {region_id}: {err}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
