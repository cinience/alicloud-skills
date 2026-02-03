---
name: alicloud-platform-openapi-product-api-discovery
description: Discover and reconcile Alibaba Cloud product catalogs from Ticket System, Support & Service, and BSS OpenAPI; fetch OpenAPI product/version/API metadata; and summarize API coverage to plan new skills. Use when you need a complete product list, product-to-API mapping, or coverage/gap reports for skill generation.
---

# Alibaba Cloud Product + API Discovery

Follow this workflow to collect products, resolve API metadata, and build summaries for skill planning.

## Workflow

1) Fetch product lists from the three sources

- Ticket System (ListProducts)
- Support & Service (ListProductByGroup)
- BSS OpenAPI (QueryProductList)

Run the bundled scripts (from this skill folder):

```bash
python scripts/products_from_ticket_system.py
python scripts/products_from_support_service.py
python scripts/products_from_bssopenapi.py
```

Provide required env vars in each script (see references).

2) Merge product lists

```bash
python scripts/merge_product_sources.py
```

This writes `output/product-scan/merged_products.json` and `.md`.

3) Fetch OpenAPI metadata product list

```bash
python scripts/products_from_openapi_meta.py
```

This writes `output/product-scan/openapi-meta/products.json` and `products_normalized.json`.

4) Fetch OpenAPI API docs per product/version

```bash
python scripts/apis_from_openapi_meta.py
```

By default this can be large. Use filters for dry runs:

- `OPENAPI_META_MAX_PRODUCTS=10`
- `OPENAPI_META_PRODUCTS=Ecs,Ons`
- `OPENAPI_META_VERSIONS=2014-05-26`

5) Join products with API counts

```bash
python scripts/join_products_with_api_meta.py
```

6) Summarize products by category/group

```bash
python scripts/summarize_openapi_meta_products.py
```

6) (Optional) Compare products vs existing skills

```bash
python scripts/analyze_products_vs_skills.py
```

## Output discipline

All generated files must go under `output/`. Do not place temporary files elsewhere.

## References

- Product source APIs: see `references/product-sources.md`
- OpenAPI meta endpoints: see `references/openapi-meta.md`
