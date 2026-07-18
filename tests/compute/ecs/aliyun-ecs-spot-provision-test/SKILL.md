---
name: aliyun-ecs-spot-provision-test
description: Use when smoke-testing the spot ECS provisioning skill without creating cloud resources by validating syntax, safety gates, and a read-only regional plan.
---

# Spot ECS Provisioning Smoke Test

## Prerequisites

- Install Alibaba Cloud CLI v3.
- Configure least-privilege credentials for read-only ECS discovery and pricing.
- Target skill: `skills/compute/ecs/aliyun-ecs-spot-provision/`.

## Test Steps

1. Compile `scripts/provision_spot_ecs.py` with `python3 -m py_compile`.
2. Run `--help` and confirm `plan`, `apply`, and `--confirm-create` are documented.
3. Run `apply` without `--confirm-create`; require a non-zero exit before any API call.
4. Run `plan` for one region and small exact CPU/memory request. Save evidence beneath `output/aliyun-ecs-spot-provision-test/`.
5. Confirm `plan.json` contains a region, zone, instance type, image ID, disk category, available offers, currency, and current hourly trade price.
6. Do not run `apply` in the smoke test.

## Expected Results

- Syntax and skill validation pass.
- The mutation safety gate fails closed.
- Read-only capacity, image, disk, and price APIs return a reproducible plan.
- No VPC, vSwitch, security group, key pair, disk, or ECS instance is created.
