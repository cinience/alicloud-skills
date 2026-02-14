# Alibaba Cloud Core AI Agent Skills

English (current) | [简体中文](README.md) | [繁體中文](README.zh-TW.md)

A curated collection of **Alibaba Cloud core AI Agent skills** covering key product lines,
including Model Studio, OSS, ECS, and more.

## Quick Start

Recommended install (all skills, skip prompts, overwrite existing):

```bash
npx skillfish add cinience/alicloud-skills --all -y --force
```

If you still see a selection prompt, press `a` to select all, then press Enter to submit.

Use a RAM user/role with least privilege. Avoid embedding AKs in code or CLI arguments.

Configure AccessKey (recommended):

```bash
export ALICLOUD_ACCESS_KEY_ID="your-ak"
export ALICLOUD_ACCESS_KEY_SECRET="your-sk"
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

## Examples (Docs Review & Benchmark)

1) Product docs + API docs review

- Prompt:
  "Use `alicloud-platform-docs-api-review` to review product docs and API docs for `Bailian`, then return prioritized P0/P1/P2 improvements with evidence links."

2) Multi-cloud comparable benchmark

- Prompt:
  "Use `alicloud-platform-multicloud-docs-api-benchmark` to benchmark `Bailian` against Alibaba Cloud/AWS/Azure/GCP/Tencent Cloud/Volcano Engine/Huawei Cloud with preset `llm-platform`, and output a score table plus gap actions."


## Repository Structure

- `skills/` — canonical skill sources grouped by product line
  - `ai/` — Model Studio (capability-based groups)
    - `text/` `image/` `audio/` `video/` `multimodal/` `search/` `misc/` `entry/`
  - `storage/` — OSS
  - `compute/` — ECS
  - `media/` — intelligent media creation
  - `network/` — VPC / SLB / EIP
  - `database/` — RDS / PolarDB / Redis
  - `security/` — RAM / KMS / WAF
  - `observability/` — SLS / ARMS / CloudMonitor
- `examples/` — end-to-end stories and usage walkthroughs

## Brand Aliases

- `modelstudio/` — symlink to `skills/ai/` (overseas brand)

## Skill Mapping (Skill → Display Name)


<!-- SKILL_MAPPING_BEGIN -->
| Skill | Display Name |
| --- | --- |
| `alicloud-ai-audio-tts` | Alibaba Cloud AI Audio TTS |
| `alicloud-ai-audio-tts-realtime` | Alibaba Cloud AI Audio TTS Realtime |
| `alicloud-ai-audio-tts-voice-clone` | Alibaba Cloud AI Audio TTS Voice Clone |
| `alicloud-ai-audio-tts-voice-design` | Alibaba Cloud AI Audio TTS Voice Design |
| `alicloud-ai-chatbot` | Alibaba Cloud AI Chatbot |
| `alicloud-ai-cloud-call-center` | Alibaba Cloud AI Cloud Call Center |
| `alicloud-ai-contactcenter-ai` | Alibaba Cloud AI Contactcenter AI |
| `alicloud-ai-content-aicontent` | Alibaba Cloud AI Content Aicontent |
| `alicloud-ai-content-aimiaobi` | Alibaba Cloud AI Content Aimiaobi |
| `alicloud-ai-entry-modelstudio` | Alibaba Cloud AI Entry Modelstudio |
| `alicloud-ai-entry-modelstudio-test` | Alibaba Cloud AI Entry Modelstudio Test |
| `alicloud-ai-image-qwen-image` | Alibaba Cloud AI Image Qwen Image |
| `alicloud-ai-image-qwen-image-edit` | Alibaba Cloud AI Image Qwen Image Edit |
| `alicloud-ai-image-zimage-turbo` | Alibaba Cloud AI Image Zimage Turbo |
| `alicloud-ai-misc-crawl-and-skill` | Alibaba Cloud AI Misc Crawl And Skill |
| `alicloud-ai-pai-aiworkspace` | Alibaba Cloud AI PAI Aiworkspace |
| `alicloud-ai-recommend-airec` | Alibaba Cloud AI Recommend Airec |
| `alicloud-ai-search-dashvector` | Alibaba Cloud AI Search Dashvector |
| `alicloud-ai-search-milvus` | Alibaba Cloud AI Search Milvus |
| `alicloud-ai-search-opensearch` | Alibaba Cloud AI Search Opensearch |
| `alicloud-ai-text-document-mind` | Alibaba Cloud AI Text Document Mind |
| `alicloud-ai-translation-anytrans` | Alibaba Cloud AI Translation Anytrans |
| `alicloud-ai-video-wan-r2v` | Alibaba Cloud AI Video Wan R2V |
| `alicloud-ai-video-wan-video` | Alibaba Cloud AI Video Wan Video |
| `alicloud-backup-bdrc` | Alibaba Cloud Backup BDRC |
| `alicloud-backup-hbr` | Alibaba Cloud Backup HBR |
| `alicloud-compute-ecs` | Alibaba Cloud Compute ECS |
| `alicloud-compute-fc-agentrun` | Alibaba Cloud Compute FC Agentrun |
| `alicloud-compute-fc-serverless-devs` | Alibaba Cloud Compute FC Serverless Devs |
| `alicloud-compute-swas-open` | Alibaba Cloud Compute Swas Open |
| `alicloud-data-analytics-dataanalysisgbi` | Alibaba Cloud Data Analytics Dataanalysisgbi |
| `alicloud-data-lake-dlf` | Alibaba Cloud Data Lake DLF |
| `alicloud-data-lake-dlf-next` | Alibaba Cloud Data Lake DLF Next |
| `alicloud-database-analyticdb-mysql` | Alibaba Cloud Database Analyticdb Mysql |
| `alicloud-database-rds-supabase` | Alibaba Cloud Database RDS Supabase |
| `alicloud-media-video-translation` | Alibaba Cloud Media Video Translation |
| `alicloud-network-dns-cli` | Alibaba Cloud Network DNS Cli |
| `alicloud-observability-sls-log-query` | Alibaba Cloud Observability SLS Log Query |
| `alicloud-platform-docs-api-review` | Alibaba Cloud Platform Docs API Review |
| `alicloud-platform-multicloud-docs-api-benchmark` | Alibaba Cloud Platform Multicloud Docs API Benchmark |
| `alicloud-platform-openapi-product-api-discovery` | Alibaba Cloud Platform OpenAPI Product API Discovery |
| `alicloud-security-center-sas` | Alibaba Cloud Security Center SAS |
| `alicloud-security-cloudfw` | Alibaba Cloud Security Cloudfw |
| `alicloud-security-content-moderation-green` | Alibaba Cloud Security Content Moderation Green |
| `alicloud-security-id-verification-cloudauth` | Alibaba Cloud Security Id Verification Cloudauth |
| `alicloud-security-kms` | Alibaba Cloud Security KMS |
| `alicloud-storage-oss-ossutil` | Alibaba Cloud Storage OSS Ossutil |
<!-- SKILL_MAPPING_END -->

## Skill Index

<!-- SKILL_INDEX_BEGIN -->
| Category | Skill | Description | Path |
| --- | --- | --- | --- |
| ai/audio | alicloud-ai-audio-tts | Generate human-like speech audio with Model Studio DashScope Qwen TTS models (qwen3-tts-flash, qwen3-tts-instruct-flash). Use when converting text to speech, producing voice lines for short drama/news videos, or documenting TTS request/response fields for DashScope. | `skills/ai/audio/alicloud-ai-audio-tts` |
| ai/audio | alicloud-ai-audio-tts-realtime | Real-time speech synthesis with Alibaba Cloud Model Studio Qwen TTS Realtime models. Use when low-latency interactive speech is required, including instruction-controlled realtime synthesis. | `skills/ai/audio/alicloud-ai-audio-tts-realtime` |
| ai/audio | alicloud-ai-audio-tts-voice-clone | Voice cloning workflows with Alibaba Cloud Model Studio Qwen TTS VC models. Use when creating cloned voices from sample audio and synthesizing text with cloned timbre. | `skills/ai/audio/alicloud-ai-audio-tts-voice-clone` |
| ai/audio | alicloud-ai-audio-tts-voice-design | Voice design workflows with Alibaba Cloud Model Studio Qwen TTS VD models. Use when creating custom synthetic voices from text descriptions and using them for speech synthesis. | `skills/ai/audio/alicloud-ai-audio-tts-voice-design` |
| ai/content | alicloud-ai-content-aicontent | Manage Alibaba Cloud AIContent (AiContent) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/ai/content/alicloud-ai-content-aicontent` |
| ai/content | alicloud-ai-content-aimiaobi | Manage Alibaba Cloud Quan Miao (AiMiaoBi) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/ai/content/alicloud-ai-content-aimiaobi` |
| ai/entry | alicloud-ai-entry-modelstudio | Route Alibaba Cloud Model Studio requests to the right local skill (Qwen Image, Qwen Image Edit, Wan Video, Wan R2V, Qwen TTS and advanced TTS variants). Use when the user asks for Model Studio without specifying a capability. | `skills/ai/entry/alicloud-ai-entry-modelstudio` |
| ai/entry | alicloud-ai-entry-modelstudio-test | Run a minimal test matrix for the Model Studio skills that exist in this repo (image/video/TTS and newly added edit/realtime/voice variants). Use to execute one small request per skill and record results. | `skills/ai/entry/alicloud-ai-entry-modelstudio-test` |
| ai/image | alicloud-ai-image-qwen-image | Generate images with Model Studio DashScope SDK using Qwen Image generation models (qwen-image-max, qwen-image-plus-2026-01-09). Use when implementing or documenting image.generate requests/responses, mapping prompt/negative_prompt/size/seed/reference_image, or integrating image generation into the video-agent pipeline. | `skills/ai/image/alicloud-ai-image-qwen-image` |
| ai/image | alicloud-ai-image-qwen-image-edit | Edit images with Alibaba Cloud Model Studio Qwen Image Edit Max (qwen-image-edit-max). Use when modifying existing images (inpaint, replace, style transfer, local edits), preserving subject consistency, or documenting image edit request/response mappings. | `skills/ai/image/alicloud-ai-image-qwen-image-edit` |
| ai/image | alicloud-ai-image-zimage-turbo | Generate images with Alibaba Cloud Model Studio Z-Image Turbo (z-image-turbo) via DashScope multimodal-generation API. Use when creating text-to-image outputs, controlling size/seed/prompt_extend, or documenting request/response mapping for Z-Image. | `skills/ai/image/alicloud-ai-image-zimage-turbo` |
| ai/misc | alicloud-ai-misc-crawl-and-skill | Refresh the Model Studio models crawl and regenerate derived summaries and `skills/ai/**` skills. Use when the models list or generated skills must be updated. | `skills/ai/misc/alicloud-ai-misc-crawl-and-skill` |
| ai/platform | alicloud-ai-pai-aiworkspace | Manage Alibaba Cloud Platform for Artificial Intelligence PAI - AIWorkspace (AIWorkSpace) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/ai/platform/alicloud-ai-pai-aiworkspace` |
| ai/recommendation | alicloud-ai-recommend-airec | Manage Alibaba Cloud AIRec (Airec) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/ai/recommendation/alicloud-ai-recommend-airec` |
| ai/search | alicloud-ai-search-dashvector | Build vector retrieval with DashVector using the Python SDK. Use when creating collections, upserting docs, and running similarity search with filters in Claude Code/Codex. | `skills/ai/search/alicloud-ai-search-dashvector` |
| ai/search | alicloud-ai-search-milvus | Use AliCloud Milvus (serverless) with PyMilvus to create collections, insert vectors, and run filtered similarity search. Optimized for Claude Code/Codex vector retrieval flows. | `skills/ai/search/alicloud-ai-search-milvus` |
| ai/search | alicloud-ai-search-opensearch | Use OpenSearch vector search edition via the Python SDK (ha3engine) to push documents and run HA/SQL searches. Ideal for RAG and vector retrieval pipelines in Claude Code/Codex. | `skills/ai/search/alicloud-ai-search-opensearch` |
| ai/service | alicloud-ai-chatbot | Manage Alibaba Cloud beebot (Chatbot) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/ai/service/alicloud-ai-chatbot` |
| ai/service | alicloud-ai-cloud-call-center | Manage Alibaba Cloud Cloud Call Center (CCC) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/ai/service/alicloud-ai-cloud-call-center` |
| ai/service | alicloud-ai-contactcenter-ai | Manage Alibaba Cloud Contact Center AI (ContactCenterAI) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/ai/service/alicloud-ai-contactcenter-ai` |
| ai/text | alicloud-ai-text-document-mind | Use Document Mind (DocMind) via Node.js SDK to submit document parsing jobs and poll results. Designed for Claude Code/Codex document understanding workflows. | `skills/ai/text/alicloud-ai-text-document-mind` |
| ai/translation | alicloud-ai-translation-anytrans | Manage Alibaba Cloud TongyiTranslate (AnyTrans) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/ai/translation/alicloud-ai-translation-anytrans` |
| ai/video | alicloud-ai-video-wan-r2v | Generate reference-based videos with Alibaba Cloud Model Studio Wan R2V (wan2.6-r2v-flash). Use when creating multi-shot videos from reference video/image material, preserving character style, or documenting reference-to-video request/response flows. | `skills/ai/video/alicloud-ai-video-wan-r2v` |
| ai/video | alicloud-ai-video-wan-video | Generate videos with Model Studio DashScope SDK using the wan2.6-i2v-flash model. Use when implementing or documenting video.generate requests/responses, mapping prompt/negative_prompt/duration/fps/size/seed/reference_image/motion_strength, or integrating video generation into the video-agent pipeline. | `skills/ai/video/alicloud-ai-video-wan-video` |
| backup/alicloud-backup-bdrc | alicloud-backup-bdrc | Manage Alibaba Cloud Backup and Disaster Recovery Center (BDRC) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/backup/alicloud-backup-bdrc` |
| backup/alicloud-backup-hbr | alicloud-backup-hbr | Manage Alibaba Cloud Cloud Backup (hbr) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/backup/alicloud-backup-hbr` |
| compute/ecs | alicloud-compute-ecs | Manage Alibaba Cloud Elastic Compute Service (ECS) via OpenAPI/SDK. Use for listing or creating instances, starting/stopping/rebooting, managing disks/snapshots/images/security groups/key pairs/ENIs, querying status, and troubleshooting workflows for this product. | `skills/compute/ecs/alicloud-compute-ecs` |
| compute/fc | alicloud-compute-fc-agentrun | Manage Function Compute AgentRun resources via OpenAPI (runtime, sandbox, model, memory, credentials). Use for creating runtimes/endpoints, querying status, and troubleshooting AgentRun workflows. | `skills/compute/fc/alicloud-compute-fc-agentrun` |
| compute/fc | alicloud-compute-fc-serverless-devs | Alibaba Cloud Function Compute (FC 3.0) skill for installing and using Serverless Devs to create, deploy, invoke, and remove a Python function. Use when users need CLI-based FC quick start or Serverless Devs setup guidance. | `skills/compute/fc/alicloud-compute-fc-serverless-devs` |
| compute/swas | alicloud-compute-swas-open | Manage Alibaba Cloud Simple Application Server (SWAS OpenAPI 2020-06-01) resources end-to-end. Use for querying instances, starting/stopping/rebooting, executing commands (cloud assistant), managing disks/snapshots/images, firewall rules/templates, key pairs, tags, monitoring, and lightweight database operations. | `skills/compute/swas/alicloud-compute-swas-open` |
| data-analytics/alicloud-data-analytics-dataanalysisgbi | alicloud-data-analytics-dataanalysisgbi | Manage Alibaba Cloud DataAnalysisGBI (DataAnalysisGBI) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/data-analytics/alicloud-data-analytics-dataanalysisgbi` |
| data-lake/alicloud-data-lake-dlf | alicloud-data-lake-dlf | Manage Alibaba Cloud Data Lake Formation (DataLake) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/data-lake/alicloud-data-lake-dlf` |
| data-lake/alicloud-data-lake-dlf-next | alicloud-data-lake-dlf-next | Manage Alibaba Cloud Data Lake Formation (DlfNext) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/data-lake/alicloud-data-lake-dlf-next` |
| database/analyticdb | alicloud-database-analyticdb-mysql | Manage Alibaba Cloud AnalyticDB for MySQL (adb) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/database/analyticdb/alicloud-database-analyticdb-mysql` |
| database/rds | alicloud-database-rds-supabase | Manage Alibaba Cloud RDS Supabase (RDS AI Service 2025-05-07) via OpenAPI. Use for creating, starting/stopping/restarting instances, resetting passwords, querying endpoints/auth/storage, configuring auth/RAG/SSL/IP whitelist, and listing instance details or conversations. | `skills/database/rds/alicloud-database-rds-supabase` |
| media/video | alicloud-media-video-translation | Create and manage Alibaba Cloud IMS video translation jobs via OpenAPI (subtitle/voice/face). Use when you need API-based video translation, status polling, and job management. | `skills/media/video/alicloud-media-video-translation` |
| network/dns | alicloud-network-dns-cli | Alibaba Cloud DNS (Alidns) CLI skill. Use to query, add, and update DNS records via aliyun-cli, including CNAME setup for Function Compute custom domains. | `skills/network/dns/alicloud-network-dns-cli` |
| observability/sls | alicloud-observability-sls-log-query | Query and troubleshoot logs in Alibaba Cloud Log Service (SLS) using query|analysis syntax and the Python SDK. Use for time-bounded log search, error investigation, and root-cause analysis workflows. | `skills/observability/sls/alicloud-observability-sls-log-query` |
| platform/docs | alicloud-platform-docs-api-review | Automatically review latest Alibaba Cloud product docs and OpenAPI docs by product name, then output detailed prioritized improvement suggestions with evidence and scoring. Use when user asks to audit product documentation quality, API documentation quality, or wants actionable doc/API optimization recommendations. | `skills/platform/docs/alicloud-platform-docs-api-review` |
| platform/docs | alicloud-platform-multicloud-docs-api-benchmark | Benchmark similar product documentation and API documentation across Alibaba Cloud, AWS, Azure, GCP, Tencent Cloud, Volcano Engine, and Huawei Cloud. Given one product keyword, auto-discover latest official docs/API links, score quality consistently, and output detailed prioritized improvement recommendations. | `skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark` |
| platform/openapi | alicloud-platform-openapi-product-api-discovery | Discover and reconcile Alibaba Cloud product catalogs from Ticket System, Support & Service, and BSS OpenAPI; fetch OpenAPI product/version/API metadata; and summarize API coverage to plan new skills. Use when you need a complete product list, product-to-API mapping, or coverage/gap reports for skill generation. | `skills/platform/openapi/alicloud-platform-openapi-product-api-discovery` |
| security/content | alicloud-security-content-moderation-green | Manage Alibaba Cloud Content Moderation (Green) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/security/content/alicloud-security-content-moderation-green` |
| security/firewall | alicloud-security-cloudfw | Manage Alibaba Cloud Cloud Firewall (Cloudfw) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/security/firewall/alicloud-security-cloudfw` |
| security/host | alicloud-security-center-sas | Manage Alibaba Cloud Security Center (Sas) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/security/host/alicloud-security-center-sas` |
| security/identity | alicloud-security-id-verification-cloudauth | Manage Alibaba Cloud ID Verification (Cloudauth) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/security/identity/alicloud-security-id-verification-cloudauth` |
| security/key-management | alicloud-security-kms | Manage Alibaba Cloud KeyManagementService (Kms) via OpenAPI/SDK. Use for listing resources, creating or updating configurations, querying status, and troubleshooting workflows for this product. | `skills/security/key-management/alicloud-security-kms` |
| storage/oss | alicloud-storage-oss-ossutil | Alibaba Cloud OSS CLI (ossutil 2.0) skill. Install, configure, and operate OSS from the command line based on the official ossutil overview. | `skills/storage/oss/alicloud-storage-oss-ossutil` |
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
