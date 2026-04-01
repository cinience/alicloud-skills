# ESA Sites

Sites are the basic management unit of ESA. Each site corresponds to a domain (or subdomain).

## Common operations

- Create: `CreateSite`
- List: `ListSites` (supports pagination and filters)
- Query: `GetSite`
- Delete: `DeleteSite`
- Check name: `CheckSiteName`
- Change access type: `UpdateSiteAccessType`
- Change coverage: `UpdateSiteCoverage`

## Access types

- **CNAME**: Keep original DNS, add CNAME record pointing to ESA edge node.
  - Pros: Simple setup, no DNS migration needed.
  - Limitation: **DNS record APIs are NOT available** (CreateRecord, ListRecords, etc. will fail).
- **NS**: Delegate nameservers to ESA, ESA takes over DNS resolution.
  - Pros: Full DNS management via API.
  - Limitation: Must change NS records at domain registrar.

## Switching access type

Use `UpdateSiteAccessType` to switch between CNAME and NS.

- NS -> CNAME: Will fail if incompatible DNS records exist. Delete A/AAAA records first.
- CNAME -> NS: Works directly. After switching, manage DNS via ESA API.

## Coverage options

- `domestic`: China mainland only
- `overseas`: Outside China mainland
- `global`: Worldwide

## Plan types

- `basicplan` / `standardplan` / `advancedplan` / `enterpriseplan`

## ListSites filters

- `SiteName`: Fuzzy match
- `Status`: Site status (active, pending, etc.)
- `AccessType`: NS or CNAME
- `Coverage`: domestic, overseas, global
- `PlanSubscribeType`: Plan type

## Behavioral notes

- Newly created sites start as `pending`; complete access verification to activate.
- Deleting a site removes all associated configuration (DNS records, cache rules, WAF rules, certificates, etc.).
- `ListSites` returns sites across all regions; no need to iterate regions.

## References

- CreateSite: https://help.aliyun.com/zh/esa/developer-reference/api-esa-2024-09-10-createsite
- ListSites: https://help.aliyun.com/zh/esa/developer-reference/api-esa-2024-09-10-listsites
- Access types: https://help.aliyun.com/zh/esa/user-guide/add-site
