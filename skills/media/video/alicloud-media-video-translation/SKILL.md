---
name: alicloud-media-video-translation
description: Create and manage Alibaba Cloud IMS video translation jobs via OpenAPI (subtitle/voice/face). Use when you need API-based video translation, status polling, and job management.
---

Category: service

# IMS 视频翻译（OpenAPI）

通过 OpenAPI 提交视频翻译任务并轮询结果，覆盖字幕级/语音级/面容级。

## Prerequisites

- 准备 OSS 输入/输出地址（建议与 API 调用 region 一致）。
- 配置 AK：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`（`ALICLOUD_REGION_ID` 可作为默认 Region；未设置时可选择最合理 Region，无法判断则询问用户）。

## Workflow

1) 准备源文件与输出 OSS 位置。  
2) 调用 `SubmitVideoTranslationJob` 提交任务。  
3) 使用 `GetSmartHandleJob` 轮询状态与结果。  
4) 需要时使用 `ListSmartJobs` / `DeleteSmartJob` 管理任务。  

## Level 选择与参数

- 字幕级 / 语音级 / 面容级的选择规则与字段见 `references/fields.md`。
- 字段示例（Input/Output/EditingConfig）也在 `references/fields.md`。

## Notes

- 如需二次修正，请在首个任务设置 `SupportEditing=true`，后续用 `OriginalJobId` 关联。
- 输入与输出的 OSS region 必须与 OpenAPI 调用 region 一致。
- 大任务需更长轮询间隔，避免频繁请求。
## References

- Source list: `references/sources.md`
