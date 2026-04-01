---
name: aliyun-modelstudio-entry
description: Use when routing Alibaba Cloud Model Studio requests to the right local skill (Qwen text, coder, deep research, image, video, audio, search and multimodal skills). Use when the user asks for Model Studio without specifying a capability.
version: 1.0.0
---

Category: task

# Alibaba Cloud Model Studio Entry (Routing)

Route requests to existing local skills to avoid duplicating model/parameter details.

## Prerequisites

- Install SDK (virtual environment recommended to avoid PEP 668 restrictions):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```
- Configure `DASHSCOPE_API_KEY` (environment variable preferred; or `dashscope_api_key` in `~/.alibabacloud/credentials`).

## Routing Table (currently supported in this repo)

| Need | Target skill |
| --- | --- |
| Text generation / reasoning / tool-calling | `skills/ai/text/aliyun-qwen-generation/` |
| Coding / repository reasoning | `skills/ai/code/aliyun-qwen-coder/` |
| Deep multi-step research | `skills/ai/research/aliyun-qwen-deep-research/` |
| Text-to-image / image generation | `skills/ai/image/aliyun-qwen-image/` |
| Image editing | `skills/ai/image/aliyun-qwen-image-edit/` |
| Text-to-video / image-to-video (t2v/i2v) | `skills/ai/video/aliyun-wan-video/` |
| Non-Wan PixVerse video generation | `skills/ai/video/aliyun-pixverse-generation/` |
| Reference-to-video (r2v) | `skills/ai/video/aliyun-wan-r2v/` |
| Digital human talking / singing avatar | `skills/ai/video/aliyun-wan-digital-human/` |
| Expressive portrait video (EMO) | `skills/ai/video/aliyun-emo/` |
| Lightweight portrait animation (LivePortrait) | `skills/ai/video/aliyun-liveportrait/` |
| Motion transfer / dancing avatar (AnimateAnyone) | `skills/ai/video/aliyun-animate-anyone/` |
| Emoji / meme portrait video | `skills/ai/video/aliyun-emoji/` |
| Text-to-speech (TTS) | `skills/ai/audio/aliyun-qwen-tts/` |
| Speech recognition/transcription (ASR) | `skills/ai/audio/aliyun-qwen-asr/` |
| Realtime speech recognition | `skills/ai/audio/aliyun-qwen-asr-realtime/` |
| Realtime TTS | `skills/ai/audio/aliyun-qwen-tts-realtime/` |
| Live speech translation | `skills/ai/audio/aliyun-qwen-livetranslate/` |
| CosyVoice voice clone | `skills/ai/audio/aliyun-cosyvoice-voice-clone/` |
| CosyVoice voice design | `skills/ai/audio/aliyun-cosyvoice-voice-design/` |
| Voice clone | `skills/ai/audio/aliyun-qwen-tts-voice-clone/` |
| Voice design | `skills/ai/audio/aliyun-qwen-tts-voice-design/` |
| Omni multimodal interaction | `skills/ai/multimodal/aliyun-qwen-omni/` |
| Visual reasoning | `skills/ai/multimodal/aliyun-qvq/` |
| OCR / document parsing / table parsing | `skills/ai/multimodal/aliyun-qwen-ocr/` |
| Text embeddings | `skills/ai/search/aliyun-qwen-text-embedding/` |
| Multimodal embeddings | `skills/ai/search/aliyun-qwen-multimodal-embedding/` |
| Rerank | `skills/ai/search/aliyun-qwen-rerank/` |
| Vector retrieval | `skills/ai/search/aliyun-dashvector-search/` or `skills/ai/search/aliyun-opensearch-search/` or `skills/ai/search/aliyun-milvus-search/` |
| Document understanding | `skills/ai/text/aliyun-docmind-extract/` |
| Video editing | `skills/ai/video/aliyun-wan-edit/` |
| Video lip-sync replacement / retalk | `skills/ai/video/aliyun-videoretalk/` |
| Model list crawl/update | `skills/ai/misc/aliyun-modelstudio-crawl-and-skill/` |

## When Not Matched

- Clarify model capability and input/output type first.
- If capability is missing in repo, add a new skill first.

## Common Missing Capabilities In This Repo (remaining gaps)

- image translation
- virtual try-on / digital human / advanced video personas

- For multimodal/ASR download failures, prefer public URLs listed above.
- For ASR parameter errors, use data URI in `input_audio.data`.
- For multimodal embedding 400, ensure `input.contents` is an array.

## Async Task Polling Template (video/long-running tasks)

When `X-DashScope-Async: enable` returns `task_id`, poll as follows:

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/<task_id>
Authorization: Bearer $DASHSCOPE_API_KEY
```

Example result fields (success):

```
{
  "output": {
    "task_status": "SUCCEEDED",
    "video_url": "https://..."
  }
}
```

Notes:
- Recommended polling interval: 15-20 seconds, max 10 attempts.
- After success, download `output.video_url`.

## Clarifying questions (ask when uncertain)

1. Are you working with text, image, audio, or video?
2. Is this generation, editing/understanding, or retrieval?
3. Do you need speech (TTS/ASR/live translate) or retrieval (embedding/rerank/vector DB)?
4. Do you want runnable SDK scripts or just API/parameter guidance?

## References

- Model list and links:`output/alicloud-model-studio-models-summary.md`
- API/parameters/examples: see target sub-skill `SKILL.md` and `references/*.md`

- Official source list:`references/sources.md`

## Validation

```bash
mkdir -p output/aliyun-modelstudio-entry
echo "validation_placeholder" > output/aliyun-modelstudio-entry/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-modelstudio-entry/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-modelstudio-entry/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Workflow

1) Confirm user intent, region, identifiers, and whether the operation is read-only or mutating.
2) Run one minimal read-only query first to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.
