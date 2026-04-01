---
name: aliyun-emo
description: Use when generating expressive portrait videos from a person image and speech audio with Alibaba Cloud Model Studio EMO (`emo-v1`). Use when creating non-Wan avatar clips with stronger expression style control from a detected portrait image.
version: 1.0.0
---

Category: provider

# Model Studio EMO

## Validation

```bash
mkdir -p output/aliyun-emo
python -m py_compile skills/ai/video/aliyun-emo/scripts/prepare_emo_request.py && echo "py_compile_ok" > output/aliyun-emo/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-emo/validate.txt` is generated.

## Output And Evidence

- Save normalized request payloads, detection boxes, and task polling snapshots under `output/aliyun-emo/`.
- Record the chosen `style_level` and the exact `face_bbox` / `ext_bbox`.

Use EMO when the input is a portrait image and speech audio, and you need a non-Wan expressive talking-head result.

## Critical model names

Use these exact model strings:
- `emo-v1-detect`
- `emo-v1`

Selection guidance:
- Run image detection first to obtain `face_bbox` and `ext_bbox`.
- Use `emo-v1` only after detection succeeds.

## Prerequisites

- China mainland (Beijing) only.
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.
- Input files must be public HTTP/HTTPS URLs.

## Normalized interface (video.emo)

### Detect Request
- `model` (string, optional): default `emo-v1-detect`
- `image_url` (string, required)

### Generate Request
- `model` (string, optional): default `emo-v1`
- `image_url` (string, required)
- `audio_url` (string, required)
- `face_bbox` (array<int>, required)
- `ext_bbox` (array<int>, required)
- `style_level` (string, optional): `normal`, `calm`, or `active`

### Response
- `task_id` (string)
- `task_status` (string)
- `video_url` (string, when finished)

## Quick start

```bash
python skills/ai/video/aliyun-emo/scripts/prepare_emo_request.py \
  --image-url "https://example.com/portrait.png" \
  --audio-url "https://example.com/speech.mp3" \
  --face-bbox 302,286,610,593 \
  --ext-bbox 71,9,840,778 \
  --style-level active
```

## Operational guidance

- Do not invent `face_bbox` or `ext_bbox`; use the detection API output.
- `ext_bbox` ratio determines output format: `1:1` yields `512x512`, `3:4` yields `512x704`.
- Keep the input portrait clear and front-facing for better expression quality.
- EMO is portrait-focused; for full-scene human videos use other skills instead.

## Output location

- Default output: `output/aliyun-emo/request.json`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/sources.md`
