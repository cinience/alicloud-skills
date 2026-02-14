# Alibaba Cloud 核心 AI Agent Skills

简体中文（当前） | [English](README.en.md) | [繁體中文](README.zh-TW.md)

Cloud Mind：把世界级云基建，折叠进你的AI对话框。


这是一个精选的 **Alibaba Cloud 核心 AI Agent skills** 集合，覆盖关键产品线，
包括 Model Studio、OSS、ECS 等。

## 快速开始

推荐安装（一次性安装全部、跳过确认、强制覆盖）：

```bash
npx skillfish add cinience/alicloud-skills --all -y --force
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

环境变量优先生效；若未设置环境变量，才会读取 `~/.alibabacloud/credentials`。`ALICLOUD_REGION_ID` 可作为默认 Region；未设置时可在执行时选择最合理的 Region，无法判断则需要询问用户。

若未设置环境变量，可使用标准 CLI/SDK 配置文件：

`~/.alibabacloud/credentials`

```ini
[default]
type = access_key
access_key_id = 你的AK
access_key_secret = 你的SK
dashscope_api_key = 你的DashScope API Key
```


## 独立技能与提示词（示例）

1) 文生图（Qwen Image）

- Demo：生成图片  
- 提示词：  
  “用 `alicloud-ai-image-qwen-image` 生成 1024*1024 海报图，主题是极简咖啡，输出文件名 poster.png。”

2) 图生视频（Wan Video）

- Demo：用一张参考图生成 4 秒视频（需提供可访问的图片 URL）
- 提示词：  
  “用 `alicloud-ai-video-wan-video`，参考图 `https://.../scene.png`，生成 4 秒 24fps 1280*720 的镜头，提示词：清晨城市延时摄影。”

3) 文字转语音（Qwen TTS）

- Demo：用 DashScope 生成音频  
- 提示词：  
  “用 `alicloud-ai-audio-tts` 把这段话合成语音，voice=Cherry，language=English，输出音频 URL。”

4) 文档结构解析（DocMind）

- Demo：解析 PDF 的标题/段落结构  
- 提示词：  
  “用 `alicloud-ai-text-document-mind` 解析这个 PDF（URL: ...），拿到结构化结果。”

5) 向量检索（DashVector）

- Demo：创建集合、写入、查询  
- 提示词：  
  “用 `alicloud-ai-search-dashvector` 创建 dimension=768 的集合，写入 2 条文档后做 topk=5 查询。”

6) OSS 上传/同步（ossutil）

- Demo：上传本地文件到 OSS  
- 提示词：  
  “用 `alicloud-storage-oss-ossutil` 把 ./local.txt 上传到 oss://xxx/path/。”

7) SLS 日志排查

- Demo：最近 15 分钟查 500 错误  
- 提示词：  
  “用 `alicloud-observability-sls-log-query` 查最近 15 分钟 500 错误，并按状态聚合。”

8) FC 3.0 快速部署（Serverless Devs）

- Demo：初始化 Python 函数并部署  
- 提示词：  
  “用 `alicloud-compute-fc-serverless-devs` 初始化 FC 3.0 Python 项目并部署。”

9) 内容安全（Green）

- Demo：通过 OpenAPI 发现/调用内容审核 API  
- 提示词：  
  “用 `alicloud-security-content-moderation-green` 先列出可用 API，再给我一条文本检测的最小参数示例。”

10) KMS 密钥管理

- Demo：列出密钥或创建密钥  
- 提示词：  
  “用 `alicloud-security-kms` 给出创建对称密钥的 OpenAPI 参数模板。”

11) 产品文档与 API 文档自动评审

- Demo：按产品名自动抓取最新文档并给出改进建议
- 提示词：
  “用 `alicloud-platform-docs-api-review` 评审产品 `百炼` 的产品文档和 API 文档，输出 P0/P1/P2 改进建议与证据链接。”

12) 跨云同类产品文档/API 对比

- Demo：对比阿里云/AWS/Azure/GCP/腾讯云/火山引擎/华为云同类产品
- 提示词：
  “用 `alicloud-platform-multicloud-docs-api-benchmark` 对 `百炼` 做跨云同类产品文档/API 对比，并用 `llm-platform` 预设输出评分表与差距建议。”

## 组合方案（场景与提示词模板）

1) 营销素材流水线（图 → 视频 → 配音 → 上传）

模板：
“按以下流程串联技能：  
① `alicloud-ai-image-qwen-image` 生成海报图（主题：{主题}，尺寸：{尺寸}）。  
② `alicloud-ai-video-wan-video` 基于上一步图片生成 {时长}s 视频（fps={fps}，size={尺寸}，镜头描述：{镜头描述}）。  
③ `alicloud-ai-audio-tts` 用 voice={音色} 合成旁白（文本：{旁白文本}，语言：{语言}）。  
④ `alicloud-storage-oss-ossutil` 上传视频与音频到 {oss路径}。  
请输出最终资产的 URL 列表与对应说明。”

2) 客服知识库检索 + 语音应答

模板：
“用 `alicloud-ai-text-document-mind` 解析文档（URL：{文档URL}）得到结构化内容；  
再用 `alicloud-ai-search-dashvector` 建库并入库；  
最后根据用户问题：{用户问题} 做 topk={topk} 检索并用 `alicloud-ai-audio-tts` 生成语音回答（voice={音色}，language={语言}）。  
请返回文本答案 + 语音 URL。”

3) 内容审核 + 发布

模板：
“用 `alicloud-security-content-moderation-green` 审核内容（类型：{文本|图片|视频}，内容：{内容/URL}）。  
若通过则用 `alicloud-storage-oss-ossutil` 上传到 {oss路径} 并返回公开链接；  
若不通过，请给出原因与建议替换文案。”

4) 站点日志排障 + 自动告警

模板：
“用 `alicloud-observability-sls-log-query` 查询 {时间范围} 内的错误（query：{查询语句}），  
按 {聚合字段} 统计并判断是否超过阈值 {阈值}；  
若超过，调用 `alicloud-compute-fc-serverless-devs` 触发告警函数（函数名：{函数名}，参数：{告警参数}）。  
输出统计结果与告警触发状态。”

5) 多语言内容生产（生成 → 翻译 → 配音）

模板：
“用 `alicloud-ai-content-aicontent` 生成主题文案（主题：{主题}，风格：{风格}，长度：{长度}）；  
用 `alicloud-ai-translation-anytrans` 翻译为 {目标语言}；  
用 `alicloud-ai-audio-tts` 生成配音（voice={音色}，language={语言}）。  
输出：原文、译文、语音 URL。”

6) 训练素材清洗与归档

模板：
“对素材进行合规检查：`alicloud-security-content-moderation-green`（内容：{内容/URL}）。  
若通过，用 `alicloud-ai-text-document-mind` 做结构化抽取（如适用）；  
最终用 `alicloud-storage-oss-ossutil` 归档到 {oss路径}，返回归档清单与 URL。”

7) 日志指标分析报表

模板：
“用 `alicloud-observability-sls-log-query` 在 {时间范围} 内执行查询：{query|analysis}，  
按 {维度} 输出统计表；  
再用 `alicloud-data-analytics-dataanalysisgbi` 生成可视化报表摘要（指标：{指标列表}，维度：{维度}）。  
输出关键指标与报表摘要。”

8) 业务搜索与推荐

模板：
“先用 `alicloud-ai-search-dashvector` 基于用户意图向量检索（topk={topk}，filter={过滤条件}），  
再用 `alicloud-ai-recommend-airec` 对结果进行排序与补充推荐（策略：{策略}）。  
输出最终推荐列表与理由。”

9) 企业通话场景（呼叫中心 + 智能客服 + 语音）

模板：
“用 `alicloud-ai-cloud-call-center` 创建/路由来电（号码：{号码}，路由策略：{策略}）；  
用 `alicloud-ai-chatbot` 给出 FAQ 命中或转人工判断；  
用 `alicloud-ai-audio-tts` 播报回复（voice={音色}，language={语言}）。  
输出最终话术与语音 URL。”

10) 安全合规闭环（密钥 + 审计）

模板：
“用 `alicloud-security-kms` 创建/管理密钥（用途：{用途}，别名：{别名}）；  
结合 `alicloud-observability-sls-log-query` 查询 {时间范围} 内的安全审计日志（query：{查询语句}）；  
如发现异常，给出处理建议或触发告警（函数：{函数名}）。  
输出密钥状态、审计结果与处置建议。”

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

## 技能索引

<!-- SKILL_INDEX_BEGIN -->
| 分类 | 技能 | 技能描述 | 路径 |
| --- | --- | --- | --- |
| ai/audio | alicloud-ai-audio-tts | 使用 Model Studio DashScope Qwen TTS 模型生成人声语音，适用于文本转语音与配音场景。 | `skills/ai/audio/alicloud-ai-audio-tts` |
| ai/audio | alicloud-ai-audio-tts-realtime | 使用 Alibaba Cloud Model Studio Qwen TTS Realtime 模型进行实时语音合成。 | `skills/ai/audio/alicloud-ai-audio-tts-realtime` |
| ai/audio | alicloud-ai-audio-tts-voice-clone | 使用 Alibaba Cloud Model Studio Qwen TTS VC 模型执行声音克隆流程。 | `skills/ai/audio/alicloud-ai-audio-tts-voice-clone` |
| ai/audio | alicloud-ai-audio-tts-voice-design | 使用 Alibaba Cloud Model Studio Qwen TTS VD 模型执行声音设计流程。 | `skills/ai/audio/alicloud-ai-audio-tts-voice-design` |
| ai/content | alicloud-ai-content-aicontent | 通过 OpenAPI/SDK 管理 Alibaba Cloud AIContent (AiContent)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/content/alicloud-ai-content-aicontent` |
| ai/content | alicloud-ai-content-aimiaobi | 通过 OpenAPI/SDK 管理 Alibaba Cloud Quan Miao (AiMiaoBi)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/content/alicloud-ai-content-aimiaobi` |
| ai/entry | alicloud-ai-entry-modelstudio | 将 Alibaba Cloud Model Studio 请求路由到最合适的本地技能（图像、视频、TTS 等）。 | `skills/ai/entry/alicloud-ai-entry-modelstudio` |
| ai/entry | alicloud-ai-entry-modelstudio-test | 为仓库中的 Model Studio 技能执行最小化测试矩阵并记录结果。 | `skills/ai/entry/alicloud-ai-entry-modelstudio-test` |
| ai/image | alicloud-ai-image-qwen-image | 通过 Model Studio DashScope SDK 进行图像生成，覆盖 prompt、size、seed 等核心参数。 | `skills/ai/image/alicloud-ai-image-qwen-image` |
| ai/image | alicloud-ai-image-qwen-image-edit | 技能 `alicloud-ai-image-qwen-image-edit` 的能力说明，详见对应 SKILL.md。 | `skills/ai/image/alicloud-ai-image-qwen-image-edit` |
| ai/image | alicloud-ai-image-zimage-turbo | 技能 `alicloud-ai-image-zimage-turbo` 的能力说明，详见对应 SKILL.md。 | `skills/ai/image/alicloud-ai-image-zimage-turbo` |
| ai/misc | alicloud-ai-misc-crawl-and-skill | 刷新 Model Studio 模型抓取结果并重新生成派生摘要及相关技能内容。 | `skills/ai/misc/alicloud-ai-misc-crawl-and-skill` |
| ai/platform | alicloud-ai-pai-aiworkspace | 通过 OpenAPI/SDK 管理 Alibaba Cloud Platform for Artificial Intelligence PAI - AIWorkspace (AIWorkSpace)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/platform/alicloud-ai-pai-aiworkspace` |
| ai/recommendation | alicloud-ai-recommend-airec | 通过 OpenAPI/SDK 管理 Alibaba Cloud AIRec (Airec)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/recommendation/alicloud-ai-recommend-airec` |
| ai/search | alicloud-ai-search-dashvector | 使用 Python SDK 构建 DashVector 向量检索能力，支持集合创建、写入与相似度查询。 | `skills/ai/search/alicloud-ai-search-dashvector` |
| ai/search | alicloud-ai-search-milvus | 使用 PyMilvus 对接 AliCloud Milvus（Serverless），用于向量写入与相似度检索。 | `skills/ai/search/alicloud-ai-search-milvus` |
| ai/search | alicloud-ai-search-opensearch | 通过 Python SDK（ha3engine）使用 OpenSearch 向量检索版，支持文档写入与检索。 | `skills/ai/search/alicloud-ai-search-opensearch` |
| ai/service | alicloud-ai-chatbot | 通过 OpenAPI/SDK 管理 Alibaba Cloud beebot (Chatbot)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/service/alicloud-ai-chatbot` |
| ai/service | alicloud-ai-cloud-call-center | 通过 OpenAPI/SDK 管理 Alibaba Cloud Cloud Call Center (CCC)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/service/alicloud-ai-cloud-call-center` |
| ai/service | alicloud-ai-contactcenter-ai | 通过 OpenAPI/SDK 管理 Alibaba Cloud Contact Center AI (ContactCenterAI)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/service/alicloud-ai-contactcenter-ai` |
| ai/text | alicloud-ai-text-document-mind | 通过 Node.js SDK 使用 Document Mind（DocMind）执行文档解析任务并轮询结果。 | `skills/ai/text/alicloud-ai-text-document-mind` |
| ai/translation | alicloud-ai-translation-anytrans | 通过 OpenAPI/SDK 管理 Alibaba Cloud TongyiTranslate (AnyTrans)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/translation/alicloud-ai-translation-anytrans` |
| ai/video | alicloud-ai-video-wan-r2v | 技能 `alicloud-ai-video-wan-r2v` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/alicloud-ai-video-wan-r2v` |
| ai/video | alicloud-ai-video-wan-video | 通过 Model Studio DashScope SDK 进行视频生成，支持时长、帧率、尺寸等参数控制。 | `skills/ai/video/alicloud-ai-video-wan-video` |
| backup/alicloud-backup-bdrc | alicloud-backup-bdrc | 通过 OpenAPI/SDK 管理 Alibaba Cloud Backup and Disaster Recovery Center (BDRC)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/backup/alicloud-backup-bdrc` |
| backup/alicloud-backup-hbr | alicloud-backup-hbr | 通过 OpenAPI/SDK 管理 Alibaba Cloud Cloud Backup (hbr)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/backup/alicloud-backup-hbr` |
| compute/ecs | alicloud-compute-ecs | 技能 `alicloud-compute-ecs` 的能力说明，详见对应 SKILL.md。 | `skills/compute/ecs/alicloud-compute-ecs` |
| compute/fc | alicloud-compute-fc-agentrun | 通过 OpenAPI 管理 Function Compute AgentRun 资源，支持运行时、端点与状态查询。 | `skills/compute/fc/alicloud-compute-fc-agentrun` |
| compute/fc | alicloud-compute-fc-serverless-devs | 技能 `alicloud-compute-fc-serverless-devs` 的能力说明，详见对应 SKILL.md。 | `skills/compute/fc/alicloud-compute-fc-serverless-devs` |
| compute/swas | alicloud-compute-swas-open | 技能 `alicloud-compute-swas-open` 的能力说明，详见对应 SKILL.md。 | `skills/compute/swas/alicloud-compute-swas-open` |
| data-analytics/alicloud-data-analytics-dataanalysisgbi | alicloud-data-analytics-dataanalysisgbi | 通过 OpenAPI/SDK 管理 Alibaba Cloud DataAnalysisGBI (DataAnalysisGBI)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/data-analytics/alicloud-data-analytics-dataanalysisgbi` |
| data-lake/alicloud-data-lake-dlf | alicloud-data-lake-dlf | 通过 OpenAPI/SDK 管理 Alibaba Cloud Data Lake Formation (DataLake)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/data-lake/alicloud-data-lake-dlf` |
| data-lake/alicloud-data-lake-dlf-next | alicloud-data-lake-dlf-next | 通过 OpenAPI/SDK 管理 Alibaba Cloud Data Lake Formation (DlfNext)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/data-lake/alicloud-data-lake-dlf-next` |
| database/analyticdb | alicloud-database-analyticdb-mysql | 通过 OpenAPI/SDK 管理 Alibaba Cloud AnalyticDB for MySQL (adb)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/database/analyticdb/alicloud-database-analyticdb-mysql` |
| database/rds | alicloud-database-rds-supabase | 通过 OpenAPI 管理 Alibaba Cloud RDS Supabase，覆盖实例生命周期与关键配置操作。 | `skills/database/rds/alicloud-database-rds-supabase` |
| media/video | alicloud-media-video-translation | 通过 OpenAPI 创建和管理 Alibaba Cloud IMS 视频翻译任务，支持字幕、语音与人脸相关配置。 | `skills/media/video/alicloud-media-video-translation` |
| network/dns | alicloud-network-dns-cli | Alibaba Cloud DNS（Alidns）CLI 技能。 | `skills/network/dns/alicloud-network-dns-cli` |
| observability/sls | alicloud-observability-sls-log-query | 技能 `alicloud-observability-sls-log-query` 的能力说明，详见对应 SKILL.md。 | `skills/observability/sls/alicloud-observability-sls-log-query` |
| platform/docs | alicloud-platform-docs-api-review | 自动评审最新 Alibaba Cloud 产品文档与 OpenAPI 文档，并输出优先级建议与证据。 | `skills/platform/docs/alicloud-platform-docs-api-review` |
| platform/docs | alicloud-platform-multicloud-docs-api-benchmark | 对阿里云及主流云厂商同类产品文档与 API 文档进行基准对比并给出改进建议。 | `skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark` |
| platform/openapi | alicloud-platform-openapi-product-api-discovery | 发现并对齐 Alibaba Cloud 产品目录与 OpenAPI 元数据，用于覆盖分析和技能规划。 | `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery` |
| security/content | alicloud-security-content-moderation-green | 通过 OpenAPI/SDK 管理 Alibaba Cloud Content Moderation (Green)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/security/content/alicloud-security-content-moderation-green` |
| security/firewall | alicloud-security-cloudfw | 通过 OpenAPI/SDK 管理 Alibaba Cloud Cloud Firewall (Cloudfw)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/security/firewall/alicloud-security-cloudfw` |
| security/host | alicloud-security-center-sas | 通过 OpenAPI/SDK 管理 Alibaba Cloud Security Center (Sas)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/security/host/alicloud-security-center-sas` |
| security/identity | alicloud-security-id-verification-cloudauth | 通过 OpenAPI/SDK 管理 Alibaba Cloud ID Verification (Cloudauth)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/security/identity/alicloud-security-id-verification-cloudauth` |
| security/key-management | alicloud-security-kms | 通过 OpenAPI/SDK 管理 Alibaba Cloud KeyManagementService (Kms)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/security/key-management/alicloud-security-kms` |
| storage/oss | alicloud-storage-oss-ossutil | Alibaba Cloud OSS CLI（ossutil 2.0）技能，支持命令行安装、配置与 OSS 资源操作。 | `skills/storage/oss/alicloud-storage-oss-ossutil` |
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
