# Alibaba Cloud 核心 Claude Skills

简体中文 | [English](README.en.md) | [繁體中文](README.zh-TW.md)

这是一个精选的 **Alibaba Cloud 核心 Claude skills** 集合，覆盖关键产品线，
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

- `ecs/alicloud-compute-ecs`
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

## 技能一览（中文简介）

| Category | Skill | 中文简介 | Path |
| --- | --- | --- | --- |
| ai/audio | alicloud-ai-audio-tts | Qwen TTS 语音合成，文本转语音与配音生成。 | `skills/ai/audio/alicloud-ai-audio-tts` |
| ai/content | alicloud-ai-content-aicontent | AIContent 内容生成/管理 OpenAPI。 | `skills/ai/content/alicloud-ai-content-aicontent` |
| ai/content | alicloud-ai-content-aimiaobi | 千妙文案（AiMiaoBi）OpenAPI 管理。 | `skills/ai/content/alicloud-ai-content-aimiaobi` |
| ai/entry | alicloud-ai-entry-modelstudio | Model Studio 能力路由入口（图/音/视频）。 | `skills/ai/entry/alicloud-ai-entry-modelstudio` |
| ai/entry | alicloud-ai-entry-modelstudio-test | Model Studio 技能最小测试矩阵执行。 | `skills/ai/entry/alicloud-ai-entry-modelstudio-test` |
| ai/image | alicloud-ai-image-qwen-image | Qwen Image 图像生成与参数映射。 | `skills/ai/image/alicloud-ai-image-qwen-image` |
| ai/misc | alicloud-ai-misc-crawl-and-skill | 刷新模型抓取并重生成 AI 技能。 | `skills/ai/misc/alicloud-ai-misc-crawl-and-skill` |
| ai/platform | alicloud-ai-pai-aiworkspace | PAI AIWorkspace OpenAPI 管理。 | `skills/ai/platform/alicloud-ai-pai-aiworkspace` |
| ai/recommendation | alicloud-ai-recommend-airec | AIRec 推荐系统 OpenAPI 管理。 | `skills/ai/recommendation/alicloud-ai-recommend-airec` |
| ai/search | alicloud-ai-search-dashvector | DashVector 向量检索（Python SDK）。 | `skills/ai/search/alicloud-ai-search-dashvector` |
| ai/search | alicloud-ai-search-milvus | Milvus Serverless 向量检索（PyMilvus）。 | `skills/ai/search/alicloud-ai-search-milvus` |
| ai/search | alicloud-ai-search-opensearch | OpenSearch 向量检索与 HA/SQL 查询。 | `skills/ai/search/alicloud-ai-search-opensearch` |
| ai/service | alicloud-ai-chatbot | beebot 机器人 OpenAPI 管理与排查。 | `skills/ai/service/alicloud-ai-chatbot` |
| ai/service | alicloud-ai-cloud-call-center | 云呼叫中心 CCC 的 OpenAPI 资源管理。 | `skills/ai/service/alicloud-ai-cloud-call-center` |
| ai/service | alicloud-ai-contactcenter-ai | Contact Center AI 资源管理与排查。 | `skills/ai/service/alicloud-ai-contactcenter-ai` |
| ai/text | alicloud-ai-text-document-mind | DocMind 文档解析任务提交与轮询。 | `skills/ai/text/alicloud-ai-text-document-mind` |
| ai/translation | alicloud-ai-translation-anytrans | 通义翻译 AnyTrans OpenAPI 管理。 | `skills/ai/translation/alicloud-ai-translation-anytrans` |
| ai/video | alicloud-ai-video-wan-video | Wan 视频生成（DashScope SDK）。 | `skills/ai/video/alicloud-ai-video-wan-video` |
| backup/alicloud-backup-bdrc | alicloud-backup-bdrc | 备份与容灾中心 BDRC OpenAPI 管理。 | `skills/backup/alicloud-backup-bdrc` |
| backup/alicloud-backup-hbr | alicloud-backup-hbr | 云备份 HBR OpenAPI 管理。 | `skills/backup/alicloud-backup-hbr` |
| compute/ecs | alicloud-compute-ecs | ECS 实例/磁盘/快照/镜像等 OpenAPI 管理。 | `skills/compute/ecs/alicloud-compute-ecs` |
| compute/fc | alicloud-compute-fc-agentrun | 函数计算 AgentRun 资源管理。 | `skills/compute/fc/alicloud-compute-fc-agentrun` |
| compute/fc | alicloud-compute-fc-serverless-devs | FC 3.0 Serverless Devs 安装与部署。 | `skills/compute/fc/alicloud-compute-fc-serverless-devs` |
| compute/swas | alicloud-compute-swas-open | 轻量应用服务器 SWAS 全量资源管理。 | `skills/compute/swas/alicloud-compute-swas-open` |
| data-analytics/alicloud-data-analytics-dataanalysisgbi | alicloud-data-analytics-dataanalysisgbi | DataAnalysisGBI OpenAPI 管理。 | `skills/data-analytics/alicloud-data-analytics-dataanalysisgbi` |
| data-lake/alicloud-data-lake-dlf | alicloud-data-lake-dlf | Data Lake Formation OpenAPI 管理。 | `skills/data-lake/alicloud-data-lake-dlf` |
| data-lake/alicloud-data-lake-dlf-next | alicloud-data-lake-dlf-next | DlfNext OpenAPI 管理。 | `skills/data-lake/alicloud-data-lake-dlf-next` |
| database/analyticdb | alicloud-database-analyticdb-mysql | AnalyticDB MySQL OpenAPI 管理。 | `skills/database/analyticdb/alicloud-database-analyticdb-mysql` |
| database/rds | alicloud-database-rds-supabase | RDS Supabase OpenAPI 管理与配置。 | `skills/database/rds/alicloud-database-rds-supabase` |
| media/video | alicloud-media-video-translation | 视频翻译任务提交与状态轮询。 | `skills/media/video/alicloud-media-video-translation` |
| network/dns | alicloud-network-dns-cli | 阿里云 DNS 记录查询/添加/更新。 | `skills/network/dns/alicloud-network-dns-cli` |
| observability/sls | alicloud-observability-sls-log-query | SLS 日志检索与排障查询。 | `skills/observability/sls/alicloud-observability-sls-log-query` |
| platform/openapi | alicloud-platform-openapi-product-api-discovery | 阿里云产品目录与 OpenAPI 覆盖分析。 | `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery` |
| security/content | alicloud-security-content-moderation-green | 内容安全 Green OpenAPI 管理。 | `skills/security/content/alicloud-security-content-moderation-green` |
| security/firewall | alicloud-security-cloudfw | 云防火墙 Cloudfw OpenAPI 管理。 | `skills/security/firewall/alicloud-security-cloudfw` |
| security/host | alicloud-security-center-sas | 安全中心 Sas OpenAPI 管理。 | `skills/security/host/alicloud-security-center-sas` |
| security/identity | alicloud-security-id-verification-cloudauth | 身份认证 Cloudauth OpenAPI 管理。 | `skills/security/identity/alicloud-security-id-verification-cloudauth` |
| security/key-management | alicloud-security-kms | KMS 密钥管理 OpenAPI。 | `skills/security/key-management/alicloud-security-kms` |
| storage/oss | alicloud-storage-oss-ossutil | OSS 命令行 ossutil 使用与配置。 | `skills/storage/oss/alicloud-storage-oss-ossutil` |

## 技能索引（路径）

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

## 典型场景（覆盖多数技能）

1. AI 内容生产流水线：文生图/视频/配音 → 生成素材 → OSS 上传 → SLS 记录 → 内容安全审核  
覆盖：`alicloud-ai-image-qwen-image`、`alicloud-ai-video-wan-video`、`alicloud-ai-audio-tts`、`alicloud-storage-oss-ossutil`、`alicloud-observability-sls-log-query`、`alicloud-security-content-moderation-green`
提示词样例：`examples/prompts/ai-content-pipeline.md`

2. 智能检索/RAG 系统：文档解析 → 向量入库 → 检索 → 结果回传  
覆盖：`alicloud-ai-text-document-mind`、`alicloud-ai-search-dashvector`/`alicloud-ai-search-opensearch`/`alicloud-ai-search-milvus`
提示词样例：`examples/prompts/rag-pipeline.md`

3. 企业客服与呼叫中心：智能客服/呼叫中心管理 → 资源配置与监控  
覆盖：`alicloud-ai-chatbot`、`alicloud-ai-cloud-call-center`、`alicloud-ai-contactcenter-ai`、`alicloud-observability-sls-log-query`
提示词样例：`examples/prompts/contact-center.md`

4. 数据平台与分析：数据湖治理 → 数据分析 → 权限与密钥管理  
覆盖：`alicloud-data-lake-dlf`、`alicloud-data-lake-dlf-next`、`alicloud-data-analytics-dataanalysisgbi`、`alicloud-security-kms`
提示词样例：`examples/prompts/data-platform-analytics.md`

5. 计算与基础设施运维：ECS/SWAS 实例管理 → 日志排查 → 备份与容灾  
覆盖：`alicloud-compute-ecs`、`alicloud-compute-swas-open`、`alicloud-observability-sls-log-query`、`alicloud-backup-hbr`/`alicloud-backup-bdrc`
提示词样例：`examples/prompts/infra-ops.md`

6. Serverless 部署与运行：FC 项目初始化 → 部署 → 运行状态排查  
覆盖：`alicloud-compute-fc-serverless-devs`、`alicloud-compute-fc-agentrun`、`alicloud-observability-sls-log-query`
提示词样例：`examples/prompts/serverless-devops.md`

7. 产品与 API 盘点：产品清单 → API 覆盖 → 新技能规划  
覆盖：`alicloud-platform-openapi-product-api-discovery`
提示词样例：`examples/prompts/product-api-discovery.md`

## 备注

- 本仓库聚焦 Alibaba Cloud 的核心能力及其 Claude skill 实现。
- 后续可在 `skills/` 下持续扩展更多技能。

## 输出规范

- 所有临时文件与生成物必须写入 `output/`。
- 按技能划分子目录，例如 `output/<skill>/...`。
- `output/` 被 git 忽略，不允许提交。
