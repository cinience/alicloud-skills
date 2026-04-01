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

## Notes

1. **Function name rules**: Only lowercase letters, numbers, hyphens; must start with lowercase letter; length >= 2
2. **Same name function**: If function exists, reuses existing function and deploys new version code
3. **Deployment environments**: Deploys to both staging and production by default
4. **Access URL**: After successful deployment, get default access domain via `defaultRelatedRecord` from `GetRoutine`
5. **Static directory deployment**: Directory cannot be empty; files in zip are placed under `assets/` prefix
6. **HTML escaping**: When wrapping as ER code, escape backticks and `$` symbols
7. **Assets deployment**: `CreateRoutineWithAssetsCodeVersion` and `CreateRoutineCodeDeployment` need to be called via `callApi` method (not directly wrapped by SDK)