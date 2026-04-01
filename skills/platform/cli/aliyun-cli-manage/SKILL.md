---
name: aliyun-cli-manage
description: Use when users need command-line operations on Alibaba Cloud resources (list/query/create/update/delete), credential/profile setup, region/endpoint selection, or API discovery from CLI.
version: 1.0.0
---

Category: tool

# Alibaba Cloud Generic CLI (aliyun) Skill

## Validation

```bash
mkdir -p output/aliyun-cli-manage
python skills/platform/cli/aliyun-cli-manage/scripts/ensure_aliyun_cli.py --help > output/aliyun-cli-manage/validate-help.txt
```

Pass criteria: command exits 0 and `output/aliyun-cli-manage/validate-help.txt` is generated.

## Output And Evidence

- Save CLI version checks, API outputs, and error logs under `output/aliyun-cli-manage/`.
- For each mutating action, keep request parameters and result summaries.

## Goals

- Use official `aliyun` CLI to execute Alibaba Cloud OpenAPI operations.
- Provide a standard flow for install, configuration, API discovery, execution, and troubleshooting.

## Quick Flow

1. Run the version guard script first (check first, then decide whether to upgrade).
2. If not installed or check interval reached, the script downloads and installs the latest official package.
3. Configure credentials and default region (recommend `default` profile).
4. Use `aliyun <product> --help` / `aliyun <product> <ApiName> --help` to confirm parameters.
5. Run read-only queries first, then mutating operations.

## Version Guard (Practical)

Prefer the bundled script to avoid unnecessary downloads on every run:

```bash
python skills/platform/cli/aliyun-cli-manage/scripts/ensure_aliyun_cli.py
```

Default behavior:

- Check interval: 24 hours (configurable via environment variable).
- Within interval and version is sufficient: skip download.
- Exceeded interval / not installed / below minimum version: auto-download and install latest official package.

Optional controls (environment variables):

- `ALIYUN_CLI_CHECK_INTERVAL_HOURS=24`：check interval.
- `ALIYUN_CLI_FORCE_UPDATE=1`：force update (ignore interval).
- `ALIYUN_CLI_MIN_VERSION=3.2.9`：minimum acceptable version.
- `ALIYUN_CLI_INSTALL_DIR=~/.local/bin`：installation directory.

Manual parameter examples:

```bash
python skills/platform/cli/aliyun-cli-manage/scripts/ensure_aliyun_cli.py \
  --interval-hours 24 \
  --min-version 3.2.9
```

## Install (Linux example)

```bash
curl -fsSL https://aliyuncli.alicdn.com/aliyun-cli-linux-latest-amd64.tgz -o /tmp/aliyun-cli.tgz
mkdir -p ~/.local/bin
tar -xzf /tmp/aliyun-cli.tgz -C /tmp
mv /tmp/aliyun ~/.local/bin/aliyun
chmod +x ~/.local/bin/aliyun
~/.local/bin/aliyun version
```

## Configure Credentials

```bash
aliyun configure set \
  --profile default \
  --mode AK \
  --access-key-id <AK> \
  --access-key-secret <SK> \
  --region cn-hangzhou
```

View configured profiles:

```bash
aliyun configure list
```

## Command structure

- Generic form:`aliyun <product> <ApiName> --Param1 value1 --Param2 value2`
- REST form:`aliyun <product> [GET|POST|PUT|DELETE] <PathPattern> --body '...json...'`

## API Discovery and Parameter Validation

```bash
aliyun help
aliyun ecs --help
aliyun ecs DescribeRegions --help
```

## Common Read-Only Examples

```bash
# ECS: list regions
aliyun ecs DescribeRegions

# ECS: list instances by region
aliyun ecs DescribeInstances --RegionId cn-hangzhou

# SLS: list projects by endpoint
aliyun sls ListProject --endpoint cn-hangzhou.log.aliyuncs.com --size 100
```

## Common Issues

- `InvalidAccessKeyId.NotFound` / `SignatureDoesNotMatch`：check AK/SK and profile.
- `MissingRegionId`：add `--region` or configure default region in profile.
- for SLS endpoint errors, explicitly pass `--endpoint <region>.log.aliyuncs.com`.

## Execution Recommendations

- Run `ensure_aliyun_cli.py` before starting tasks.
- If resource scope is unclear, query first then mutate.
- Before delete/overwrite operations, output the target resource list first.
- For batch operations, validate one item in a small scope first.

## References

- Official source list:`references/sources.md`

## Prerequisites

- Configure least-privilege Alibaba Cloud credentials before execution.
- Prefer environment variables: `ALICLOUD_ACCESS_KEY_ID`, `ALICLOUD_ACCESS_KEY_SECRET`, optional `ALICLOUD_REGION_ID`.
- If region is unclear, ask the user before running mutating operations.

## Workflow

1) Confirm user intent, region, identifiers, and whether the operation is read-only or mutating.
2) Run one minimal read-only query first to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.

