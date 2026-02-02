# Alibaba Cloud 核心 Claude Skills

简体中文 | [English](README.en.md) | [繁體中文](README.zh-TW.md)

Cloud Mind：把世界级云基建，折叠进你的对话框。


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

## 可做的 Demo 与提示词（示例）

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
