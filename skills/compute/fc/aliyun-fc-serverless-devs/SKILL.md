---
name: aliyun-fc-serverless-devs
description: Alibaba Cloud Function Compute (FC 3.0) skill for installing and using Serverless Devs to create, deploy, invoke, and remove a Python function. Use when users need CLI-based FC quick start or Serverless Devs setup guidance.
version: 1.0.0
---

Category: tool

# Function Compute (FC 3.0) Serverless Devs

## Goals

- Install and validate Serverless Devs.
- Configure credentials, initialize example project, deploy, invoke, and remove.
- Provide CLI flow with Python runtime example.

## Quick Start Flow

1. Install Node.js (14+) and npm.
2. Install and validate Serverless Devs.
3. Configure credentials via guided setup.
4. Initialize example project and enter directory.
5. Deploy, invoke, and optionally remove.

## Install Serverless Devs (npm)

Global install (requires sudo):

```bash
sudo npm install @serverless-devs/s -g
sudo s -v
```

No-sudo alternative (recommended in restricted environments):

```bash
npx -y @serverless-devs/s -v
```

## Configure Credentials (guided)

```bash
sudo s config add
```

Choose `Alibaba Cloud (alibaba)`, provide `AccountID`, `AccessKeyID`, `AccessKeySecret`, and set alias.

## Configure Credentials (command)

Use CLI args to configure credential alias in one command (non-interactive):

```bash
s config add -a default --AccessKeyID <AK> --AccessKeySecret <SK> -f
```

If using environment variables, inject them into the command (example):

```bash
s config add -a default -kl AccessKeyID,AccessKeySecret -il ${ALIBABA_CLOUD_ACCESS_KEY_ID},${ALIBABA_CLOUD_ACCESS_KEY_SECRET} -f
```

Or use Serverless Devs convention JSON environment variable (example):

```bash
export default_serverless_devs_key='{\"AccountID\":\"<AccountID>\",\"AccessKeyID\":\"<AK>\",\"AccessKeySecret\":\"<SK>\"}'
```

Reference in `s.yaml`:

```yaml
access: default_serverless_devs_key
```

## Initialize Example (Python)

```bash
sudo s init start-fc3-python
cd start-fc3-python
```

Initialization creates `s.yaml`, `code/`, and `readme.md`; edit `code/index.py` for function logic.

## Deploy, Invoke, and Remove

```bash
sudo s deploy
sudo s invoke -e "test"
sudo s remove
```

## Custom Domain Binding (Avoid Default Domain Forced Download)

> Note: FC default domain adds `Content-Disposition: attachment`, causing browser downloads.
> Use a custom domain to avoid this behavior.

### Step 1: Configure CNAME for your domain

Configure DNS CNAME to FC public CNAME:

```
<account_id>.<region_id>.fc.aliyuncs.com
```

Example (Hangzhou region):

```
1629965279769872.cn-hangzhou.fc.aliyuncs.com
```

Note: if using apex domain (e.g. `animus.run`) and DNS provider does not support CNAME at apex,
use ALIAS/ANAME records, or switch to a subdomain such as `www.animus.run`.

### Step 2: Create custom domain in Serverless Devs

Option A: add `fc3-domain` resource in `s.yaml`:

```yaml
resources:
  newsDomain:
    component: fc3-domain
    props:
      region: cn-hangzhou
      domainName: animus.run
      protocol: HTTP
      routeConfig:
        routes:
          - functionName: honnold-taipei101-news
            qualifier: LATEST
            methods:
              - GET
              - HEAD
            path: /*
```

`region` is example default; ask user when the best region is unclear.

Then deploy:

```bash
printf 'y\n' | npx -y @serverless-devs/s deploy
```

Option B: use Console (Advanced Features > Custom Domains) to create and route custom domain.

### Common Errors

- `DomainNameNotResolved`: domain not resolved to correct FC CNAME.
- `InvalidICPLicense`: mainland China regions require ICP filing associated with Alibaba Cloud.

## References

- See `references/install_serverless_devs_and_docker.md` for detailed official steps.
- HTTP trigger limitations and response header behavior (default domain enforces Content-Disposition: attachment)
  - https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/http-triggers-overview
- Custom domain binding and CNAME guidance
  - https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names

- Official source list:`references/sources.md`

## Validation

```bash
mkdir -p output/aliyun-fc-serverless-devs
echo "validation_placeholder" > output/aliyun-fc-serverless-devs/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-fc-serverless-devs/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-fc-serverless-devs/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Prerequisites

- Configure least-privilege Alibaba Cloud credentials before execution.
- Prefer environment variables: `ALICLOUD_ACCESS_KEY_ID`, `ALICLOUD_ACCESS_KEY_SECRET`, optional `ALICLOUD_REGION_ID`.
- If region is unclear, ask the user before running mutating operations.

## Workflow

1) Confirm user intent, region, identifiers, and whether the operation is read-only or mutating.
2) Run one minimal read-only query first to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.

