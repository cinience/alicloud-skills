---
name: aliyun-wan-animate-move
description: Use when generating motion videos from a person image and a reference video with DashScope Wan 2.2 animate-move model (wan2.2-animate-move). Use when transferring actions, expressions, or dance moves from a reference video onto a character image via the image2video async API.
---

# Wan 2.2 Animate Move (Image-to-Motion)

## Validation

```bash
mkdir -p output/aliyun-wan-animate-move
python -m py_compile skills/ai/video/aliyun-wan-animate-move/scripts/generate_animate_move.py && echo "py_compile_ok" > output/aliyun-wan-animate-move/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-wan-animate-move/validate.txt` is generated.

## Output And Evidence

- Save task IDs, polling responses, and final video URLs to `output/aliyun-wan-animate-move/`.
- Keep at least one end-to-end run log for troubleshooting.

## Prerequisites

- Install SDK (recommended in a venv):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install requests
```
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Critical model names

- `wan2.2-animate-move` -- supports motion transfer from reference video to character image

## Capabilities

| Capability | Description | Required inputs |
|---|---|---|
| Motion transfer | Transfer actions/expressions from reference video to character image | `image_url` + `video_url` |

## Service modes

| Mode | Description |
|---|---|
| `wan-std` | Standard mode, faster generation, cost-effective, suitable for preview and basic animation |
| `wan-pro` | Professional mode, smoother animation, better quality, longer processing time |

## API endpoint (async only)

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis
```

Required headers:
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- `X-DashScope-Async: enable`

Singapore endpoint: replace `dashscope.aliyuncs.com` with `dashscope-intl.aliyuncs.com`.

## Normalized interface

### Request
- `image_url` (string, required) -- public HTTP/HTTPS URL of the character image
- `video_url` (string, required) -- public HTTP/HTTPS URL of the reference motion video
- `watermark` (boolean, optional) -- add watermark (default: false)
- `mode` (string, required) -- `wan-std` or `wan-pro`
- `check_image` (boolean, optional) -- whether to perform image detection (default: true)

### Image input limits

- Formats: JPG, JPEG, PNG, BMP, WEBP
- Resolution: [200, 4096] pixels per side
- Aspect ratio: 1:3 to 3:1
- Max size: 5MB
- Content: single person, facing camera, face fully visible, moderate proportion in frame

### Video input limits

- Formats: MP4, AVI, MOV
- Duration: 2-30s
- Resolution: [200, 2048] pixels per side
- Aspect ratio: 1:3 to 3:1
- Max size: 200MB
- Content: single person, facing camera, face fully visible, moderate proportion in frame

### Response (task creation)
- `output.task_id` (string) -- use for polling, valid 24 hours
- `output.task_status` (string) -- PENDING | RUNNING | SUCCEEDED | FAILED | CANCELED | UNKNOWN
- `request_id` (string)

### Response (task result)
- `output.video_url` (string) -- generated video URL
- `usage.video_count` (integer)
- `usage.video_duration` (integer) -- duration in seconds

## Quick start (Python + HTTP)

```python
import os
import json
import time
import requests

API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"

def create_animate_move_task(image_url: str, video_url: str, mode: str = "wan-std") -> str:
    """Create an animate-move task and return task_id."""
    payload = {
        "model": "wan2.2-animate-move",
        "input": {
            "image_url": image_url,
            "video_url": video_url,
            "watermark": False,
        },
        "parameters": {
            "mode": mode,
        },
    }
    resp = requests.post(
        f"{BASE_URL}/services/aigc/image2video/video-synthesis",
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

## Error handling

| Error | Likely cause | Action |
|---|---|---|
| 401/403 | Missing or invalid `DASHSCOPE_API_KEY` | Check env var or credentials file |
| 400 `InvalidParameter` | Unsupported image/video format, bad dimensions, missing fields | Validate parameters |
| "does not support synchronous calls" | Missing `X-DashScope-Async: enable` header | Add required header |
| 429 | Rate limit or quota | Retry with backoff |

## Output location

- Default output: `output/aliyun-wan-animate-move/videos/`
- Override base dir with `OUTPUT_DIR`.

## Anti-patterns

- Do not use model names other than `wan2.2-animate-move`.
- Do not call this API synchronously -- async header is required.
- Do not use multiple people in image or video -- single person only.
- Video URLs expire after 24 hours; download and persist immediately.
- Do not use images with occluded faces or extreme proportions.

## Workflow

1) Confirm user intent: transfer motion from reference video to character image.
2) Select service mode: `wan-std` (fast/cheap) or `wan-pro` (high quality).
3) Prepare image URL and video URL with valid formats and dimensions.
4) Create async task and poll for results.
5) Download and save generated video before URL expiration.

## References

- See `references/api_reference.md` for full HTTP API details.
- See `references/sources.md` for source links.
