# Task Templates

## 1) List pipeline inventory (read-only)

Goal: list all pipelines and capture IDs for later operations.

Suggested API path:

- `QueryPipelineList`
- Optional exact lookup: `SearchPipeline`

Evidence to save:

- request parameters
- response summary
- pipeline IDs and states

## 2) Validate template setup (read-only)

Goal: verify available transcode/watermark templates before submitting jobs.

Suggested API path:

- `QueryTemplateList`
- `QueryWaterMarkTemplateList`

Evidence to save:

- template IDs and names
- template state/status

## 3) Submit and track a processing job

Goal: submit one bounded processing job and observe status transitions.

Suggested API path:

- `SubmitJobs`
- `QueryJobList` or `ListJob`
- optional cancel path: `CancelJob`

Evidence to save:

- pipeline/template IDs used
- input/output location
- job ID and final status

## 4) Submit snapshot extraction

Goal: generate snapshots from target media and verify completion.

Suggested API path:

- `SubmitSnapshotJob`
- `QuerySnapshotJobList`

Evidence to save:

- snapshot configuration
- job IDs
- completion result
