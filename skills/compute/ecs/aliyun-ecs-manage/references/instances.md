# ECS instances

Use these APIs for instance lifecycle, configuration, and queries.

## Common operations

- Create: `RunInstances`, `CreateInstance`
- Start/Stop/Reboot: `StartInstance(s)`, `StopInstance(s)`, `RebootInstance(s)`
- Delete: `DeleteInstance(s)`
- Query: `DescribeInstances`, `DescribeInstanceStatus`, `DescribeInstanceAttribute`
- Modify: `ModifyInstanceSpec`, `ModifyInstanceAttribute`

## Behavioral notes

- Instance lifecycle operations are asynchronous; use `DescribeInstanceStatus` to verify state transitions.
- Stop behavior depends on billing; pay-as-you-go supports stop charging or keep charging.

## References

- API overview: `https://www.alibabacloud.com/help/en/ecs/developer-reference/api-ecs-2014-05-26-overview`
- StopInstance: `https://www.alibabacloud.com/help/en/ecs/developer-reference/stopinstance`
- StartInstance: `https://www.alibabacloud.com/help/en/ecs/developer-reference/startinstance`
- DescribeInstances: `https://www.alibabacloud.com/help/en/ecs/developer-reference/describeinstances`
