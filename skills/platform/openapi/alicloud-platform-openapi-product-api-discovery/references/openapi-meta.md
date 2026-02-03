# OpenAPI Metadata Endpoints

Use these metadata endpoints to fetch product, version, and API information.

## Product list

```text
https://api.aliyun.com/meta/v1/products.json?language=EN_US
```

- `language` can be `EN_US` or `ZH_CN`.
- Response contains product codes and versions.

Script: `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery/scripts/products_from_openapi_meta.py`

## API list per product version

```text
https://api.aliyun.com/meta/v1/products/{ProductCode}/versions/{Version}/api-docs.json
```

- Response contains API names and metadata for the product/version.

Script: `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery/scripts/apis_from_openapi_meta.py`

## API definition (single API)

```text
https://api.aliyun.com/meta/v1/products/{ProductCode}/versions/{Version}/apis/{ApiName}/api.json
```

Use this for deep inspection of request/response schemas.
