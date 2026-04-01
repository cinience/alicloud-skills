# ECS security groups

## Common operations

- Create/delete/modify: `CreateSecurityGroup`, `DeleteSecurityGroup`, `ModifySecurityGroupPolicy`
- Rules: `AuthorizeSecurityGroup`, `RevokeSecurityGroup`, `DescribeSecurityGroupAttribute`
- Query: `DescribeSecurityGroups`

## Rule notes

- Smaller `Priority` means higher priority.
- If a rule already exists, the API still returns success.
- A single ENI supports up to 1000 security group rules.

## References

- CreateSecurityGroup: `https://www.alibabacloud.com/help/en/ecs/developer-reference/createsecuritygroup`
- AuthorizeSecurityGroup: `https://www.alibabacloud.com/help/en/ecs/developer-reference/authorizesecuritygroup`
