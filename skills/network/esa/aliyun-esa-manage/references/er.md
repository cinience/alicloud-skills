# Edge Routine (ER) — Edge Function Reference

ESA Edge Routine is a serverless edge function service where code runs on global edge nodes. Supports full lifecycle management: creation, code submission, deployment, route configuration, and record management.

Manage Edge Routine via Python SDK calling ESA OpenAPI.

## API List

### Function Management

| API | Description | Key Parameters |
|-----|-------------|----------------|
| `CreateRoutine` | Create edge function | `Name`(required, lowercase letters/numbers/hyphens, >=2 chars), `Description`(optional) |
| `DeleteRoutine` | Delete edge function | `Name`(required) |
| `GetRoutine` | Get edge function details, including code version list, related records, default access domain | `Name`(required) |
| `GetRoutineUserInfo` | Get user edge function overview info | No parameters |
| `ListUserRoutines` | Paginate all edge functions under account | `PageNumber`, `PageSize` |

### Code Version Management

| API | Description | Key Parameters |
|-----|-------------|----------------|
| `GetRoutineStagingCodeUploadInfo` | Get signature info for code upload to OSS | `Name`(required) |
| `CommitRoutineStagingCode` | Submit staging code, generate formal code version | `Name`(required), `CodeDescription`(optional) |
| `PublishRoutineCodeVersion` | Publish code version to staging/production | `Name`(required), `Env`(required, "staging"/"production"), `CodeVersion`(required) |
| `DeleteRoutineCodeVersion` | Delete code version | `Name`(required), `CodeVersion`(required) |
| `CreateRoutineWithAssetsCodeVersion` | Create code version with assets (for static file deployment) | `Name`(required), `CodeDescription`(optional) |
| `GetRoutineCodeVersionInfo` | Get code version status (init/available/failed) | `Name`(required), `CodeVersion`(required) |
| `CreateRoutineCodeDeployment` | Deploy code version to specified environment by percentage (for assets deployment) | `Name`(required), `Env`(required), `Strategy`(required), `CodeVersions`(required, JSON) |
| `ListRoutineCodeVersions` | Paginate function's code versions | `Name`(required), `PageNumber`, `PageSize` |
| `GetRoutineCodeVersion` | Query single code version details | `Name`(required), `CodeVersion`(required) |

### Route Management

| API | Description | Key Parameters |
|-----|-------------|----------------|
| `CreateRoutineRoute` | Create route | `SiteId`(required), `Route`(path, e.g. `test.example.com/*`), `RoutineName`(required), `RouteName`(required), `RouteEnable`("on"/"off"), `Bypass`("on"/"off") |
| `UpdateRoutineRoute` | Update route configuration | `SiteId`(required), `ConfigId`(required), `RouteName`(required), `RouteEnable`(required), `Rule`(required), `RoutineName`(required), `Bypass`(required) |
| `DeleteRoutineRoute` | Delete route | `SiteId`(required), `ConfigId`(required) |
| `GetRoutineRoute` | Get route details | `SiteId`(required), `ConfigId`(required) |
| `ListRoutineRoutes` | List all routes for a function | `RoutineName`(required), `RouteName`(optional filter), `PageNumber`, `PageSize` |
| `ListSiteRoutes` | List all routes for a site | `SiteId`(required), `RouteName`(optional filter), `PageNumber`, `PageSize` |

### Related Record Management

| API | Description | Key Parameters |
|-----|-------------|----------------|
| `CreateRoutineRelatedRecord` | Create function related record (domain), triggers function execution | `Name`(required), `SiteId`(required), `RecordName`(required) |
| `DeleteRoutineRelatedRecord` | Delete related record | `Name`(required), `SiteId`(required), `RecordName`(required), `RecordId`(optional) |
| `ListRoutineRelatedRecords` | List all related records for a function | `Name`(required), `PageNumber`, `PageSize`, `SearchKeyWord`(optional) |

## Standard Workflow

### Create and Deploy Edge Function (Complete Flow)

```
1. CreateRoutine                           → Create function
2. GetRoutineStagingCodeUploadInfo          → Get upload signature
3. Upload code to OSS (POST with signature) → Code upload
4. CommitRoutineStagingCode                 → Submit code version
5. PublishRoutineCodeVersion(env=staging)   → Deploy to staging
6. PublishRoutineCodeVersion(env=production)→ Deploy to production
7. (Optional) CreateRoutineRoute           → Bind custom domain route
8. (Optional) CreateRoutineRelatedRecord   → Create related record
9. GetRoutine                              → Get details, obtain default access URL
```

### Code Format Requirements

Edge Routine code must export `fetch` handler:

```javascript
async function handleRequest(request) {
  return new Response("Hello World", {
    headers: { "content-type": "text/html;charset=UTF-8" },
  });
}

export default {
  async fetch(request) {
    return handleRequest(request);
  },
};
```

### Route Pattern Explanation

Route's `Rule` field uses ESA rule expression, for example:
- `(http.host eq "test.example.com" and starts_with(http.request.uri.path, "/"))`

Simplified path format (e.g. `test.example.com/*`) needs to be converted to rule expression:
- Domain prefix `*` = `ends_with(http.host, ".example.com")`
- Path suffix `*` = `starts_with(http.request.uri.path, "/")`

## Python SDK Usage

```python
from alibabacloud_esa20240910.client import Client as Esa20240910Client
from alibabacloud_esa20240910 import models as esa_models
from alibabacloud_tea_openapi import models as open_api_models
import requests


def create_client(region_id: str = "cn-hangzhou") -> Esa20240910Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint="esa.cn-hangzhou.aliyuncs.com",
    )
    return Esa20240910Client(config)


# Create edge function
def create_routine(name: str, description: str = ""):
    client = create_client()
    request = esa_models.CreateRoutineRequest(name=name, description=description)
    return client.create_routine(request)


# List edge functions
def list_routines():
    client = create_client()
    resp = client.get_routine_user_info()
    return resp.body


# Get function details
def get_routine(name: str):
    client = create_client()
    request = esa_models.GetRoutineRequest(name=name)
    return client.get_routine(request)


# Delete edge function
def delete_routine(name: str):
    client = create_client()
    request = esa_models.DeleteRoutineRequest(name=name)
    return client.delete_routine_with_options(request)


# Upload code and deploy (complete flow)
def deploy_code(name: str, code: str, env: str = "production"):
    client = create_client()

    # 1. Get upload signature
    upload_info = client.get_routine_staging_code_upload_info(
        esa_models.GetRoutineStagingCodeUploadInfoRequest(name=name)
    )
    oss_config = upload_info.body.oss_post_config

    # 2. Upload code to OSS
    form_data = {
        "OSSAccessKeyId": oss_config.ossaccess_key_id,
        "Signature": oss_config.signature,
        "callback": oss_config.callback,
        "x:codeDescription": oss_config.x_code_description,
        "policy": oss_config.policy,
        "key": oss_config.key,
    }
    requests.post(oss_config.url, data=form_data, files={"file": code.encode()})

    # 3. Submit code version
    commit_resp = client.commit_routine_staging_code(
        esa_models.CommitRoutineStagingCodeRequest(name=name)
    )
    code_version = commit_resp.body.code_version

    # 4. Deploy
    client.publish_routine_code_version(
        esa_models.PublishRoutineCodeVersionRequest(
            name=name, env=env, code_version=code_version
        )
    )
    return code_version
```

### Route Management

```python
# Create route
def create_route(site_id: int, routine_name: str, route_name: str, rule: str):
    client = create_client()
    request = esa_models.CreateRoutineRouteRequest(
        site_id=site_id,
        routine_name=routine_name,
        route_name=route_name,
        rule=rule,
        route_enable="on",
        bypass="off",
    )
    return client.create_routine_route(request)


# List function routes
def list_routine_routes(routine_name: str):
    client = create_client()
    request = esa_models.ListRoutineRoutesRequest(routine_name=routine_name)
    return client.list_routine_routes(request)
```

### Related Record Management

```python
# Create related record
def create_related_record(name: str, site_id: int, record_name: str):
    client = create_client()
    request = esa_models.CreateRoutineRelatedRecordRequest(
        name=name, site_id=site_id, record_name=record_name
    )
    return client.create_routine_related_record(request)
```
