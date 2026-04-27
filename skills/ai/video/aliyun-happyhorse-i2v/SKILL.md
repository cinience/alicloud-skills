---
name: aliyun-happyhorse-i2v
description: Use when generating videos from a single first-frame image with DashScope HappyHorse 1.0 image-to-video model (happyhorse-1.0-i2v). Use when implementing first-frame video generation with optional text guidance via the video-synthesis async API on Alibaba Cloud Model Studio.
---

# HappyHorse 1.0 Image-to-Video (First Frame)

## Validation

```bash
mkdir -p output/aliyun-happyhorse-i2v
python -m py_compile skills/ai/video/aliyun-happyhorse-i2v/scripts/i2v_happyhorse.py && echo "py_compile_ok" > output/aliyun-happyhorse-i2v/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-happyhorse-i2v/validate.txt` is generated.

## Output And Evidence

- Save task IDs, polling responses, and final video URLs to `output/aliyun-happyhorse-i2v/`.
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

- `happyhorse-1.0-i2v` — first-frame image-to-video; output aspect ratio follows the input image automatically

## Capabilities

| Capability | Description | Required media |
|---|---|---|
| First-frame video | Generate a video from one first-frame image, optionally guided by a text prompt | `first_frame` (exactly 1) |

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
- `model` (string, required) — fixed `happyhorse-1.0-i2v`
- `input.prompt` (string, optional) — up to 5000 non-CJK / 2500 CJK characters
- `input.media` (array, required) — exactly one element with:
  - `type`: `first_frame`
  - `url`: public HTTP/HTTPS URL of the first-frame image
- `parameters.resolution` (string, optional) — `720P` or `1080P` (default: `1080P`)
- `parameters.duration` (integer, optional) — video length in seconds, range [3, 15] (default: 5)
- `parameters.watermark` (boolean, optional) — bottom-right "Happy Horse" watermark (default: `true`)
- `parameters.seed` (integer, optional) — range [0, 2147483647]

The output video aspect ratio follows the input first-frame image; **`ratio` is not supported** for i2v.

### Media input limits

**First-frame image** (`type=first_frame`):
- Formats: JPEG, JPG, PNG, WEBP
- Resolution: width and height ≥ 300 pixels
- Aspect ratio: 1:2.5 ~ 2.5:1
- Max size: 10 MB

### Response (task creation)
- `output.task_id` (string) — valid 24 hours
- `output.task_status` (string) — `PENDING` | `RUNNING` | `SUCCEEDED` | `FAILED` | `CANCELED` | `UNKNOWN`
- `request_id` (string)

### Response (task result, on SUCCEEDED)
- `output.video_url` (string) — generated MP4 (H.264, 24fps) URL, valid 24 hours
- `output.orig_prompt` (string)
- `output.submit_time` / `output.scheduled_time` / `output.end_time` (string)
- `usage.duration` (integer) — billable duration in seconds
- `usage.output_video_duration` (integer)
- `usage.input_video_duration` (integer) — fixed 0 for i2v
- `usage.SR` (integer) — output resolution tier
- `usage.video_count` (integer) — fixed 1

## Quick start (Python + HTTP)

```python
import os
import time
import requests

API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"


def create_i2v_task(req: dict) -> str:
    """Create an image-to-video task and return task_id."""
    payload = {
        "model": "happyhorse-1.0-i2v",
        "input": {
            "prompt": req.get("prompt", ""),
            "media": [{"type": "first_frame", "url": req["first_frame_url"]}],
        },
        "parameters": {
            "resolution": req.get("resolution", "1080P"),
            "duration": req.get("duration", 5),
            "watermark": req.get("watermark", True),
        },
    }
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
# Minimal — first-frame only
task_id = create_i2v_task({
    "first_frame_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png",
    "prompt": "一只猫在草地上奔跑",
    "duration": 5,
})

# 720P with custom seed for reproducibility
task_id = create_i2v_task({
    "first_frame_url": "https://example.com/portrait.jpg",
    "prompt": "Slow head turn, soft window light",
    "resolution": "720P",
    "duration": 8,
    "seed": 42,
})
```

## Error handling

| Error | Likely cause | Action |
|---|---|---|
| 401 / `InvalidApiKey` | Missing or invalid `DASHSCOPE_API_KEY` | Check env var or credentials file |
| 400 `InvalidParameter` | Wrong resolution, duration out of [3,15], image too small or wrong format | Validate parameters and image |
| `current user api does not support synchronous calls` | Missing `X-DashScope-Async: enable` header | Add the required header |
| `task_status: UNKNOWN` | task_id older than 24 hours | Re-create the task |
| 429 | RPS or quota exceeded | Retry with backoff; query RPS default 20 |

## Output location

- Default output: `output/aliyun-happyhorse-i2v/videos/`
- Override base dir with `OUTPUT_DIR`.

## Anti-patterns

- Do not use any model ID other than `happyhorse-1.0-i2v`.
- Do not call this API synchronously — async header is required.
- Do not pass `ratio` — output aspect ratio follows the first-frame image automatically.
- Do not pass more than 1 first-frame, or any `last_frame` / `reference_image` / `video` — only `first_frame` is supported.
- Video URLs expire after 24 hours; download and persist immediately.
- Do not use this skill for pure text-to-video (use `aliyun-happyhorse-t2v`), reference-image fusion (`aliyun-happyhorse-r2v`), or video editing (`aliyun-happyhorse-videoedit`).

## Workflow

1) Confirm intent: single first-frame image with optional text prompt.
2) Validate the image meets format / size / resolution / aspect-ratio limits.
3) Create async task and poll `/tasks/{task_id}` every ~15s.
4) Download `output.video_url` before the 24-hour expiration.

## References

- See `references/api_reference.md` for full HTTP API details.
- See `references/sources.md` for source links.
