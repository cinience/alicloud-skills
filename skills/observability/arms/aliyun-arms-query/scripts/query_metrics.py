import argparse
import json
import time

from alibabacloud_arms20190808 import models

from _common import create_client, default_region


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ARMS metrics query")
    parser.add_argument("--metric", required=True, help="metric name (e.g. appstat.incall)")
    parser.add_argument("--pid", required=True, help="application PID (e.g. xxx@cn-hangzhou)")
    parser.add_argument("--region", default=default_region())
    parser.add_argument("--measures", default="rt,count,error", help="comma-separated measures")
    parser.add_argument("--dimensions", default="rpc", help="comma-separated dimensions")
    parser.add_argument("--interval", type=int, default=60000, help="aggregation interval in ms (min 60000)")
    parser.add_argument("--start", type=int, default=None, help="start time in epoch ms")
    parser.add_argument("--end", type=int, default=None, help="end time in epoch ms")
    parser.add_argument("--last-minutes", type=int, default=15)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=10)
    parser.add_argument("--order-by", default=None, help="sort field")
    parser.add_argument("--order", default=None, choices=["ASC", "DESC"])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = create_client(args.region)

    end_ms = args.end or int(time.time() * 1000)
    start_ms = args.start or (end_ms - args.last_minutes * 60 * 1000)

    measures = [m.strip() for m in args.measures.split(",")]
    dimensions = [d.strip() for d in args.dimensions.split(",")]

    request = models.QueryMetricByPageRequest(
        metric=args.metric,
        start_time=start_ms,
        end_time=end_ms,
        interval_in_sec=args.interval,
        measures=measures,
        dimensions=dimensions,
        filters=[models.QueryMetricByPageRequestFilters(key="pid", value=args.pid)],
        current_page=args.page,
        page_size=args.page_size,
        order_by=args.order_by,
        order=args.order,
    )
    response = client.query_metric_by_page(request)
    data = response.body.data

    result = {
        "total": data.total,
        "page": data.page,
        "page_size": data.page_size,
        "completed": data.completed,
        "items": data.items or [],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
