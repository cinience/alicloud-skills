---
name: aliyun-emoji
description: Use when generating template-driven emoji videos with Alibaba Cloud Model Studio Emoji (`emoji-v1`) from a detected portrait image. Use when producing fixed-style meme or emoji motion clips from a single face image and a selected template ID.
version: 1.0.0
---

Category: provider

# Model Studio Emoji

## Validation

```bash
mkdir -p output/aliyun-emoji
python -m py_compile skills/ai/video/aliyun-emoji/scripts/prepare_emoji_request.py && echo "py_compile_ok" > output/aliyun-emoji/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-emoji/validate.txt` is generated.

## Output And Evidence

- Save normalized request payloads, detected face boxes, selected template ID, and task polling snapshots under `output/aliyun-emoji/`.
- Record the exact portrait URL and whether detection passed.

Use Emoji when the user wants a fixed-template facial animation clip rather than open-ended video generation.

## Critical model names

Use these exact model strings:
- `emoji-detect-v1`
- `emoji-v1`

Selection guidance:
- Run `emoji-detect-v1` first to obtain `face_bbox` and `ext_bbox_face`.
- Use `emoji-v1` only after detection succeeds.

## Prerequisites

- China mainland (Beijing) only.
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.
- Input image must be a public HTTP/HTTPS URL.

## Normalized interface (video.emoji)

### Detect Request
- `model` (string, optional): default `emoji-detect-v1`
- `image_url` (string, required)

### Generate Request
- `model` (string, optional): default `emoji-v1`
- `image_url` (string, required)
- `face_bbox` (array<int>, required)
- `ext_bbox_face` (array<int>, required)
- `template_id` (string, required)

### Response
- `task_id` (string)
- `task_status` (string)
- `video_url` (string, when finished)

## Quick start

```bash
python skills/ai/video/aliyun-emoji/scripts/prepare_emoji_request.py \
  --image-url "https://example.com/portrait.png" \
  --face-bbox 302,286,610,593 \
  --ext-bbox-face 71,9,840,778 \
  --template-id emoji_001
```

## Operational guidance

- Use a single-person, front-facing portrait with no face occlusion.
- Template IDs come from the official template list or console experience; do not invent them in production calls.
- Emoji output is a person video clip, not a sticker pack or text overlay asset.

## Output location

- Default output: `output/aliyun-emoji/request.json`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/sources.md`
