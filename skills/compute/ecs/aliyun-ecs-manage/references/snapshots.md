# ECS snapshots

## Common operations

- Create/copy/delete: `CreateSnapshot`, `CopySnapshot`, `DeleteSnapshot`
- Query/modify: `DescribeSnapshots`, `ModifySnapshotAttribute`
- Policy: `CreateAutoSnapshotPolicy`, `ApplyAutoSnapshotPolicy`, `CancelAutoSnapshotPolicy`, `DescribeAutoSnapshotPolicyEx`

## Notes

- A disk must have been attached to an instance before you can create a snapshot.
- The disk must be in `In_use` or `Available` state.
- Snapshot creation is asynchronous; use `DescribeSnapshots` to check status.

## References

- CreateSnapshot: `https://www.alibabacloud.com/help/en/ecs/developer-reference/createsnapshot`
- DescribeSnapshots: `https://www.alibabacloud.com/help/en/ecs/developer-reference/describesnapshots`
