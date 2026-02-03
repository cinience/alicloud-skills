---
name: alicloud-data-lake-dlf
description: Manage Alibaba Cloud Data Lake Formation (DataLake) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. Also use to discover APIs via OpenAPI metadata when unsure.
---

Category: service

# Data Lake Formation

Use Alibaba Cloud OpenAPI (RPC) with official SDKs or OpenAPI Explorer to manage resources for Data Lake Formation.

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

- Product code: `DataLake`
- Default API version: `2020-07-10`
- Use OpenAPI metadata endpoints to list APIs and get schemas (see references).

## Output policy

If you need to save responses or generated artifacts, write them under:
`output/alicloud-data-lake-dlf/`

## References

- Sources: `references/sources.md`
