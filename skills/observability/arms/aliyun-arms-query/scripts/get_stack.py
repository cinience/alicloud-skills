import argparse
import json
import time

from alibabacloud_arms20190808 import models

from _common import create_client, default_region


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ARMS get span method stack")
    parser.add_argument("--trace-id", required=True)
    parser.add_argument("--rpc-id", required=True, help="RPC ID of the span")
    parser.add_argument("--pid", required=True, help="application PID (e.g. xxx@cn-hangzhou)")
    parser.add_argument("--region", default=default_region())
    parser.add_argument("--span-id", default=None)
    parser.add_argument("--start", type=int, default=None, help="start time in epoch ms")
    parser.add_argument("--end", type=int, default=None, help="end time in epoch ms")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = create_client(args.region)

    end_ms = args.end or int(time.time() * 1000)
    start_ms = args.start or (end_ms - 24 * 60 * 60 * 1000)

    request = models.GetStackRequest(
        trace_id=args.trace_id,
        rpc_id=args.rpc_id,
        pid=args.pid,
        region_id=args.region,
        span_id=args.span_id,
        start_time=start_ms,
        end_time=end_ms,
    )
    response = client.get_stack(request)

    stacks = []
    for entry in response.body.stack_info or []:
        stacks.append({
            "api": entry.api,
            "duration": entry.duration,
            "exception": entry.exception,
            "line": entry.line,
            "rpc_id": entry.rpc_id,
            "service_name": entry.service_name,
            "start_time": entry.start_time,
        })

    result = {
        "trace_id": args.trace_id,
        "rpc_id": args.rpc_id,
        "stack_count": len(stacks),
        "stacks": stacks,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
