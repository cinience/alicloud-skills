# ESA DNS Records

DNS records management for ESA sites.

## Access Type & Record Restrictions

- **NS access**: Full DNS record management via API, supports all record types (A/AAAA, CNAME, MX, TXT, NS, SRV, CAA).
- **CNAME access**: DNS record APIs are available, but with restrictions:
  - **Only `CNAME` and `A/AAAA` record types** are allowed. Other types (MX, TXT, NS, SRV, CAA) will fail.
  - Records **cannot disable acceleration** (proxy must remain enabled, i.e. `Proxied` must be `true`).

## Common operations

- Create: `CreateRecord`
- List: `ListRecords` (supports pagination and filters)
- Query: `GetRecord`
- Update: `UpdateRecord`
- Delete: `DeleteRecord`
- Batch create: `BatchCreateRecords`
- Export: `ExportRecords`

## Supported record types

| Type | NS access | CNAME access |
|------|-----------|-------------|
| `A/AAAA` | Supported | Supported (must enable proxy) |
| `CNAME` | Supported | Supported (must enable proxy) |
| `MX` | Supported | Not supported |
| `TXT` | Supported | Not supported |
| `NS` | Supported | Not supported |
| `SRV` | Supported | Not supported |
| `CAA` | Supported | Not supported |

**Note**: Record type must be exact: use `A/AAAA` (not just `A`).

## ListRecords filters

- `Type`: Record type (e.g., `A/AAAA`, `CNAME`)
- `RecordName`: Record name (fuzzy match)
- `Proxied`: Whether proxied through ESA (true/false)

## CreateRecord parameters

Required:
- `SiteId`: Site ID
- `RecordName`: **Must be the full domain name** (e.g., `www.example.com`), not just the subdomain prefix (e.g., `www`). The suffix must match the site name, otherwise returns `InvalidParameter.InvalidRecordNameSuffix`.
- `Type`: Record type
- `Data`: Record value in JSON format (e.g., `{"Value":"1.2.3.4"}` for A/AAAA, `{"Value":"target.com"}` for CNAME)
- `Ttl`: Time to live (seconds). Set to `1` for system-determined TTL.

Conditionally required:
- `BizName`: **Required when `Proxied` is `true`** (i.e., acceleration enabled). Valid values: `web`, `api`, `image_video`. Omitting it when proxy is on causes `InvalidParameter.InvalidBiz`.
- `SourceType`: Required for CNAME records. Valid values: `OSS`, `S3`, `LB`, `OP`, `Domain`. Defaults to `Domain` if omitted.

Optional:
- `Proxied`: Enable ESA proxy/acceleration (default: false). CNAME-access sites must set this to `true`.
- `Priority`: Priority for MX/SRV records.
- `HostPolicy`: Origin host policy for CNAME records: `follow_hostname` or `follow_origin_domain`.
- `Comment`: Record comment (max 100 characters).

### Key gotchas

1. **RecordName must be full domain**: `qodertest.qoder.weiyigirl.top`, not `qodertest`.
2. **BizName is required when Proxied=true**: Without it, API returns `InvalidParameter.InvalidBiz` with misleading message "business type is empty or incorrect".
3. **CNAME-access sites must enable proxy**: Setting `Proxied=false` on CNAME-access sites will fail.

## Behavioral notes

- Record names must be unique within the same type
- Deleting a record that doesn't exist returns success (idempotent)
- `BatchCreateRecords` can create multiple records of different types at once
- `ExportRecords` returns all DNS records in BIND zone file format

## References

- CreateRecord: https://help.aliyun.com/zh/esa/developer-reference/api-esa-2024-09-10-createrecord
- ListRecords: https://help.aliyun.com/zh/esa/developer-reference/api-esa-2024-09-10-listrecords
