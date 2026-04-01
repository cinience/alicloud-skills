import os
import sys
from pathlib import Path
import json


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if not value:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def main() -> None:
    """Quickstart for AgentRun OpenAPI (ListAgentRuntimes)."""
    try:
        from alibabacloud_agentrun20250910.client import Client as AgentRunClient
        from alibabacloud_agentrun20250910 import models as agentrun_models
        from alibabacloud_tea_openapi import models as open_api_models
    except Exception:
        print(
            "Missing AgentRun SDK. Generate or install SDK from OpenAPI Explorer "
            "or install the package if available.",
            file=sys.stderr,
        )
        sys.exit(1)

    endpoint = get_env("AGENTRUN_ENDPOINT")
    access_key_id = get_env("ALICLOUD_ACCESS_KEY_ID")
    access_key_secret = get_env("ALICLOUD_ACCESS_KEY_SECRET")
    security_token = os.getenv("ALICLOUD_SECURITY_TOKEN") or os.getenv("ALIBABA_CLOUD_SECURITY_TOKEN")

    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=endpoint,
    )
    if security_token:
        config.security_token = security_token
    client = AgentRunClient(config)

    request = agentrun_models.ListAgentRuntimesRequest()
    response = client.list_agent_runtimes(request)

    output_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "compute-fc-agentrun" / "responses"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / "list_agent_runtimes.json"

    with out_file.open("w", encoding="utf-8") as f:
        json.dump(response.to_map(), f, ensure_ascii=False, indent=2)

    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()
