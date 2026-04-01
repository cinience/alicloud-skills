---
name: aliyun-cloudauth-verify
description: Use when managing Alibaba Cloud ID Verification (Cloudauth) via OpenAPI/SDK, including the user is working on identity-verification resource operations, config updates, status checks, or troubleshooting Cloudauth API workflows.
version: 1.0.0
---

Category: service

# ID Verification (Cloudauth)

Use Alibaba Cloud OpenAPI (RPC) with official SDKs or OpenAPI Explorer to manage resources for ID Verification.

## Workflow

1) Confirm region, resource identifiers, and desired action.
2) Discover API list and required parameters (see references).
3) Call API with SDK or OpenAPI Explorer.
4) Verify results with describe/list APIs.

## AccessKey priority (must follow)

1) Environment variables: `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`
Region policy: `ALICLOUD_REGION_ID` is an optional default. If unset, decide the most reasonable region for the task; if unclear, ask the user.
2) Shared config file: `~/.alibabacloud/credentials`

## API discovery

- Product code: `Cloudauth`
- Default API version: `2022-11-25`
- Use OpenAPI metadata endpoints to list APIs and get schemas (see references).

## High-frequency operation patterns

1) Inventory/list: prefer `List*` / `Describe*` APIs to get current resources.
2) Change/configure: prefer `Create*` / `Update*` / `Modify*` / `Set*` APIs for mutations.
3) Status/troubleshoot: prefer `Get*` / `Query*` / `Describe*Status` APIs for diagnosis.

## Minimal executable quickstart

Use metadata-first discovery before calling business APIs:

```bash
python scripts/list_openapi_meta_apis.py
```

Optional overrides:

```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```

The script writes API inventory artifacts under the skill output directory.

## Output policy

If you need to save responses or generated artifacts, write them under:
`output/aliyun-cloudauth-verify/`

## Validation

```bash
mkdir -p output/aliyun-cloudauth-verify
for f in skills/security/identity/aliyun-cloudauth-verify/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-cloudauth-verify/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-cloudauth-verify/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-cloudauth-verify/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Prerequisites

- Configure least-privilege Alibaba Cloud credentials before execution.
- Prefer environment variables: `ALICLOUD_ACCESS_KEY_ID`, `ALICLOUD_ACCESS_KEY_SECRET`, optional `ALICLOUD_REGION_ID`.
- If region is unclear, ask the user before running mutating operations.

## References

- Sources: `references/sources.md`
