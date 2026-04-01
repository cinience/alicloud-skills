# ECS OpenAPI endpoints

ECS uses RPC-style OpenAPI. Prefer SDK or OpenAPI Explorer to avoid manual signing.

## Public endpoint pattern

- Regional endpoint: `ecs.<region-id>.aliyuncs.com`
- Example (China East 1): `ecs.cn-hangzhou.aliyuncs.com`

## VPC endpoint pattern

- VPC endpoint: `ecs-vpc.<region-id>.aliyuncs.com`

## Notes

- The API version for ECS is `2014-05-26`.
- Always use the endpoint matching your instance region.

## References

- Endpoint list and usage: https://www.alibabacloud.com/help/en/ecs/developer-reference/endpoints
