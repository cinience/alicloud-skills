# Product Source APIs

Keep this file short. Update versions and endpoints from the official docs when they change.

## Ticket System - ListProducts

- Action: `ListProducts`
- Required: endpoint, version, access key, secret
- Optional: `Name`, `Language`

Script: `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery/scripts/products_from_ticket_system.py`

## Support & Service - ListProductByGroup

- Action: `ListProductByGroup`
- Required: `OpenGroupId`, endpoint, version, access key, secret

Script: `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery/scripts/products_from_support_service.py`

## BSS OpenAPI - QueryProductList

- Action: `QueryProductList`
- Endpoint: `business.aliyuncs.com`
- Version: `2017-12-14`
- Params: `PageNum`, `PageSize`, `QueryTotalCount`

Script: `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery/scripts/products_from_bssopenapi.py`
