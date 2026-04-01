import argparse
import os
import sys

from pymilvus import MilvusClient


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if not value:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AliCloud Milvus quickstart")
    parser.add_argument("--collection", default=os.getenv("MILVUS_COLLECTION", "docs"))
    parser.add_argument("--dimension", type=int, default=int(os.getenv("MILVUS_DIMENSION", "8")))
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--filter", default='source == "kb" and chunk >= 0')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = MilvusClient(
        uri=get_env("MILVUS_URI"),
        token=get_env("MILVUS_TOKEN"),
        db_name=get_env("MILVUS_DB", "default"),
    )

    print("Creating collection...")
    client.create_collection(collection_name=args.collection, dimension=args.dimension)

    print("Inserting data...")
    items = [
        {"id": 1, "vector": [0.01] * args.dimension, "source": "kb", "chunk": 0},
        {"id": 2, "vector": [0.02] * args.dimension, "source": "kb", "chunk": 1},
    ]
    client.insert(collection_name=args.collection, data=items)

    print("Searching...")
    query_vectors = [[0.01] * args.dimension]
    res = client.search(
        collection_name=args.collection,
        data=query_vectors,
        limit=args.limit,
        filter=args.filter,
        output_fields=["source", "chunk"],
    )
    print(res)


if __name__ == "__main__":
    main()
