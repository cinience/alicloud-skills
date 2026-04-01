# DescribeInstances (ECS)

Use this API to query ECS instances and inventory.

## Key fields

- `TotalCount`: total instances for the current query scope
- `Instances.Instance[]`: instance list

## Common filters

- `VpcId`, `VSwitchId`, `ZoneId`
- `SecurityGroupId`
- `InstanceIds` (JSON array string)

## Pagination

- `PageNumber` + `PageSize`
- Or `NextToken` + `MaxResults` for token-based pagination when available

## Permissions check

- If the RAM user/role lacks permissions, the API returns an empty list.
- `DryRun=True` validates permissions without executing the request.

## References

- https://www.alibabacloud.com/help/en/ecs/developer-reference/describeinstances
