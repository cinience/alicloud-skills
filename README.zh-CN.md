# Alibaba Cloud 核心 Claude Skills

简体中文 | [English](README.en.md) | [繁體中文](README.zh-TW.md)

这是一个精选的 **Alibaba Cloud 核心 Claude skills** 集合，覆盖关键产品线，
包括 Model Studio、OSS、ECS 等。

## 快速开始

推荐安装（一次性安装全部、跳过确认、强制覆盖）：

```bash
npx skillfish add cinience/alicloud-skills --all -y --force
```

安装全部并跳过确认（不覆盖已有技能）：

```bash
npx skillfish add cinience/alicloud-skills --all -y
```

如果仍出现选择界面，按 `a` 全选后回车提交。

建议使用 RAM 用户/角色并遵循最小权限原则，避免在代码或命令行中明文暴露 AK。

优先使用环境变量：

```bash
export ALICLOUD_ACCESS_KEY_ID="你的AK"
export ALICLOUD_ACCESS_KEY_SECRET="你的SK"
export ALICLOUD_REGION_ID="cn-beijing"
export DASHSCOPE_API_KEY="你的DashScope API Key"
```

或者使用标准 CLI/SDK 配置文件：

`~/.alibabacloud/credentials`

```ini
[default]
type = access_key
access_key_id = 你的AK
access_key_secret = 你的SK
```

`~/.alibabacloud/config`

```ini
[default]
region_id = cn-beijing
```

## 项目结构

- `skills/` — 按产品线归类的技能源目录
  - `ai/` — Model Studio（按能力分组）
    - `text/` `image/` `audio/` `video/` `multimodal/` `search/` `misc/` `entry/`
  - `storage/` — OSS
  - `compute/` — ECS
  - `media/` — 智能媒体创作
  - `network/` — VPC / SLB / EIP
  - `database/` — RDS / PolarDB / Redis
  - `security/` — RAM / KMS / WAF
  - `observability/` — SLS / ARMS / CloudMonitor
- `examples/` — 端到端故事与使用流程示例

## 品牌别名

- `modelstudio/` — 指向 `skills/ai/` 的软链接（海外品牌）

## 已包含技能（当前）

位于 `skills/ai/`：

- `entry/alicloud-ai-entry-modelstudio`
- `entry/alicloud-ai-entry-modelstudio-test`
- `misc/alicloud-ai-misc-crawl-and-skill`
- `image/alicloud-ai-image-qwen-image`
- `audio/alicloud-ai-audio-tts`
- `video/alicloud-ai-video-wan-video`
- `search/alicloud-ai-search-dashvector`
- `search/alicloud-ai-search-opensearch`
- `search/alicloud-ai-search-milvus`
- `text/alicloud-ai-text-document-mind`

位于 `skills/storage/`：

- `oss/alicloud-storage-oss-ossutil`

位于 `skills/compute/`：

- `fc/alicloud-compute-fc-serverless-devs`
- `fc/alicloud-compute-fc-agentrun`
- `swas/alicloud-compute-swas-open`

位于 `skills/database/`：

- `rds/alicloud-database-rds-supabase`

位于 `skills/network/`：

- `dns/alicloud-network-dns-cli`

位于 `skills/media/`：

- `video/alicloud-media-video-translation`

位于 `skills/observability/`：

- `sls/alicloud-observability-sls-log-query`

## 技能索引

<!-- SKILL_INDEX_BEGIN -->
| Category | Skill | Path |
| --- | --- | --- |
| ai/audio | alicloud-ai-audio-tts | `skills/ai/audio/alicloud-ai-audio-tts` |
| ai/content | alicloud-ai-content-aicontent | `skills/ai/content/alicloud-ai-content-aicontent` |
| ai/content | alicloud-ai-content-aimiaobi | `skills/ai/content/alicloud-ai-content-aimiaobi` |
| ai/entry | alicloud-ai-entry-modelstudio | `skills/ai/entry/alicloud-ai-entry-modelstudio` |
| ai/entry | alicloud-ai-entry-modelstudio-test | `skills/ai/entry/alicloud-ai-entry-modelstudio-test` |
| ai/image | alicloud-ai-image-qwen-image | `skills/ai/image/alicloud-ai-image-qwen-image` |
| ai/misc | alicloud-ai-misc-crawl-and-skill | `skills/ai/misc/alicloud-ai-misc-crawl-and-skill` |
| ai/platform | alicloud-ai-pai-aiworkspace | `skills/ai/platform/alicloud-ai-pai-aiworkspace` |
| ai/recommendation | alicloud-ai-recommend-airec | `skills/ai/recommendation/alicloud-ai-recommend-airec` |
| ai/search | alicloud-ai-search-dashvector | `skills/ai/search/alicloud-ai-search-dashvector` |
| ai/search | alicloud-ai-search-milvus | `skills/ai/search/alicloud-ai-search-milvus` |
| ai/search | alicloud-ai-search-opensearch | `skills/ai/search/alicloud-ai-search-opensearch` |
| ai/service | alicloud-ai-chatbot | `skills/ai/service/alicloud-ai-chatbot` |
| ai/service | alicloud-ai-cloud-call-center | `skills/ai/service/alicloud-ai-cloud-call-center` |
| ai/service | alicloud-ai-contactcenter-ai | `skills/ai/service/alicloud-ai-contactcenter-ai` |
| ai/text | alicloud-ai-text-document-mind | `skills/ai/text/alicloud-ai-text-document-mind` |
| ai/translation | alicloud-ai-translation-anytrans | `skills/ai/translation/alicloud-ai-translation-anytrans` |
| ai/video | alicloud-ai-video-wan-video | `skills/ai/video/alicloud-ai-video-wan-video` |
| backup/alicloud-backup-bdrc | alicloud-backup-bdrc | `skills/backup/alicloud-backup-bdrc` |
| backup/alicloud-backup-hbr | alicloud-backup-hbr | `skills/backup/alicloud-backup-hbr` |
| compute/fc | alicloud-compute-fc-agentrun | `skills/compute/fc/alicloud-compute-fc-agentrun` |
| compute/fc | alicloud-compute-fc-serverless-devs | `skills/compute/fc/alicloud-compute-fc-serverless-devs` |
| compute/swas | alicloud-compute-swas-open | `skills/compute/swas/alicloud-compute-swas-open` |
| data-analytics/alicloud-data-analytics-dataanalysisgbi | alicloud-data-analytics-dataanalysisgbi | `skills/data-analytics/alicloud-data-analytics-dataanalysisgbi` |
| data-lake/alicloud-data-lake-dlf | alicloud-data-lake-dlf | `skills/data-lake/alicloud-data-lake-dlf` |
| data-lake/alicloud-data-lake-dlf-next | alicloud-data-lake-dlf-next | `skills/data-lake/alicloud-data-lake-dlf-next` |
| database/analyticdb | alicloud-database-analyticdb-mysql | `skills/database/analyticdb/alicloud-database-analyticdb-mysql` |
| database/rds | alicloud-database-rds-supabase | `skills/database/rds/alicloud-database-rds-supabase` |
| media/video | alicloud-media-video-translation | `skills/media/video/alicloud-media-video-translation` |
| network/dns | alicloud-network-dns-cli | `skills/network/dns/alicloud-network-dns-cli` |
| observability/sls | alicloud-observability-sls-log-query | `skills/observability/sls/alicloud-observability-sls-log-query` |
| platform/openapi | alicloud-platform-openapi-product-api-discovery | `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery` |
| security/content | alicloud-security-content-moderation-green | `skills/security/content/alicloud-security-content-moderation-green` |
| security/firewall | alicloud-security-cloudfw | `skills/security/firewall/alicloud-security-cloudfw` |
| security/host | alicloud-security-center-sas | `skills/security/host/alicloud-security-center-sas` |
| security/identity | alicloud-security-id-verification-cloudauth | `skills/security/identity/alicloud-security-id-verification-cloudauth` |
| security/key-management | alicloud-security-kms | `skills/security/key-management/alicloud-security-kms` |
| storage/oss | alicloud-storage-oss-ossutil | `skills/storage/oss/alicloud-storage-oss-ossutil` |
<!-- SKILL_INDEX_END -->

更新索引：运行 `scripts/update_skill_index.sh`

## 行业场景示例

详见：`examples/industry-use-cases.md`

## 备注

- 本仓库聚焦 Alibaba Cloud 的核心能力及其 Claude skill 实现。
- 后续可在 `skills/` 下持续扩展更多技能。

## 输出规范

- 所有临时文件与生成物必须写入 `output/`。
- 按技能划分子目录，例如 `output/<skill>/...`。
- `output/` 被 git 忽略，不允许提交。
