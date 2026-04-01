# Alibaba Cloud Core AI Agent Skills

## Language

**English (current)** | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md)

Quick links: [Quick Start](#quick-start) | [Skill Index](#skill-index)

Cloud Mind: fold world-class cloud infrastructure into your AI chat box.
AI云：把世界级云基础设施带进你的 AI 对话框。

A curated collection of **Alibaba Cloud core AI Agent skills** covering key product lines,
including Model Studio, OSS, ECS, and more.

## Quick Start

Recommended install (all skills, skip prompts, overwrite existing):

```bash
npx skills add cinience/alicloud-skills --all -y --force
```

If you still see a selection prompt, press `a` to select all, then press Enter to submit.

Use a RAM user/role with least privilege. Avoid embedding AKs in code or CLI arguments.

Configure AccessKey (recommended):

```bash
export ALICLOUD_ACCESS_KEY_ID="your-ak"
export ALICLOUD_ACCESS_KEY_SECRET="your-sk"
export ALICLOUD_SECURITY_TOKEN="your-sts-token" # optional, for STS
export ALICLOUD_REGION_ID="cn-beijing"
export DASHSCOPE_API_KEY="your-dashscope-api-key"
```

Environment variables take precedence. If they are not set, the CLI/SDK falls back to `~/.alibabacloud/credentials`. `ALICLOUD_REGION_ID` is an optional default region; if unset, choose the most reasonable region at execution time, and ask the user when ambiguous.

If env vars are not set, use standard CLI/SDK config files:

`~/.alibabacloud/credentials`

```ini
[default]
type = access_key
access_key_id = your-ak
access_key_secret = your-sk
dashscope_api_key = your-dashscope-api-key
```

For STS, set `type = sts` and add `security_token = your-sts-token`.

## Examples (Docs Review & Benchmark)

1) Product docs + API docs review

- Prompt:
  "Use `aliyun-platform-docs-review` to review product docs and API docs for `Bailian`, then return prioritized P0/P1/P2 improvements with evidence links."

2) Multi-cloud comparable benchmark

- Prompt:
  "Use `aliyun-platform-docs-benchmark` to benchmark `Bailian` against Alibaba Cloud/AWS/Azure/GCP/Tencent Cloud/Volcano Engine/Huawei Cloud with preset `llm-platform`, and output a score table plus gap actions."

## Standalone Skills With Prompt Examples

1) Text-to-image (Qwen Image)

- Demo: Generate an image
- Prompt:
  "Use `aliyun-qwen-image` to generate a 1024*1024 poster with a minimalist coffee theme, output filename `poster.png`."

2) Image-to-video (Wan Video)

- Demo: Generate a 4-second video from a reference image (public image URL required)
- Prompt:
  "Use `aliyun-wan-video` with reference image `https://.../scene.png` to generate a 4-second, 24fps, 1280*720 shot. Prompt: morning city timelapse."

3) Text-to-speech (Qwen TTS)

- Demo: Generate speech audio with DashScope
- Prompt:
  "Use `aliyun-qwen-tts` to synthesize this paragraph, `voice=Cherry`, `language=English`, and return the audio URL."

4) Document structure parsing (DocMind)

- Demo: Parse title/paragraph structure from PDF
- Prompt:
  "Use `aliyun-docmind-extract` to parse this PDF (URL: ...), and return structured results."

5) Vector retrieval (DashVector)

- Demo: Create collection, insert, and query
- Prompt:
  "Use `aliyun-dashvector-search` to create a collection with `dimension=768`, insert 2 records, then run a `topk=5` query."

6) OSS upload/sync (ossutil)

- Demo: Upload a local file to OSS
- Prompt:
  "Use `aliyun-oss-ossutil` to upload `./local.txt` to `oss://xxx/path/`."

7) SLS log troubleshooting

- Demo: Query 500 errors in the last 15 minutes
- Prompt:
  "Use `aliyun-sls-log-query` to find 500 errors in the last 15 minutes and aggregate by status."

8) FC 3.0 quick deployment (Serverless Devs)

- Demo: Initialize and deploy a Python function
- Prompt:
  "Use `aliyun-fc-serverless-devs` to initialize an FC 3.0 Python project and deploy it."

9) Content safety moderation (Green)

- Demo: Discover/call moderation APIs via OpenAPI
- Prompt:
  "Use `aliyun-green-moderation` to list available APIs first, then provide a minimal text-moderation parameter example."

10) KMS key management

- Demo: List keys or create a key
- Prompt:
  "Use `aliyun-kms-manage` to provide an OpenAPI parameter template for creating a symmetric key."

11) Automated product docs and API docs review

- Demo: Auto-fetch latest docs by product and output improvement suggestions
- Prompt:
  "Use `aliyun-platform-docs-review` to review product docs and API docs for `Bailian`, and output prioritized P0/P1/P2 suggestions with evidence links."

12) Cross-cloud docs/API benchmark

- Demo: Compare similar products across Alibaba Cloud/AWS/Azure/GCP/Tencent Cloud/Volcano Engine/Huawei Cloud
- Prompt:
  "Use `aliyun-platform-docs-benchmark` for `Bailian` with preset `llm-platform`, and output a score table and gap recommendations."

## Solution Playbooks (Scenario Prompt Templates)

1) Marketing asset pipeline (image -> video -> voice-over -> upload)

Template:
"Chain these skills in order:
1. `aliyun-qwen-image` to generate a poster image (theme: {theme}, size: {size}).
2. `aliyun-wan-video` to generate a {duration}s video from that image (fps={fps}, size={size}, shot description: {shot_desc}).
3. `aliyun-qwen-tts` to synthesize narration (voice={voice}, text: {narration_text}, language={language}).
4. `aliyun-oss-ossutil` to upload video and audio to {oss_path}.
Return final asset URLs and descriptions."

2) Customer-support knowledge retrieval + voice answer

Template:
"Use `aliyun-docmind-extract` to parse document (URL: {doc_url}) into structured content;
then `aliyun-dashvector-search` to build and ingest the vector index;
then answer user question `{user_question}` with `topk={topk}` retrieval and generate spoken response using `aliyun-qwen-tts` (voice={voice}, language={language}).
Return text answer + audio URL."

3) Content moderation + publishing

Template:
"Use `aliyun-green-moderation` to moderate content (type: {text|image|video}, content: {content_or_url}).
If passed, upload with `aliyun-oss-ossutil` to {oss_path} and return public URL.
If failed, return reason and replacement suggestions."

4) Site log troubleshooting + automated alert

Template:
"Use `aliyun-sls-log-query` to query errors in {time_range} (query: {query}),
aggregate by {aggregate_field}, and determine if threshold {threshold} is exceeded.
If exceeded, use `aliyun-fc-serverless-devs` to trigger alert function (function: {function_name}, params: {alert_params}).
Return stats and alert status."

5) Multilingual content production (generate -> translate -> voice-over)

Template:
"Use `aliyun-aicontent-generate` to generate copy (topic: {topic}, style: {style}, length: {length});
use `aliyun-anytrans-translate` to translate to {target_language};
use `aliyun-qwen-tts` for speech (voice={voice}, language={language}).
Return original text, translated text, and audio URL."

6) Training data cleaning and archiving

Template:
"Run compliance check with `aliyun-green-moderation` (content: {content_or_url}).
If passed, run structured extraction with `aliyun-docmind-extract` when applicable.
Finally archive to {oss_path} with `aliyun-oss-ossutil`, and return archive manifest + URLs."

7) Log metric analysis report

Template:
"Use `aliyun-sls-log-query` in {time_range} with {query|analysis},
output a stats table by {dimension},
then summarize a visualization report using `aliyun-gbi-analytics` (metrics: {metrics}, dimensions: {dimensions}).
Return key metrics and report summary."

8) Business search and recommendation

Template:
"Use `aliyun-dashvector-search` for intent-based vector retrieval (topk={topk}, filter={filter}),
then `aliyun-airec-manage` for reranking and supplementary recommendations (strategy: {strategy}).
Return final recommendation list and rationale."

9) Enterprise call scenario (call center + chatbot + voice)

Template:
"Use `aliyun-ccc-manage` to create/route inbound calls (number: {number}, routing: {routing_strategy});
use `aliyun-chatbot-manage` for FAQ hit or handoff decision;
use `aliyun-qwen-tts` to play responses (voice={voice}, language={language}).
Return final script and audio URL."

10) Security and compliance closed loop (key management + audit)

Template:
"Use `aliyun-kms-manage` to create/manage keys (purpose: {purpose}, alias: {alias});
use `aliyun-sls-log-query` to query security audit logs in {time_range} (query: {query});
if anomalies are found, return mitigation suggestions or trigger an alert function ({function_name}).
Return key status, audit results, and remediation suggestions."

## Repository Structure

- `skills/` — canonical skill sources grouped by product line
  - `ai/` — Model Studio (capability-based groups)
    - `text/` `image/` `audio/` `video/` `multimodal/` `search/` `recommendation/` `content/` `service/` `translation/` `platform/` `misc/` `entry/`
  - `backup/` — BDRC / HBR
  - `compute/` — ECS / FC / SWAS
  - `data-analytics/` — DataAnalysisGBI
  - `data-lake/` — DLF
  - `database/` — AnalyticDB / RDS
  - `media/` — intelligent media creation
  - `network/` — DNS / ALB / ESA
  - `observability/` — SLS
  - `platform/` — CLI / OpenAPI / docs workflows
  - `security/` — content moderation / firewall / host security / identity / key management
  - `storage/` — OSS
- `examples/` — end-to-end stories and usage walkthroughs

## Brand Aliases

- `modelstudio/` — symlink to `skills/ai/` (overseas brand)

## Governance Checks

Run repository governance checks locally:

```bash
bash scripts/verify_governance.sh
```

Workflow gate (prepare -> validate -> deploy):

```bash
bash scripts/workflow_prepare.sh demo-20260303
bash scripts/workflow_validate.sh demo-20260303
bash scripts/workflow_deploy.sh demo-20260303
```

Standards and migration notes:

- `docs/standards/skill-template.md`
- `docs/standards/skill-template-migration.md`
- `docs/standards/coverage-policy.md`
- `docs/standards/workflow-gate.md`

## Skill Index

<!-- SKILL_INDEX_BEGIN -->
| Category | Skill | Description | Path |
| --- | --- | --- | --- |
| ai/audio | aliyun-qwen-asr | Transcribe non-realtime speech with Alibaba Cloud Model Studio Qwen ASR models (`qwen3-asr-flash`, `qwen-audio-asr`, `qwen3-asr-flash-filetrans`). Use when converting recorded audio files to text, generating transcripts with timestamps, or documenting DashScope/OpenAI-compatible ASR request and response fields. | `skills/ai/audio/aliyun-qwen-asr` |
| ai/audio | aliyun-qwen-asr-realtime | Use when low-latency realtime speech recognition is needed with Alibaba Cloud Model Studio Qwen ASR Realtime models, including streaming microphone input, live captions, or duplex voice agents. | `skills/ai/audio/aliyun-qwen-asr-realtime` |
| ai/audio | aliyun-cosyvoice-voice-clone | Use when creating cloned voices with Alibaba Cloud Model Studio CosyVoice customization models, especially cosyvoice-v3.5-plus or cosyvoice-v3.5-flash, from reference audio and then reusing the returned voice_id in later TTS calls. | `skills/ai/audio/aliyun-cosyvoice-voice-clone` |
| ai/audio | aliyun-cosyvoice-voice-design | Use when designing custom voices with Alibaba Cloud Model Studio CosyVoice customization models, especially cosyvoice-v3.5-plus or cosyvoice-v3.5-flash, from a voice prompt plus preview text before using the returned voice_id in TTS. | `skills/ai/audio/aliyun-cosyvoice-voice-design` |
| ai/audio | aliyun-qwen-livetranslate | Use when live speech translation is needed with Alibaba Cloud Model Studio Qwen LiveTranslate models, including bilingual meetings, realtime interpretation, and speech-to-speech or speech-to-text translation flows. | `skills/ai/audio/aliyun-qwen-livetranslate` |
| ai/audio | aliyun-qwen-tts | Generate human-like speech audio with Model Studio DashScope Qwen TTS models (qwen3-tts-flash, qwen3-tts-instruct-flash). Use when converting text to speech, producing voice lines for short drama/news videos, or documenting TTS request/response fields for DashScope. | `skills/ai/audio/aliyun-qwen-tts` |
| ai/audio | aliyun-qwen-tts-realtime | Real-time speech synthesis with Alibaba Cloud Model Studio Qwen TTS Realtime models. Use when low-latency interactive speech is required, including instruction-controlled realtime synthesis. | `skills/ai/audio/aliyun-qwen-tts-realtime` |
| ai/audio | aliyun-qwen-tts-voice-clone | Voice cloning workflows with Alibaba Cloud Model Studio Qwen TTS VC models. Use when creating cloned voices from sample audio and synthesizing text with cloned timbre. | `skills/ai/audio/aliyun-qwen-tts-voice-clone` |
| ai/audio | aliyun-qwen-tts-voice-design | Voice design workflows with Alibaba Cloud Model Studio Qwen TTS VD models. Use when creating custom synthetic voices from text descriptions and using them for speech synthesis. | `skills/ai/audio/aliyun-qwen-tts-voice-design` |
| ai/code | aliyun-qwen-coder | Use when code generation, repository understanding, or coding-agent tasks need Alibaba Cloud Model Studio Qwen Coder models (`qwen3-coder-next`, `qwen3-coder-plus` and related coder variants). | `skills/ai/code/aliyun-qwen-coder` |
| ai/content | aliyun-aicontent-generate | Manage Alibaba Cloud AIContent (AiContent) via OpenAPI/SDK. Use whenever the user needs AI content generation or content workflow operations in Alibaba Cloud, including listing assets, creating/updating generation configurations, checking task status, or troubleshooting failed content jobs. | `skills/ai/content/aliyun-aicontent-generate` |
| ai/content | aliyun-aimiaobi-generate | Manage Alibaba Cloud Quan Miao (AiMiaoBi) via OpenAPI/SDK. Use whenever the user asks for Alibaba Cloud MiaoBi content operations, including listing resources, creating/updating configurations, querying runtime status, and diagnosing API or workflow failures. | `skills/ai/content/aliyun-aimiaobi-generate` |
| ai/entry | aliyun-modelstudio-entry | Route Alibaba Cloud Model Studio requests to the right local skill (Qwen text, coder, deep research, image, video, audio, search and multimodal skills). Use when the user asks for Model Studio without specifying a capability. | `skills/ai/entry/aliyun-modelstudio-entry` |
| ai/entry | aliyun-modelstudio-entry-test | Run a minimal test matrix for the Model Studio skills that exist in this repo, including image/video/audio, realtime speech, omni, visual reasoning, embedding, rerank, and edit variants. Use to execute one small request per skill and record results. | `skills/ai/entry/aliyun-modelstudio-entry-test` |
| ai/image | aliyun-qwen-image | Generate images with Model Studio DashScope SDK using Qwen Image generation models (qwen-image, qwen-image-plus, qwen-image-max, qwen-image-2.0 series and snapshots). Use when implementing or documenting image.generate requests/responses, mapping prompt/negative_prompt/size/seed/reference_image, or integrating image generation into the video-agent pipeline. | `skills/ai/image/aliyun-qwen-image` |
| ai/image | aliyun-qwen-image-edit | Edit images with Alibaba Cloud Model Studio Qwen Image Edit models (qwen-image-edit, qwen-image-edit-plus, qwen-image-edit-max, qwen-image-2.0 series and snapshots). Use when modifying existing images (inpaint, replace, style transfer, local edits), preserving subject consistency, or documenting image edit request/response mappings. | `skills/ai/image/aliyun-qwen-image-edit` |
| ai/image | aliyun-zimage-turbo | Generate images with Alibaba Cloud Model Studio Z-Image Turbo (z-image-turbo) via DashScope multimodal-generation API. Use when creating text-to-image outputs, controlling size/seed/prompt_extend, or documenting request/response mapping for Z-Image. | `skills/ai/image/aliyun-zimage-turbo` |
| ai/misc | aliyun-modelstudio-crawl-and-skill | Refresh the Model Studio models crawl and regenerate derived summaries and `skills/ai/**` skills. Use when the models list or generated skills must be updated. | `skills/ai/misc/aliyun-modelstudio-crawl-and-skill` |
| ai/multimodal | aliyun-qvq | Use when visual reasoning is needed with Alibaba Cloud Model Studio QVQ models, including step-by-step image reasoning, chart analysis, and visually grounded problem solving. | `skills/ai/multimodal/aliyun-qvq` |
| ai/multimodal | aliyun-qwen-ocr | Use when OCR-specialized extraction is needed with Alibaba Cloud Model Studio Qwen OCR models (`qwen-vl-ocr`, `qwen-vl-ocr-latest`, and snapshots), including document parsing, table parsing, multilingual OCR, formula recognition, and key information extraction. | `skills/ai/multimodal/aliyun-qwen-ocr` |
| ai/multimodal | aliyun-qwen-omni | Use when tasks require all-in-one multimodal understanding or generation with Alibaba Cloud Model Studio Qwen Omni models, including image-plus-audio interaction, voice assistants, and realtime multimodal agents. | `skills/ai/multimodal/aliyun-qwen-omni` |
| ai/multimodal | aliyun-qwen-vl | Understand images with Alibaba Cloud Model Studio Qwen VL models (qwen3-vl-plus/qwen3-vl-flash and latest aliases). Use when building image Q&A, visual analysis, OCR-like extraction, chart/table reading, or screenshot understanding workflows. | `skills/ai/multimodal/aliyun-qwen-vl` |
| ai/platform | aliyun-pai-workspace | Manage Alibaba Cloud PAI AIWorkspace (AIWorkSpace) via OpenAPI/SDK. Use whenever the user is operating AIWorkspace resources such as workspace/project inventory, create/update actions, status queries, permission or configuration troubleshooting, or automation around PAI workspace lifecycle. | `skills/ai/platform/aliyun-pai-workspace` |
| ai/recommendation | aliyun-airec-manage | Manage Alibaba Cloud AIRec (Airec) via OpenAPI/SDK. Use whenever the user needs recommendation-engine resource operations in Alibaba Cloud, including list/create/update flows, status inspection, and troubleshooting AIRec configuration or runtime issues. | `skills/ai/recommendation/aliyun-airec-manage` |
| ai/research | aliyun-qwen-deep-research | Use when a task needs Alibaba Cloud Model Studio Qwen Deep Research models to plan multi-step investigation, run iterative web research, and produce structured reports with citations or evidence summaries. | `skills/ai/research/aliyun-qwen-deep-research` |
| ai/search | aliyun-dashvector-search | Build vector retrieval with DashVector using the Python SDK. Use when creating collections, upserting docs, and running similarity search with filters in Claude Code/Codex. | `skills/ai/search/aliyun-dashvector-search` |
| ai/search | aliyun-milvus-search | Use AliCloud Milvus (serverless) with PyMilvus to create collections, insert vectors, and run filtered similarity search. Optimized for Claude Code/Codex vector retrieval flows. | `skills/ai/search/aliyun-milvus-search` |
| ai/search | aliyun-qwen-multimodal-embedding | Use when multimodal embeddings are needed from Alibaba Cloud Model Studio models such as `qwen3-vl-embedding` for image, video, and text retrieval, cross-modal search, clustering, or offline vectorization pipelines. | `skills/ai/search/aliyun-qwen-multimodal-embedding` |
| ai/search | aliyun-opensearch-search | Use OpenSearch vector search edition via the Python SDK (ha3engine) to push documents and run HA/SQL searches. Ideal for RAG and vector retrieval pipelines in Claude Code/Codex. | `skills/ai/search/aliyun-opensearch-search` |
| ai/search | aliyun-qwen-rerank | Use when reranking search candidates is needed with Alibaba Cloud Model Studio rerank models, including hybrid retrieval, top-k refinement, and multilingual relevance sorting. | `skills/ai/search/aliyun-qwen-rerank` |
| ai/search | aliyun-qwen-text-embedding | Use when text embeddings are needed from Alibaba Cloud Model Studio models for semantic search, retrieval-augmented generation, clustering, or offline vectorization pipelines. | `skills/ai/search/aliyun-qwen-text-embedding` |
| ai/service | aliyun-chatbot-manage | Manage Alibaba Cloud beebot (Chatbot) via OpenAPI/SDK. Use whenever the user asks to configure, query, or troubleshoot Alibaba Cloud chatbot resources, including bot inventory, configuration changes, status checks, and API-level diagnostics. | `skills/ai/service/aliyun-chatbot-manage` |
| ai/service | aliyun-ccc-manage | Manage Alibaba Cloud Cloud Call Center (CCC) via OpenAPI/SDK. Use whenever the user is working on CCC operations such as instance/resource management, configuration updates, status checks, and troubleshooting call-center API workflows. | `skills/ai/service/aliyun-ccc-manage` |
| ai/service | aliyun-ccai-manage | Manage Alibaba Cloud Contact Center AI (ContactCenterAI) via OpenAPI/SDK. Use whenever the task involves Contact Center AI resource lifecycle operations, configuration changes, status queries, or troubleshooting failed ContactCenterAI API calls. | `skills/ai/service/aliyun-ccai-manage` |
| ai/text | aliyun-docmind-extract | Use Document Mind (DocMind) via Node.js SDK to submit document parsing jobs and poll results. Designed for Claude Code/Codex document understanding workflows. | `skills/ai/text/aliyun-docmind-extract` |
| ai/text | aliyun-qwen-generation | Generate or reason over text with Alibaba Cloud Model Studio Qwen flagship text models (`qwen3-max`, `qwen3.5-plus`, `qwen3.5-flash`, snapshots, and compatible open-source variants). Use when building chat, agent, tool-calling, or long-context text generation workflows on Model Studio. | `skills/ai/text/aliyun-qwen-generation` |
| ai/translation | aliyun-anytrans-translate | Manage Alibaba Cloud TongyiTranslate (AnyTrans) via OpenAPI/SDK. Use whenever the user needs translation service resource operations in Alibaba Cloud, including list/create/update actions, task status checks, and troubleshooting AnyTrans API workflows. | `skills/ai/translation/aliyun-anytrans-translate` |
| ai/video | aliyun-pixverse-generation | Generate videos with Alibaba Cloud Model Studio PixVerse models (`pixverse/pixverse-v5.6-t2v`, `pixverse/pixverse-v5.6-it2v`, `pixverse/pixverse-v5.6-kf2v`, `pixverse/pixverse-v5.6-r2v`). Use when building non-Wan text-to-video, first-frame image-to-video, keyframe-to-video, or multi-image reference-to-video workflows on Model Studio. | `skills/ai/video/aliyun-pixverse-generation` |
| ai/video | aliyun-animate-anyone | Generate dance or motion-transfer videos with Alibaba Cloud Model Studio AnimateAnyone (`animate-anyone-gen2`) using a detected character image and an action template. Use when cloning motion from a dance/action video into a target character image. | `skills/ai/video/aliyun-animate-anyone` |
| ai/video | aliyun-wan-digital-human | Generate talking, singing, or presentation videos from a single character image and audio with Alibaba Cloud Model Studio digital-human model `wan2.2-s2v`. Use when creating narrated avatar videos, singing portraits, or broadcast-style talking-head clips. | `skills/ai/video/aliyun-wan-digital-human` |
| ai/video | aliyun-emo | Generate expressive portrait videos from a person image and speech audio with Alibaba Cloud Model Studio EMO (`emo-v1`). Use when creating non-Wan avatar clips with stronger expression style control from a detected portrait image. | `skills/ai/video/aliyun-emo` |
| ai/video | aliyun-emoji | Generate template-driven emoji videos with Alibaba Cloud Model Studio Emoji (`emoji-v1`) from a detected portrait image. Use when producing fixed-style meme or emoji motion clips from a single face image and a selected template ID. | `skills/ai/video/aliyun-emoji` |
| ai/video | aliyun-liveportrait | Generate lightweight talking-head portrait videos with Alibaba Cloud Model Studio LivePortrait (`liveportrait`) from a detected portrait image and speech audio. Use when you need long-form or simple broadcast-style portrait animation beyond the typical short expressive models. | `skills/ai/video/aliyun-liveportrait` |
| ai/video | aliyun-videoretalk | Replace lip sync in existing videos with Alibaba Cloud Model Studio VideoRetalk (`videoretalk`). Use when creating dubbed videos, replacing narration, or synchronizing a talking-head video to a new speech track. | `skills/ai/video/aliyun-videoretalk` |
| ai/video | aliyun-wan-edit | Use when Alibaba Cloud Model Studio Wan video editing models are needed for style transfer, keyframe-controlled editing, or animation remix workflows. | `skills/ai/video/aliyun-wan-edit` |
| ai/video | aliyun-wan-r2v | Generate reference-based videos with Alibaba Cloud Model Studio Wan R2V models (wan2.6-r2v-flash, wan2.6-r2v). Use when creating multi-shot videos from reference video/image material, preserving character style, or documenting reference-to-video request/response flows. | `skills/ai/video/aliyun-wan-r2v` |
| ai/video | aliyun-wan-video | Generate videos with Model Studio DashScope SDK using Wan video generation models (wan2.6-t2v, wan2.6-i2v-flash, wan2.6-i2v and regional variants). Use when implementing or documenting video.generate requests/responses, mapping prompt/negative_prompt/duration/fps/size/seed/reference_image/motion_strength, or integrating video generation into the video-agent pipeline. | `skills/ai/video/aliyun-wan-video` |
| backup/aliyun-bdrc-backup | aliyun-bdrc-backup | Manage Alibaba Cloud Backup and Disaster Recovery Center (BDRC) via OpenAPI/SDK. Use whenever the user needs backup/disaster-recovery resource operations, including inventory, policy/configuration changes, status checks, and troubleshooting BDRC workflows. | `skills/backup/aliyun-bdrc-backup` |
| backup/aliyun-hbr-backup | aliyun-hbr-backup | Manage Alibaba Cloud Cloud Backup (HBR) via OpenAPI/SDK. Use whenever the user asks for backup lifecycle operations such as resource listing, policy/config updates, job status queries, and troubleshooting HBR backup or restore workflows. | `skills/backup/aliyun-hbr-backup` |
| compute/ecs | aliyun-ecs-manage | Manage Alibaba Cloud Elastic Compute Service (ECS) via OpenAPI/SDK. Use for listing or creating instances, starting/stopping/rebooting, managing disks/snapshots/images/security groups/key pairs/ENIs, querying status, and troubleshooting workflows for this product. | `skills/compute/ecs/aliyun-ecs-manage` |
| compute/fc | aliyun-fc-agentrun | Manage Function Compute AgentRun resources via OpenAPI (runtime, sandbox, model, memory, credentials). Use for creating runtimes/endpoints, querying status, and troubleshooting AgentRun workflows. | `skills/compute/fc/aliyun-fc-agentrun` |
| compute/fc | aliyun-fc-serverless-devs | Alibaba Cloud Function Compute (FC 3.0) skill for installing and using Serverless Devs to create, deploy, invoke, and remove a Python function. Use when users need CLI-based FC quick start or Serverless Devs setup guidance. | `skills/compute/fc/aliyun-fc-serverless-devs` |
| compute/swas | aliyun-swas-manage | Manage Alibaba Cloud Simple Application Server (SWAS OpenAPI 2020-06-01) resources end-to-end. Use for querying instances, starting/stopping/rebooting, executing commands (cloud assistant), managing disks/snapshots/images, firewall rules/templates, key pairs, tags, monitoring, and lightweight database operations. | `skills/compute/swas/aliyun-swas-manage` |
| data-analytics/aliyun-gbi-analytics | aliyun-gbi-analytics | Manage Alibaba Cloud DataAnalysisGBI via OpenAPI/SDK. Use whenever the user needs DataAnalysisGBI resource lifecycle operations, configuration changes, status inspection, or troubleshooting for analytics service workflows. | `skills/data-analytics/aliyun-gbi-analytics` |
| data-lake/aliyun-dlf-manage | aliyun-dlf-manage | Manage Alibaba Cloud Data Lake Formation (DataLake) via OpenAPI/SDK. Use whenever the user asks for DataLake catalog resource operations, configuration updates, status queries, or troubleshooting DataLake API workflows. | `skills/data-lake/aliyun-dlf-manage` |
| data-lake/aliyun-dlf-manage-next | aliyun-dlf-manage-next | Manage Alibaba Cloud Data Lake Formation (DlfNext) via OpenAPI/SDK. Use whenever the user needs DLF Next catalog/governance resource operations, including listing resources, create/update flows, status checks, and troubleshooting metadata workflow issues. | `skills/data-lake/aliyun-dlf-manage-next` |
| database/analyticdb | aliyun-adb-mysql | Manage Alibaba Cloud AnalyticDB for MySQL (ADB) via OpenAPI/SDK. Use whenever the user needs AnalyticDB resource lifecycle and configuration operations, status checks, or troubleshooting ADB API and cluster workflow issues. | `skills/database/analyticdb/aliyun-adb-mysql` |
| database/rds | aliyun-rds-supabase | Manage Alibaba Cloud RDS Supabase (RDS AI Service 2025-05-07) via OpenAPI. Use for creating, starting/stopping/restarting instances, resetting passwords, querying endpoints/auth/storage, configuring auth/RAG/SSL/IP whitelist, and listing instance details or conversations. | `skills/database/rds/aliyun-rds-supabase` |
| media/ice | aliyun-ice-manage | Manage Alibaba Cloud Intelligent Cloud Editing (ICE) media workflows via OpenAPI/SDK. Use for media processing jobs, template/workflow orchestration, editing and production pipelines, and job status troubleshooting. | `skills/media/ice/aliyun-ice-manage` |
| media/live | aliyun-live-manage | Manage Alibaba Cloud ApsaraVideo Live resources and workflows via OpenAPI/SDK. Use for live domain configuration, stream ingest and playback setup, recording/transcoding templates, monitoring queries, and live stream operations. | `skills/media/live/aliyun-live-manage` |
| media/mps | aliyun-mps-manage | Manage Alibaba Cloud ApsaraVideo for Media Processing (MPS/MTS) resources and workflows via OpenAPI/SDK. Use for media ingest and metadata tasks, transcoding/snapshot jobs, pipeline/template/workflow operations, and MPS job troubleshooting. | `skills/media/mps/aliyun-mps-manage` |
| media/video | aliyun-mps-video-translation | Create and manage Alibaba Cloud IMS video translation jobs via OpenAPI (subtitle/voice/face). Use when you need API-based video translation, status polling, and job management. | `skills/media/video/aliyun-mps-video-translation` |
| media/vod | aliyun-vod-manage | Manage Alibaba Cloud ApsaraVideo VOD resources and media workflows via OpenAPI/SDK. Use for upload and media asset operations, transcoding templates, playback authorization, AI processing jobs, and VOD troubleshooting. | `skills/media/vod/aliyun-vod-manage` |
| network/cdn | aliyun-cdn-manage | Manage Alibaba Cloud CDN via OpenAPI/SDK. Use for CDN domain onboarding and lifecycle operations, cache refresh/preload, HTTPS certificate updates, and log/monitoring data queries. | `skills/network/cdn/aliyun-cdn-manage` |
| network/dns | aliyun-dns-cli | Alibaba Cloud DNS (Alidns) CLI skill. Use to query, add, and update DNS records via aliyun-cli, including CNAME setup for Function Compute custom domains. | `skills/network/dns/aliyun-dns-cli` |
| network/esa | aliyun-esa-manage | Manage Alibaba Cloud ESA — deploy HTML/static sites via Pages, manage Edge Routines (ER) for serverless edge functions, use Edge KV for distributed key-value storage, handle site management, DNS records, cache rules, and query traffic analytics via OpenAPI/SDK. Use when working with ESA, edge deployment, edge functions, Pages, ER, KV storage, DNS, cache, site configuration, traffic analytics, bandwidth trends, or top-N rankings. | `skills/network/esa/aliyun-esa-manage` |
| network/slb | aliyun-alb-manage | Manage and troubleshoot Alibaba Cloud ALB (Application Load Balancer). Use whenever the user asks to inspect, create, change, or debug ALB instances, listeners, server groups, rules, certificates, ACLs, security policies, or health checks in Alibaba Cloud. | `skills/network/slb/aliyun-alb-manage` |
| observability/pts | aliyun-pts-manage | Manage Alibaba Cloud Performance Testing Service (PTS) via OpenAPI/SDK. Use for scene lifecycle operations, test start/stop control, report retrieval, and metadata-driven API discovery before production changes. | `skills/observability/pts/aliyun-pts-manage` |
| observability/sls | aliyun-sls-openclaw-integration | "Use when the user needs to integrate OpenClaw with Alibaba Cloud SLS/Observability, including collector setup, machine groups, indexes, dashboards, collection configs, or Logtail bindings on Linux." | `skills/observability/sls/aliyun-sls-openclaw-integration` |
| observability/sls | aliyun-sls-log-query | Query and troubleshoot logs in Alibaba Cloud Log Service (SLS) using query|analysis syntax and the Python SDK. Use for time-bounded log search, error investigation, and root-cause analysis workflows. | `skills/observability/sls/aliyun-sls-log-query` |
| platform/cli | aliyun-cli-manage | Alibaba Cloud generic CLI skill for installing, configuring, and using aliyun CLI to call OpenAPI actions across products. Use when users need command-line operations on Alibaba Cloud resources (list/query/create/update/delete), credential/profile setup, region/endpoint selection, or API discovery from CLI. | `skills/platform/cli/aliyun-cli-manage` |
| platform/devops | aliyun-devops-manage | Manage Alibaba Cloud DevOps (Yunxiao 2020) via OpenAPI/SDK. Use for project/repository/pipeline resource discovery, read-only inspection, and safe change planning before mutating operations. | `skills/platform/devops/aliyun-devops-manage` |
| platform/docs | aliyun-platform-docs-review | Automatically review latest Alibaba Cloud product docs and OpenAPI docs by product name, then output detailed prioritized improvement suggestions with evidence and scoring. Use when user asks to audit product documentation quality, API documentation quality, or wants actionable doc/API optimization recommendations. | `skills/platform/docs/aliyun-platform-docs-review` |
| platform/docs | aliyun-platform-docs-benchmark | Benchmark similar product documentation and API documentation across Alibaba Cloud, AWS, Azure, GCP, Tencent Cloud, Volcano Engine, and Huawei Cloud. Given one product keyword, auto-discover latest official docs/API links, score quality consistently, and output detailed prioritized improvement recommendations. | `skills/platform/docs/aliyun-platform-docs-benchmark` |
| platform/openapi | aliyun-openapi-discovery | Discover and reconcile Alibaba Cloud product catalogs from Ticket System, Support & Service, and BSS OpenAPI; fetch OpenAPI product/version/API metadata; and summarize API coverage to plan new skills. Use when you need a complete product list, product-to-API mapping, or coverage/gap reports for skill generation. | `skills/platform/openapi/aliyun-openapi-discovery` |
| platform/openclaw | aliyun-openclaw-setup | Install and configure OpenClaw with DingTalk, Feishu, Discord, and additional channels with Bailian/DashScope models on Linux hosts. Use when provisioning a new OpenClaw node, troubleshooting gateway/channel startup, standardizing openclaw.json mapping, or automatically discovering extra channels from https://docs.openclaw.ai/channels. | `skills/platform/openclaw/aliyun-openclaw-setup` |
| platform/skills | aliyun-skill-creator | Create, migrate, and optimize skills for this alicloud-skills repository. Use whenever users ask to add a new skill, import an external skill, refactor skill structure, improve trigger descriptions, add smoke tests under tests/**, or benchmark skill quality before merge. | `skills/platform/skills/aliyun-skill-creator` |
| security/content | aliyun-green-moderation | Manage Alibaba Cloud Content Moderation (Green) via OpenAPI/SDK. Use whenever the user needs content moderation resource and policy operations, including list/create/update actions, status inspection, and troubleshooting moderation workflow failures. | `skills/security/content/aliyun-green-moderation` |
| security/firewall | aliyun-cloudfw-manage | Manage Alibaba Cloud Cloud Firewall (Cloudfw) via OpenAPI/SDK. Use whenever the user requests firewall policy/resource operations, change management, status checks, or troubleshooting Cloud Firewall API workflows. | `skills/security/firewall/aliyun-cloudfw-manage` |
| security/host | aliyun-sas-manage | Manage Alibaba Cloud Security Center (Sas) via OpenAPI/SDK. Use whenever the user needs Security Center resource operations, configuration updates, status queries, and troubleshooting Sas API or security workflow issues. | `skills/security/host/aliyun-sas-manage` |
| security/identity | aliyun-cloudauth-verify | Manage Alibaba Cloud ID Verification (Cloudauth) via OpenAPI/SDK. Use whenever the user is working on identity-verification resource operations, config updates, status checks, or troubleshooting Cloudauth API workflows. | `skills/security/identity/aliyun-cloudauth-verify` |
| security/key-management | aliyun-kms-manage | Manage Alibaba Cloud Key Management Service (KMS) via OpenAPI/SDK. Use whenever the user needs key lifecycle/resource operations, policy/configuration changes, status inspection, or troubleshooting KMS API workflows. | `skills/security/key-management/aliyun-kms-manage` |
| solutions/aliyun-solution-article-illustrator | aliyun-solution-article-illustrator | Use when the user needs an end-to-end article illustration workflow in this repository that preserves Type x Style planning, loads article-illustration preferences, recommends Alibaba Cloud image backends, and produces a Markdown article with inserted local image references. | `skills/solutions/aliyun-solution-article-illustrator` |
| storage/oss | aliyun-oss-ossutil | Alibaba Cloud OSS CLI (ossutil 2.0) skill. Install, configure, and operate OSS from the command line based on the official ossutil overview. | `skills/storage/oss/aliyun-oss-ossutil` |
<!-- SKILL_INDEX_END -->

Update the index by running: `scripts/update_skill_index.sh`

## Industry Use Cases

See: `examples/industry-use-cases.md`

## Notes

- This repository focuses on Alibaba Cloud's core capabilities and their Claude skill implementations.
- More skills can be added under `skills/` as they become available.

## Output Policy

- All temporary files and generated artifacts must be written under `output/`.
- Use subfolders per skill, e.g. `output/<skill>/...`.
- `output/` is ignored by git and should not be committed.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=cinience/alicloud-skills&type=Date)](https://star-history.com/#cinience/alicloud-skills&Date)
