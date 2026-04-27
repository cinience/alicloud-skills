---
name: aliyun-sls-log-query-test
description: Minimal smoke test for SLS log query skill. Validate SDK auth and one bounded query.
version: 1.0.0
---

Category: test

# SLS 日志查询Minimal Viable Test

## Prerequisites

- 配置 `ALIBABACLOUD_ACCESS_KEY_ID`、`ALIBABACLOUD_ACCESS_KEY_SECRET`。
- 配置 `SLS_ENDPOINT`、`SLS_PROJECT`、`SLS_LOGSTORE`。
- GoalsSkill: `skills/observability/sls/aliyun-sls-log-query/`。

## Test Steps

1) 执行 5 分钟窗口的基础查询（如 `* | select count(*)`）。
2) 记录耗时与返回行数。
3) 若失败，记录完整错误码。

## Expected Results

- 查询成功返回统计结果，或返回可诊断错误。
