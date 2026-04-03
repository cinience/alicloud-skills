---
name: aliyun-wan-videoedit
description: Use when editing videos with DashScope Wan 2.7 video editing model (wan2.7-videoedit). Use when implementing video style transfer, instruction-based video editing with optional reference images, or video content modification via the video-synthesis async API.
---

# Wan 2.7 Video Editing

## Validation

```bash
mkdir -p output/aliyun-wan-videoedit
python -m py_compile skills/ai/video/aliyun-wan-videoedit/scripts/edit_video.py && echo "py_compile_ok" > output/aliyun-wan-videoedit/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-wan-videoedit/validate.txt` is generated.

## Output And Evidence

- Save task IDs, polling responses, and final video URLs to `output/aliyun-wan-videoedit/`.
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

- `wan2.7-videoedit` — supports style transfer and instruction-based video editing

## Capabilities

| Capability | Description | Required media |
|---|---|---|
| Style transfer | Convert video to a different visual style (clay, anime, etc.) | `video` only |
| Instruction editing | Edit video content with text instructions and optional reference images | `video` + optional `reference_image` (up to 3) |

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
- `prompt` (string, optional) — up to 5000 characters, describes desired editing
- `negative_prompt` (string, optional) — up to 500 characters
- `media` (array, required) — media objects with `type` and `url` fields:
  - `type`: `video` (required, exactly 1) | `reference_image` (optional, up to 3)
  - `url`: public URL (HTTP/HTTPS) or OSS temporary URL
- `resolution` (string, optional) — `720P` or `1080P` (default: `1080P`)
- `ratio` (string, optional) — output aspect ratio: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`. If omitted, follows input video ratio.
- `duration` (integer, optional) — truncate input video to this length in seconds, range [2, 10]. Default `0` (use input video duration).
- `audio_setting` (string, optional) — `auto` (default, AI decides) or `origin` (keep original audio)
- `prompt_extend` (boolean, optional) — AI prompt rewriting (default: true)
- `watermark` (boolean, optional) — add "AI generated" watermark (default: false)
- `seed` (integer, optional) — range [0, 2147483647]

### Media input limits

**Video** (type=video):
- Formats: mp4, mov
- Duration: 2-10s
- Resolution: [240, 4096] pixels per side
- Aspect ratio: 1:8 to 8:1
- Max size: 100MB

**Reference images** (type=reference_image):
- Formats: JPEG, JPG, PNG (no transparency), BMP, WEBP
- Resolution: [240, 8000] pixels per side
- Aspect ratio: 1:8 to 8:1
- Max size: 20MB
- Maximum 3 reference images

### Resolution output table

| Resolution | Ratio | Output (W*H) |
|---|---|---|
| 720P | 16:9 | 1280*720 |
| 720P | 9:16 | 720*1280 |
| 720P | 1:1 | 960*960 |
| 720P | 4:3 | 1104*832 |
| 720P | 3:4 | 832*1104 |
| 1080P | 16:9 | 1920*1080 |
| 1080P | 9:16 | 1080*1920 |
| 1080P | 1:1 | 1440*1440 |
| 1080P | 4:3 | 1648*1248 |
| 1080P | 3:4 | 1248*1648 |

### Response (task creation)
- `output.task_id` (string) — use for polling, valid 24 hours
- `output.task_status` (string) — PENDING | RUNNING | SUCCEEDED | FAILED | CANCELED
- `request_id` (string)

### Response (task result)
- `output.video_url` (string) — edited video URL
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

def create_videoedit_task(req: dict) -> str:
    """Create a video editing task and return task_id."""
    payload = {
        "model": "wan2.7-videoedit",
        "input": {
            "prompt": req.get("prompt", ""),
            "media": req["media"],
        },
        "parameters": {
            "resolution": req.get("resolution", "1080P"),
            "prompt_extend": req.get("prompt_extend", True),
            "watermark": req.get("watermark", False),
        },
    }
    if req.get("negative_prompt"):
        payload["input"]["negative_prompt"] = req["negative_prompt"]
    if req.get("ratio"):
        payload["parameters"]["ratio"] = req["ratio"]
    if req.get("duration"):
        payload["parameters"]["duration"] = req["duration"]
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

## Usage examples

```python
# Style transfer — convert to clay style
media = [{"type": "video", "url": "https://example.com/input.mp4"}]
task_id = create_videoedit_task({
    "prompt": "将整个画面转换为黏土风格",
    "media": media,
    "resolution": "720P",
})

# Instruction editing with reference image
media = [
    {"type": "video", "url": "https://example.com/input.mp4"},
    {"type": "reference_image", "url": "https://example.com/hat.jpg"},
]
task_id = create_videoedit_task({
    "prompt": "为人物换上酷闪的衣服，再戴参考图里的帽子",
    "media": media,
    "audio_setting": "origin",
})
```

## Error handling

| Error | Likely cause | Action |
|---|---|---|
| 401/403 | Missing or invalid `DASHSCOPE_API_KEY` | Check env var or credentials file |
| 400 `InvalidParameter` | Bad resolution, missing video, too many reference images | Validate parameters |
| "does not support synchronous calls" | Missing `X-DashScope-Async: enable` header | Add required header |
| 429 | Rate limit or quota | Retry with backoff |

## Output location

- Default output: `output/aliyun-wan-videoedit/videos/`
- Override base dir with `OUTPUT_DIR`.

## Anti-patterns

- Do not use model names other than `wan2.7-videoedit`.
- Do not call this API synchronously — async header is required.
- Do not pass more than 1 video or more than 3 reference images.
- Video URLs expire after 24 hours; download and persist immediately.
- Do not use this API for video generation — use `aliyun-wan-i2v` instead.

## Workflow

1) Confirm user intent: style transfer or instruction-based editing.
2) Prepare media array with video (required) and optional reference images.
3) Create async task and poll for results.
4) Download and save edited video before URL expiration.

## References

- See `references/api_reference.md` for full HTTP API details.
- See `references/sources.md` for source links.
