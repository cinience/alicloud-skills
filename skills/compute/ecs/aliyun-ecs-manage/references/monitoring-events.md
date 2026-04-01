# ECS monitoring and events

## Common operations

- Instance status/events: `DescribeInstancesFullStatus`, `DescribeInstanceHistoryEvents`
- Disk status: `DescribeDisksFullStatus`
- Monitoring: `DescribeInstanceMonitorData`, `DescribeDiskMonitorData`, `DescribeEniMonitorData`, `DescribeSnapshotMonitorData`

## Notes

- Use status/events APIs to detect impaired or scheduled maintenance events.

## References

- API overview: `https://www.alibabacloud.com/help/en/ecs/developer-reference/api-ecs-2014-05-26-overview`
