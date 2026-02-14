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

## 技能索引

<!-- SKILL_INDEX_BEGIN -->
| 分類 | 技能 | 技能描述 | 路徑 |
| --- | --- | --- | --- |
| ai/audio | alicloud-ai-audio-tts | 使用 Model Studio DashScope Qwen TTS 模型生成人聲語音，適用於文字轉語音與配音場景。 | `skills/ai/audio/alicloud-ai-audio-tts` |
| ai/audio | alicloud-ai-audio-tts-realtime | 使用 Alibaba Cloud Model Studio Qwen TTS Realtime 模型進行即時語音合成。 | `skills/ai/audio/alicloud-ai-audio-tts-realtime` |
| ai/audio | alicloud-ai-audio-tts-voice-clone | 使用 Alibaba Cloud Model Studio Qwen TTS VC 模型執行聲音克隆流程。 | `skills/ai/audio/alicloud-ai-audio-tts-voice-clone` |
| ai/audio | alicloud-ai-audio-tts-voice-design | 使用 Alibaba Cloud Model Studio Qwen TTS VD 模型執行聲音設計流程。 | `skills/ai/audio/alicloud-ai-audio-tts-voice-design` |
| ai/content | alicloud-ai-content-aicontent | 透過 OpenAPI/SDK 管理 Alibaba Cloud AIContent (AiContent)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/ai/content/alicloud-ai-content-aicontent` |
| ai/content | alicloud-ai-content-aimiaobi | 透過 OpenAPI/SDK 管理 Alibaba Cloud Quan Miao (AiMiaoBi)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/ai/content/alicloud-ai-content-aimiaobi` |
| ai/entry | alicloud-ai-entry-modelstudio | 將 Alibaba Cloud Model Studio 請求路由到最合適的本地技能（圖像、影片、TTS 等）。 | `skills/ai/entry/alicloud-ai-entry-modelstudio` |
| ai/entry | alicloud-ai-entry-modelstudio-test | 為倉庫中的 Model Studio 技能執行最小化測試矩陣並記錄結果。 | `skills/ai/entry/alicloud-ai-entry-modelstudio-test` |
| ai/image | alicloud-ai-image-qwen-image | 透過 Model Studio DashScope SDK 進行圖像生成，涵蓋 prompt、size、seed 等核心參數。 | `skills/ai/image/alicloud-ai-image-qwen-image` |
| ai/image | alicloud-ai-image-qwen-image-edit | 技能 `alicloud-ai-image-qwen-image-edit` 的能力說明，詳見對應 SKILL.md。 | `skills/ai/image/alicloud-ai-image-qwen-image-edit` |
| ai/image | alicloud-ai-image-zimage-turbo | 技能 `alicloud-ai-image-zimage-turbo` 的能力說明，詳見對應 SKILL.md。 | `skills/ai/image/alicloud-ai-image-zimage-turbo` |
| ai/misc | alicloud-ai-misc-crawl-and-skill | 刷新 Model Studio 模型抓取結果並重新產生衍生摘要與相關技能內容。 | `skills/ai/misc/alicloud-ai-misc-crawl-and-skill` |
| ai/platform | alicloud-ai-pai-aiworkspace | 透過 OpenAPI/SDK 管理 Alibaba Cloud Platform for Artificial Intelligence PAI - AIWorkspace (AIWorkSpace)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/ai/platform/alicloud-ai-pai-aiworkspace` |
| ai/recommendation | alicloud-ai-recommend-airec | 透過 OpenAPI/SDK 管理 Alibaba Cloud AIRec (Airec)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/ai/recommendation/alicloud-ai-recommend-airec` |
| ai/search | alicloud-ai-search-dashvector | 使用 Python SDK 建立 DashVector 向量檢索能力，支援集合建立、寫入與相似度查詢。 | `skills/ai/search/alicloud-ai-search-dashvector` |
| ai/search | alicloud-ai-search-milvus | 使用 PyMilvus 對接 AliCloud Milvus（Serverless），用於向量寫入與相似度檢索。 | `skills/ai/search/alicloud-ai-search-milvus` |
| ai/search | alicloud-ai-search-opensearch | 透過 Python SDK（ha3engine）使用 OpenSearch 向量檢索版，支援文件寫入與檢索。 | `skills/ai/search/alicloud-ai-search-opensearch` |
| ai/service | alicloud-ai-chatbot | 透過 OpenAPI/SDK 管理 Alibaba Cloud beebot (Chatbot)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/ai/service/alicloud-ai-chatbot` |
| ai/service | alicloud-ai-cloud-call-center | 透過 OpenAPI/SDK 管理 Alibaba Cloud Cloud Call Center (CCC)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/ai/service/alicloud-ai-cloud-call-center` |
| ai/service | alicloud-ai-contactcenter-ai | 透過 OpenAPI/SDK 管理 Alibaba Cloud Contact Center AI (ContactCenterAI)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/ai/service/alicloud-ai-contactcenter-ai` |
| ai/text | alicloud-ai-text-document-mind | 透過 Node.js SDK 使用 Document Mind（DocMind）執行文件解析任務並輪詢結果。 | `skills/ai/text/alicloud-ai-text-document-mind` |
| ai/translation | alicloud-ai-translation-anytrans | 透過 OpenAPI/SDK 管理 Alibaba Cloud TongyiTranslate (AnyTrans)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/ai/translation/alicloud-ai-translation-anytrans` |
| ai/video | alicloud-ai-video-wan-r2v | 技能 `alicloud-ai-video-wan-r2v` 的能力說明，詳見對應 SKILL.md。 | `skills/ai/video/alicloud-ai-video-wan-r2v` |
| ai/video | alicloud-ai-video-wan-video | 透過 Model Studio DashScope SDK 進行影片生成，支援時長、幀率、尺寸等參數控制。 | `skills/ai/video/alicloud-ai-video-wan-video` |
| backup/alicloud-backup-bdrc | alicloud-backup-bdrc | 透過 OpenAPI/SDK 管理 Alibaba Cloud Backup and Disaster Recovery Center (BDRC)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/backup/alicloud-backup-bdrc` |
| backup/alicloud-backup-hbr | alicloud-backup-hbr | 透過 OpenAPI/SDK 管理 Alibaba Cloud Cloud Backup (hbr)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/backup/alicloud-backup-hbr` |
| compute/ecs | alicloud-compute-ecs | 技能 `alicloud-compute-ecs` 的能力說明，詳見對應 SKILL.md。 | `skills/compute/ecs/alicloud-compute-ecs` |
| compute/fc | alicloud-compute-fc-agentrun | 透過 OpenAPI 管理 Function Compute AgentRun 資源，支援執行環境、端點與狀態查詢。 | `skills/compute/fc/alicloud-compute-fc-agentrun` |
| compute/fc | alicloud-compute-fc-serverless-devs | 技能 `alicloud-compute-fc-serverless-devs` 的能力說明，詳見對應 SKILL.md。 | `skills/compute/fc/alicloud-compute-fc-serverless-devs` |
| compute/swas | alicloud-compute-swas-open | 技能 `alicloud-compute-swas-open` 的能力說明，詳見對應 SKILL.md。 | `skills/compute/swas/alicloud-compute-swas-open` |
| data-analytics/alicloud-data-analytics-dataanalysisgbi | alicloud-data-analytics-dataanalysisgbi | 透過 OpenAPI/SDK 管理 Alibaba Cloud DataAnalysisGBI (DataAnalysisGBI)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/data-analytics/alicloud-data-analytics-dataanalysisgbi` |
| data-lake/alicloud-data-lake-dlf | alicloud-data-lake-dlf | 透過 OpenAPI/SDK 管理 Alibaba Cloud Data Lake Formation (DataLake)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/data-lake/alicloud-data-lake-dlf` |
| data-lake/alicloud-data-lake-dlf-next | alicloud-data-lake-dlf-next | 透過 OpenAPI/SDK 管理 Alibaba Cloud Data Lake Formation (DlfNext)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/data-lake/alicloud-data-lake-dlf-next` |
| database/analyticdb | alicloud-database-analyticdb-mysql | 透過 OpenAPI/SDK 管理 Alibaba Cloud AnalyticDB for MySQL (adb)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/database/analyticdb/alicloud-database-analyticdb-mysql` |
| database/rds | alicloud-database-rds-supabase | 透過 OpenAPI 管理 Alibaba Cloud RDS Supabase，涵蓋實例生命週期與關鍵設定操作。 | `skills/database/rds/alicloud-database-rds-supabase` |
| media/video | alicloud-media-video-translation | 透過 OpenAPI 建立與管理 Alibaba Cloud IMS 影片翻譯任務，支援字幕、語音與人臉相關設定。 | `skills/media/video/alicloud-media-video-translation` |
| network/dns | alicloud-network-dns-cli | Alibaba Cloud DNS（Alidns）CLI 技能，支援查詢、新增與更新 DNS 記錄。 | `skills/network/dns/alicloud-network-dns-cli` |
| observability/sls | alicloud-observability-sls-log-query | 技能 `alicloud-observability-sls-log-query` 的能力說明，詳見對應 SKILL.md。 | `skills/observability/sls/alicloud-observability-sls-log-query` |
| platform/docs | alicloud-platform-docs-api-review | 自動評審最新 Alibaba Cloud 產品文件與 OpenAPI 文件，並輸出優先級建議與證據。 | `skills/platform/docs/alicloud-platform-docs-api-review` |
| platform/docs | alicloud-platform-multicloud-docs-api-benchmark | 對阿里雲及主流雲廠商同類產品文件與 API 文件進行基準對比並給出改進建議。 | `skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark` |
| platform/openapi | alicloud-platform-openapi-product-api-discovery | 發現並對齊 Alibaba Cloud 產品目錄與 OpenAPI 中繼資料，用於覆蓋分析與技能規劃。 | `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery` |
| security/content | alicloud-security-content-moderation-green | 透過 OpenAPI/SDK 管理 Alibaba Cloud Content Moderation (Green)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/security/content/alicloud-security-content-moderation-green` |
| security/firewall | alicloud-security-cloudfw | 透過 OpenAPI/SDK 管理 Alibaba Cloud Cloud Firewall (Cloudfw)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/security/firewall/alicloud-security-cloudfw` |
| security/host | alicloud-security-center-sas | 透過 OpenAPI/SDK 管理 Alibaba Cloud Security Center (Sas)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/security/host/alicloud-security-center-sas` |
| security/identity | alicloud-security-id-verification-cloudauth | 透過 OpenAPI/SDK 管理 Alibaba Cloud ID Verification (Cloudauth)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/security/identity/alicloud-security-id-verification-cloudauth` |
| security/key-management | alicloud-security-kms | 透過 OpenAPI/SDK 管理 Alibaba Cloud KeyManagementService (Kms)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/security/key-management/alicloud-security-kms` |
| storage/oss | alicloud-storage-oss-ossutil | Alibaba Cloud OSS CLI（ossutil 2.0）技能，支援命令列安裝、設定與 OSS 資源操作。 | `skills/storage/oss/alicloud-storage-oss-ossutil` |
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
