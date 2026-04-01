---
name: aliyun-kms-manage
description: Manage Alibaba Cloud Key Management Service (KMS) via OpenAPI/SDK. Use whenever the user needs key lifecycle/resource operations, policy/configuration changes, status inspection, or troubleshooting KMS API workflows.
version: 1.0.0
---

Category: service

# Key Management Service

## Validation

```bash
mkdir -p output/aliyun-kms-manage
python -m py_compile skills/security/key-management/aliyun-kms-manage/scripts/list_openapi_meta_apis.py && echo "py_compile_ok" > output/aliyun-kms-manage/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-kms-manage/validate.txt` is generated.

## Output And Evidence

- Save KMS API discovery outputs and operation results in `output/aliyun-kms-manage/`.
- Keep at least one request parameter example per operation type.

Use Alibaba Cloud OpenAPI (RPC) with official SDKs or OpenAPI Explorer to manage resources for KeyManagementService.

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

- Product code: `Kms`
- Default API version: `2016-01-20`
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
`output/aliyun-kms-manage/`

## Prerequisites

- Configure least-privilege Alibaba Cloud credentials before execution.
- Prefer environment variables: `ALICLOUD_ACCESS_KEY_ID`, `ALICLOUD_ACCESS_KEY_SECRET`, optional `ALICLOUD_REGION_ID`.
- If region is unclear, ask the user before running mutating operations.

## References

- Sources: `references/sources.md`
