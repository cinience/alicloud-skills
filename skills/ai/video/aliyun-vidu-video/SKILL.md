---
name: aliyun-vidu-video
description: Use when generating videos with DashScope Vidu models. Use when implementing text-to-video, image-to-video (first frame), keyframe-to-video (first+last frame), or reference-to-video generation via the video-synthesis async API.
---

# Vidu Video Generation

## Validation

```bash
mkdir -p output/aliyun-vidu-video
python -m py_compile skills/ai/video/aliyun-vidu-video/scripts/generate_vidu_video.py && echo "py_compile_ok" > output/aliyun-vidu-video/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-vidu-video/validate.txt` is generated.

## Output And Evidence

- Save task IDs, polling responses, and final video URLs to `output/aliyun-vidu-video/`.
- Keep at least one end-to-end run log for troubleshooting.

## Prerequisites

- Set `DASHSCOPE_API_KEY` in your environment (Beijing region key required).
- Region: China Mainland (Beijing) only. Model, Endpoint URL, and API Key must belong to the same region.
- Enable Vidu models in the Alibaba Cloud Model Studio console before first use.

## Critical model names

### Text-to-video
- `vidu/viduq3-pro_text2video`
- `vidu/viduq3-turbo_text2video`
- `vidu/viduq2_text2video`

### Image-to-video (first frame)
- `vidu/viduq3-pro_img2video`
- `vidu/viduq3-turbo_img2video`
- `vidu/viduq2-pro_img2video`
- `vidu/viduq2-turbo_img2video`

### Keyframe-to-video (first+last frame)
- `vidu/viduq3-pro_start-end2video`
- `vidu/viduq3-turbo_start-end2video`
- `vidu/viduq2-pro_start-end2video`
- `vidu/viduq2-turbo_start-end2video`

### Reference-to-video
- `vidu/viduq2_reference2video`
- `vidu/viduq2-pro_reference2video`

## Capabilities

| Capability | Description | Model suffix | Required input |
|---|---|---|---|
| Text-to-video | Generate video from text prompt only | `_text2video` | `prompt` |
| Image-to-video | Generate video from a single image + optional prompt | `_img2video` | `media[image]` |
| Keyframe-to-video | Interpolate video between first and last frame images | `_start-end2video` | `media[image x2]` + `prompt` |
| Reference-to-video | Embed reference subject(s) into prompted scene | `_reference2video` | `media[image 1-7]` + `prompt` |

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
- `model` (string, required) -- one of the model names listed above
- `input.prompt` (string) -- up to 5000 characters, describes desired video content
  - Required for text-to-video, keyframe, and reference modes
  - Optional for image-to-video
- `input.media` (array) -- media objects with `type` and `url` fields (not used for text-to-video)
  - `type`: `image` or `video`
  - `url`: public URL (HTTP/HTTPS)
- `parameters.resolution` (string, optional) -- `540P`, `720P` (default), or `1080P`
- `parameters.size` (string, optional) -- pixel dimensions `width*height` (e.g., `1280*720`). Values depend on resolution tier. For text-to-video and reference-to-video, explicit size values are supported.
- `parameters.duration` (integer, optional) -- video length in seconds
  - Q3 models: [1, 16], default 5
  - Q2 models: [1, 10], default 5
- `parameters.audio` (boolean, optional) -- generate audio track (Q3 models only, default false)
- `parameters.watermark` (boolean, optional) -- add "AI generated" watermark (default false)
- `parameters.seed` (integer, optional) -- range [0, 2147483647]

### Size values by resolution tier (text-to-video)

| Resolution | Aspect ratio | Size (width*height) |
|---|---|---|
| 540P | 16:9 | 960*528 |
| 540P | 9:16 | 528*960 |
| 540P | 1:1 | 720*720 |
| 540P | 4:3 | 816*608 |
| 540P | 3:4 | 608*816 |
| 720P | 16:9 | 1280*720 |
| 720P | 9:16 | 720*1280 |
| 720P | 1:1 | 960*960 |
| 720P | 4:3 | 1104*816 |
| 720P | 3:4 | 816*1104 |
| 1080P | 16:9 | 1920*1080 |
| 1080P | 9:16 | 1080*1920 |
| 1080P | 1:1 | 1440*1440 |
| 1080P | 4:3 | 1674*1238 |
| 1080P | 3:4 | 1238*1674 |

### Size values by resolution tier (reference-to-video)

| Resolution | Aspect ratio | Size (width*height) |
|---|---|---|
| 540P | 16:9 | 960*540 |
| 540P | 9:16 | 540*960 |
| 540P | 1:1 | 540*540 |
| 540P | 4:3 | 720*540 |
| 540P | 3:4 | 540*720 |
| 720P | 16:9 | 1280*720 |
| 720P | 9:16 | 720*1280 |
| 720P | 1:1 | 720*720 |
| 720P | 4:3 | 960*720 |
| 720P | 3:4 | 720*960 |
| 1080P | 16:9 | 1920*1080 |
| 1080P | 9:16 | 1080*1920 |
| 1080P | 1:1 | 1080*1080 |
| 1080P | 4:3 | 1440*1080 |
| 1080P | 3:4 | 1080*1440 |

### Media input limits

**Images** (type=image):
- Formats: JPG, PNG, WEBP
- Aspect ratio: 1:4 to 4:1
- Max size: 50MB

**Videos** (type=video, reference-to-video only):
- Formats: mp4, avi, mov
- Resolution: min 128x128 pixels
- Aspect ratio: 1:4 to 4:1
- Duration: 1-5s
- Max size: 50MB

### Response (task creation)
- `output.task_id` (string) -- use for polling, valid 24 hours
- `output.task_status` (string) -- PENDING | RUNNING | SUCCEEDED | FAILED | CANCELED | UNKNOWN
- `request_id` (string)

### Response (task result)
- `output.video_url` (string) -- generated video URL (MP4, H.264), valid 24 hours
- `output.orig_prompt` (string) -- original prompt
- `usage.duration` (integer) -- billable video duration in seconds
- `usage.output_video_duration` (integer) -- actual output duration
- `usage.size` (string) -- output resolution
- `usage.fps` (integer) -- frame rate (24)
- `usage.audio` (boolean) -- whether audio was generated
- `usage.SR` (string) -- resolution tier

## Quick start (Python + HTTP)

```python
import os
import json
import time
import requests

API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"

def create_vidu_task(req: dict) -> str:
    """Create a Vidu video generation task and return task_id."""
    payload = {
        "model": req["model"],
        "input": {},
        "parameters": {
            "resolution": req.get("resolution", "720P"),
            "duration": req.get("duration", 5),
        },
    }
    if req.get("prompt"):
        payload["input"]["prompt"] = req["prompt"]
    if req.get("media"):
        payload["input"]["media"] = req["media"]
    if req.get("size"):
        payload["parameters"]["size"] = req["size"]
    if req.get("audio") is not None:
        payload["parameters"]["audio"] = req["audio"]
    if req.get("watermark") is not None:
        payload["parameters"]["watermark"] = req["watermark"]
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

## Mode-specific examples

```python
# Text-to-video
task_id = create_vidu_task({
    "model": "vidu/viduq3-turbo_text2video",
    "prompt": "A cat running under moonlight",
    "resolution": "540P",
    "size": "960*528",
    "duration": 5,
})

# Image-to-video (first frame)
task_id = create_vidu_task({
    "model": "vidu/viduq3-pro_img2video",
    "prompt": "Camera slowly pans upward",
    "media": [{"type": "image", "url": "https://example.com/image.jpg"}],
    "resolution": "720P",
    "duration": 5,
})

# Keyframe-to-video (first + last frame)
task_id = create_vidu_task({
    "model": "vidu/viduq3-turbo_start-end2video",
    "prompt": "A cat jumps from windowsill to sofa",
    "media": [
        {"type": "image", "url": "https://example.com/first.png"},
        {"type": "image", "url": "https://example.com/last.png"},
    ],
    "resolution": "540P",
    "duration": 5,
})

# Reference-to-video
task_id = create_vidu_task({
    "model": "vidu/viduq2_reference2video",
    "prompt": "Man playing guitar in a cafe",
    "media": [
        {"type": "image", "url": "https://example.com/ref1.jpg"},
        {"type": "image", "url": "https://example.com/ref2.jpg"},
    ],
    "resolution": "720P",
    "size": "1280*720",
    "duration": 5,
})
```

## Error handling

| Error | Likely cause | Action |
|---|---|---|
| 401/403 | Missing or invalid `DASHSCOPE_API_KEY` | Check env var; ensure Beijing region key |
| 400 `InvalidParameter` | Unsupported resolution/size combo, bad duration, missing media | Validate parameters against size tables |
| "does not support synchronous calls" | Missing `X-DashScope-Async: enable` header | Add required header |
| 429 | Rate limit or quota | Retry with backoff |
| Cross-region error | Model and API Key from different regions | Ensure all are Beijing region |

## Output location

- Default output: `output/aliyun-vidu-video/videos/`
- Override base dir with `OUTPUT_DIR`.

## Anti-patterns

- Do not use model names not listed in "Critical model names" above.
- Do not call this API synchronously -- async header is required.
- Do not omit `size` when using reference-to-video -- it is required for that mode.
- Do not pass `audio=true` with Q2 models -- only Q3 models support audio generation.
- Video URLs expire after 24 hours; download and persist immediately.
- For image-to-video, supply exactly 1 image. For keyframe, supply exactly 2 images (first, then last).
- For reference-to-video with `viduq2_reference2video`, only images are accepted (1-7). For `viduq2-pro_reference2video`, images (1-4) plus optional videos (1-2) are accepted.
- Keyframe mode: first and last frame pixel count ratio must be between 0.8 and 1.25.

## Workflow

1) Confirm user intent: text-to-video, image-to-video, keyframe, or reference-to-video.
2) Select the appropriate model name based on capability and quality tier (Q3 pro/turbo or Q2).
3) Prepare input: prompt and/or media array with correct types and valid public URLs.
4) Set resolution, size, and duration parameters.
5) Create async task and poll for results (15s interval recommended).
6) Download and save generated video before URL expiration (24 hours).

## References

- See `references/api_reference.md` for full HTTP API details.
- See `references/sources.md` for source links.
