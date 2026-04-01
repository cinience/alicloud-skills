# ECS disks (EBS)

## Common operations

- Create/attach/detach: `CreateDisk`, `AttachDisk`, `DetachDisk`
- Resize/modify: `ResizeDisk`, `ModifyDiskAttribute`, `ModifyDiskSpec`
- Replace/rollback: `ReplaceSystemDisk`, `ResetDisk`, `ReInitDisk`
- Query/delete: `DescribeDisks`, `DeleteDisk`

## Attach/Detach notes

- The disk and instance must be in the same zone.
- The disk must be `Available` when attaching.
- The instance must be `Running` or `Stopped`.
- A system disk can only be attached to its original instance and the instance must be stopped.

## References

- API overview: `https://www.alibabacloud.com/help/en/ecs/developer-reference/api-ecs-2014-05-26-overview`
- AttachDisk: `https://www.alibabacloud.com/help/en/ecs/developer-reference/attachdisk`
