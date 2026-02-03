---
name: alicloud-storage-oss-ossutil
description: Alibaba Cloud OSS CLI (ossutil 2.0) skill. Install, configure, and operate OSS from the command line based on the official ossutil overview.
---

Category: tool

# OSS（ossutil 2.0）命令行技能

## 目标

- 使用 ossutil 2.0 管理 OSS：上传、下载、同步与资源管理。
- 统一安装、配置、凭证与 Region/Endpoint 的 CLI 流程。

## 快速接入流程

1. 安装 ossutil 2.0。
2. 运行 `ossutil config` 完成交互式配置。
3. 执行命令（高级命令或 API 级命令）。

## 安装 ossutil 2.0

- 按平台安装步骤见 `references/install.md`。

## 配置 ossutil

- 交互式配置：

```bash
ossutil config
```

- 默认配置文件路径：
  - Linux：`/root/.ossutilconfig`
  - Windows：`C:\Users\issuser\.ossutilconfig`

配置项主要包括：
- `AccessKey ID`
- `AccessKey Secret`
- `Region`（示例默认 `cn-hangzhou`；未确定最合理 Region 时需询问）
- `Endpoint`（可选；未指定时按 Region 自动推导）

## AccessKey 配置提示

建议使用 RAM 用户/角色并遵循最小权限原则，避免在命令行中明文传入 AK。

推荐方式（环境变量）：

```bash
export ALICLOUD_ACCESS_KEY_ID="你的AK"
export ALICLOUD_ACCESS_KEY_SECRET="你的SK"
export ALICLOUD_REGION_ID="cn-beijing"
```

`ALICLOUD_REGION_ID` 可作为默认 Region；未设置时可选择最合理 Region，无法判断则询问用户。

或使用标准共享凭证文件：

`~/.alibabacloud/credentials`

```ini
[default]
type = access_key
access_key_id = 你的AK
access_key_secret = 你的SK
```


## 命令结构（2.0）

- 高级命令示例：`ossutil config`
- API 级命令示例：`ossutil api put-bucket-acl`

## 常用命令示例

```bash
ossutil ls
ossutil cp ./local.txt oss://your-bucket/path/local.txt
ossutil cp oss://your-bucket/path/remote.txt ./remote.txt
ossutil sync ./local-dir oss://your-bucket/path/ --delete
```

## 凭证与安全建议

- 优先使用 RAM 用户的 AK 进行访问控制。
- 命令行选项可覆盖配置文件，但直接在命令行传入密钥存在泄露风险。
- 生产环境建议使用配置文件或环境变量方式管理密钥。

## 选择问题（不确定时提问）

1. 你的操作对象是 Bucket 还是 Object？
2. 需要上传/下载/同步，还是权限/生命周期/跨域等管理操作？
3. 目标 Region 与 Endpoint 是什么？
4. 是否在同地域 ECS 上访问 OSS（可考虑内网 Endpoint）？

## 参考

- OSSUTIL 2.0 概述与安装/配置：
  - https://help.aliyun.com/zh/oss/developer-reference/ossutil-overview

- 官方文档来源清单：`references/sources.md`
