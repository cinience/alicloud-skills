import argparse
import json

from alibabacloud_arms20190808 import models

from _common import create_client, default_region


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ARMS list traced applications")
    parser.add_argument("--region", default=default_region())
    parser.add_argument("--app-type", default=None, choices=["TRACE", "EBPF"])
    parser.add_argument("--resource-group-id", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = create_client(args.region)

    request = models.ListTraceAppsRequest(
        region_id=args.region,
        app_type=args.app_type,
        resource_group_id=args.resource_group_id,
    )
    response = client.list_trace_apps(request)

    apps = []
    for app in response.body.trace_apps or []:
        apps.append({
            "pid": app.pid,
            "app_name": app.app_name,
            "type": app.type,
            "region_id": app.region_id,
            "create_time": app.create_time,
            "update_time": app.update_time,
        })

    result = {"total": len(apps), "apps": apps}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
