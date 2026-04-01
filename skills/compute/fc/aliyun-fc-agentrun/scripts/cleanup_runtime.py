import os
import sys
import json
from pathlib import Path


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if not value:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def main() -> None:
    """Delete runtime endpoint then delete runtime."""
    try:
        from alibabacloud_agentrun20250910.client import Client as AgentRunClient
        from alibabacloud_agentrun20250910 import models as agentrun_models
        from alibabacloud_tea_openapi import models as open_api_models
    except Exception:
        print(
            "Missing AgentRun SDK. Generate or install SDK from OpenAPI Explorer.",
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

    runtime_id = get_env("AGENTRUN_RUNTIME_ID")
    runtime_endpoint_id = get_env("AGENTRUN_RUNTIME_ENDPOINT_ID")

    delete_endpoint_req = agentrun_models.DeleteAgentRuntimeEndpointRequest(
        runtime_id=runtime_id,
        endpoint_id=runtime_endpoint_id,
    )
    delete_endpoint_resp = client.delete_agent_runtime_endpoint(delete_endpoint_req)

    delete_runtime_req = agentrun_models.DeleteAgentRuntimeRequest(runtime_id=runtime_id)
    delete_runtime_resp = client.delete_agent_runtime(delete_runtime_req)

    output_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "compute-fc-agentrun" / "responses"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / "cleanup_runtime.json"

    payload = {
        "delete_endpoint": delete_endpoint_resp.to_map(),
        "delete_runtime": delete_runtime_resp.to_map(),
    }

    with out_file.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()
