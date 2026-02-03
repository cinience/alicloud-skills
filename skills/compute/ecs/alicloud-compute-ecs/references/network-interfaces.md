# ECS network interfaces (ENI)

## Common operations

- Create/delete: `CreateNetworkInterface`, `DeleteNetworkInterface`
- Attach/detach: `AttachNetworkInterface`, `DetachNetworkInterface`
- Query/modify: `DescribeNetworkInterfaces`, `ModifyNetworkInterfaceAttribute`

## Notes

- ENI and instance must be in the same VPC and zone.
- An ENI can be attached to only one instance at a time.
- A single ENI supports up to 49 secondary private IPs.

## References

- CreateNetworkInterface: `https://www.alibabacloud.com/help/en/ecs/developer-reference/createnetworkinterface`
