---
name: aliyun-kling-video
description: Use when generating videos with Kling v3 models on DashScope (kling/kling-v3-video-generation, kling/kling-v3-omni-video-generation). Use when implementing text-to-video, image-to-video, reference-to-video, smart storyboard, or video editing via the video-synthesis async API.
---

# Kling V3 Video Generation

## Validation

```bash
mkdir -p output/aliyun-kling-video
python -m py_compile skills/ai/video/aliyun-kling-video/scripts/generate_kling_video.py && echo "py_compile_ok" > output/aliyun-kling-video/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-kling-video/validate.txt` is generated.

## Output And Evidence

- Save task IDs, polling responses, and final video URLs to `output/aliyun-kling-video/`.
- Keep at least one end-to-end run log for troubleshooting.

## Prerequisites

- Install dependencies (recommended in a venv):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install requests
```
- Set `DASHSCOPE_API_KEY` in your environment (must be Beijing region API Key).
- Enable Kling in [百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) — search "kling" and activate.

## Critical model names

- `kling/kling-v3-video-generation` — standard model: t2v, i2v (first frame, first+last frame)
- `kling/kling-v3-omni-video-generation` — omni model: adds reference-to-video, video editing, multi-subject references

## Capabilities

| Capability | Model | Required media |
|---|---|---|
| Text-to-video | both | none |
| Smart storyboard (multi-shot) | both | none (use `multi_prompt`) |
| Image-to-video (first frame) | both | `first_frame` |
| Image-to-video (first+last frame) | both | `first_frame` + `last_frame` |
| Reference-to-video | omni only | `refer` and/or `feature` |
| Video editing | omni only | `base` + optional `refer` |

## API endpoint (async only)

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

Required headers:
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- `X-DashScope-Async: enable`

**Region**: Beijing only. No Singapore endpoint.

## Normalized interface

### Request (input)
- `prompt` (string, conditional) — up to 2500 characters. Required for `shot_type=intelligence`. For omni reference-to-video, use `<<<element_1>>>`, `<<<image_1>>>`, `<<<video_1>>>` to reference media.
- `negative_prompt` (string, optional) — content to exclude
- `media` (array, optional) — media objects with `type` and `url`:
  - Standard model types: `first_frame`, `last_frame`
  - Omni model types: `first_frame`, `last_frame`, `refer`, `base`, `feature`
- `multi_shot` (boolean, optional) — enable multi-shot generation (default: false)
- `shot_type` (string, conditional) — `intelligence` (AI auto-split) or `customize` (manual). Required when `multi_shot=true`.
- `multi_prompt` (array, optional) — per-shot prompts when `shot_type=customize`
- `element_list` (array, optional) — multi-subject element images (omni model only)
- `keep_original_sound` (string, optional) — `no` (default) or `yes`, for videos (omni model only)

### Request (parameters)
- `mode` (string, optional) — `pro` (default, 1080P) or `std` (720P)
- `aspect_ratio` (string, conditional) — `16:9` (default), `9:16`, `1:1`. Required for t2v and reference-to-video.
- `duration` (integer, optional) — video length [3, 15] seconds (default: 5). When using reference video, [3, 10].
- `audio` (boolean, optional) — generate audio (default: false). Affects pricing.
- `watermark` (boolean, optional) — add "可灵 AI" watermark (default: false)

### Media input limits

**Images** (first_frame, last_frame, refer):
- Formats: JPEG, JPG, PNG (no transparency)
- Resolution: [300, 8000] pixels per side
- Max size: 10MB

**Videos** (base, feature):
- Formats: mp4, mov
- Duration: 3-10s
- Resolution: [720, 2160] pixels per side
- Frame rate: 24-60 fps
- Max size: 200MB

### Media combination rules

**kling/kling-v3-video-generation**:
- i2v first frame: `first_frame` (1 image)
- i2v first+last: `first_frame` + `last_frame` (1 each)

**kling/kling-v3-omni-video-generation** (all above plus):
- Reference: `feature` only (1 video), or `refer` only (up to 7 with elements), or `feature+refer` (1 video + up to 4 with elements), or `feature+first_frame` (1 video + 1 image)
- Video editing: `base` only (1 video), or `base+refer` (1 video + up to 4 with elements)

### Response (task creation)
- `output.task_id` (string) — valid 24 hours
- `output.task_status` (string) — PENDING | RUNNING | SUCCEEDED | FAILED | CANCELED
- `request_id` (string)

### Response (task result)
- `output.video_url` (string) — generated video URL
- `output.watermark_video_url` (string) — watermarked video URL
- `usage.duration` (integer), `usage.size` (string), `usage.fps` (integer), `usage.audio` (boolean)

## Quick start (Python + HTTP)

```python
import os
import json
import time
import requests

API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"

def create_kling_task(req: dict) -> str:
    """Create a Kling video generation task and return task_id."""
    payload = {
        "model": req.get("model", "kling/kling-v3-video-generation"),
        "input": {"prompt": req.get("prompt", "")},
        "parameters": {
            "mode": req.get("mode", "pro"),
            "duration": req.get("duration", 5),
            "audio": req.get("audio", False),
            "watermark": req.get("watermark", False),
        },
    }
    if req.get("aspect_ratio"):
        payload["parameters"]["aspect_ratio"] = req["aspect_ratio"]
    if req.get("negative_prompt"):
        payload["input"]["negative_prompt"] = req["negative_prompt"]
    if req.get("media"):
        payload["input"]["media"] = req["media"]

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
# Text-to-video
task_id = create_kling_task({
    "prompt": "一只小猫在月光下奔跑",
    "aspect_ratio": "16:9",
    "duration": 5,
    "mode": "std",
})

# Image-to-video (first frame)
task_id = create_kling_task({
    "prompt": "花朵绽放的延时摄影",
    "media": [{"type": "first_frame", "url": "https://example.com/flower.jpg"}],
    "duration": 5,
})

# Reference-to-video with omni model
task_id = create_kling_task({
    "model": "kling/kling-v3-omni-video-generation",
    "prompt": "一只<<<element_1>>>在月光下奔跑",
    "media": [{"type": "refer", "url": "https://example.com/cat.jpg"}],
    "aspect_ratio": "16:9",
})
```

## Error handling

| Error | Likely cause | Action |
|---|---|---|
| 401/403 | Missing or invalid API Key | Check env var, must be Beijing region |
| 400 `InvalidParameter` | Bad media combination or missing required params | Validate against model's media rules |
| "does not support synchronous calls" | Missing `X-DashScope-Async: enable` header | Add required header |
| 429 | Rate limit or quota | Retry with backoff |

## Output location

- Default output: `output/aliyun-kling-video/videos/`
- Override base dir with `OUTPUT_DIR`.

## Anti-patterns

- Do not use model names other than `kling/kling-v3-video-generation` or `kling/kling-v3-omni-video-generation`.
- Do not call this API synchronously — async header is required.
- Do not use `refer`, `base`, or `feature` media types with the standard model — use omni only.
- Do not mix incompatible media combinations.
- Video URLs expire; download and persist immediately.
- Beijing region only — do not use Singapore endpoint.

## Workflow

1) Confirm user intent: t2v, i2v, reference-to-video, editing, or storyboard.
2) Select appropriate model (standard for basic t2v/i2v, omni for reference/editing).
3) Prepare media array with correct types and valid URLs.
4) Create async task and poll for results.
5) Download and save generated video before URL expiration.

## References

- See `references/api_reference.md` for full HTTP API details.
- See `references/sources.md` for source links.
