---
name: aliyun-modelstudio-retalk
description: Replace lip sync in existing videos with Alibaba Cloud Model Studio VideoRetalk (`videoretalk`). Use when creating dubbed videos, replacing narration, or synchronizing a talking-head video to a new speech track.
version: 1.0.0
---

Category: provider

# Model Studio VideoRetalk

## Validation

```bash
mkdir -p output/aliyun-modelstudio-retalk
python -m py_compile skills/ai/video/aliyun-modelstudio-retalk/scripts/prepare_retalk_request.py && echo "py_compile_ok" > output/aliyun-modelstudio-retalk/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-modelstudio-retalk/validate.txt` is generated.

## Output And Evidence

- Save normalized request payloads, target face selection settings, and task polling snapshots under `output/aliyun-modelstudio-retalk/`.
- Record the exact video/audio input URLs and whether `video_extension` was enabled.

Use VideoRetalk when the input is already a person video and the job is to replace lip sync with a new speech track.

## Critical model names

Use this exact model string:
- `videoretalk`

## Prerequisites

- This model currently only supports China mainland (Beijing).
- API is HTTP async only; there is no online console experience.
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Normalized interface (video.retalk)

### Request
- `model` (string, optional): default `videoretalk`
- `video_url` (string, required)
- `audio_url` (string, required)
- `ref_image_url` (string, optional): target face when input video contains multiple faces
- `video_extension` (bool, optional): extend video to match longer audio
- `query_face_threshold` (int, optional): `120` to `200`

### Response
- `task_id` (string)
- `task_status` (string)
- `video_url` (string, when finished)
- `usage` (object, optional)

## Endpoint and execution model

- Submit task: `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis/`
- Poll task: `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`
- HTTP calls are async only and must set header `X-DashScope-Async: enable`.

## Quick start

```bash
python skills/ai/video/aliyun-modelstudio-retalk/scripts/prepare_retalk_request.py \
  --video-url "https://example.com/talking-head.mp4" \
  --audio-url "https://example.com/new-voice.wav" \
  --video-extension
```

## Operational guidance

- Keep input videos front-facing and close enough for stable face tracking.
- If the video contains multiple faces, provide `ref_image_url` to anchor the intended target.
- If the new audio is longer than the input video, decide explicitly whether to extend the picture track or truncate the audio.
- URLs must be public HTTP/HTTPS links; local file paths are not accepted by the API.

## Output location

- Default output: `output/aliyun-modelstudio-retalk/request.json`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/sources.md`
