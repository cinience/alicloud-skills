# DevOps Operation Templates

## 1) Read-only inventory template

- Goal: identify projects, repositories, and pipelines in scope.
- Inputs:
  - region: `<region-id>`
  - org/project keyword: `<keyword>`
- Steps:
  1. Run API metadata discovery script.
  2. Pick one read-only API from each category (`Get*`/`List*`).
  3. Save response summaries under `output/aliyun-devops-manage/`.

## 2) Change planning template

- Goal: plan one mutation safely (project/repo/pipeline/work item).
- Inputs:
  - target resource id: `<resource-id>`
  - owner confirmation: `<owner>`
  - rollback action: `<rollback-api-or-step>`
- Steps:
  1. Snapshot current state with read-only APIs.
  2. Execute one mutation with minimal scope.
  3. Validate with a read-only follow-up query.
  4. Record request id, key params, and results.

## 3) Failure triage template

- Required failure record:
  - API name
  - error code and message
  - request id and timestamp
  - retry decision (yes/no) and reason
