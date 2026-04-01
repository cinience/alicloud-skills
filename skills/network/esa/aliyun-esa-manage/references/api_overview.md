# ESA OpenAPI overview (2024-09-10) - Pages, ER, KV, Site Management, DNS & Cache

API index for Pages deployment, Edge Routine, Edge KV, site management, configuration, DNS records, and cache rules.
All APIs via Python SDK (`alibabacloud_esa20240910`).

## Pages (Based on Edge Routine)

Underlying ER API calls, see `references/pages.md` for complete flow.

### HTML Deployment Core APIs
- CreateRoutine - Create edge function
- GetRoutineStagingCodeUploadInfo - Get code upload OSS signature
- CommitRoutineStagingCode - Submit code version
- PublishRoutineCodeVersion - Publish to staging/production
- GetRoutine - Get access URL

### Static Directory Deployment Core APIs
- CreateRoutine - Create edge function
- CreateRoutineWithAssetsCodeVersion - Create code version with assets
- GetRoutineCodeVersionInfo - Query version build status
- CreateRoutineCodeDeployment - Deploy by percentage to specified environment
- GetRoutine - Get access URL

## Edge Routine (ER)

### Function Management
- CreateRoutine - Create edge function
- DeleteRoutine - Delete edge function
- GetRoutine - Get edge function details
- GetRoutineUserInfo - Get user edge function info
- ListUserRoutines - Paginate all edge functions

### Code Version
- GetRoutineStagingCodeUploadInfo - Get code upload info
- CommitRoutineStagingCode - Submit staging code version
- PublishRoutineCodeVersion - Publish code version to staging/production
- DeleteRoutineCodeVersion - Delete code version
- CreateRoutineWithAssetsCodeVersion - Create code version with assets (for static directory deployment)
- GetRoutineCodeVersionInfo - Get code version status
- CreateRoutineCodeDeployment - Create code deployment (for assets deployment)
- ListRoutineCodeVersions - Paginate code versions
- GetRoutineCodeVersion - Query single code version details
- UpdateRoutineConfigDescription - Update function description

### Route Management
- CreateRoutineRoute - Create function route
- DeleteRoutineRoute - Delete function route
- GetRoutineRoute - Get route details
- UpdateRoutineRoute - Update function route
- ListRoutineRoutes - List function routes
- ListSiteRoutes - List site routes

### Related Record Management
- CreateRoutineRelatedRecord - Create function related record (domain)
- DeleteRoutineRelatedRecord - Delete function related record
- ListRoutineRelatedRecords - List function related records

## Edge KV

Edge key-value storage, supports Namespace and Key-Value management.

### Namespace Management
- CreateKvNamespace - Create KV storage space
- DeleteKvNamespace - Delete KV storage space
- GetKvNamespace - Query single namespace info
- GetKvAccount - Query account KV usage info and all namespaces
- DescribeKvAccountStatus - Query if Edge KV is enabled

### Single Key Operations
- PutKv - Write key-value pair (≤2MB)
- PutKvWithHighCapacity - Write large capacity key-value pair (≤25MB)
- GetKv - Read key's value
- GetKvDetail - Read key-value and TTL info
- DeleteKv - Delete key-value pair

### Batch Operations
- BatchPutKv - Batch write key-value pairs (≤2MB)
- BatchPutKvWithHighCapacity - Batch write large capacity (≤100MB)
- BatchDeleteKv - Batch delete key-value pairs (≤10000)
- BatchDeleteKvWithHighCapacity - Batch delete large capacity (≤100MB)
- ListKvs - List all keys under namespace (supports prefix filter and pagination)

## Site Management

- CreateSite - Add site
- ListSites - List sites (supports pagination and filters)
- GetSite - Get site details
- DeleteSite - Delete site
- CheckSiteName - Check site name availability
- VerifySite - Verify site ownership
- UpdateSiteAccessType - Update access type (CNAME/NS)
- UpdateSiteCoverage - Update coverage area
- GetSiteCurrentNS - Get current NS servers
- UpdateSiteVanityNS - Update custom NS
- UpdateSitePause - Pause/resume site proxy
- GetSitePause - Get site proxy status
- UpdateSiteNameExclusive - Set site exclusive
- GetSiteNameExclusive - Get site exclusive status
- ActivateVersionManagement - Enable version management
- DeactivateVersionManagement - Disable version management

## Site Configuration

- GetIPv6 - Get IPv6 config
- UpdateIPv6 - Update IPv6 config

## DNS Records

NS access: supports all record types. CNAME access: only `CNAME` and `A/AAAA`, and proxy (acceleration) cannot be disabled.

- CreateRecord - Create DNS record
- ListRecords - List DNS records (supports Type, RecordName, Proxied filters)
- GetRecord - Get DNS record details
- UpdateRecord - Update DNS record
- DeleteRecord - Delete DNS record
- BatchCreateRecords - Batch create DNS records
- ExportRecords - Export DNS records

## Cache Rules

- CreateCacheRule - Create cache rule
- ListCacheRules - List cache rules
- GetCacheRule - Get cache rule details
- UpdateCacheRule - Update cache rule
- DeleteCacheRule - Delete cache rule

## References

- Official API list: https://next.api.aliyun.com/document/ESA/2024-09-10/overview
- API metadata: https://api.aliyun.com/meta/v1/products/ESA/versions/2024-09-10/api-docs.json
