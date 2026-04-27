# Alibaba Cloud 核心 AI Agent Skills

## 语言

[English](README.md) | **简体中文（当前）** | [繁體中文](README.zh-TW.md)

快速入口：[快速开始](#快速开始) | [技能索引](#技能索引)

Cloud Mind：把世界级云基建，折叠进你的AI对话框。


这是一个精选的 **Alibaba Cloud 核心 AI Agent skills** 集合，覆盖关键产品线，
包括 Model Studio、OSS、ECS 等。

## 最新覆盖

- DashScope 视频生成能力现已覆盖 Wan、Kling v3、Vidu、Animate-Move 与视频风格重绘工作流。
- 网络运维能力新增 `aliyun-vpc-manage`，可处理 VPC/VSwitch 盘点、创建、删除与可用区查询。
- 根目录三份 README 的技能索引统一从 `skills/**/SKILL.md` 自动生成，便于随技能演进同步更新。

## 快速开始

推荐安装（一次性安装全部、跳过确认、强制覆盖）：

```bash
npx skills add cinience/alicloud-skills --all -y --force
```

如果仍出现选择界面，按 `a` 全选后回车提交。

建议使用 RAM 用户/角色并遵循最小权限原则，避免在代码或命令行中明文暴露 AK。

优先使用环境变量：

```bash
export ALIBABACLOUD_ACCESS_KEY_ID="你的AK"
export ALIBABACLOUD_ACCESS_KEY_SECRET="你的SK"
export ALIBABACLOUD_SECURITY_TOKEN="你的STS Token" # 可选，使用 STS 时填写
export ALIBABACLOUD_REGION_ID="cn-beijing"
export DASHSCOPE_API_KEY="你的DashScope API Key"
```

环境变量优先生效；若未设置环境变量，才会读取 `~/.alibabacloud/credentials`。`ALIBABACLOUD_REGION_ID` 可作为默认 Region；未设置时可在执行时选择最合理的 Region，无法判断则需要询问用户。

默认推荐使用 `ALIBABACLOUD_*` 前缀。本仓库的运行时脚本也兼容历史上的 `ALIBABA_CLOUD_*` 和 `ALICLOUD_*` 前缀。

若未设置环境变量，可使用标准 CLI/SDK 配置文件：

`~/.alibabacloud/credentials`

```ini
[default]
type = access_key
access_key_id = 你的AK
access_key_secret = 你的SK
dashscope_api_key = 你的DashScope API Key
```

如使用 STS，请设置 `type = sts` 并补充 `security_token = 你的STS Token`。

## 示例（文档评审与跨云对比）

1) 产品文档 + API 文档评审

- 提示词：
  “用 `aliyun-platform-docs-review` 评审产品 `百炼` 的产品文档与 API 文档，输出 P0/P1/P2 改进建议并附证据链接。”

2) 跨云同类产品对比

- 提示词：
  “用 `aliyun-platform-docs-benchmark` 对 `百炼` 做跨云对比（阿里云/AWS/Azure/GCP/腾讯云/火山引擎/华为云），使用 `llm-platform` 预设，输出评分表与改进建议。”

## 独立技能与提示词（示例）

1) 文生图（Qwen Image）

- Demo：生成图片  
- 提示词：  
  “用 `aliyun-qwen-image` 生成 1024*1024 海报图，主题是极简咖啡，输出文件名 poster.png。”

2) 图生视频（Wan Video）

- Demo：用一张参考图生成 4 秒视频（需提供可访问的图片 URL）
- 提示词：  
  “用 `aliyun-wan-video`，参考图 `https://.../scene.png`，生成 4 秒 24fps 1280*720 的镜头，提示词：清晨城市延时摄影。”

3) VPC 盘点与规划

- Demo：列出某地域 VPC 与 VSwitch，并给出新建规划建议
- 提示词：
  “用 `aliyun-vpc-manage` 列出 `cn-hangzhou` 下所有 VPC 和 VSwitch，并为双可用区生产环境建议一个 `/16` VPC 网段和 `/24` VSwitch 划分方案。”

4) Kling V3 视频生成

- Demo：用 DashScope Kling 生成分镜或图生视频任务
- 提示词：
  “用 `aliyun-kling-video` 生成一个 5 秒 16:9 视频，提示词是 `a neon-lit alley in the rain`，并说明什么时候该选 omni 模型而不是 standard 模型。”

5) Vidu 视频生成

- Demo：比较文生视频与首尾帧关键帧视频的最小请求体
- 提示词：
  “用 `aliyun-vidu-video` 展示 `vidu/viduq3-pro_text2video` 和 `vidu/viduq3-pro_start-end2video` 的最小请求体，并附推荐的 `resolution`、`size` 与 `duration`。”

6) 文字转语音（Qwen TTS）

- Demo：用 DashScope 生成音频  
- 提示词：  
  “用 `aliyun-qwen-tts` 把这段话合成语音，voice=Cherry，language=English，输出音频 URL。”

7) 文档结构解析（DocMind）

- Demo：解析 PDF 的标题/段落结构  
- 提示词：  
  “用 `aliyun-docmind-extract` 解析这个 PDF（URL: ...），拿到结构化结果。”

8) 向量检索（DashVector）

- Demo：创建集合、写入、查询  
- 提示词：  
  “用 `aliyun-dashvector-search` 创建 dimension=768 的集合，写入 2 条文档后做 topk=5 查询。”

9) OSS 上传/同步（ossutil）

- Demo：上传本地文件到 OSS  
- 提示词：  
  “用 `aliyun-oss-ossutil` 把 ./local.txt 上传到 oss://xxx/path/。”

10) SLS 日志排查

- Demo：最近 15 分钟查 500 错误  
- 提示词：  
  “用 `aliyun-sls-log-query` 查最近 15 分钟 500 错误，并按状态聚合。”

11) FC 3.0 快速部署（Serverless Devs）

- Demo：初始化 Python 函数并部署  
- 提示词：  
  “用 `aliyun-fc-serverless-devs` 初始化 FC 3.0 Python 项目并部署。”

12) 内容安全（Green）

- Demo：通过 OpenAPI 发现/调用内容审核 API  
- 提示词：  
  “用 `aliyun-green-moderation` 先列出可用 API，再给我一条文本检测的最小参数示例。”

13) KMS 密钥管理

- Demo：列出密钥或创建密钥  
- 提示词：  
  “用 `aliyun-kms-manage` 给出创建对称密钥的 OpenAPI 参数模板。”

14) 产品文档与 API 文档自动评审

- Demo：按产品名自动抓取最新文档并给出改进建议
- 提示词：
  “用 `aliyun-platform-docs-review` 评审产品 `百炼` 的产品文档和 API 文档，输出 P0/P1/P2 改进建议与证据链接。”

15) 跨云同类产品文档/API 对比

- Demo：对比阿里云/AWS/Azure/GCP/腾讯云/火山引擎/华为云同类产品
- 提示词：
  “用 `aliyun-platform-docs-benchmark` 对 `百炼` 做跨云同类产品文档/API 对比，并用 `llm-platform` 预设输出评分表与差距建议。”

## 组合方案（场景与提示词模板）

1) 营销素材流水线（图 → 视频 → 配音 → 上传）

模板：
“按以下流程串联技能：  
① `aliyun-qwen-image` 生成海报图（主题：{主题}，尺寸：{尺寸}）。  
② `aliyun-wan-video` 基于上一步图片生成 {时长}s 视频（fps={fps}，size={尺寸}，镜头描述：{镜头描述}）。  
③ `aliyun-qwen-tts` 用 voice={音色} 合成旁白（文本：{旁白文本}，语言：{语言}）。  
④ `aliyun-oss-ossutil` 上传视频与音频到 {oss路径}。  
请输出最终资产的 URL 列表与对应说明。”

2) 客服知识库检索 + 语音应答

模板：
“用 `aliyun-docmind-extract` 解析文档（URL：{文档URL}）得到结构化内容；  
再用 `aliyun-dashvector-search` 建库并入库；  
最后根据用户问题：{用户问题} 做 topk={topk} 检索并用 `aliyun-qwen-tts` 生成语音回答（voice={音色}，language={语言}）。  
请返回文本答案 + 语音 URL。”

3) 内容审核 + 发布

模板：
“用 `aliyun-green-moderation` 审核内容（类型：{文本|图片|视频}，内容：{内容/URL}）。  
若通过则用 `aliyun-oss-ossutil` 上传到 {oss路径} 并返回公开链接；  
若不通过，请给出原因与建议替换文案。”

4) 站点日志排障 + 自动告警

模板：
“用 `aliyun-sls-log-query` 查询 {时间范围} 内的错误（query：{查询语句}），  
按 {聚合字段} 统计并判断是否超过阈值 {阈值}；  
若超过，调用 `aliyun-fc-serverless-devs` 触发告警函数（函数名：{函数名}，参数：{告警参数}）。  
输出统计结果与告警触发状态。”

5) 多语言内容生产（生成 → 翻译 → 配音）

模板：
“用 `aliyun-aicontent-generate` 生成主题文案（主题：{主题}，风格：{风格}，长度：{长度}）；  
用 `aliyun-anytrans-translate` 翻译为 {目标语言}；  
用 `aliyun-qwen-tts` 生成配音（voice={音色}，language={语言}）。  
输出：原文、译文、语音 URL。”

6) 训练素材清洗与归档

模板：
“对素材进行合规检查：`aliyun-green-moderation`（内容：{内容/URL}）。  
若通过，用 `aliyun-docmind-extract` 做结构化抽取（如适用）；  
最终用 `aliyun-oss-ossutil` 归档到 {oss路径}，返回归档清单与 URL。”

7) 日志指标分析报表

模板：
“用 `aliyun-sls-log-query` 在 {时间范围} 内执行查询：{query|analysis}，  
按 {维度} 输出统计表；  
再用 `aliyun-gbi-analytics` 生成可视化报表摘要（指标：{指标列表}，维度：{维度}）。  
输出关键指标与报表摘要。”

8) 业务搜索与推荐

模板：
“先用 `aliyun-dashvector-search` 基于用户意图向量检索（topk={topk}，filter={过滤条件}），  
再用 `aliyun-airec-manage` 对结果进行排序与补充推荐（策略：{策略}）。  
输出最终推荐列表与理由。”

9) 企业通话场景（呼叫中心 + 智能客服 + 语音）

模板：
“用 `aliyun-ccc-manage` 创建/路由来电（号码：{号码}，路由策略：{策略}）；  
用 `aliyun-chatbot-manage` 给出 FAQ 命中或转人工判断；  
用 `aliyun-qwen-tts` 播报回复（voice={音色}，language={语言}）。  
输出最终话术与语音 URL。”

10) 安全合规闭环（密钥 + 审计）

模板：
“用 `aliyun-kms-manage` 创建/管理密钥（用途：{用途}，别名：{别名}）；  
结合 `aliyun-sls-log-query` 查询 {时间范围} 内的安全审计日志（query：{查询语句}）；  
如发现异常，给出处理建议或触发告警（函数：{函数名}）。  
输出密钥状态、审计结果与处置建议。”

## 项目结构

- `skills/` — 按产品线归类的技能源目录
  - `ai/` — Model Studio（按能力分组）
    - `text/` `image/` `audio/` `video/` `multimodal/` `search/` `recommendation/` `content/` `service/` `translation/` `platform/` `misc/` `entry/`
  - `backup/` — BDRC / HBR
  - `compute/` — ECS / FC / SWAS
  - `data-analytics/` — DataAnalysisGBI
  - `data-lake/` — DLF
  - `database/` — AnalyticDB / RDS
  - `media/` — 智能媒体创作
  - `network/` — CDN / DNS / VPC / ALB / ESA
  - `observability/` — SLS
  - `platform/` — CLI / OpenAPI / 文档工作流
  - `security/` — 内容安全 / 防火墙 / 主机安全 / 身份 / 密钥管理
  - `storage/` — OSS
- `examples/` — 端到端故事与使用流程示例

## 品牌别名

- `modelstudio/` — 指向 `skills/ai/` 的软链接（海外品牌）

## 技能索引

<!-- SKILL_INDEX_BEGIN -->
| 分类 | 技能 | 技能描述 | 路径 |
| --- | --- | --- | --- |
| ai/audio | aliyun-cosyvoice-voice-clone | 技能 `aliyun-cosyvoice-voice-clone` 的能力说明，详见对应 SKILL.md。 | `skills/ai/audio/aliyun-cosyvoice-voice-clone` |
| ai/audio | aliyun-cosyvoice-voice-design | 技能 `aliyun-cosyvoice-voice-design` 的能力说明，详见对应 SKILL.md。 | `skills/ai/audio/aliyun-cosyvoice-voice-design` |
| ai/audio | aliyun-qwen-asr | 使用 Alibaba Cloud Model Studio Qwen ASR 模型进行非实时语音识别与转写，支持短音频同步识别和长音频异步转写。 | `skills/ai/audio/aliyun-qwen-asr` |
| ai/audio | aliyun-qwen-asr-realtime | 技能 `aliyun-qwen-asr-realtime` 的能力说明，详见对应 SKILL.md。 | `skills/ai/audio/aliyun-qwen-asr-realtime` |
| ai/audio | aliyun-qwen-livetranslate | 技能 `aliyun-qwen-livetranslate` 的能力说明，详见对应 SKILL.md。 | `skills/ai/audio/aliyun-qwen-livetranslate` |
| ai/audio | aliyun-qwen-tts | 使用 Model Studio DashScope Qwen TTS 模型生成人声语音，适用于文本转语音与配音场景。 | `skills/ai/audio/aliyun-qwen-tts` |
| ai/audio | aliyun-qwen-tts-realtime | 使用 Alibaba Cloud Model Studio Qwen TTS Realtime 模型进行实时语音合成。 | `skills/ai/audio/aliyun-qwen-tts-realtime` |
| ai/audio | aliyun-qwen-tts-voice-clone | 使用 Alibaba Cloud Model Studio Qwen TTS VC 模型执行声音克隆流程。 | `skills/ai/audio/aliyun-qwen-tts-voice-clone` |
| ai/audio | aliyun-qwen-tts-voice-design | 使用 Alibaba Cloud Model Studio Qwen TTS VD 模型执行声音设计流程。 | `skills/ai/audio/aliyun-qwen-tts-voice-design` |
| ai/code | aliyun-qwen-coder | 技能 `aliyun-qwen-coder` 的能力说明，详见对应 SKILL.md。 | `skills/ai/code/aliyun-qwen-coder` |
| ai/content | aliyun-aicontent-generate | 通过 OpenAPI/SDK 管理 Alibaba Cloud AIContent (AiContent)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/content/aliyun-aicontent-generate` |
| ai/content | aliyun-aimiaobi-generate | 通过 OpenAPI/SDK 管理 Alibaba Cloud Quan Miao (AiMiaoBi)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/content/aliyun-aimiaobi-generate` |
| ai/entry | aliyun-modelstudio-entry | 将 Alibaba Cloud Model Studio 请求路由到最合适的本地技能（图像、视频、TTS、ASR 等）。 | `skills/ai/entry/aliyun-modelstudio-entry` |
| ai/entry | aliyun-modelstudio-entry-test | 为仓库中的 Model Studio 技能执行最小化测试矩阵并记录结果。 | `skills/ai/entry/aliyun-modelstudio-entry-test` |
| ai/image | aliyun-qwen-image | 通过 Model Studio DashScope SDK 进行图像生成，覆盖 prompt、size、seed 等核心参数。 | `skills/ai/image/aliyun-qwen-image` |
| ai/image | aliyun-qwen-image-edit | 技能 `aliyun-qwen-image-edit` 的能力说明，详见对应 SKILL.md。 | `skills/ai/image/aliyun-qwen-image-edit` |
| ai/image | aliyun-wan-image | 技能 `aliyun-wan-image` 的能力说明，详见对应 SKILL.md。 | `skills/ai/image/aliyun-wan-image` |
| ai/image | aliyun-zimage-turbo | 技能 `aliyun-zimage-turbo` 的能力说明，详见对应 SKILL.md。 | `skills/ai/image/aliyun-zimage-turbo` |
| ai/misc | aliyun-modelstudio-crawl-and-skill | 刷新 Model Studio 模型抓取结果并重新生成派生摘要及相关技能内容。 | `skills/ai/misc/aliyun-modelstudio-crawl-and-skill` |
| ai/multimodal | aliyun-qvq | 技能 `aliyun-qvq` 的能力说明，详见对应 SKILL.md。 | `skills/ai/multimodal/aliyun-qvq` |
| ai/multimodal | aliyun-qwen-ocr | 技能 `aliyun-qwen-ocr` 的能力说明，详见对应 SKILL.md。 | `skills/ai/multimodal/aliyun-qwen-ocr` |
| ai/multimodal | aliyun-qwen-omni | 技能 `aliyun-qwen-omni` 的能力说明，详见对应 SKILL.md。 | `skills/ai/multimodal/aliyun-qwen-omni` |
| ai/multimodal | aliyun-qwen-vl | 技能 `aliyun-qwen-vl` 的能力说明，详见对应 SKILL.md。 | `skills/ai/multimodal/aliyun-qwen-vl` |
| ai/platform | aliyun-pai-workspace | 通过 OpenAPI/SDK 管理 Alibaba Cloud Platform for Artificial Intelligence PAI - AIWorkspace (AIWorkSpace)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/platform/aliyun-pai-workspace` |
| ai/recommendation | aliyun-airec-manage | 通过 OpenAPI/SDK 管理 Alibaba Cloud AIRec (Airec)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/recommendation/aliyun-airec-manage` |
| ai/research | aliyun-qwen-deep-research | 技能 `aliyun-qwen-deep-research` 的能力说明，详见对应 SKILL.md。 | `skills/ai/research/aliyun-qwen-deep-research` |
| ai/search | aliyun-dashvector-search | 使用 Python SDK 构建 DashVector 向量检索能力，支持集合创建、写入与相似度查询。 | `skills/ai/search/aliyun-dashvector-search` |
| ai/search | aliyun-milvus-search | 使用 PyMilvus 对接 AliCloud Milvus（Serverless），用于向量写入与相似度检索。 | `skills/ai/search/aliyun-milvus-search` |
| ai/search | aliyun-opensearch-search | 通过 Python SDK（ha3engine）使用 OpenSearch 向量检索版，支持文档写入与检索。 | `skills/ai/search/aliyun-opensearch-search` |
| ai/search | aliyun-qwen-multimodal-embedding | 技能 `aliyun-qwen-multimodal-embedding` 的能力说明，详见对应 SKILL.md。 | `skills/ai/search/aliyun-qwen-multimodal-embedding` |
| ai/search | aliyun-qwen-rerank | 技能 `aliyun-qwen-rerank` 的能力说明，详见对应 SKILL.md。 | `skills/ai/search/aliyun-qwen-rerank` |
| ai/search | aliyun-qwen-text-embedding | 技能 `aliyun-qwen-text-embedding` 的能力说明，详见对应 SKILL.md。 | `skills/ai/search/aliyun-qwen-text-embedding` |
| ai/service | aliyun-ccai-manage | 通过 OpenAPI/SDK 管理 Alibaba Cloud Contact Center AI (ContactCenterAI)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/service/aliyun-ccai-manage` |
| ai/service | aliyun-ccc-manage | 通过 OpenAPI/SDK 管理 Alibaba Cloud Cloud Call Center (CCC)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/service/aliyun-ccc-manage` |
| ai/service | aliyun-chatbot-manage | 通过 OpenAPI/SDK 管理 Alibaba Cloud beebot (Chatbot)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/service/aliyun-chatbot-manage` |
| ai/text | aliyun-docmind-extract | 通过 Node.js SDK 使用 Document Mind（DocMind）执行文档解析任务并轮询结果。 | `skills/ai/text/aliyun-docmind-extract` |
| ai/text | aliyun-qwen-generation | 技能 `aliyun-qwen-generation` 的能力说明，详见对应 SKILL.md。 | `skills/ai/text/aliyun-qwen-generation` |
| ai/translation | aliyun-anytrans-translate | 通过 OpenAPI/SDK 管理 Alibaba Cloud TongyiTranslate (AnyTrans)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/ai/translation/aliyun-anytrans-translate` |
| ai/video | aliyun-animate-anyone | 技能 `aliyun-animate-anyone` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-animate-anyone` |
| ai/video | aliyun-emo | 技能 `aliyun-emo` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-emo` |
| ai/video | aliyun-emoji | 技能 `aliyun-emoji` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-emoji` |
| ai/video | aliyun-happyhorse-i2v | 使用 DashScope HappyHorse 1.0 图生视频模型（happyhorse-1.0-i2v）从单张首帧图像生成视频，输出宽高比自动跟随首帧。 | `skills/ai/video/aliyun-happyhorse-i2v` |
| ai/video | aliyun-happyhorse-r2v | 使用 DashScope HappyHorse 1.0 参考生视频模型（happyhorse-1.0-r2v）融合 1-9 张参考图像生成视频，prompt 中以 character1..N 引用素材。 | `skills/ai/video/aliyun-happyhorse-r2v` |
| ai/video | aliyun-happyhorse-t2v | 使用 DashScope HappyHorse 1.0 文生视频模型（happyhorse-1.0-t2v）从文本提示生成视频，覆盖分辨率、宽高比、时长等参数与异步任务轮询。 | `skills/ai/video/aliyun-happyhorse-t2v` |
| ai/video | aliyun-happyhorse-videoedit | 使用 DashScope HappyHorse 1.0 视频编辑模型（happyhorse-1.0-video-edit）按指令进行风格变换或局部替换，可附带 0-5 张参考图像与音频保留控制。 | `skills/ai/video/aliyun-happyhorse-videoedit` |
| ai/video | aliyun-kling-video | 使用 DashScope Kling v3 模型生成视频，支持文生视频、图生视频、参考生视频、智能分镜与视频编辑。 | `skills/ai/video/aliyun-kling-video` |
| ai/video | aliyun-liveportrait | 技能 `aliyun-liveportrait` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-liveportrait` |
| ai/video | aliyun-pixverse-generation | 技能 `aliyun-pixverse-generation` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-pixverse-generation` |
| ai/video | aliyun-video-style-repaint | 技能 `aliyun-video-style-repaint` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-video-style-repaint` |
| ai/video | aliyun-videoretalk | 技能 `aliyun-videoretalk` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-videoretalk` |
| ai/video | aliyun-vidu-video | 使用 DashScope Vidu 模型生成视频，覆盖文生视频、首帧图生视频、首尾帧关键帧视频与参考图生视频。 | `skills/ai/video/aliyun-vidu-video` |
| ai/video | aliyun-wan-animate-move | 技能 `aliyun-wan-animate-move` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-wan-animate-move` |
| ai/video | aliyun-wan-digital-human | 技能 `aliyun-wan-digital-human` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-wan-digital-human` |
| ai/video | aliyun-wan-edit | 技能 `aliyun-wan-edit` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-wan-edit` |
| ai/video | aliyun-wan-i2v | 技能 `aliyun-wan-i2v` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-wan-i2v` |
| ai/video | aliyun-wan-r2v | 技能 `aliyun-wan-r2v` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-wan-r2v` |
| ai/video | aliyun-wan-video | 通过 Model Studio DashScope SDK 进行视频生成，支持时长、帧率、尺寸等参数控制。 | `skills/ai/video/aliyun-wan-video` |
| ai/video | aliyun-wan-videoedit | 技能 `aliyun-wan-videoedit` 的能力说明，详见对应 SKILL.md。 | `skills/ai/video/aliyun-wan-videoedit` |
| backup/aliyun-bdrc-backup | aliyun-bdrc-backup | 通过 OpenAPI/SDK 管理 Alibaba Cloud Backup and Disaster Recovery Center (BDRC)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/backup/aliyun-bdrc-backup` |
| backup/aliyun-hbr-backup | aliyun-hbr-backup | 通过 OpenAPI/SDK 管理 Alibaba Cloud Cloud Backup (hbr)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/backup/aliyun-hbr-backup` |
| compute/ecs | aliyun-ecs-manage | 技能 `aliyun-ecs-manage` 的能力说明，详见对应 SKILL.md。 | `skills/compute/ecs/aliyun-ecs-manage` |
| compute/fc | aliyun-fc-agentrun | 通过 OpenAPI 管理 Function Compute AgentRun 资源，支持运行时、端点与状态查询。 | `skills/compute/fc/aliyun-fc-agentrun` |
| compute/fc | aliyun-fc-serverless-devs | 技能 `aliyun-fc-serverless-devs` 的能力说明，详见对应 SKILL.md。 | `skills/compute/fc/aliyun-fc-serverless-devs` |
| compute/swas | aliyun-swas-manage | 技能 `aliyun-swas-manage` 的能力说明，详见对应 SKILL.md。 | `skills/compute/swas/aliyun-swas-manage` |
| data-analytics/aliyun-gbi-analytics | aliyun-gbi-analytics | 通过 OpenAPI/SDK 管理 Alibaba Cloud DataAnalysisGBI (DataAnalysisGBI)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/data-analytics/aliyun-gbi-analytics` |
| data-lake/aliyun-dlf-manage | aliyun-dlf-manage | 通过 OpenAPI/SDK 管理 Alibaba Cloud Data Lake Formation (DataLake)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/data-lake/aliyun-dlf-manage` |
| data-lake/aliyun-dlf-manage-next | aliyun-dlf-manage-next | 通过 OpenAPI/SDK 管理 Alibaba Cloud Data Lake Formation (DlfNext)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/data-lake/aliyun-dlf-manage-next` |
| database/analyticdb | aliyun-adb-mysql | 通过 OpenAPI/SDK 管理 Alibaba Cloud AnalyticDB for MySQL (adb)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/database/analyticdb/aliyun-adb-mysql` |
| database/rds | aliyun-rds-supabase | 通过 OpenAPI 管理 Alibaba Cloud RDS Supabase，覆盖实例生命周期与关键配置操作。 | `skills/database/rds/aliyun-rds-supabase` |
| media/ice | aliyun-ice-manage | 技能 `aliyun-ice-manage` 的能力说明，详见对应 SKILL.md。 | `skills/media/ice/aliyun-ice-manage` |
| media/live | aliyun-live-manage | 技能 `aliyun-live-manage` 的能力说明，详见对应 SKILL.md。 | `skills/media/live/aliyun-live-manage` |
| media/mps | aliyun-mps-manage | 技能 `aliyun-mps-manage` 的能力说明，详见对应 SKILL.md。 | `skills/media/mps/aliyun-mps-manage` |
| media/video | aliyun-mps-video-translation | 通过 OpenAPI 创建和管理 Alibaba Cloud IMS 视频翻译任务，支持字幕、语音与人脸相关配置。 | `skills/media/video/aliyun-mps-video-translation` |
| media/vod | aliyun-vod-manage | 技能 `aliyun-vod-manage` 的能力说明，详见对应 SKILL.md。 | `skills/media/vod/aliyun-vod-manage` |
| network/cdn | aliyun-cdn-manage | 通过 OpenAPI/SDK 管理 Alibaba Cloud CDN，覆盖域名生命周期、缓存刷新与预热、HTTPS 证书更新及日志监控查询。 | `skills/network/cdn/aliyun-cdn-manage` |
| network/dns | aliyun-dns-cli | Alibaba Cloud DNS（Alidns）CLI 技能。 | `skills/network/dns/aliyun-dns-cli` |
| network/esa | aliyun-esa-manage | 技能 `aliyun-esa-manage` 的能力说明，详见对应 SKILL.md。 | `skills/network/esa/aliyun-esa-manage` |
| network/slb | aliyun-alb-manage | 管理和排障阿里云 ALB（应用型负载均衡）。覆盖实例、监听、服务器组、转发规则、证书、ACL、安全策略、健康检查及异步任务轮询的全生命周期管理，包含 28 个 CLI 脚本。 | `skills/network/slb/aliyun-alb-manage` |
| network/vpc | aliyun-vpc-manage | 通过 OpenAPI/SDK 管理阿里云专有网络 VPC，支持 VPC 与 VSwitch 的查询、创建、删除、可用区查询及网络排障。 | `skills/network/vpc/aliyun-vpc-manage` |
| observability/pts | aliyun-pts-manage | 技能 `aliyun-pts-manage` 的能力说明，详见对应 SKILL.md。 | `skills/observability/pts/aliyun-pts-manage` |
| observability/sls | aliyun-sls-log-query | 技能 `aliyun-sls-log-query` 的能力说明，详见对应 SKILL.md。 | `skills/observability/sls/aliyun-sls-log-query` |
| observability/sls | aliyun-sls-openclaw-integration | 技能 `aliyun-sls-openclaw-integration` 的能力说明，详见对应 SKILL.md。 | `skills/observability/sls/aliyun-sls-openclaw-integration` |
| platform/cli | aliyun-cli-manage | 通用 Alibaba Cloud CLI（aliyun）技能，覆盖安装、凭证/配置、API 发现与跨产品 OpenAPI 命令行调用。 | `skills/platform/cli/aliyun-cli-manage` |
| platform/devops | aliyun-devops-manage | 技能 `aliyun-devops-manage` 的能力说明，详见对应 SKILL.md。 | `skills/platform/devops/aliyun-devops-manage` |
| platform/docs | aliyun-platform-docs-benchmark | 对阿里云及主流云厂商同类产品文档与 API 文档进行基准对比并给出改进建议。 | `skills/platform/docs/aliyun-platform-docs-benchmark` |
| platform/docs | aliyun-platform-docs-review | 自动评审最新 Alibaba Cloud 产品文档与 OpenAPI 文档，并输出优先级建议与证据。 | `skills/platform/docs/aliyun-platform-docs-review` |
| platform/openapi | aliyun-openapi-discovery | 发现并对齐 Alibaba Cloud 产品目录与 OpenAPI 元数据，用于覆盖分析和技能规划。 | `skills/platform/openapi/aliyun-openapi-discovery` |
| platform/openclaw | aliyun-openclaw-setup | 技能 `aliyun-openclaw-setup` 的能力说明，详见对应 SKILL.md。 | `skills/platform/openclaw/aliyun-openclaw-setup` |
| platform/skills | aliyun-skill-creator | 技能 `aliyun-skill-creator` 的能力说明，详见对应 SKILL.md。 | `skills/platform/skills/aliyun-skill-creator` |
| security/content | aliyun-green-moderation | 通过 OpenAPI/SDK 管理 Alibaba Cloud Content Moderation (Green)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/security/content/aliyun-green-moderation` |
| security/firewall | aliyun-cloudfw-manage | 通过 OpenAPI/SDK 管理 Alibaba Cloud Cloud Firewall (Cloudfw)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/security/firewall/aliyun-cloudfw-manage` |
| security/host | aliyun-sas-manage | 通过 OpenAPI/SDK 管理 Alibaba Cloud Security Center (Sas)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/security/host/aliyun-sas-manage` |
| security/identity | aliyun-cloudauth-verify | 通过 OpenAPI/SDK 管理 Alibaba Cloud ID Verification (Cloudauth)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/security/identity/aliyun-cloudauth-verify` |
| security/key-management | aliyun-kms-manage | 通过 OpenAPI/SDK 管理 Alibaba Cloud KeyManagementService (Kms)，用于资源查询、创建或更新配置、状态查询与故障排查。 | `skills/security/key-management/aliyun-kms-manage` |
| solutions/aliyun-solution-article-illustrator | aliyun-solution-article-illustrator | 技能 `aliyun-solution-article-illustrator` 的能力说明，详见对应 SKILL.md。 | `skills/solutions/aliyun-solution-article-illustrator` |
| storage/oss | aliyun-oss-ossutil | Alibaba Cloud OSS CLI（ossutil 2.0）技能，支持命令行安装、配置与 OSS 资源操作。 | `skills/storage/oss/aliyun-oss-ossutil` |
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

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=cinience/alicloud-skills&type=Date)](https://star-history.com/#cinience/alicloud-skills&Date)
