---
name: aliyun-skill-creator
description: Use when creating, migrating, or optimizing skills for this alicloud-skills repository. Use whenever users ask to add a new skill, import an external skill, refactor skill structure, improve trigger descriptions, add smoke tests under tests/**, or benchmark skill quality before merge.
version: 1.0.0
---

Category: tool

# Alibaba Cloud Skill Creator

Repository-specific skill engineering workflow for `alicloud-skills`.

## Use this skill when

- Creating a new skill under `skills/**`.
- Importing an external skill and adapting it to this repository.
- Updating skill trigger quality (`name` and `description` in frontmatter).
- Adding or fixing smoke tests under `tests/**`.
- Running structured benchmark loops before merge.

## Do not use this skill when

- The user only needs to execute an existing product skill.
- The task is purely application code under `apps/` with no skill changes.

## Repository constraints (must enforce)

- Skills live under `skills/<domain>/<subdomain>/<skill-name>/`.
- Skill folder names use kebab-case and should start with `alicloud-`.
- Every skill must include `SKILL.md` frontmatter with `name` and `description`.
- `skills/**/SKILL.md` content must stay English-only.
- Smoke tests must be in `tests/<domain>/<subdomain>/<skill-name>-test/SKILL.md`.
- Generated evidence goes to `output/<skill-or-test-skill>/` only.
- If skill inventory changes, refresh README index with `scripts/update_skill_index.sh`.
- **Every create/refresh pass MUST start by re-fetching the upstream official docs** — do not edit a skill from memory or from the previous draft alone. See "Fetching latest Alibaba Cloud documentation".

## Standard deliverable layout

```text
skills/<domain>/<subdomain>/<skill-name>/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   └── sources.md
└── scripts/ (optional)

tests/<domain>/<subdomain>/<skill-name>-test/
└── SKILL.md
```

## Workflow

1) Capture intent

- Confirm domain/subdomain and target skill name.
- Confirm whether this is new creation, migration, or refactor.
- Confirm expected outputs and success criteria.
- **Re-fetch the upstream documentation now**, even for a refresh — see "Fetching latest Alibaba Cloud documentation". Diff what you find against the existing skill before changing anything.

2) Implement skill changes

- For new skills: scaffold structure and draft `SKILL.md` + `agents/openai.yaml`.
- For migration from external repo: copy full source tree first, then adapt.
- Keep adaptation minimal but explicit:
  - Replace environment-specific instructions that do not match this repo.
  - Add repository validation and output discipline sections.
  - Keep reusable bundled resources (`scripts/`, `references/`, `assets/`).
- Always ground the skill in the latest official Alibaba Cloud documentation (see "Fetching latest Alibaba Cloud documentation" below) and record every authoritative URL in `references/sources.md`.

3) Add smoke test

- Create or update `tests/**/<skill-name>-test/SKILL.md`.
- Keep it minimal, reproducible, and low-risk.
- Include exact pass criteria and evidence location.

4) Validate locally

Run script compile validation for the skill:

```bash
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/<domain>/<subdomain>/<skill-name> \
  --output output/<skill-name>-test/compile-check.json
```

Refresh skill index when inventory changed:

```bash
scripts/update_skill_index.sh
```

Confirm index presence:

```bash
rg -n "<skill-name>" README.md README.zh-CN.md README.zh-TW.md
```

Optional broader checks:

```bash
make test
make build-cli
```

5) Benchmark loop (optional, for major skills)

If the user asks for quantitative skill evaluation, reuse bundled tooling:

- `scripts/run_eval.py`
- `scripts/aggregate_benchmark.py`
- `eval-viewer/generate_review.py`

Prefer placing benchmark artifacts in a sibling workspace directory and keep per-iteration outputs.

## Definition of done

- Skill path and naming follow repository conventions.
- Frontmatter is complete and trigger description is explicit.
- Test skill exists and has objective pass criteria.
- Validation artifacts are saved under `output/`.
- README skill index is refreshed if inventory changed.
- `references/sources.md` lists every upstream URL consulted in this pass, with last-checked date in the note.
- Model ids, parameter names, quotas, and pricing in `SKILL.md` cite a URL fetched in this pass — none copied forward unverified.

## Fetching latest Alibaba Cloud documentation

**Hard rule: every create or refresh pass starts here.** Re-fetch the upstream doc tree first, diff it against the existing skill, then write. Do not trust model memory and do not trust the prior draft — Alibaba Cloud rotates model ids, parameter names, and pricing on a weekly cadence.

Order of authority (stop at the first source that fully answers the question):

### 1. Help Center (`help.aliyun.com/zh/...`) — primary source

The Chinese path (`/zh/`) ships first and is the most accurate. The English path (`/en/`) often lags by weeks; only link to it after confirming parity.

| Document type | URL pattern | When to use |
|---|---|---|
| Product overview | `https://help.aliyun.com/zh/<product-slug>/product-overview/` | First read for a new skill |
| API reference | `https://help.aliyun.com/zh/<product-slug>/<api-reference-slug>` | Authoritative request/response schema |
| Quick start | `https://help.aliyun.com/zh/<product-slug>/getting-started/` | Minimal end-to-end example |
| Pricing | `https://help.aliyun.com/zh/<product-slug>/billing-overview` (or `model-pricing` for Model Studio) | Cost-relevant decisions |
| Legacy article id | `https://help.aliyun.com/document_detail/<id>.html` | Older articles only — replace with the `/zh/` slug when one exists |

Fetch with `WebFetch`:

```text
WebFetch(url="https://help.aliyun.com/zh/<product-slug>/<api-reference-slug>",
         prompt="Extract endpoint, parameters, response schema, model ids, and limits.")
```

If the response is a redirect notice, re-issue `WebFetch` against the redirect URL.

### 2. Bailian / Model Studio (`/zh/model-studio/...`) — entry portal

For any DashScope-backed skill (LLM, image, video, audio, embedding, rerank, agent, application), the canonical entry is:

```text
https://help.aliyun.com/zh/model-studio/models
```

From this page, walk into the topic sub-trees below. Always check `newly-released-models` first — that page is the source of truth for which model ids are GA right now and which were silently retired.

| Topic | URL slug under `/zh/model-studio/` | Notes |
|---|---|---|
| Model catalog (entry) | `models` | Full list of currently-served models, links into each detail page |
| Model release log | `newly-released-models` | Authoritative for new/retired model ids and dates |
| Pricing | `model-pricing` | Per-model token/image/second pricing |
| Getting started | `getting-started/models` | Account, key, region prerequisites |
| OpenAI-compatible mode | `openai-compatible` | When the user wants `openai` SDK shape |
| Quick start (per modality) | `<modality>-quick-start` (e.g. `emoji-quick-start`) | Smallest working example |
| Text generation (Qwen) | `qwen`, `qwen-coder`, `qwen-vl-ocr`, `qwen3-coder-next` | Family-specific guides |
| Image generation/editing | `wan-image-generation-and-editing-api-reference`, `wan-image-generation-api-reference`, `qwen-image-edit-guide`, `z-image-api-reference` | Wan / Qwen / Z image lines |
| Video generation | `use-video-generation`, `image-to-video-general-api-reference`, `wan-video-editing-api-reference`, `text-to-video-prompt` | Wan video + prompt guide |
| Avatar/face/emoji video | `emoji-detect-api`, `emoji-api`, `liveportrait-*`, `videoretalk-*`, `animate-anyone-*` | Avatar/digital-human pipelines |
| Audio (TTS) | `qwen-tts-realtime`, `qwen-tts-voice-cloning`, `qwen-tts-voice-design` | Realtime, cloning, voice design |
| Audio (ASR) | `qwen-asr`, `qwen-asr-filetrans-api`, `recorded-speech-recognition-qwen` | Streaming and file-transcribe |
| File handling | `get-temporary-file-url` | OSS temporary URL upload for media APIs |
| Embeddings & rerank | `embedding-api-details`, `text-embedding-async-api`, `text-rerank-api` | Vector + rerank stack |
| Application & agent | `agent-application`, `bailian-application-api` | Hosted Bailian application/agent runtime |
| Tool integration | `cline`, `langchain`, `dify-integration` | Third-party client wiring |

If a slug is unknown, GET the entry page first and let the sidebar tell you the current path — slugs occasionally change.

DashScope runtime base URLs:

```text
Mainland:   https://dashscope.aliyuncs.com/api/v1/...
Singapore:  https://dashscope-intl.aliyuncs.com/api/v1/...
```

### 3. OpenAPI Portal metadata (`api.aliyun.com`) — machine-readable spec

Use this for non-DashScope products (ECS, OSS, RDS, SLS, ESA, …) when you need exact request/response field types or a complete API list.

```text
# All products (one-time index, EN labels)
https://api.aliyun.com/meta/v1/products.json?language=EN_US

# All APIs for a product/version
https://api.aliyun.com/meta/v1/products/<Product>/versions/<YYYY-MM-DD>/api-docs.json

# Single API definition (full schema)
https://api.aliyun.com/meta/v1/products/<Product>/versions/<YYYY-MM-DD>/apis/<ApiName>/api.json
```

Repository helpers already wrap these endpoints — reuse them rather than writing one-off scrapers:

```bash
python3 scripts/products_from_openapi_meta.py        # refresh product index
python3 scripts/apis_from_openapi_meta.py            # fetch APIs per product (env-driven)
```

Browsable portal: `https://api.aliyun.com/product/<Product>` — for human inspection and to confirm a `<Product>` code before scripting.

### 4. Official SDKs and CLIs

| Source | URL pattern | Use for |
|---|---|---|
| GitHub orgs | `https://github.com/aliyun`, `https://github.com/AliyunContainerService`, `https://github.com/alibabacloud-sdk` | Reference SDK code, examples |
| PyPI | `https://pypi.org/project/dashscope/`, `https://pypi.org/project/alibabacloud-<product>/` | Python install + current version |
| npm | `https://www.npmjs.com/package/@alicloud/<product>` | Node install + current version |
| Aliyun CLI | `https://github.com/aliyun/aliyun-cli` and `aliyun <product> help` | Shell-based skills |

### 5. Recording sources

Every skill MUST list the URLs it actually consulted in this pass, in `references/sources.md`:

```markdown
# Sources

- [<Human title>](<URL>) — what this covers (last checked YYYY-MM-DD)
```

Include at minimum: API reference, model/version notice (`newly-released-models` for Model Studio), pricing (if relevant), and SDK home page. Date-stamp each entry — that is how the next maintainer knows what is stale.

### Red flags — STOP and re-fetch

- Editing the skill without opening any upstream URL in this session.
- Copying model ids, parameter names, or quotas forward from the existing draft.
- Linking only to `/en/` pages without checking `/zh/`.
- Saving raw HTML/JSON dumps under `references/` instead of summarizing into `SKILL.md`.
- Writing `curl` loops when `scripts/products_from_openapi_meta.py` / `scripts/apis_from_openapi_meta.py` already cover the call.

## References

- `references/schemas.md`
- `references/sources.md`
