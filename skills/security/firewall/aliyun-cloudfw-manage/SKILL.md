---
name: aliyun-cloudfw-manage
description: Use when managing Alibaba Cloud Cloud Firewall (Cloudfw) via OpenAPI/SDK, including the user requests firewall policy/resource operations, change management, status checks, or troubleshooting Cloud Firewall API workflows.
version: 1.0.0
---

Category: service

# Cloud Firewall

Use Alibaba Cloud OpenAPI (RPC) with official SDKs or OpenAPI Explorer to manage resources for Cloud Firewall.

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

- Product code: `Cloudfw`
- Default API version: `2017-12-07`
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
`output/aliyun-cloudfw-manage/`

## Validation

```bash
mkdir -p output/aliyun-cloudfw-manage
for f in skills/security/firewall/aliyun-cloudfw-manage/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-cloudfw-manage/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-cloudfw-manage/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-cloudfw-manage/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Prerequisites

- Configure least-privilege Alibaba Cloud credentials before execution.
- Prefer environment variables: `ALICLOUD_ACCESS_KEY_ID`, `ALICLOUD_ACCESS_KEY_SECRET`, optional `ALICLOUD_REGION_ID`.
- If region is unclear, ask the user before running mutating operations.

## References

- Sources: `references/sources.md`
