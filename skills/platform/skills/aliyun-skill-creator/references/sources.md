# Sources

## Skill engineering reference

- [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) — upstream skill-authoring guide
- `AGENTS.md` — repository conventions (this repo)
- `scripts/generate_skill_index.py` — README index generator
- `tests/common/compile_skill_scripts.py` — smoke-test helper

## Authoritative Alibaba Cloud documentation entry points

Always re-fetch these on every skill create / refresh pass. Prefer Chinese (`/zh/`) — it lands first; only fall back to `/en/` when content is verified equivalent.

### Help Center (general products)

- Product index: `https://help.aliyun.com/`
- Product overview: `https://help.aliyun.com/zh/<product-slug>/product-overview/`
- API reference: `https://help.aliyun.com/zh/<product-slug>/<api-reference-slug>`
- Quick start: `https://help.aliyun.com/zh/<product-slug>/getting-started/`
- Pricing: `https://help.aliyun.com/zh/<product-slug>/billing-overview`
- Legacy article id: `https://help.aliyun.com/document_detail/<id>.html`

### Bailian / Model Studio (DashScope) — entry portal

Start every Model Studio skill from the model catalog and the release log:

- Model catalog (entry): https://help.aliyun.com/zh/model-studio/models
- Newly released / retired models (truth source for ids): https://help.aliyun.com/zh/model-studio/newly-released-models
- Pricing: https://help.aliyun.com/zh/model-studio/model-pricing
- Getting started + auth: https://help.aliyun.com/zh/model-studio/getting-started/models
- OpenAI-compatible mode: https://help.aliyun.com/zh/model-studio/openai-compatible

#### Text generation (Qwen family)

- Qwen overview: https://help.aliyun.com/zh/model-studio/qwen
- Qwen-Coder: https://help.aliyun.com/zh/model-studio/qwen-coder
- Qwen-VL OCR: https://help.aliyun.com/zh/model-studio/qwen-vl-ocr

#### Image generation & editing

- Wan 2.7 image generation + editing API: https://help.aliyun.com/zh/model-studio/wan-image-generation-and-editing-api-reference
- Wan 2.6 image generation API: https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference
- Qwen-Image edit guide: https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide
- Z-Image API: https://help.aliyun.com/zh/model-studio/z-image-api-reference

#### Video generation & editing

- Video generation overview: https://help.aliyun.com/zh/model-studio/use-video-generation
- Image-to-video API (Wan i2v): https://help.aliyun.com/zh/model-studio/image-to-video-general-api-reference
- Wan video editing API: https://help.aliyun.com/zh/model-studio/wan-video-editing-api-reference
- Text-to-video / image-to-video prompt guide: https://help.aliyun.com/zh/model-studio/text-to-video-prompt

#### Avatar / face / emoji video

- Emoji video generation API: https://help.aliyun.com/zh/model-studio/emoji-api
- Emoji image detection API: https://help.aliyun.com/zh/model-studio/emoji-detect-api
- Emoji quick start: https://help.aliyun.com/zh/model-studio/emoji-quick-start/

#### Audio — TTS

- Qwen-TTS realtime: https://help.aliyun.com/zh/model-studio/qwen-tts-realtime
- Qwen-TTS voice cloning: https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning
- Qwen-TTS voice design: https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design

#### Audio — ASR

- Qwen-ASR realtime: https://help.aliyun.com/zh/model-studio/qwen-asr
- Qwen-ASR file transcription API: https://help.aliyun.com/zh/model-studio/qwen-asr-filetrans-api
- Recorded speech recognition (Qwen): https://help.aliyun.com/zh/model-studio/recorded-speech-recognition-qwen

#### File handling

- Get temporary OSS URL: https://help.aliyun.com/zh/model-studio/get-temporary-file-url

#### Tooling integrations

- Cline (Qwen3-Coder): https://help.aliyun.com/zh/model-studio/cline

DashScope runtime base URLs:

- Mainland: `https://dashscope.aliyuncs.com/api/v1/...`
- Singapore: `https://dashscope-intl.aliyuncs.com/api/v1/...`

> Slugs occasionally change. If a path 404s, GET the model catalog (`/zh/model-studio/models`) and follow the sidebar to discover the current slug — never guess.

### OpenAPI Portal (machine-readable spec, non-DashScope products)

- Browsable portal: `https://api.aliyun.com/product/<Product>`
- Product index JSON: `https://api.aliyun.com/meta/v1/products.json?language=EN_US`
- API list per product/version: `https://api.aliyun.com/meta/v1/products/<Product>/versions/<YYYY-MM-DD>/api-docs.json`
- Single API definition: `https://api.aliyun.com/meta/v1/products/<Product>/versions/<YYYY-MM-DD>/apis/<ApiName>/api.json`

Repository wrappers (reuse instead of writing one-off scrapers):

- `scripts/products_from_openapi_meta.py`
- `scripts/apis_from_openapi_meta.py`
- `scripts/summarize_openapi_meta_products.py`

### SDKs and CLIs

- Aliyun GitHub orgs: `https://github.com/aliyun`, `https://github.com/AliyunContainerService`, `https://github.com/alibabacloud-sdk`
- DashScope Python SDK: https://pypi.org/project/dashscope/
- Per-product Python SDK: `https://pypi.org/project/alibabacloud-<product>/`
- Per-product Node SDK: `https://www.npmjs.com/package/@alicloud/<product>`
- Aliyun CLI: https://github.com/aliyun/aliyun-cli (and `aliyun <product> help` for live usage)

## Fetching policy

- Re-fetch on every pass — model knowledge drifts; never trust the prior draft.
- Use `WebFetch` for narrative pages; use `urllib`/repo scripts for the OpenAPI metadata JSON endpoints.
- Date-stamp every link recorded in a skill's own `references/sources.md` (`(last checked YYYY-MM-DD)`).
- If a link 404s during fetch, re-discover it through the entry portal (`/zh/model-studio/models` for Bailian, `/zh/<product>/product-overview/` for everything else).
