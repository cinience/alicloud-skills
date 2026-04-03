---
name: aliyun-video-style-repaint
description: Use when transforming video style with DashScope video-style-transform model. Use when converting videos to artistic styles such as Japanese manga, American comics, 3D cartoon, Chinese ink painting, paper art, or simple illustration via the video-synthesis async API.
---

# Video Style Repaint

## Validation

```bash
mkdir -p output/aliyun-video-style-repaint
python -m py_compile skills/ai/video/aliyun-video-style-repaint/scripts/repaint_video.py && echo "py_compile_ok" > output/aliyun-video-style-repaint/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-video-style-repaint/validate.txt` is generated.

## Output And Evidence

- Save task IDs, polling responses, and final video URLs to `output/aliyun-video-style-repaint/`.
- Keep at least one end-to-end run log for troubleshooting.

## Prerequisites

- Install SDK (recommended in a venv):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install requests
```
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.
- This API is only available in the Beijing region. You must use a Beijing-region API Key.

## Critical model names

- `video-style-transform` -- supports 8 preset artistic styles

## Supported styles

| Style ID | Name (EN) | Name (CN) |
|---|---|---|
| 0 | Japanese Manga | 日式漫画 |
| 1 | American Comics | 美式漫画 |
| 2 | Fresh Comics | 清新漫画 |
| 3 | 3D Cartoon | 3D 卡通 |
| 4 | Chinese Cartoon | 国风卡通 |
| 5 | Paper Art | 纸艺风格 |
| 6 | Simple Illustration | 简易插画 |
| 7 | Chinese Ink Painting | 国风水墨 |

## API endpoint (async only)

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

Required headers:
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- `X-DashScope-Async: enable`

## Normalized interface

### Request
- `video_url` (string, required) -- public HTTP/HTTPS URL of the input video
- `style` (integer, optional) -- style ID 0-7 (default: 0, Japanese Manga)
- `video_fps` (integer, optional) -- output frame rate, range [15, 25] (default: 15)
- `animate_emotion` (boolean, optional) -- facial expression optimization (default: true)
- `min_len` (integer, optional) -- output short-side pixels, 720 or 540 (default: 720)
- `use_SR` (boolean, optional) -- super-resolution enhancement (default: false)

### Video input limits

- Formats: MP4, AVI, MKV, MOV, FLV, TS, MPG, MXF
- Resolution: [256, 4096] pixels per side, aspect ratio max 1.8:1
- Duration: up to 30 seconds
- Max size: 100MB
- URL: must be URL-encoded if contains non-ASCII characters

### Response (task creation)
- `output.task_id` (string) -- use for polling, valid 24 hours
- `output.task_status` (string) -- PENDING | RUNNING | SUSPENDED | SUCCEEDED | FAILED
- `request_id` (string)

### Response (task result)
- `output.output_video_url` (string) -- result video URL
- `output.task_status` (string) -- final status
- `output.submit_time` (string) -- task submission time
- `output.scheduled_time` (string) -- task execution start time
- `output.end_time` (string) -- task completion time
- `usage.duration` (integer) -- video duration in seconds
- `usage.SR` (integer) -- resolution used

## Quick start (Python + HTTP)

```python
import os
import json
import time
import requests

API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"

def create_style_repaint_task(video_url: str, style: int = 0) -> str:
    """Create a video style repaint task and return task_id."""
    payload = {
        "model": "video-style-transform",
        "input": {
            "video_url": video_url,
        },
        "parameters": {
            "style": style,
            "video_fps": 15,
        },
    }
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
        if status in ("SUCCEEDED", "FAILED", "CANCELED", "SUSPENDED"):
            return data
        time.sleep(interval)
```

## Error handling

| Error | Likely cause | Action |
|---|---|---|
| 401/403 | Missing or invalid `DASHSCOPE_API_KEY` | Check env var or credentials file |
| 400 `InvalidParameter` | Unsupported video format, bad dimensions, invalid style | Validate parameters |
| "does not support synchronous calls" | Missing `X-DashScope-Async: enable` header | Add required header |
| 429 | Rate limit or quota | Retry with backoff |

## Output location

- Default output: `output/aliyun-video-style-repaint/videos/`
- Override base dir with `OUTPUT_DIR`.

## Anti-patterns

- Do not use model names other than `video-style-transform`.
- Do not call this API synchronously -- async header is required.
- Do not use style IDs outside 0-7 range.
- Video URLs expire after 24 hours; download and persist immediately.
- Do not use Singapore endpoint -- this API is Beijing-region only.

## Workflow

1) Confirm user intent: select desired artistic style from the 8 presets.
2) Prepare video URL with valid format and dimensions.
3) Configure parameters (style, fps, resolution, super-resolution).
4) Create async task and poll for results.
5) Download and save transformed video before URL expiration.

## References

- See `references/api_reference.md` for full HTTP API details.
- See `references/sources.md` for source links.
