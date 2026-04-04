# ESA Pages — Edge Page Deployment Reference

ESA Pages provides the ability to quickly deploy HTML pages or static file directories to edge nodes. Built on Edge Routine, deployments are completed via Python SDK calling ESA OpenAPI.

## Deploy HTML Pages

### Flow

```
1. CreateRoutine(name)                     → Create routine (skip if exists)
2. GetRoutineStagingCodeUploadInfo(name)   → Get OSS upload signature
3. POST code to OSS                        → Upload code file
4. CommitRoutineStagingCode(name)          → Commit code version
5. PublishRoutineCodeVersion(staging)      → Deploy to staging
6. PublishRoutineCodeVersion(production)   → Deploy to production
7. GetRoutine(name)                        → Get defaultRelatedRecord as access URL
```

### Code Template

HTML content needs to be wrapped as Edge Routine code:

```javascript
const html = `<html><body>Hello World</body></html>`;

async function handleRequest(request) {
  return new Response(html, {
    headers: { "content-type": "text/html;charset=UTF-8" },
  });
}

export default {
  async fetch(request) {
    return handleRequest(request);
  },
};
```

### Python SDK Example

```python
from alibabacloud_esa20240910.client import Client as Esa20240910Client
from alibabacloud_esa20240910 import models as esa_models
from alibabacloud_tea_openapi import models as open_api_models
import requests


def create_client() -> Esa20240910Client:
    config = open_api_models.Config(
        region_id="cn-hangzhou",
        endpoint="esa.cn-hangzhou.aliyuncs.com",
    )
    return Esa20240910Client(config)


def deploy_html(name: str, html: str):
    """Deploy HTML page to ESA Pages"""
    client = create_client()

    # Escape special characters in template string
    escaped_html = html.replace("`", "\\`").replace("$", "\\$")
    code = f'''const html = `{escaped_html}`;

async function handleRequest(request) {{
  return new Response(html, {{
    headers: {{ "content-type": "text/html;charset=UTF-8" }},
  }});
}}

export default {{
  async fetch(request) {{
    return handleRequest(request);
  }},
}};'''

    # 1. Create routine (skip if exists)
    try:
        client.create_routine(esa_models.CreateRoutineRequest(name=name))
    except Exception as e:
        if "RoutineNameAlreadyExist" not in str(e):
            raise

    # 2. Get upload signature
    upload_info = client.get_routine_staging_code_upload_info(
        esa_models.GetRoutineStagingCodeUploadInfoRequest(name=name)
    )
    oss = upload_info.body.oss_post_config

    # 3. Upload code to OSS
    form_data = {
        "OSSAccessKeyId": oss.ossaccess_key_id,
        "Signature": oss.signature,
        "callback": oss.callback,
        "x:codeDescription": oss.x_code_description,
        "policy": oss.policy,
        "key": oss.key,
    }
    requests.post(oss.url, data=form_data, files={"file": code.encode()})

    # 4. Commit code version
    commit = client.commit_routine_staging_code(
        esa_models.CommitRoutineStagingCodeRequest(name=name)
    )
    version = commit.body.code_version

    # 5-6. Deploy to staging and production
    for env in ["staging", "production"]:
        client.publish_routine_code_version(
            esa_models.PublishRoutineCodeVersionRequest(
                name=name, env=env, code_version=version
            )
        )

    # 7. Get access URL
    routine = client.get_routine(esa_models.GetRoutineRequest(name=name))
    domain = routine.body.default_related_record
    return f"https://{domain}" if domain else None
```

## Deploy Static File Directory

### Flow

```
1. CreateRoutine(name)                            → Create routine (skip if exists)
2. CreateRoutineWithAssetsCodeVersion(name)       → Create assets code version, get OSS signature
3. Package directory as zip → POST zip to OSS     → Upload assets
4. Poll GetRoutineCodeVersionInfo(name, version)  → Wait for available status
5. CreateRoutineCodeDeployment(staging, 100%)     → Deploy to staging
6. CreateRoutineCodeDeployment(production, 100%)  → Deploy to production
7. GetRoutine(name)                               → Get access URL
```

### Zip Package Structure

The zip package structure created during deployment depends on the project's `EDGE_ROUTINE_TYPE`, with three cases:

#### 1. JS_ONLY (entry file only)

```
your-project.zip
└── routine/
    └── index.js        ← Code bundled by esbuild (or source file directly when --no-bundle)
```

#### 2. ASSETS_ONLY (static resources only)

```
your-project.zip
└── assets/
    ├── image.png
    ├── style.css
    └── subdir/
        └── data.json   ← All files under assets directory, maintaining original structure
```

#### 3. JS_AND_ASSETS (entry file + static resources, most common)

```
your-project.zip
├── routine/
│   └── index.js        ← Dynamic code (bundled JS)
└── assets/
    ├── image.png
    └── ...             ← Static resources, maintaining original structure
```

#### Key Details

- `index.js` content source: By default, produced by prodBuild (esbuild) bundling the entry file; if `--no-bundle` is passed, reads source file directly
- Paths under `assets/` are relative to `assets.directory` in configuration, recursively traversing all subdirectories and files
- Zip package is converted to Buffer via `zip.toBuffer()` and uploaded to OSS (first get OSS temporary credentials via API, then POST upload), with max 3 retries
- Project type determination logic is in `checkEdgeRoutineType`, based on whether entry file and assets directory actually exist
- Configuration source priority: CLI args > `esa.jsonc` / `esa.toml` config file

### Python SDK Example

```python
import os
import zipfile
import io
import time
import json
import requests


def deploy_folder(name: str, folder_path: str, description: str = ""):
    """Deploy static directory to ESA Pages"""
    client = create_client()

    # 1. Create routine
    try:
        client.create_routine(
            esa_models.CreateRoutineRequest(name=name, description=description)
        )
    except Exception as e:
        if "RoutineNameAlreadyExist" not in str(e):
            raise

    # 2. Create assets code version
    # Note: This API needs to be called via callApi method
    from alibabacloud_tea_openapi import models as api_models
    params = api_models.Params(
        action="CreateRoutineWithAssetsCodeVersion",
        version="2024-09-10", protocol="https", method="POST",
        auth_type="AK", body_type="json", req_body_type="json",
        style="RPC", pathname="/",
    )
    body = {"Name": name, "CodeDescription": description}
    request = api_models.OpenApiRequest(body=body)
    runtime = {}
    result = client._client.call_api(params, request, runtime)
    oss_config = result.get("body", {}).get("OssPostConfig", {})
    code_version = result.get("body", {}).get("CodeVersion")

    # 3. Package and upload zip
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, folder_path).replace(os.sep, "/")
                zf.write(full, f"assets/{rel}")
    buf.seek(0)

    form_data = {
        "OSSAccessKeyId": oss_config["OSSAccessKeyId"],
        "Signature": oss_config["Signature"],
        "policy": oss_config["Policy"],
        "key": oss_config["Key"],
    }
    if oss_config.get("XOssSecurityToken"):
        form_data["x-oss-security-token"] = oss_config["XOssSecurityToken"]
    requests.post(oss_config["Url"], data=form_data, files={"file": buf.getvalue()})

    # 4. Wait for version ready
    for _ in range(300):
        info = client._client.call_api(
            api_models.Params(
                action="GetRoutineCodeVersionInfo", version="2024-09-10",
                protocol="https", method="GET", auth_type="AK",
                body_type="json", req_body_type="json", style="RPC", pathname="/",
            ),
            api_models.OpenApiRequest(query={"Name": name, "CodeVersion": code_version}),
            {},
        )
        status = info.get("body", {}).get("Status", "").lower()
        if status == "available":
            break
        if status not in ("", "init"):
            raise RuntimeError(f"Build failed: {status}")
        time.sleep(1)

    # 5-6. Deploy
    for env in ["staging", "production"]:
        client._client.call_api(
            api_models.Params(
                action="CreateRoutineCodeDeployment", version="2024-09-10",
                protocol="https", method="POST", auth_type="AK",
                body_type="json", req_body_type="json", style="RPC", pathname="/",
            ),
            api_models.OpenApiRequest(query={
                "Name": name, "Env": env, "Strategy": "percentage",
                "CodeVersions": json.dumps([{"Percentage": 100, "CodeVersion": code_version}]),
            }),
            {},
        )

    # 7. Get access URL
    routine = client.get_routine(esa_models.GetRoutineRequest(name=name))
    domain = routine.body.default_related_record
    return f"https://{domain}" if domain else None
```

## Common Use Cases

### 1. Deploy Single HTML Page

Suitable for quick prototypes, games, demo pages:

```python
url = deploy_html("game-2048", "<html><body>...</body></html>")
print(f"Access URL: {url}")
```

### 2. Deploy Frontend Build Output

Suitable for React/Vue/Angular frontend projects' dist/build directories:

```python
url = deploy_folder("my-app", "/path/to/dist")
print(f"Access URL: {url}")
```

## Bind Custom Domain (CNAME-Access Sites)

After deploying to Pages, the routine gets a default domain like `{name}.{hash}.er.aliyun-esa.net`. To use a custom domain (e.g. `agent.example.com`) on a **CNAME-access** ESA site, follow this flow:

### Flow

```
1. CreateRecord(A/AAAA, proxied=true)     → Register domain in ESA CDN, get record_cname
2. CreateRoutineRoute(rule expression)     → Route matching traffic to Edge Routine
3. External DNS: CNAME → record_cname      → Point domain to ESA CDN
4. ApplyCertificate(lets_encrypt)          → Provision SSL certificate
5. Wait for certificate status → OK        → HTTPS ready
```

### Step-by-Step

#### 1. Create ESA DNS Record

Create an A/AAAA record with proxy enabled so ESA CDN accepts traffic for this domain:

```python
data_obj = esa_models.CreateRecordRequestData(value="<any-origin-ip>")
req = esa_models.CreateRecordRequest(
    site_id=SITE_ID,
    record_name="agent.example.com",  # Must be full domain name
    type="A/AAAA",
    data=data_obj,
    ttl=1,
    proxied=True,
    biz_name="web",
)
resp = client.create_record_with_options(req, runtime)
# resp.body.record_id → save for reference
```

After creation, list records to get the `record_cname` (e.g. `agent.example.com.a1.initaf.com`):

```python
records = client.list_records(esa_models.ListRecordsRequest(site_id=SITE_ID))
for r in records.body.records:
    print(f"{r.record_name} → CNAME: {r.record_cname}")
```

#### 2. Create Edge Routine Route

Create a route that intercepts traffic for this domain and forwards it to the Edge Routine:

```python
req = esa_models.CreateRoutineRouteRequest(
    site_id=SITE_ID,
    rule='(http.host eq "agent.example.com")',  # ESA rule expression
    routine_name="my-routine",
    route_name="agent-route",
    route_enable="on",
    bypass="off",
)
resp = client.create_routine_route(req)
# resp.body.config_id → save for reference
```

**Important**: The parameter is `rule` (ESA rule expression), NOT `route`. Use `(http.host eq "domain")` syntax.

#### 3. Update External DNS

At your DNS provider (e.g. Alibaba Cloud DNS / alidns), add a CNAME record:

```
agent  CNAME  agent.example.com.a1.initaf.com
```

The CNAME target follows the pattern: `{record_name}.{cname_zone}` — get the exact value from `record_cname` in step 1.

If a wildcard A record (`* → some-ip`) exists, add an explicit CNAME record for the subdomain to override it.

```python
# Example using alidns SDK
from alibabacloud_alidns20150109.client import Client as DnsClient
from alibabacloud_alidns20150109 import models as dns_models

dns_client = DnsClient(config)
dns_client.add_domain_record(dns_models.AddDomainRecordRequest(
    domain_name="example.com",
    rr="agent",
    type="CNAME",
    value="agent.example.com.a1.initaf.com",
))
```

#### 4. Apply SSL Certificate

ESA does **not** auto-provision SSL certificates for new records. You must request one:

```python
resp = client.apply_certificate(esa_models.ApplyCertificateRequest(
    site_id=SITE_ID,
    domains="agent.example.com",
    type="lets_encrypt",
))
```

Certificate provisioning takes 1-5 minutes. Check status:

```python
certs = client.list_certificates(esa_models.ListCertificatesRequest(site_id=SITE_ID))
for c in certs.body.result:
    print(f"{c.common_name} status={c.status}")
# status: Applying → OK
```

**During provisioning, HTTPS returns TLS internal error. HTTP works immediately.**

### Key Gotchas

1. **Do NOT use `CreateRoutineRelatedRecord` for CNAME-access sites** — it creates an internal binding but does NOT create a visible DNS record in ESA, so CDN cannot match the domain and falls back to origin.
2. **You need BOTH an ESA DNS record AND a Route** — the DNS record makes CDN accept traffic; the Route redirects it to the Edge Routine instead of origin.
3. **`CreateRoutineRoute` uses `rule` parameter** (ESA rule expression like `(http.host eq "domain")`), not `route`. The SDK model parameter is `rule`, not `route`.
4. **SSL certificate must be manually applied** — unlike some CDN services, ESA does not auto-provision certs for new DNS records.
5. **DNS record conflicts** — if you create both a regular DNS record and a related record for the same domain, you get `DependedByOthers` error. Delete one before creating the other.
6. **Route propagation delay** — routes may take 3-5 minutes to propagate to all edge nodes. During this time, traffic still goes to origin. HTTP verification may show `Server: ESA` before HTTPS works.

### Complete Example

```python
def bind_custom_domain(client, site_id, routine_name, domain, route_name):
    """Bind a custom domain to an ESA Pages/ER routine (CNAME-access site)"""
    from alibabacloud_tea_util import models as util_models
    runtime = util_models.RuntimeOptions()

    # 1. Create ESA DNS record
    data_obj = esa_models.CreateRecordRequestData(value="127.0.0.1")
    client.create_record_with_options(
        esa_models.CreateRecordRequest(
            site_id=site_id, record_name=domain,
            type="A/AAAA", data=data_obj, ttl=1,
            proxied=True, biz_name="web",
        ), runtime,
    )

    # 2. Create route
    client.create_routine_route(esa_models.CreateRoutineRouteRequest(
        site_id=site_id,
        rule=f'(http.host eq "{domain}")',
        routine_name=routine_name,
        route_name=route_name,
        route_enable="on", bypass="off",
    ))

    # 3. Apply SSL certificate
    client.apply_certificate(esa_models.ApplyCertificateRequest(
        site_id=site_id, domains=domain, type="lets_encrypt",
    ))

    # 4. Get CNAME target for external DNS
    records = client.list_records(esa_models.ListRecordsRequest(
        site_id=site_id, record_name=domain.split(".")[0],
    ))
    for r in (records.body.records or []):
        if r.record_name == domain:
            return r.record_cname  # → set this as CNAME in external DNS
```

## Notes

1. **Function name rules**: Only lowercase letters, numbers, hyphens; must start with lowercase letter; length >= 2
2. **Same name function**: If function exists, reuses existing function and deploys new version code
3. **Deployment environments**: Deploys to both staging and production by default
4. **Access URL**: After successful deployment, get default access domain via `defaultRelatedRecord` from `GetRoutine`
5. **Static directory deployment**: Directory cannot be empty; files in zip are placed under `assets/` prefix
6. **HTML escaping**: When wrapping as ER code, escape backticks and `$` symbols
7. **Assets deployment**: `CreateRoutineWithAssetsCodeVersion` and `CreateRoutineCodeDeployment` need to be called via `callApi` method (not directly wrapped by SDK)
8. **callApi runtime parameter**: Must pass `util_models.RuntimeOptions()` object, NOT an empty dict `{}`. Using `{}` causes `AttributeError: 'dict' object has no attribute 'key'`