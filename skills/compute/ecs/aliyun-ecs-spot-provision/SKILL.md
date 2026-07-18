---
name: aliyun-ecs-spot-provision
description: Plan, price, provision, and verify one Alibaba Cloud ECS spot instance with minimal VPC networking, restricted SSH access, a managed key pair, configurable system-disk size, and optional scheduled release. Use when Codex must buy, launch, or reproduce a complete preemptible/spot ECS workflow rather than only manage an existing instance.
---

# Provision an Alibaba Cloud Spot ECS Instance

Use the bundled CLI wrapper to preserve the fragile ordering and evidence trail of a spot purchase. Keep account-specific IDs, IP addresses, image dates, and prices out of the skill.

## Preconditions

- Require Alibaba Cloud CLI v3 and credentials with least-privilege ECS and VPC permissions.
- Treat `plan` as read-only and run it before every `apply`.
- Obtain an explicit region. Obtain an explicit SSH source CIDR when public SSH is requested.
- Explain that spot capacity and price can change between planning and creation.
- Write all evidence beneath `output/aliyun-ecs-spot-provision/<name>/`.

## Workflow

1. Run `plan` to discover exact CPU/memory matches, select an available zone and instance type, resolve a current Ubuntu image, verify a disk category, and query the current hourly quote.
2. Review `plan.json`. Report compute, disk, and fixed bandwidth prices separately; pay-by-traffic outbound transfer is not an hourly fixed charge.
3. Run `apply --confirm-create` only after the requested region, size, disk, public bandwidth, SSH CIDR, and release behavior are settled.
4. Let the script create or reuse a VPC, vSwitch, security group, and key pair. Never print or commit the private key.
5. Require the `RunInstances` dry run to return `DryRunOperation` before submitting the real request.
6. Verify the returned instance with `DescribeInstances` until it reaches `Running`.
7. Report all created IDs, the private-key path, current quote, verification evidence, and remaining interruption/data-retention risks.

Do not automatically delete partially created infrastructure after an error. Preserve `state.json`, diagnose, and resume with the same command so resource IDs are reused.

## Commands

Read-only plan:

```bash
python3 skills/compute/ecs/aliyun-ecs-spot-provision/scripts/provision_spot_ecs.py plan \
  --name batch-worker \
  --region ap-southeast-8 \
  --cpu 8 \
  --memory-gib 16 \
  --system-disk-size 800 \
  --internet-bandwidth-out 5 \
  --ssh-cidr 203.0.113.10/32
```

Create exactly one instance from the saved plan:

```bash
python3 skills/compute/ecs/aliyun-ecs-spot-provision/scripts/provision_spot_ecs.py apply \
  --name batch-worker \
  --region ap-southeast-8 \
  --cpu 8 \
  --memory-gib 16 \
  --system-disk-size 800 \
  --internet-bandwidth-out 5 \
  --ssh-cidr 203.0.113.10/32 \
  --confirm-create
```

Prefer `--instance-type` and `--zone` when the user chooses an exact offer. Use `--auto-release-time` for a true scheduled release; `--spot-duration 1` is only a one-hour protection period.

## Safety Rules

- Never infer `0.0.0.0/0` for SSH. Require an explicit CIDR for public SSH.
- Default public bandwidth to zero. A public IP is requested only when `--internet-bandwidth-out` is positive.
- Generate a new RSA private key with mode `0600`; fail instead of overwriting an existing key.
- Use automatic spot bidding by default. Use `--spot-price-limit` only when the user supplies a maximum hourly compute price.
- Set the system-disk size during creation. For resizing an existing disk and filesystem, use `aliyun-ecs-manage` instead.
- Warn that a system disk created with the instance is normally released with a reclaimed spot instance.
- Never equate `ExpiredTime=2099...` or `SpotDuration=1` with a scheduled deletion.

## References

Read [references/operations.md](references/operations.md) when diagnosing partial creation, interpreting prices, configuring release behavior, or validating the guest filesystem.
See [references/sources.md](references/sources.md) for the official ECS and VPC documentation checked for this skill.

## Output And Evidence

- Save the resolved request and current quote to `output/aliyun-ecs-spot-provision/<name>/plan.json`.
- Save every CLI response and error stream beside the plan using operation-specific names.
- Save created resource IDs and recovery state to `state.json`; save the final normalized result to `summary.json`.
- Store generated private keys only below the evidence directory's `private/` folder with directory mode `0700` and key mode `0600`.
- Never copy private keys, AccessKeys, or credential files into reports or committed fixtures.

## Validation

```bash
python3 -m py_compile skills/compute/ecs/aliyun-ecs-spot-provision/scripts/provision_spot_ecs.py
python3 skills/compute/ecs/aliyun-ecs-spot-provision/scripts/provision_spot_ecs.py --help
python3 /home/vipas/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/compute/ecs/aliyun-ecs-spot-provision
```
