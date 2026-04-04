import os
import sys
import json
from pathlib import Path


def get_env(*names: str, default: str | None = None) -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    if default is not None:
        return default
    print(f"Missing env var: {' / '.join(names)}", file=sys.stderr)
    sys.exit(1)


def get_optional_env(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def main() -> None:
    """Create runtime -> publish version -> create endpoint."""
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
    access_key_id = get_env(
        "ALIBABACLOUD_ACCESS_KEY_ID",
        "ALIBABA_CLOUD_ACCESS_KEY_ID",
        "ALICLOUD_ACCESS_KEY_ID",
    )
    access_key_secret = get_env(
        "ALIBABACLOUD_ACCESS_KEY_SECRET",
        "ALIBABA_CLOUD_ACCESS_KEY_SECRET",
        "ALICLOUD_ACCESS_KEY_SECRET",
    )
    security_token = get_optional_env(
        "ALIBABACLOUD_SECURITY_TOKEN",
        "ALIBABA_CLOUD_SECURITY_TOKEN",
        "ALICLOUD_SECURITY_TOKEN",
    )

    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=endpoint,
    )
    if security_token:
        config.security_token = security_token
    client = AgentRunClient(config)

    runtime_name = get_env("AGENTRUN_RUNTIME_NAME")
    runtime_desc = os.getenv("AGENTRUN_RUNTIME_DESC", "created-by-skill")
    runtime_endpoint_name = get_env("AGENTRUN_RUNTIME_ENDPOINT_NAME")

    # Create runtime
    create_runtime_req = agentrun_models.CreateAgentRuntimeRequest(
        name=runtime_name,
        description=runtime_desc,
    )
    create_runtime_resp = client.create_agent_runtime(create_runtime_req)
    runtime_id = create_runtime_resp.body.runtime_id

    # Publish runtime version
    publish_req = agentrun_models.PublishRuntimeVersionRequest(
        runtime_id=runtime_id,
        description="initial",
    )
    publish_resp = client.publish_runtime_version(publish_req)
    version_id = publish_resp.body.version_id

    # Create runtime endpoint
    create_endpoint_req = agentrun_models.CreateAgentRuntimeEndpointRequest(
        runtime_id=runtime_id,
        version_id=version_id,
        name=runtime_endpoint_name,
    )
    create_endpoint_resp = client.create_agent_runtime_endpoint(create_endpoint_req)

    output_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "compute-fc-agentrun" / "responses"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / "runtime_flow.json"

    payload = {
        "create_runtime": create_runtime_resp.to_map(),
        "publish_version": publish_resp.to_map(),
        "create_endpoint": create_endpoint_resp.to_map(),
    }

    with out_file.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()
