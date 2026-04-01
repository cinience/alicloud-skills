import argparse
import os
import sys

from alibabacloud_ha3engine import client, models
from Tea.exceptions import TeaException, RetryError


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if not value:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpenSearch vector quickstart")
    parser.add_argument("--cluster", default=os.getenv("OPENSEARCH_CLUSTER", "general"))
    parser.add_argument("--hit", type=int, default=5)
    parser.add_argument("--query", default="title:hello")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = models.Config(
        endpoint=get_env("OPENSEARCH_ENDPOINT"),
        instance_id=get_env("OPENSEARCH_INSTANCE_ID"),
        protocol="http",
        access_user_name=get_env("OPENSEARCH_USERNAME"),
        access_pass_word=get_env("OPENSEARCH_PASSWORD"),
    )
    ha3 = client.Client(cfg)

    data_source = get_env("OPENSEARCH_DATASOURCE")
    pk_field = get_env("OPENSEARCH_PK_FIELD", "id")

    documents = [
        {"fields": {"id": 1, "title": "hello", "content": "world"}, "cmd": "add"},
        {"fields": {"id": 2, "title": "faq", "content": "vector search"}, "cmd": "add"},
    ]

    try:
        print("Pushing docs...")
        req = models.PushDocumentsRequestModel({}, documents)
        resp = ha3.push_documents(data_source, pk_field, req)
        print(resp.body)

        print("Searching...")
        query_str = (
            f"config=hit:{args.hit},format:json,qrs_chain:search"
            f"&&query={args.query}"
            f"&&cluster={args.cluster}"
        )
        ha_query = models.SearchQuery(query=query_str)
        req = models.SearchRequestModel({}, ha_query)
        resp = ha3.search(req)
        print(resp)
    except (TeaException, RetryError) as exc:
        print(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
