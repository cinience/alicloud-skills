# ECS key pairs

## Common operations

- Create/import/delete: `CreateKeyPair`, `ImportKeyPair`, `DeleteKeyPairs`
- Query: `DescribeKeyPairs`

## Notes

- `CreateKeyPair` returns the private key only once; store it securely.
- Maximum number of key pairs per region is limited by quota.

## References

- CreateKeyPair: `https://www.alibabacloud.com/help/en/ecs/developer-reference/createkeypair`
