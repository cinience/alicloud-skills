---
name: aliyun-happyhorse-videoedit
description: Use when editing videos with DashScope HappyHorse 1.0 video editing model (happyhorse-1.0-video-edit). Use when implementing instruction-based video editing such as style transfer or local replacement, optionally guided by 0-5 reference images, via the video-synthesis async API on Alibaba Cloud Model Studio.
---

# HappyHorse 1.0 Video Editing

## Validation

```bash
mkdir -p output/aliyun-happyhorse-videoedit
python -m py_compile skills/ai/video/aliyun-happyhorse-videoedit/scripts/edit_happyhorse.py && echo "py_compile_ok" > output/aliyun-happyhorse-videoedit/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-happyhorse-videoedit/validate.txt` is generated.

## Output And Evidence

- Save task IDs, polling responses, and final video URLs to `output/aliyun-happyhorse-videoedit/`.
- Keep at least one end-to-end run log for troubleshooting.

## Prerequisites

- Install dependencies (recommended in a venv):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install requests
```
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Critical model names

- `happyhorse-1.0-video-edit` — instruction-based video editing with optional reference images and audio retention control

## Capabilities

| Capability | Description | Required media |
|---|---|---|
| Style transfer | Convert the input video to a different visual style via a text instruction | exactly 1 `video` |
| Local replacement / instruction edit | Replace or modify subjects guided by a prompt and optional reference images | 1 `video` + 0-5 `reference_image` |

## API endpoint (async only)

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

Required headers:
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- `X-DashScope-Async: enable`

Singapore endpoint: replace `dashscope.aliyuncs.com` with `dashscope-intl.aliyuncs.com`.

Polling endpoint: `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` — recommended interval 15s.

## Normalized interface

### Request
- `model` (string, required) — fixed `happyhorse-1.0-video-edit`
- `input.prompt` (string, required) — up to 5000 non-CJK / 2500 CJK characters describing the edit
- `input.media` (array, required) — exactly 1 `video` element, plus 0-5 `reference_image` elements:
  - `type`: `video` (required, exactly 1) | `reference_image` (optional, 0-5)
  - `url`: public HTTP/HTTPS URL
- `parameters.resolution` (string, optional) — `720P` or `1080P` (default: `1080P`)
- `parameters.audio_setting` (string, optional) — `auto` (default, model decides) or `origin` (keep input audio)
- `parameters.watermark` (boolean, optional) — bottom-right "Happy Horse" watermark (default: `true`)
- `parameters.seed` (integer, optional) — range [0, 2147483647]

### Media input limits

**Input video** (`type=video`):
- Formats: MP4, MOV (H.264 encoding recommended)
- Duration: 3-60 seconds (output is capped at 15s; videos >15s are truncated to the first 15s)
- Resolution: long side ≤ 2160 px, short side ≥ 320 px
- Aspect ratio: 1:2.5 ~ 2.5:1
- Frame rate: > 8 fps
- Max size: 100 MB

**Reference image** (`type=reference_image`):
- Formats: JPEG, JPG, PNG, WEBP
- Resolution: width and height ≥ 300 pixels
- Aspect ratio: 1:2.5 ~ 2.5:1
- Max size: 10 MB

### Output duration rule

- Input ≤ 15s → output duration = input duration.
- Input > 15s → input is truncated to the first 15s; output ≤ 15s.

### Response (task creation)
- `output.task_id` (string) — valid 24 hours
- `output.task_status` (string) — `PENDING` | `RUNNING` | `SUCCEEDED` | `FAILED` | `CANCELED` | `UNKNOWN`
- `request_id` (string)

### Response (task result, on SUCCEEDED)
- `output.video_url` (string) — edited MP4 (H.264) URL, valid 24 hours
- `output.orig_prompt` (string)
- `output.submit_time` / `output.scheduled_time` / `output.end_time` (string)
- `usage.duration` (float) — billable duration in seconds
- `usage.input_video_duration` (float)
- `usage.output_video_duration` (float)
- `usage.SR` (integer) — output resolution tier
- `usage.video_count` (integer) — fixed 1

## Quick start (Python + HTTP)

```python
import os
import time
import requests

API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"


def create_videoedit_task(req: dict) -> str:
    """Create a video-edit task and return task_id."""
    media = [{"type": "video", "url": req["video_url"]}]
    for url in req.get("reference_images", []):
        media.append({"type": "reference_image", "url": url})
    if len(media) - 1 > 5:
        raise ValueError("At most 5 reference images")

    payload = {
        "model": "happyhorse-1.0-video-edit",
        "input": {"prompt": req["prompt"], "media": media},
        "parameters": {
            "resolution": req.get("resolution", "1080P"),
            "watermark": req.get("watermark", True),
        },
    }
    if req.get("audio_setting"):
        payload["parameters"]["audio_setting"] = req["audio_setting"]
    if req.get("seed") is not None:
        payload["parameters"]["seed"] = req["seed"]

    resp = requests.post(
        f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable",
        },
        json=payload,
    )
    resp.raise_for_status()
    return resp.json()["output"]["task_id"]


def poll_task(task_id: str, interval: int = 15) -> dict:
    while True:
        resp = requests.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
        )
        resp.raise_for_status()
        data = resp.json()
        if data["output"]["task_status"] in ("SUCCEEDED", "FAILED", "CANCELED"):
            return data
        time.sleep(interval)
```

## Usage examples

```python
# Style transfer — instruction only, no reference image
task_id = create_videoedit_task({
    "video_url": "https://example.com/input.mp4",
    "prompt": "将整个画面转换为水墨画风格",
    "resolution": "720P",
})

# Local replacement with a reference image, keep original audio
task_id = create_videoedit_task({
    "video_url": "https://example.com/character.mp4",
    "reference_images": ["https://example.com/striped-sweater.webp"],
    "prompt": "让视频中的马头人身角色穿上图片中的条纹毛衣",
    "audio_setting": "origin",
})
```

## Error handling

| Error | Likely cause | Action |
|---|---|---|
| 401 / `InvalidApiKey` | Missing or invalid `DASHSCOPE_API_KEY` | Check env var or credentials file |
| 400 `InvalidParameter` | Bad resolution, >5 reference images, video out of duration / size limits | Validate parameters and media |
| `current user api does not support synchronous calls` | Missing `X-DashScope-Async: enable` header | Add the required header |
| `task_status: UNKNOWN` | task_id older than 24 hours | Re-create the task |
| 429 | RPS or quota exceeded | Retry with backoff; query RPS default 20 |

## Output location

- Default output: `output/aliyun-happyhorse-videoedit/videos/`
- Override base dir with `OUTPUT_DIR`.

## Anti-patterns

- Do not use any model ID other than `happyhorse-1.0-video-edit`.
- Do not call this API synchronously — async header is required.
- Do not pass more than 1 video, more than 5 reference images, or any `first_frame` / `last_frame` / `driving_audio`.
- Do not pass `ratio` or `duration` — output ratio follows the input video and duration follows the truncation rule.
- Video URLs expire after 24 hours; download and persist immediately.
- Do not use this skill for generation from scratch — use `aliyun-happyhorse-t2v`, `aliyun-happyhorse-i2v`, or `aliyun-happyhorse-r2v` instead.

## Workflow

1) Confirm intent: style transfer vs. instruction edit, and whether reference images are needed.
2) Validate the input video meets format / duration / resolution / fps / size limits.
3) Build the `media` array with exactly 1 `video` plus 0-5 `reference_image` entries.
4) Create async task and poll `/tasks/{task_id}` every ~15s; download `output.video_url` before 24-hour expiration.

## References

- See `references/api_reference.md` for full HTTP API details.
- See `references/sources.md` for source links.
