#!/usr/bin/env python3
"""Wait for an ALB async job to complete.

Most ALB write operations (create/update/delete listener, rule, ALB instance)
return a job_id. Use this script to poll until the job reaches a terminal state.

Job statuses: Processing → Succeeded / Failed

Examples:
    # Wait for a job (default 120s timeout)
    python wait_for_job.py --region cn-chengdu --job-id 606f647c-5873-42a7-aa40-7ced282037b7

    # Custom timeout and interval
    python wait_for_job.py --region cn-chengdu --job-id xxx --timeout 300 --interval 3

    # JSON output
    python wait_for_job.py --region cn-chengdu --job-id xxx --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from alibabacloud_alb20200616.client import Client as Alb20200616Client
from alibabacloud_alb20200616 import models as alb_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Alb20200616Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"alb.{region_id}.aliyuncs.com",
    )
    ak = os.getenv("ALICLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALICLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    token = os.getenv("ALICLOUD_SECURITY_TOKEN") or os.getenv("ALIBABA_CLOUD_SECURITY_TOKEN")
    if not ak or not sk:
        raise RuntimeError("ALICLOUD_ACCESS_KEY_ID and ALICLOUD_ACCESS_KEY_SECRET must be set")
    config.access_key_id = ak
    config.access_key_secret = sk
    if token:
        config.security_token = token
    return Alb20200616Client(config)


TERMINAL_STATUSES = {"Succeeded", "Failed"}


def poll_job(client: Alb20200616Client, job_id: str, timeout: int, interval: int) -> dict:
    """Poll job status until terminal or timeout."""
    elapsed = 0
    last_status = None

    while elapsed < timeout:
        try:
            resp = client.list_asyn_jobs(alb_models.ListAsynJobsRequest(
                job_ids=[job_id],
                max_results=1,
            ))
            jobs = resp.body.jobs or []
            if not jobs:
                # Job not found yet, might need a moment to appear
                if elapsed > 10:
                    return {
                        "job_id": job_id,
                        "status": "NotFound",
                        "error": "Job not found after waiting",
                    }
            else:
                job = jobs[0]
                last_status = job.status
                if last_status in TERMINAL_STATUSES:
                    result = {
                        "job_id": job.id,
                        "status": job.status,
                        "api_name": job.api_name,
                        "resource_type": job.resource_type,
                        "resource_id": job.resource_id,
                        "operate_type": job.operate_type,
                        "elapsed_seconds": elapsed,
                    }
                    if job.error_code:
                        result["error_code"] = job.error_code
                    if job.error_message:
                        result["error_message"] = job.error_message
                    return result
        except Exception as e:
            print(f"  Warning: poll error: {e}", file=sys.stderr)

        time.sleep(interval)
        elapsed += interval

    return {
        "job_id": job_id,
        "status": last_status or "Unknown",
        "error": f"Timeout after {timeout}s",
        "elapsed_seconds": elapsed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Wait for ALB async job to complete")
    parser.add_argument("--region", required=True, help="Region ID")
    parser.add_argument("--job-id", required=True, help="Async job ID")
    parser.add_argument("--timeout", type=int, default=120, help="Max wait time in seconds (default: 120)")
    parser.add_argument("--interval", type=int, default=2, help="Poll interval in seconds (default: 2)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")

    args = parser.parse_args()

    client = create_client(args.region)
    result = poll_job(client, args.job_id, args.timeout, args.interval)

    if args.json:
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        status = result["status"]
        elapsed = result.get("elapsed_seconds", "?")
        api = result.get("api_name", "")
        resource = result.get("resource_id", "")
        if status == "Succeeded":
            output = f"Job {args.job_id} succeeded ({elapsed}s). {api} → {resource}"
        elif status == "Failed":
            err = result.get("error_message") or result.get("error_code") or "unknown error"
            output = f"Job {args.job_id} failed: {err}"
        else:
            output = f"Job {args.job_id}: status={status} (timeout or not found)"

    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0 if result["status"] == "Succeeded" else 1


if __name__ == "__main__":
    raise SystemExit(main())
