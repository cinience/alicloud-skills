# ICE Task Templates

Use these templates after confirming region and OSS input/output locations.

## 1) Create a media workflow

- API: `CreateMediaWorkflow`
- Required params template:
  - `Name`: `<workflow-name>`
  - `Topology`: `<json-topology-definition>`
  - `TriggerMode`: `<OssAutoTrigger|NotInAuto>`

## 2) Submit a media producing job

- API: `SubmitMediaProducingJob`
- Required params template:
  - `WorkflowId`: `<workflow-id>`
  - `InputConfig`: `<json-input-config>`
  - `OutputConfig`: `<json-output-config>`
  - `UserData`: `<optional-biz-context-json>`

## 3) Query producing job result

- API: `GetMediaProducingJob`
- Required params template:
  - `JobId`: `<job-id>`

## 4) Search media in ICE

- API: `SearchMedia`
- Required params template:
  - `Match`: `<query-expression>`
  - `PageNo`: `<1>`
  - `PageSize`: `<20>`

## 5) Query task/runtime diagnostics

- APIs: `GetTaskInfo`, `ListJobs`
- Required params template:
  - `TaskId` (for `GetTaskInfo`): `<task-id>`
  - `JobType` / `Status` / `NextToken` (for `ListJobs`): `<filters>`

## Evidence Checklist

- Save request payloads and API responses under `output/aliyun-ice-manage/`.
- Keep workflow IDs, job IDs, and output object paths in one evidence file.
