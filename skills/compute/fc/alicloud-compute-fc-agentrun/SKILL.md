---
name: alicloud-compute-fc-agentrun
description: Manage Function Compute AgentRun resources via OpenAPI (runtime, sandbox, model, memory, credentials). Use for creating runtimes/endpoints, querying status, and troubleshooting AgentRun workflows.
---

Category: service

# Function Compute AgentRun (OpenAPI)

Use AgentRun OpenAPI (ROA) to manage runtimes, sandboxes, model services, memory, and credentials.

## Prerequisites

- AccessKey via RAM user (least privilege).
- Select the correct regional endpoint (see `references/endpoints.md`). If unsure, choose the most reasonable region for the task or ask the user.
- Use OpenAPI Explorer or official SDK to avoid manual signing (ROA requires SignatureV1).

## Workflow

1) Choose region endpoint (`agentrun.cn-<region>.aliyuncs.com`).
2) Create runtime → publish version → create runtime endpoint.
3) Create sandbox/template if needed.
4) Configure credentials and model services as required.
5) Query resources for troubleshooting.

## API Groups

See `references/api_overview.md` for the full API list and grouping.

## Script quickstart

```bash
python skills/compute/fc/alicloud-compute-fc-agentrun/scripts/quickstart.py
```

Environment variables:

- `AGENTRUN_ENDPOINT`
- `ALICLOUD_ACCESS_KEY_ID`
- `ALICLOUD_ACCESS_KEY_SECRET`
- `OUTPUT_DIR` (optional)

## Runtime flow script

```bash
AGENTRUN_RUNTIME_NAME="my-runtime" \\
AGENTRUN_RUNTIME_ENDPOINT_NAME="my-runtime-endpoint" \\
python skills/compute/fc/alicloud-compute-fc-agentrun/scripts/runtime_flow.py
```

Environment variables:

- `AGENTRUN_ENDPOINT`
- `ALICLOUD_ACCESS_KEY_ID`
- `ALICLOUD_ACCESS_KEY_SECRET`
- `AGENTRUN_RUNTIME_NAME`
- `AGENTRUN_RUNTIME_ENDPOINT_NAME`
- `AGENTRUN_RUNTIME_DESC` (optional)
- `OUTPUT_DIR` (optional)

## Cleanup script

```bash
AGENTRUN_RUNTIME_ID="runtime-id" \\
AGENTRUN_RUNTIME_ENDPOINT_ID="endpoint-id" \\
python skills/compute/fc/alicloud-compute-fc-agentrun/scripts/cleanup_runtime.py
```

Environment variables:

- `AGENTRUN_ENDPOINT`
- `ALICLOUD_ACCESS_KEY_ID`
- `ALICLOUD_ACCESS_KEY_SECRET`
- `AGENTRUN_RUNTIME_ID`
- `AGENTRUN_RUNTIME_ENDPOINT_ID`
- `OUTPUT_DIR` (optional)

## SDK Notes

See `references/sdk.md` for SDK acquisition guidance.

## Output Policy

If you store any generated files or responses, write them under:
`output/compute-fc-agentrun/`.

## References

- API overview and operation list: `references/api_overview.md`
- Regional endpoints: `references/endpoints.md`
- SDK guidance: `references/sdk.md`

- Source list: `references/sources.md`
