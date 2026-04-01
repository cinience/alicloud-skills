# DevOps API Quick Map (2021-06-25)

Source: `https://api.aliyun.com/meta/v1/products/devops/versions/2021-06-25/api-docs.json`

## Project And Membership

- `CreateProject`
- `GetProject`
- `UpdateProject`
- `GetProjectMembers`
- `AddGroupMember`

## Repository And Code Flow

- `CreateRepository`
- `GetRepository`
- `ListRepositories`
- `CreateBranch`
- `CreateTag`
- `CreateMergeRequest`
- `CloseMergeRequest`

## Pipeline And Release

- `CreatePipeline`
- `GetPipeline`
- `ListPipelines`
- `RunPipeline`
- `StopPipeline`
- `CreatePipelineGroup`

## Work Items And Test

- `CreateWorkitem`
- `GetWorkitemDetail`
- `UpdateWorkitem`
- `CreateWorkitemComment`
- `ListTestCase`
- `CreateTestCase`

## Notes

- Use the metadata list script to confirm latest API names and request fields before execution.
- Prefer read-only APIs for baseline discovery.
