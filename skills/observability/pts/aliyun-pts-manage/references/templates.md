# PTS Operation Templates

Use these templates as planning checklists before running PTS APIs. Replace placeholders with real values.

## 1) Read-only inventory template

- Goal: List current scenes and pick one target scene.
- Inputs:
  - region: `<region-id>`
  - filters: `<keyword / page size / scene type>`
- Recommended APIs:
  - `ListPtsScene`
  - `ListOpenJMeterScenes`
  - `GetPtsScene` (for one selected scene)
- Evidence to save:
  - request summary (region + filters)
  - response summary (scene count + selected scene id)
  - raw API output path in `output/aliyun-pts-manage/`

## 2) Start a test template

- Goal: Start one bounded test run.
- Inputs:
  - region: `<region-id>`
  - scene id: `<scene-id>`
  - run constraints: `<duration / concurrency / speed>`
- Recommended APIs:
  - `GetPtsScene` (pre-check)
  - `StartPtsScene` or `StartTestingJMeterScene`
  - `GetPtsSceneRunningStatus` / `GetJMeterSceneRunningData` (poll)
- Safety checklist:
  - Confirm change window.
  - Confirm stop condition and owner.
  - Confirm rollback: `StopPtsScene` or `StopTestingJMeterScene`.

## 3) Stop and verify template

- Goal: Stop an ongoing run and verify final state.
- Inputs:
  - region: `<region-id>`
  - scene id / report id: `<id>`
- Recommended APIs:
  - `StopPtsScene` or `StopTestingJMeterScene`
  - `GetPtsSceneRunningStatus`
  - `ListPtsReports` / `GetPtsReportDetails`
- Evidence to save:
  - stop request timestamp
  - final status
  - report link/id and key metrics summary

## 4) Baseline update template

- Goal: Update baseline from a stable report.
- Inputs:
  - scene id: `<scene-id>`
  - report id: `<report-id>`
  - baseline policy note: `<why this report is selected>`
- Recommended APIs:
  - `GetPtsReportDetails`
  - `CreatePtsSceneBaseLineFromReport` or `UpdatePtsSceneBaseLine`
  - `GetPtsSceneBaseLine` (post-check)

## 5) Failure triage template

- Common checks:
  - Invalid scene/config: call `GetPtsScene` and validate required fields.
  - Environment mismatch: validate `ListEnvs` and VPC related APIs.
  - Runtime issues: inspect `GetPtsDebugSampleLogs`, `GetJMeterSamplingLogs`, `GetJMeterLogs`.
- Required failure record:
  - exact API name
  - error code and message
  - request id and timestamp
  - retry decision (yes/no) and reason
