---
name: aliyun-pixverse-generation
description: Generate videos with Alibaba Cloud Model Studio PixVerse models (`pixverse/pixverse-v5.6-t2v`, `pixverse/pixverse-v5.6-it2v`, `pixverse/pixverse-v5.6-kf2v`, `pixverse/pixverse-v5.6-r2v`). Use when building non-Wan text-to-video, first-frame image-to-video, keyframe-to-video, or multi-image reference-to-video workflows on Model Studio.
version: 1.0.0
---

Category: provider

# Model Studio Aishi Video Generation

## Validation

```bash
mkdir -p output/aliyun-pixverse-generation
python -m py_compile skills/ai/video/aliyun-pixverse-generation/scripts/prepare_aishi_request.py && echo "py_compile_ok" > output/aliyun-pixverse-generation/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-pixverse-generation/validate.txt` is generated.

## Output And Evidence

- Save normalized request payloads, chosen model variant, and task polling snapshots under `output/aliyun-pixverse-generation/`.
- Record region, resolution/size, duration, and whether audio generation was enabled.

Use Aishi when the user explicitly wants the non-Wan PixVerse family for video generation.

## Critical model names

Use one of these exact model strings:
- `pixverse/pixverse-v5.6-t2v`
- `pixverse/pixverse-v5.6-it2v`
- `pixverse/pixverse-v5.6-kf2v`
- `pixverse/pixverse-v5.6-r2v`

Selection guidance:
- Use `pixverse/pixverse-v5.6-t2v` for text-only generation.
- Use `pixverse/pixverse-v5.6-it2v` for first-frame image-to-video.
- Use `pixverse/pixverse-v5.6-kf2v` for first-frame + last-frame transitions.
- Use `pixverse/pixverse-v5.6-r2v` for multi-image character/style consistency.

## Prerequisites

- This family currently only supports China mainland (Beijing).
- Install SDK or call HTTP directly:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```

- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Normalized interface (video.generate)

### Request
- `model` (string, required)
- `prompt` (string, optional for `it2v`, required for other variants)
- `media` (array<object>, optional)
- `size` (string, optional): direct pixel size such as `1280*720`, used by `t2v` and `r2v`
- `resolution` (string, optional): `360P`/`540P`/`720P`/`1080P`, used by `it2v` and `kf2v`
- `duration` (int, required): `5`/`8`/`10`, except 1080P only supports `5`/`8`
- `audio` (bool, optional)
- `watermark` (bool, optional)
- `seed` (int, optional)

### Response
- `task_id` (string)
- `task_status` (string)
- `video_url` (string, when finished)

## Endpoint and execution model

- Submit task: `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
- Poll task: `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`
- HTTP calls are async only and must set header `X-DashScope-Async: enable`.

## Quick start

Text-to-video:

```bash
python skills/ai/video/aliyun-pixverse-generation/scripts/prepare_aishi_request.py \
  --model pixverse/pixverse-v5.6-t2v \
  --prompt "A compact robot walks through a rainy neon alley." \
  --size 1280*720 \
  --duration 5
```

Image-to-video:

```bash
python skills/ai/video/aliyun-pixverse-generation/scripts/prepare_aishi_request.py \
  --model pixverse/pixverse-v5.6-it2v \
  --prompt "The turtle swims slowly as the camera rises." \
  --media image_url=https://example.com/turtle.webp \
  --resolution 720P \
  --duration 5
```

## Operational guidance

- `t2v` and `r2v` use `size`; `it2v` and `kf2v` use `resolution`.
- For `kf2v`, provide exactly one `first_frame` and one `last_frame`.
- For `r2v`, you can pass up to 7 reference images.
- Aishi returns task IDs first; do not treat the initial response as the final video result.

## Output location

- Default output: `output/aliyun-pixverse-generation/request.json`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/sources.md`
