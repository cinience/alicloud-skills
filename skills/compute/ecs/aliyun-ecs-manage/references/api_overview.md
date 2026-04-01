# ECS OpenAPI overview (2014-05-26)

Use the official API overview to locate exact operation names and required parameters.
Keep this file as a quick index for common workflows; always verify details in the docs.

## Regions and resource discovery

- Regions/Zones/Capacity: `DescribeRegions`, `DescribeZones`, `DescribeAvailableResource`
- Quotas/limits: `DescribeAccountAttributes`
- Instance type changes: `DescribeResourcesModification`, `DescribeRecommendInstanceType`

## Pricing and renewal

- Price and renewal: `DescribePrice`, `DescribeRenewalPrice`, `DescribeInstanceModificationPrice`

## Instances (lifecycle and config)

- Create: `RunInstances`, `CreateInstance`
- Start/Stop/Reboot: `StartInstance(s)`, `StopInstance(s)`, `RebootInstance(s)`
- Delete: `DeleteInstance(s)`
- Query: `DescribeInstances`, `DescribeInstanceStatus`, `DescribeInstanceAttribute`
- Modify: `ModifyInstanceAttribute`, `ModifyInstanceSpec`, `ModifyPrepayInstanceSpec`
- Network/metadata: `ModifyInstanceNetworkOptions`, `ModifyInstanceMetadataOptions`
- RAM role: `AttachInstanceRamRole`, `DescribeInstanceRamRole`, `DetachInstanceRamRole`
- User data: `DescribeUserData`
- Auto renew: `DescribeInstanceAutoRenewAttribute`, `ModifyInstanceAutoRenewAttribute`
- Spot: `DescribeSpotPriceHistory`, `DescribeSpotAdvice`

## Images

- Create/delete/modify: `CreateImage`, `DeleteImage`, `ModifyImageAttribute`
- Query: `DescribeImages`, `DescribeImageFromFamily`, `DescribeImageSupportInstanceTypes`
- Share: `DescribeImageSharePermission`, `ModifyImageSharePermission`
- Import/export/copy: `ImportImage`, `ExportImage`, `CopyImage`, `CancelCopyImage`

## Disks (EBS)

- Create/attach/detach: `CreateDisk`, `AttachDisk`, `DetachDisk`
- Resize/modify: `ResizeDisk`, `ModifyDiskAttribute`, `ModifyDiskSpec`, `ModifyDiskChargeType`
- Replace/rollback: `ReplaceSystemDisk`, `ResetDisk`, `ReInitDisk`
- Query/delete: `DescribeDisks`, `DeleteDisk`

## Snapshots

- Create/copy/delete: `CreateSnapshot`, `CopySnapshot`, `DeleteSnapshot`
- Query/modify: `DescribeSnapshots`, `ModifySnapshotAttribute`
- Snapshot policy: `CreateAutoSnapshotPolicy`, `ApplyAutoSnapshotPolicy`, `CancelAutoSnapshotPolicy`, `DescribeAutoSnapshotPolicyEx`

## Security groups

- Create/delete/modify: `CreateSecurityGroup`, `DeleteSecurityGroup`, `ModifySecurityGroupPolicy`
- Rules: `AuthorizeSecurityGroup`, `RevokeSecurityGroup`, `DescribeSecurityGroupAttribute`
- Query: `DescribeSecurityGroups`

## Network interfaces (ENI)

- Create/delete: `CreateNetworkInterface`, `DeleteNetworkInterface`
- Attach/detach: `AttachNetworkInterface`, `DetachNetworkInterface`
- Query/modify: `DescribeNetworkInterfaces`, `ModifyNetworkInterfaceAttribute`

## Key pairs

- Create/import/delete: `CreateKeyPair`, `ImportKeyPair`, `DeleteKeyPairs`
- Query: `DescribeKeyPairs`

## Tags

- Tagging: `TagResources`, `UntagResources`, `ListTagResources`

## Cloud Assistant (commands)

- Run commands: `RunCommand`
- Query results: `DescribeInvocations`, `DescribeInvocationResults`
- Install agent: `InstallCloudAssistant`, check status with `DescribeCloudAssistantStatus`

## System events and monitoring

- Status/events: `DescribeInstancesFullStatus`, `DescribeInstanceHistoryEvents`, `DescribeDisksFullStatus`
- Monitoring: `DescribeInstanceMonitorData`, `DescribeDiskMonitorData`, `DescribeEniMonitorData`, `DescribeSnapshotMonitorData`

## References

- Official operation list: https://www.alibabacloud.com/help/en/ecs/developer-reference/api-ecs-2014-05-26-overview
