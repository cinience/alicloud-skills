# Alibaba Cloud 核心 AI Agent Skills

## 語言

[English](README.md) | [简体中文](README.zh-CN.md) | **繁體中文（目前）**

快速入口：[快速開始](#快速開始) | [技能索引](#技能索引)

這是一套精選的 **Alibaba Cloud 核心 AI Agent skills**，涵蓋關鍵產品線，
包括 Model Studio、OSS、ECS 等。

## 快速開始

推薦安裝（一次性安裝全部、跳過確認、強制覆蓋）：

```bash
npx skills add cinience/alicloud-skills --all -y --force
```

如果仍出現選擇介面，按 `a` 全選後再按 Enter 送出。

建議使用 RAM 使用者/角色並遵循最小權限原則，避免在程式或命令列中明文暴露 AK。

優先使用環境變數：

```bash
export ALICLOUD_ACCESS_KEY_ID="你的AK"
export ALICLOUD_ACCESS_KEY_SECRET="你的SK"
export ALICLOUD_SECURITY_TOKEN="你的STS Token" # 選填，使用 STS 時填寫
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

若使用 STS，請設定 `type = sts` 並補上 `security_token = 你的STS Token`。

## 示例（文件評審與跨雲對比）

1) 產品文件 + API 文件評審

- 提示詞：
  「用 `alicloud-platform-docs-api-review` 評審產品 `百煉` 的產品文件與 API 文件，輸出 P0/P1/P2 改進建議並附證據連結。」

2) 跨雲同類產品對比

- 提示詞：
  「用 `alicloud-platform-multicloud-docs-api-benchmark` 對 `百煉` 做跨雲對比（阿里雲/AWS/Azure/GCP/騰訊雲/火山引擎/華為雲），使用 `llm-platform` 預設，輸出評分表與改進建議。」

## 獨立技能與提示詞（示例）

1) 文生圖（Qwen Image）

- Demo：生成圖片
- 提示詞：
  「用 `alicloud-ai-image-qwen-image` 生成 1024*1024 海報圖，主題是極簡咖啡，輸出檔名 `poster.png`。」

2) 圖生影片（Wan Video）

- Demo：用一張參考圖生成 4 秒影片（需提供可存取的圖片 URL）
- 提示詞：
  「用 `alicloud-ai-video-wan-video`，參考圖 `https://.../scene.png`，生成 4 秒 24fps 1280*720 的鏡頭，提示詞：清晨城市縮時攝影。」

3) 文字轉語音（Qwen TTS）

- Demo：用 DashScope 生成音訊
- 提示詞：
  「用 `alicloud-ai-audio-tts` 把這段話合成語音，`voice=Cherry`，`language=English`，輸出音訊 URL。」

4) 文件結構解析（DocMind）

- Demo：解析 PDF 的標題/段落結構
- 提示詞：
  「用 `alicloud-ai-text-document-mind` 解析這份 PDF（URL: ...），取得結構化結果。」

5) 向量檢索（DashVector）

- Demo：建立集合、寫入、查詢
- 提示詞：
  「用 `alicloud-ai-search-dashvector` 建立 `dimension=768` 的集合，寫入 2 筆文件後做 `topk=5` 查詢。」

6) OSS 上傳/同步（ossutil）

- Demo：上傳本機檔案到 OSS
- 提示詞：
  「用 `alicloud-storage-oss-ossutil` 把 `./local.txt` 上傳到 `oss://xxx/path/`。」

7) SLS 日誌排查

- Demo：最近 15 分鐘查 500 錯誤
- 提示詞：
  「用 `alicloud-observability-sls-log-query` 查最近 15 分鐘 500 錯誤，並按狀態聚合。」

8) FC 3.0 快速部署（Serverless Devs）

- Demo：初始化 Python 函式並部署
- 提示詞：
  「用 `alicloud-compute-fc-serverless-devs` 初始化 FC 3.0 Python 專案並部署。」

9) 內容安全（Green）

- Demo：透過 OpenAPI 探索/呼叫內容審核 API
- 提示詞：
  「用 `alicloud-security-content-moderation-green` 先列出可用 API，再給我一條文字檢測的最小參數示例。」

10) KMS 金鑰管理

- Demo：列出金鑰或建立金鑰
- 提示詞：
  「用 `alicloud-security-kms` 給出建立對稱金鑰的 OpenAPI 參數範本。」

11) 產品文件與 API 文件自動評審

- Demo：按產品名自動抓取最新文件並給出改進建議
- 提示詞：
  「用 `alicloud-platform-docs-api-review` 評審產品 `百煉` 的產品文件與 API 文件，輸出 P0/P1/P2 改進建議與證據連結。」

12) 跨雲同類產品文件/API 對比

- Demo：對比阿里雲/AWS/Azure/GCP/騰訊雲/火山引擎/華為雲同類產品
- 提示詞：
  「用 `alicloud-platform-multicloud-docs-api-benchmark` 對 `百煉` 做跨雲同類產品文件/API 對比，並用 `llm-platform` 預設輸出評分表與差距建議。」

## 組合方案（場景與提示詞範本）

1) 行銷素材流水線（圖 -> 影片 -> 配音 -> 上傳）

範本：
「按以下流程串聯技能：
1. `alicloud-ai-image-qwen-image` 生成海報圖（主題：{主題}，尺寸：{尺寸}）。
2. `alicloud-ai-video-wan-video` 基於上一步圖片生成 {時長}s 影片（fps={fps}，size={尺寸}，鏡頭描述：{鏡頭描述}）。
3. `alicloud-ai-audio-tts` 用 voice={音色} 合成旁白（文本：{旁白文本}，語言：{語言}）。
4. `alicloud-storage-oss-ossutil` 上傳影片與音訊到 {oss路徑}。
請輸出最終資產 URL 清單與對應說明。」

2) 客服知識庫檢索 + 語音應答

範本：
「用 `alicloud-ai-text-document-mind` 解析文件（URL：{文件URL}）得到結構化內容；
再用 `alicloud-ai-search-dashvector` 建庫並入庫；
最後根據使用者問題：{使用者問題} 做 `topk={topk}` 檢索並用 `alicloud-ai-audio-tts` 生成語音回答（voice={音色}，language={語言}）。
請回傳文字答案 + 語音 URL。」

3) 內容審核 + 發布

範本：
「用 `alicloud-security-content-moderation-green` 審核內容（類型：{文字|圖片|影片}，內容：{內容/URL}）。
若通過則用 `alicloud-storage-oss-ossutil` 上傳到 {oss路徑} 並回傳公開連結；
若不通過，請給出原因與建議替代文案。」

4) 站點日誌排障 + 自動告警

範本：
「用 `alicloud-observability-sls-log-query` 查詢 {時間範圍} 內的錯誤（query：{查詢語句}），
按 {聚合欄位} 統計並判斷是否超過閾值 {閾值}；
若超過，呼叫 `alicloud-compute-fc-serverless-devs` 觸發告警函式（函式名：{函式名}，參數：{告警參數}）。
輸出統計結果與告警觸發狀態。」

5) 多語言內容生產（生成 -> 翻譯 -> 配音）

範本：
「用 `alicloud-ai-content-aicontent` 生成主題文案（主題：{主題}，風格：{風格}，長度：{長度}）；
用 `alicloud-ai-translation-anytrans` 翻譯為 {目標語言}；
用 `alicloud-ai-audio-tts` 生成配音（voice={音色}，language={語言}）。
輸出：原文、譯文、語音 URL。」

6) 訓練素材清洗與歸檔

範本：
「對素材進行合規檢查：`alicloud-security-content-moderation-green`（內容：{內容/URL}）。
若通過，用 `alicloud-ai-text-document-mind` 做結構化抽取（如適用）；
最終用 `alicloud-storage-oss-ossutil` 歸檔到 {oss路徑}，回傳歸檔清單與 URL。」

7) 日誌指標分析報表

範本：
「用 `alicloud-observability-sls-log-query` 在 {時間範圍} 內執行查詢：{query|analysis}，
按 {維度} 輸出統計表；
再用 `alicloud-data-analytics-dataanalysisgbi` 生成視覺化報表摘要（指標：{指標列表}，維度：{維度}）。
輸出關鍵指標與報表摘要。」

8) 業務搜尋與推薦

範本：
「先用 `alicloud-ai-search-dashvector` 基於使用者意圖向量檢索（topk={topk}，filter={過濾條件}），
再用 `alicloud-ai-recommend-airec` 對結果進行排序與補充推薦（策略：{策略}）。
輸出最終推薦清單與理由。」

9) 企業通話場景（呼叫中心 + 智能客服 + 語音）

範本：
「用 `alicloud-ai-cloud-call-center` 建立/路由來電（號碼：{號碼}，路由策略：{策略}）；
用 `alicloud-ai-chatbot` 給出 FAQ 命中或轉人工判斷；
用 `alicloud-ai-audio-tts` 播報回覆（voice={音色}，language={語言}）。
輸出最終話術與語音 URL。」

10) 安全合規閉環（金鑰 + 稽核）

範本：
「用 `alicloud-security-kms` 建立/管理金鑰（用途：{用途}，別名：{別名}）；
結合 `alicloud-observability-sls-log-query` 查詢 {時間範圍} 內的安全稽核日誌（query：{查詢語句}）；
如發現異常，給出處理建議或觸發告警（函式：{函式名}）。
輸出金鑰狀態、稽核結果與處置建議。」


## 專案結構

- `skills/` — 依產品線歸類的技能來源
  - `ai/` — Model Studio（依能力分組）
    - `text/` `image/` `audio/` `video/` `multimodal/` `search/` `misc/` `entry/`
  - `storage/` — OSS
  - `compute/` — ECS
  - `media/` — 智慧媒體創作
  - `network/` — DNS / ALB（應用型負載均衡）/ ESA
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
| ai/audio | alicloud-ai-audio-asr | 使用 Alibaba Cloud Model Studio Qwen ASR 模型進行非即時語音辨識與轉寫，支援短音訊同步辨識與長音訊非同步轉寫。 | `skills/ai/audio/alicloud-ai-audio-asr` |
| ai/audio | alicloud-ai-audio-tts | 使用 Model Studio DashScope Qwen TTS 模型生成人聲語音，適用於文字轉語音與配音場景。 | `skills/ai/audio/alicloud-ai-audio-tts` |
| ai/audio | alicloud-ai-audio-tts-realtime | 使用 Alibaba Cloud Model Studio Qwen TTS Realtime 模型進行即時語音合成。 | `skills/ai/audio/alicloud-ai-audio-tts-realtime` |
| ai/audio | alicloud-ai-audio-tts-voice-clone | 使用 Alibaba Cloud Model Studio Qwen TTS VC 模型執行聲音克隆流程。 | `skills/ai/audio/alicloud-ai-audio-tts-voice-clone` |
| ai/audio | alicloud-ai-audio-tts-voice-design | 使用 Alibaba Cloud Model Studio Qwen TTS VD 模型執行聲音設計流程。 | `skills/ai/audio/alicloud-ai-audio-tts-voice-design` |
| ai/content | alicloud-ai-content-aicontent | 透過 OpenAPI/SDK 管理 Alibaba Cloud AIContent (AiContent)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/ai/content/alicloud-ai-content-aicontent` |
| ai/content | alicloud-ai-content-aimiaobi | 透過 OpenAPI/SDK 管理 Alibaba Cloud Quan Miao (AiMiaoBi)，用於資源查詢、建立或更新配置、狀態查詢與故障排查。 | `skills/ai/content/alicloud-ai-content-aimiaobi` |
| ai/entry | alicloud-ai-entry-modelstudio | 將 Alibaba Cloud Model Studio 請求路由到最合適的本地技能（圖像、影片、TTS、ASR 等）。 | `skills/ai/entry/alicloud-ai-entry-modelstudio` |
| ai/entry | alicloud-ai-entry-modelstudio-test | 為倉庫中的 Model Studio 技能執行最小化測試矩陣並記錄結果。 | `skills/ai/entry/alicloud-ai-entry-modelstudio-test` |
| ai/image | alicloud-ai-image-qwen-image | 透過 Model Studio DashScope SDK 進行圖像生成，涵蓋 prompt、size、seed 等核心參數。 | `skills/ai/image/alicloud-ai-image-qwen-image` |
| ai/image | alicloud-ai-image-qwen-image-edit | 技能 `alicloud-ai-image-qwen-image-edit` 的能力說明，詳見對應 SKILL.md。 | `skills/ai/image/alicloud-ai-image-qwen-image-edit` |
| ai/image | alicloud-ai-image-zimage-turbo | 技能 `alicloud-ai-image-zimage-turbo` 的能力說明，詳見對應 SKILL.md。 | `skills/ai/image/alicloud-ai-image-zimage-turbo` |
| ai/misc | alicloud-ai-misc-crawl-and-skill | 刷新 Model Studio 模型抓取結果並重新產生衍生摘要與相關技能內容。 | `skills/ai/misc/alicloud-ai-misc-crawl-and-skill` |
| ai/multimodal | alicloud-ai-multimodal-qwen-vl | 技能 `alicloud-ai-multimodal-qwen-vl` 的能力說明，詳見對應 SKILL.md。 | `skills/ai/multimodal/alicloud-ai-multimodal-qwen-vl` |
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
| media/ice | alicloud-media-ice | 技能 `alicloud-media-ice` 的能力說明，詳見對應 SKILL.md。 | `skills/media/ice/alicloud-media-ice` |
| media/live | alicloud-media-live | 技能 `alicloud-media-live` 的能力說明，詳見對應 SKILL.md。 | `skills/media/live/alicloud-media-live` |
| media/video | alicloud-media-video-translation | 透過 OpenAPI 建立與管理 Alibaba Cloud IMS 影片翻譯任務，支援字幕、語音與人臉相關設定。 | `skills/media/video/alicloud-media-video-translation` |
| media/vod | alicloud-media-vod | 技能 `alicloud-media-vod` 的能力說明，詳見對應 SKILL.md。 | `skills/media/vod/alicloud-media-vod` |
| network/dns | alicloud-network-dns-cli | Alibaba Cloud DNS（Alidns）CLI 技能，支援查詢、新增與更新 DNS 記錄。 | `skills/network/dns/alicloud-network-dns-cli` |
| network/esa | alicloud-network-esa | 技能 `alicloud-network-esa` 的能力說明，詳見對應 SKILL.md。 | `skills/network/esa/alicloud-network-esa` |
| network/slb | alicloud-network-alb | 管理與排障阿里雲 ALB（應用型負載均衡）。涵蓋實例、監聽、伺服器群組、轉發規則、憑證、ACL、安全策略、健康檢查及非同步任務輪詢的全生命週期管理，包含 28 個 CLI 腳本。 | `skills/network/slb/alicloud-network-alb` |
| observability/sls | alicloud-observability-sls-log-query | 技能 `alicloud-observability-sls-log-query` 的能力說明，詳見對應 SKILL.md。 | `skills/observability/sls/alicloud-observability-sls-log-query` |
| platform/cli | alicloud-platform-aliyun-cli | 通用 Alibaba Cloud CLI（aliyun）技能，涵蓋安裝、憑證/設定、API 探索與跨產品 OpenAPI 命令列呼叫。 | `skills/platform/cli/alicloud-platform-aliyun-cli` |
| platform/docs | alicloud-platform-docs-api-review | 自動評審最新 Alibaba Cloud 產品文件與 OpenAPI 文件，並輸出優先級建議與證據。 | `skills/platform/docs/alicloud-platform-docs-api-review` |
| platform/docs | alicloud-platform-multicloud-docs-api-benchmark | 對阿里雲及主流雲廠商同類產品文件與 API 文件進行基準對比並給出改進建議。 | `skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark` |
| platform/openapi | alicloud-platform-openapi-product-api-discovery | 發現並對齊 Alibaba Cloud 產品目錄與 OpenAPI 中繼資料，用於覆蓋分析與技能規劃。 | `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery` |
| platform/openclaw | alicloud-platform-openclaw-setup | 技能 `alicloud-platform-openclaw-setup` 的能力說明，詳見對應 SKILL.md。 | `skills/platform/openclaw/alicloud-platform-openclaw-setup` |
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

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=cinience/alicloud-skills&type=Date)](https://star-history.com/#cinience/alicloud-skills&Date)
