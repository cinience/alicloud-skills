import argparse
import json
import time

from alibabacloud_arms20190808 import models

from _common import create_client, default_region


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ARMS trace search")
    parser.add_argument("--region", default=default_region())
    parser.add_argument("--service-name", default=None)
    parser.add_argument("--operation-name", default=None)
    parser.add_argument("--min-duration", type=int, default=None, help="minimum duration in ms")
    parser.add_argument("--service-ip", default=None)
    parser.add_argument("--error-only", action="store_true")
    parser.add_argument("--pid", default=None, help="application PID (e.g. xxx@cn-hangzhou)")
    parser.add_argument("--session-id", default=None, help="shortcut for --tag session.id=VALUE")
    parser.add_argument("--tag", action="append", default=[], help="KEY=VALUE tag filter (repeatable)")
    parser.add_argument("--exclusion-filter", action="append", default=[], help="KEY=VALUE exclusion filter (repeatable)")
    parser.add_argument("--start", type=int, default=None, help="start time in epoch ms")
    parser.add_argument("--end", type=int, default=None, help="end time in epoch ms")
    parser.add_argument("--last-minutes", type=int, default=15)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=20)
    parser.add_argument("--reverse", action="store_true", help="sort by time descending")
    return parser.parse_args()


def parse_tags(raw_tags: list[str]) -> list[models.SearchTracesByPageRequestTags] | None:
    if not raw_tags:
        return None
    tags = []
    for t in raw_tags:
        if "=" not in t:
            raise SystemExit(f"Invalid tag format (expected KEY=VALUE): {t}")
        key, value = t.split("=", 1)
        tags.append(models.SearchTracesByPageRequestTags(key=key, value=value))
    return tags


def parse_exclusion_filters(raw: list[str]) -> list[models.SearchTracesByPageRequestExclusionFilters] | None:
    if not raw:
        return None
    filters = []
    for item in raw:
        if "=" not in item:
            raise SystemExit(f"Invalid exclusion filter format (expected KEY=VALUE): {item}")
        key, value = item.split("=", 1)
        filters.append(models.SearchTracesByPageRequestExclusionFilters(key=key, value=value))
    return filters


def main() -> None:
    args = parse_args()
    client = create_client(args.region)

    # --session-id shortcut
    if args.session_id:
        args.tag.append(f"session.id={args.session_id}")

    end_ms = args.end or int(time.time() * 1000)
    start_ms = args.start or (end_ms - args.last_minutes * 60 * 1000)

    request = models.SearchTracesByPageRequest(
        region_id=args.region,
        start_time=start_ms,
        end_time=end_ms,
        service_name=args.service_name,
        operation_name=args.operation_name,
        min_duration=args.min_duration,
        service_ip=args.service_ip,
        pid=args.pid,
        is_error=args.error_only if args.error_only else None,
        tags=parse_tags(args.tag),
        exclusion_filters=parse_exclusion_filters(args.exclusion_filter),
        page_number=args.page,
        page_size=args.page_size,
        reverse=args.reverse,
    )
    response = client.search_traces_by_page(request)
    page_bean = response.body.page_bean

    result = {
        "total": page_bean.total,
        "page": page_bean.page_number,
        "page_size": page_bean.page_size,
        "traces": [],
    }
    for trace in page_bean.trace_infos or []:
        result["traces"].append({
            "trace_id": trace.trace_id,
            "duration": trace.duration,
            "service_name": trace.service_name,
            "operation_name": trace.operation_name,
            "service_ip": trace.service_ip,
            "timestamp": trace.timestamp,
        })

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
