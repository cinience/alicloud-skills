---
name: aliyun-wan-i2v
description: Use when generating videos from images with DashScope Wan 2.7 image-to-video model (wan2.7-i2v). Use when implementing first-frame video generation, first+last frame interpolation, video continuation, or audio-driven video synthesis via the video-synthesis async API.
---

# Wan 2.7 Image-to-Video

## Validation

```bash
mkdir -p output/aliyun-wan-i2v
python -m py_compile skills/ai/video/aliyun-wan-i2v/scripts/generate_i2v.py && echo "py_compile_ok" > output/aliyun-wan-i2v/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-wan-i2v/validate.txt` is generated.

## Output And Evidence

- Save task IDs, polling responses, and final video URLs to `output/aliyun-wan-i2v/`.
- Keep at least one end-to-end run log for troubleshooting.

## Prerequisites

- Install SDK (recommended in a venv):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Critical model names

- `wan2.7-i2v` — supports first-frame, first+last frame, video continuation, and audio-driven generation

## Capabilities

| Capability | Description | Required media types |
|---|---|---|
| First-frame video | Generate video from a single image | `first_frame` |
| First+last frame | Interpolate video between two images | `first_frame` + `last_frame` |
| Video continuation | Extend an existing video clip | `first_clip` |
| Audio-driven | Drive video with audio (lip-sync, rhythm) | `first_frame` + `driving_audio` |

## API endpoint (async only)

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

Required headers:
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- `X-DashScope-Async: enable`

Singapore endpoint: replace `dashscope.aliyuncs.com` with `dashscope-intl.aliyuncs.com`.

## Normalized interface

### Request
- `prompt` (string, optional) — up to 5000 characters, describes desired video content
- `negative_prompt` (string, optional) — up to 500 characters
- `media` (array, required) — media objects with `type` and `url` fields:
  - `type`: `first_frame` | `last_frame` | `driving_audio` | `first_clip`
  - `url`: public URL (HTTP/HTTPS) or OSS temporary URL
- `resolution` (string, optional) — `720P` or `1080P` (default: `1080P`)
- `duration` (integer, optional) — video length in seconds, range [2, 15] (default: 5)
- `prompt_extend` (boolean, optional) — AI prompt rewriting (default: true)
- `watermark` (boolean, optional) — add "AI generated" watermark (default: false)
- `seed` (integer, optional) — range [0, 2147483647]

### Media input limits

**Images** (first_frame, last_frame):
- Formats: JPEG, JPG, PNG (no transparency), BMP, WEBP
- Resolution: [240, 8000] pixels per side
- Aspect ratio: 1:8 to 8:1
- Max size: 20MB

**Audio** (driving_audio):
- Formats: wav, mp3
- Duration: 2-30s
- Max size: 15MB
- Auto-truncated to `duration` value if longer

**Video** (first_clip):
- Formats: mp4, mov
- Duration: 2-10s
- Resolution: [240, 4096] pixels per side
- Aspect ratio: 1:8 to 8:1
- Max size: 100MB

### Response (task creation)
- `output.task_id` (string) — use for polling, valid 24 hours
- `output.task_status` (string) — PENDING | RUNNING | SUCCEEDED | FAILED | CANCELED
- `request_id` (string)

### Response (task result)
- `output.video_url` (string) — generated video URL
- `output.orig_prompt` (string) — original prompt
- `output.actual_prompt` (string) — rewritten prompt (if prompt_extend enabled)
- `usage.video_count` (integer)
- `usage.video_duration` (integer) — duration in seconds

## Quick start (Python + HTTP)

```python
import os
import json
import time
import requests

API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"

def create_i2v_task(req: dict) -> str:
    """Create an image-to-video task and return task_id."""
    payload = {
        "model": "wan2.7-i2v",
        "input": {
            "prompt": req.get("prompt", ""),
            "media": req["media"],
        },
        "parameters": {
            "resolution": req.get("resolution", "1080P"),
            "duration": req.get("duration", 5),
            "prompt_extend": req.get("prompt_extend", True),
            "watermark": req.get("watermark", False),
        },
    }
    if req.get("negative_prompt"):
        payload["input"]["negative_prompt"] = req["negative_prompt"]
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
    data = resp.json()
    return data["output"]["task_id"]


def poll_task(task_id: str, interval: int = 15) -> dict:
    """Poll until task completes. Returns final response."""
    while True:
        resp = requests.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
        )
        resp.raise_for_status()
        data = resp.json()
        status = data["output"]["task_status"]
        if status in ("SUCCEEDED", "FAILED", "CANCELED"):
            return data
        time.sleep(interval)
```

## Media combination examples

```python
# First-frame only
media = [{"type": "first_frame", "url": "https://example.com/image.jpg"}]

# First + last frame interpolation
media = [
    {"type": "first_frame", "url": "https://example.com/start.jpg"},
    {"type": "last_frame", "url": "https://example.com/end.jpg"},
]

# Audio-driven from first frame
media = [
    {"type": "first_frame", "url": "https://example.com/face.jpg"},
    {"type": "driving_audio", "url": "https://example.com/speech.mp3"},
]

# Video continuation
media = [{"type": "first_clip", "url": "https://example.com/clip.mp4"}]
```

## Error handling

| Error | Likely cause | Action |
|---|---|---|
| 401/403 | Missing or invalid `DASHSCOPE_API_KEY` | Check env var or credentials file |
| 400 `InvalidParameter` | Unsupported resolution, bad duration, missing media | Validate parameters |
| "does not support synchronous calls" | Missing `X-DashScope-Async: enable` header | Add required header |
| 429 | Rate limit or quota | Retry with backoff |

## Output location

- Default output: `output/aliyun-wan-i2v/videos/`
- Override base dir with `OUTPUT_DIR`.

## Anti-patterns

- Do not use model names other than `wan2.7-i2v`.
- Do not call this API synchronously — async header is required.
- Do not pass duplicate media types (e.g., two `first_frame` entries).
- Video URLs expire after 24 hours; download and persist immediately.
- Do not use this API for video editing — use `aliyun-wan-videoedit` instead.

## Workflow

1) Confirm user intent: first-frame, first+last frame, video continuation, or audio-driven.
2) Prepare media array with correct types and valid URLs.
3) Create async task and poll for results.
4) Download and save generated video before URL expiration.

## References

- See `references/api_reference.md` for full HTTP API details.
- See `references/sources.md` for source links.
