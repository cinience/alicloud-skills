---
name: alicloud-storage-oss-ossutil-test
description: Minimal OSSUTIL 2.0 smoke tests. Validate config, list bucket, and upload/download with OSS.
version: 1.0.0
---

Category: test

# OSSUTIL 2.0 Minimal Viable Test

## Goals

- 验证 AK/Region 配置正确。
- 验证 OSS 访问（列桶、上传、下载）。

## Prerequisites

- 已配置 AK（推荐环境变量或 `~/.alibabacloud/credentials`）。
- 已准备一个可读写的 OSS Bucket。

## Test Steps (Minimal)

1) 查看配置

```bash
ossutil config get region
```

2) 列出 Bucket

```bash
ossutil ls
```

3) 选择一个 bucket，按该 bucket 地域列对象（显式 region + endpoint）

```bash
# 示例（按实际 bucket 地域替换）
ossutil ls oss://<bucket> -r --short-format --region cn-shanghai -e https://oss-cn-shanghai.aliyuncs.com --limited-num 20
```

4) 上传小文件

```bash
echo "ossutil-test" > /tmp/ossutil-test.txt
ossutil cp /tmp/ossutil-test.txt oss://<bucket>/tests/ossutil-test.txt --region cn-shanghai -e https://oss-cn-shanghai.aliyuncs.com
```

5) 下载并校验

```bash
ossutil cp oss://<bucket>/tests/ossutil-test.txt /tmp/ossutil-test-down.txt --region cn-shanghai -e https://oss-cn-shanghai.aliyuncs.com
cat /tmp/ossutil-test-down.txt
```

## Expected Results

- `ossutil ls` 能返回至少一个 bucket 或无权限说明。
- 指定 `--region` + `-e` 后，列对象可正常返回。
- 上传/下载成功，文件内容一致。

## 常见失败

- Region 不匹配：确认 `ALIBABACLOUD_REGION_ID` 或配置文件中的 region。
- AK 无权限：确认 RAM 策略允许 `oss:*` 或最小读写权限。
