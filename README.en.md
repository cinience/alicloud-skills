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

## Included Skills (current)


<!-- INCLUDED_SKILLS_BEGIN -->
Located in `skills/ai/`:

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

Located in `skills/storage/`:

- `oss/alicloud-storage-oss-ossutil`

Located in `skills/compute/`:

- `ecs/alicloud-compute-ecs`
- `fc/alicloud-compute-fc-agentrun`
- `fc/alicloud-compute-fc-serverless-devs`
- `swas/alicloud-compute-swas-open`

Located in `skills/database/`:

- `analyticdb/alicloud-database-analyticdb-mysql`
- `rds/alicloud-database-rds-supabase`

Located in `skills/network/`:

- `dns/alicloud-network-dns-cli`

Located in `skills/media/`:

- `video/alicloud-media-video-translation`

Located in `skills/observability/`:

- `sls/alicloud-observability-sls-log-query`

Located in `skills/backup/`:

- `alicloud-backup-bdrc`
- `alicloud-backup-hbr`

Located in `skills/data-lake/`:

- `alicloud-data-lake-dlf`
- `alicloud-data-lake-dlf-next`

Located in `skills/data-analytics/`:

- `alicloud-data-analytics-dataanalysisgbi`

Located in `skills/platform/`:

- `docs/alicloud-platform-docs-api-review`
- `docs/alicloud-platform-multicloud-docs-api-benchmark`
- `openapi/alicloud-platform-openapi-product-api-discovery`

Located in `skills/security/`:

- `content/alicloud-security-content-moderation-green`
- `firewall/alicloud-security-cloudfw`
- `host/alicloud-security-center-sas`
- `identity/alicloud-security-id-verification-cloudauth`
- `key-management/alicloud-security-kms`
<!-- INCLUDED_SKILLS_END -->

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
