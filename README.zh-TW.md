# Alibaba Cloud 核心 AI Agent Skills

繁體中文（目前） | [English](README.en.md) | [简体中文](README.md)

這是一套精選的 **Alibaba Cloud 核心 AI Agent skills**，涵蓋關鍵產品線，
包括 Model Studio、OSS、ECS 等。

## 快速開始

推薦安裝（一次性安裝全部、跳過確認、強制覆蓋）：

```bash
npx skillfish add cinience/alicloud-skills --all -y --force
```

如果仍出現選擇介面，按 `a` 全選後再按 Enter 送出。

建議使用 RAM 使用者/角色並遵循最小權限原則，避免在程式或命令列中明文暴露 AK。

優先使用環境變數：

```bash
export ALICLOUD_ACCESS_KEY_ID="你的AK"
export ALICLOUD_ACCESS_KEY_SECRET="你的SK"
export ALICLOUD_REGION_ID="cn-beijing"
export DASHSCOPE_API_KEY="你的DashScope API Key"
```

環境變數優先生效；若未設定環境變數，才會讀取 `~/.alibabacloud/credentials`。`ALICLOUD_REGION_ID` 可作為預設 Region；未設定時可在執行時選擇最合理的 Region，無法判斷則需詢問使用者。

若未設定環境變數，可使用標準 CLI/SDK 設定檔：

`~/.alibabacloud/credentials`

```ini
[default]
type = access_key
access_key_id = 你的AK
access_key_secret = 你的SK
dashscope_api_key = 你的DashScope API Key
```

## 示例（文件評審與跨雲對比）

1) 產品文件 + API 文件評審

- 提示詞：
  「用 `alicloud-platform-docs-api-review` 評審產品 `百煉` 的產品文件與 API 文件，輸出 P0/P1/P2 改進建議並附證據連結。」

2) 跨雲同類產品對比

- 提示詞：
  「用 `alicloud-platform-multicloud-docs-api-benchmark` 對 `百煉` 做跨雲對比（阿里雲/AWS/Azure/GCP/騰訊雲/火山引擎/華為雲），使用 `llm-platform` 預設，輸出評分表與改進建議。」


## 專案結構

- `skills/` — 依產品線歸類的技能來源
  - `ai/` — Model Studio（依能力分組）
    - `text/` `image/` `audio/` `video/` `multimodal/` `search/` `misc/` `entry/`
  - `storage/` — OSS
  - `compute/` — ECS
  - `media/` — 智慧媒體創作
  - `network/` — VPC / SLB / EIP
  - `database/` — RDS / PolarDB / Redis
  - `security/` — RAM / KMS / WAF
  - `observability/` — SLS / ARMS / CloudMonitor
- `examples/` — 端到端故事與使用流程示例

## 品牌別名

- `modelstudio/` — 指向 `skills/ai/` 的軟連結（海外品牌）

## 已包含技能（目前）


<!-- INCLUDED_SKILLS_BEGIN -->
位於 `skills/ai/`：

- `audio/alicloud-ai-audio-tts`
- `audio/alicloud-ai-audio-tts-realtime`
- `audio/alicloud-ai-audio-tts-voice-clone`
- `audio/alicloud-ai-audio-tts-voice-design`
- `content/alicloud-ai-content-aicontent`
- `content/alicloud-ai-content-aimiaobi`
- `entry/alicloud-ai-entry-modelstudio`
- `entry/alicloud-ai-entry-modelstudio-test`
- `image/alicloud-ai-image-qwen-image`
- `image/alicloud-ai-image-qwen-image-edit`
- `image/alicloud-ai-image-zimage-turbo`
- `misc/alicloud-ai-misc-crawl-and-skill`
- `platform/alicloud-ai-pai-aiworkspace`
- `recommendation/alicloud-ai-recommend-airec`
- `search/alicloud-ai-search-dashvector`
- `search/alicloud-ai-search-milvus`
- `search/alicloud-ai-search-opensearch`
- `service/alicloud-ai-chatbot`
- `service/alicloud-ai-cloud-call-center`
- `service/alicloud-ai-contactcenter-ai`
- `text/alicloud-ai-text-document-mind`
- `translation/alicloud-ai-translation-anytrans`
- `video/alicloud-ai-video-wan-r2v`
- `video/alicloud-ai-video-wan-video`

位於 `skills/storage/`：

- `oss/alicloud-storage-oss-ossutil`

位於 `skills/compute/`：

- `ecs/alicloud-compute-ecs`
- `fc/alicloud-compute-fc-agentrun`
- `fc/alicloud-compute-fc-serverless-devs`
- `swas/alicloud-compute-swas-open`

位於 `skills/database/`：

- `analyticdb/alicloud-database-analyticdb-mysql`
- `rds/alicloud-database-rds-supabase`

位於 `skills/network/`：

- `dns/alicloud-network-dns-cli`

位於 `skills/media/`：

- `video/alicloud-media-video-translation`

位於 `skills/observability/`：

- `sls/alicloud-observability-sls-log-query`

位於 `skills/backup/`：

- `alicloud-backup-bdrc`
- `alicloud-backup-hbr`

位於 `skills/data-lake/`：

- `alicloud-data-lake-dlf`
- `alicloud-data-lake-dlf-next`

位於 `skills/data-analytics/`：

- `alicloud-data-analytics-dataanalysisgbi`

位於 `skills/platform/`：

- `docs/alicloud-platform-docs-api-review`
- `docs/alicloud-platform-multicloud-docs-api-benchmark`
- `openapi/alicloud-platform-openapi-product-api-discovery`

位於 `skills/security/`：

- `content/alicloud-security-content-moderation-green`
- `firewall/alicloud-security-cloudfw`
- `host/alicloud-security-center-sas`
- `identity/alicloud-security-id-verification-cloudauth`
- `key-management/alicloud-security-kms`
<!-- INCLUDED_SKILLS_END -->

## 技能索引

<!-- SKILL_INDEX_BEGIN -->
| Category | Skill | Path |
| --- | --- | --- |
| ai/audio | alicloud-ai-audio-tts | `skills/ai/audio/alicloud-ai-audio-tts` |
| ai/audio | alicloud-ai-audio-tts-realtime | `skills/ai/audio/alicloud-ai-audio-tts-realtime` |
| ai/audio | alicloud-ai-audio-tts-voice-clone | `skills/ai/audio/alicloud-ai-audio-tts-voice-clone` |
| ai/audio | alicloud-ai-audio-tts-voice-design | `skills/ai/audio/alicloud-ai-audio-tts-voice-design` |
| ai/content | alicloud-ai-content-aicontent | `skills/ai/content/alicloud-ai-content-aicontent` |
| ai/content | alicloud-ai-content-aimiaobi | `skills/ai/content/alicloud-ai-content-aimiaobi` |
| ai/entry | alicloud-ai-entry-modelstudio | `skills/ai/entry/alicloud-ai-entry-modelstudio` |
| ai/entry | alicloud-ai-entry-modelstudio-test | `skills/ai/entry/alicloud-ai-entry-modelstudio-test` |
| ai/image | alicloud-ai-image-qwen-image | `skills/ai/image/alicloud-ai-image-qwen-image` |
| ai/image | alicloud-ai-image-qwen-image-edit | `skills/ai/image/alicloud-ai-image-qwen-image-edit` |
| ai/image | alicloud-ai-image-zimage-turbo | `skills/ai/image/alicloud-ai-image-zimage-turbo` |
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
| ai/video | alicloud-ai-video-wan-r2v | `skills/ai/video/alicloud-ai-video-wan-r2v` |
| ai/video | alicloud-ai-video-wan-video | `skills/ai/video/alicloud-ai-video-wan-video` |
| backup/alicloud-backup-bdrc | alicloud-backup-bdrc | `skills/backup/alicloud-backup-bdrc` |
| backup/alicloud-backup-hbr | alicloud-backup-hbr | `skills/backup/alicloud-backup-hbr` |
| compute/ecs | alicloud-compute-ecs | `skills/compute/ecs/alicloud-compute-ecs` |
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
| platform/docs | alicloud-platform-docs-api-review | `skills/platform/docs/alicloud-platform-docs-api-review` |
| platform/docs | alicloud-platform-multicloud-docs-api-benchmark | `skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark` |
| platform/openapi | alicloud-platform-openapi-product-api-discovery | `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery` |
| security/content | alicloud-security-content-moderation-green | `skills/security/content/alicloud-security-content-moderation-green` |
| security/firewall | alicloud-security-cloudfw | `skills/security/firewall/alicloud-security-cloudfw` |
| security/host | alicloud-security-center-sas | `skills/security/host/alicloud-security-center-sas` |
| security/identity | alicloud-security-id-verification-cloudauth | `skills/security/identity/alicloud-security-id-verification-cloudauth` |
| security/key-management | alicloud-security-kms | `skills/security/key-management/alicloud-security-kms` |
| storage/oss | alicloud-storage-oss-ossutil | `skills/storage/oss/alicloud-storage-oss-ossutil` |
<!-- SKILL_INDEX_END -->

更新索引：執行 `scripts/update_skill_index.sh`

## 產業場景示例

詳見：`examples/industry-use-cases.md`

## 備註

- 本專案聚焦 Alibaba Cloud 的核心能力及其 Claude skill 實作。
- 之後可持續在 `skills/` 下擴充更多技能。

## 輸出規範

- 所有臨時檔案與生成物必須寫入 `output/`。
- 按技能劃分子目錄，例如 `output/<skill>/...`。
- `output/` 會被 git 忽略，不允許提交。
