import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from aliyun.log import LogClient, GetLogsRequest


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if not value:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SLS log query")
    parser.add_argument("--query", default="*")
    parser.add_argument("--project", default=os.getenv("SLS_PROJECT"))
    parser.add_argument(
        "--logstore",
        action="append",
        default=None,
        help="logstore name (repeatable, or comma-separated values)",
    )
    parser.add_argument("--endpoint", default=os.getenv("SLS_ENDPOINT"))
    parser.add_argument("--start", type=int, default=None, help="epoch seconds")
    parser.add_argument("--end", type=int, default=None, help="epoch seconds")
    parser.add_argument("--last-minutes", type=int, default=15)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--parallel", type=int, default=4, help="max concurrent logstore queries")
    return parser.parse_args()


def parse_logstores(raw_values: list[str] | None, fallback: str | None) -> list[str]:
    values = raw_values or []
    if not values and fallback:
        values = [fallback]
    out: list[str] = []
    seen: set[str] = set()
    for raw in values:
        for item in (part.strip() for part in raw.split(",")):
            if not item or item in seen:
                continue
            seen.add(item)
            out.append(item)
    if not out:
        print("Missing env var or arg: SLS_LOGSTORE / --logstore", file=sys.stderr)
        sys.exit(1)
    return out


def fetch_logs(
    client: LogClient,
    project: str,
    logstore: str,
    start_time: int,
    end_time: int,
    query: str,
    limit: int,
) -> list[dict]:
    request = GetLogsRequest(
        project,
        logstore,
        start_time,
        end_time,
        query=query,
        line=limit,
    )
    response = client.get_logs(request)
    rows: list[dict] = []
    for log in response.get_logs():
        item = dict(log.contents)
        item["__project"] = project
        item["__logstore"] = logstore
        rows.append(item)
    return rows


def main() -> None:
    args = parse_args()
    project = args.project or get_env("SLS_PROJECT")
    logstores = parse_logstores(args.logstore, os.getenv("SLS_LOGSTORE"))
    endpoint = args.endpoint or get_env("SLS_ENDPOINT")

    start_time = args.start
    end_time = args.end
    if end_time is None:
        end_time = int(time.time())
    if start_time is None:
        start_time = end_time - args.last_minutes * 60

    client = LogClient(
        endpoint,
        get_env("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        get_env("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )

    max_workers = max(1, min(args.parallel, len(logstores)))
    failures: list[str] = []
    all_rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(
                fetch_logs,
                client,
                project,
                logstore,
                start_time,
                end_time,
                args.query,
                args.limit,
            ): logstore
            for logstore in logstores
        }
        for fut in as_completed(futures):
            logstore = futures[fut]
            try:
                all_rows.extend(fut.result())
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{logstore}: {exc}")

    for row in all_rows:
        print(json.dumps(row, ensure_ascii=False))
    if failures:
        print("partial failures:", file=sys.stderr)
        for msg in failures:
            print(f"- {msg}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
