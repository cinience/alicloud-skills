---
name: alicloud-ai-video-digital-human
description: Generate talking, singing, or presentation videos from a single character image and audio with Alibaba Cloud Model Studio digital-human model `wan2.2-s2v`. Use when creating narrated avatar videos, singing portraits, or broadcast-style talking-head clips.
version: 1.0.0
---

Category: provider

# Model Studio Digital Human

## Validation

```bash
mkdir -p output/alicloud-ai-video-digital-human
python -m py_compile skills/ai/video/alicloud-ai-video-digital-human/scripts/prepare_digital_human_request.py && echo "py_compile_ok" > output/alicloud-ai-video-digital-human/validate.txt
```

Pass criteria: command exits 0 and `output/alicloud-ai-video-digital-human/validate.txt` is generated.

## Output And Evidence

- Save normalized request payloads, chosen resolution, and task polling snapshots under `output/alicloud-ai-video-digital-human/`.
- Record image/audio URLs and whether the input image passed detection.

Use this skill for image + audio driven speaking, singing, or presenting characters.

## Critical model names

Use these exact model strings:
- `wan2.2-s2v-detect`
- `wan2.2-s2v`

Selection guidance:
- Run `wan2.2-s2v-detect` first to validate the image.
- Use `wan2.2-s2v` for the actual video generation job.

## Prerequisites

- China mainland (Beijing) only.
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.
- Input audio should contain clear speech or singing, and input image should depict a clear subject.

## Normalized interface (video.digital_human)

### Detect Request
- `model` (string, optional): default `wan2.2-s2v-detect`
- `image_url` (string, required)

### Generate Request
- `model` (string, optional): default `wan2.2-s2v`
- `image_url` (string, required)
- `audio_url` (string, required)
- `resolution` (string, optional): `480P` or `720P`
- `scenario` (string, optional): `talk`, `sing`, or `perform`

### Response
- `task_id` (string)
- `task_status` (string)
- `video_url` (string, when finished)

## Quick start

```bash
python skills/ai/video/alicloud-ai-video-digital-human/scripts/prepare_digital_human_request.py \
  --image-url "https://example.com/anchor.png" \
  --audio-url "https://example.com/voice.mp3" \
  --resolution 720P \
  --scenario talk
```

## Operational guidance

- Use a portrait, half-body, or full-body image with a clear face and stable framing.
- Match audio length to the desired output duration; the output follows the audio length up to the model limit.
- Keep image and audio as public HTTP/HTTPS URLs.
- If the image fails detection, do not proceed directly to video generation.

## Output location

- Default output: `output/alicloud-ai-video-digital-human/request.json`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/sources.md`
