import argparse
import os
import sys

import dashvector
from dashvector import Doc


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if not value:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DashVector quickstart")
    parser.add_argument("--collection", default=os.getenv("DASHVECTOR_COLLECTION", "docs"))
    parser.add_argument("--dimension", type=int, default=int(os.getenv("DASHVECTOR_DIMENSION", "8")))
    parser.add_argument("--topk", type=int, default=5)
    parser.add_argument("--filter", default="source = 'kb' AND chunk >= 0")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    api_key = get_env("DASHVECTOR_API_KEY")
    endpoint = get_env("DASHVECTOR_ENDPOINT")

    client = dashvector.Client(api_key=api_key, endpoint=endpoint)

    print("Creating collection...")
    ret = client.create(
        name=args.collection,
        dimension=args.dimension,
        metric="cosine",
        fields_schema={"source": str, "chunk": int},
    )
    if not ret:
        raise RuntimeError("create collection failed")

    collection = client.get(name=args.collection)
    print("Upserting docs...")
    docs = [
        Doc(id="1", vector=[0.01] * args.dimension, fields={"source": "kb", "chunk": 0}),
        Doc(id="2", vector=[0.02] * args.dimension, fields={"source": "kb", "chunk": 1}),
    ]
    ret = collection.upsert(docs)
    if not ret:
        raise RuntimeError("upsert failed")

    print("Querying...")
    ret = collection.query(
        vector=[0.01] * args.dimension,
        topk=args.topk,
        filter=args.filter,
        output_fields=["source", "chunk"],
        include_vector=False,
    )
    for doc in ret:
        print(doc.id, doc.fields)


if __name__ == "__main__":
    main()
