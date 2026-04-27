---
name: aliyun-happyhorse-r2v
description: Use when generating videos that fuse 1-9 reference images with DashScope HappyHorse 1.0 reference-to-video model (happyhorse-1.0-r2v). Use when implementing multi-subject reference-to-video synthesis where prompts cite the input images as character1..N via the video-synthesis async API.
---

# HappyHorse 1.0 Reference-to-Video

## Validation

```bash
mkdir -p output/aliyun-happyhorse-r2v
python -m py_compile skills/ai/video/aliyun-happyhorse-r2v/scripts/r2v_happyhorse.py && echo "py_compile_ok" > output/aliyun-happyhorse-r2v/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-happyhorse-r2v/validate.txt` is generated.

## Output And Evidence

- Save task IDs, polling responses, and final video URLs to `output/aliyun-happyhorse-r2v/`.
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

- `happyhorse-1.0-r2v` — reference-to-video; 1-9 reference images fused into a single video, with `character1..N` references in the prompt

## Capabilities

| Capability | Description | Required media |
|---|---|---|
| Reference-to-video | Generate a video by fusing multiple subject/object reference images, guided by a prompt that references them as `character1`, `character2`, ... in input order | 1-9 `reference_image` entries |

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
- `model` (string, required) — fixed `happyhorse-1.0-r2v`
- `input.prompt` (string, required) — up to 5000 non-CJK / 2500 CJK characters; reference subjects via `character1`, `character2`, ... matching `media` array order
- `input.media` (array, required) — 1 to 9 elements, each:
  - `type`: `reference_image`
  - `url`: public HTTP/HTTPS URL of a reference image
- `parameters.resolution` (string, optional) — `720P` or `1080P` (default: `1080P`)
- `parameters.ratio` (string, optional) — `16:9` (default), `9:16`, `1:1`, `4:3`, `3:4`
- `parameters.duration` (integer, optional) — video length in seconds, range [3, 15] (default: 5)
- `parameters.watermark` (boolean, optional) — bottom-right "Happy Horse" watermark (default: `true`)
- `parameters.seed` (integer, optional) — range [0, 2147483647]

### Media input limits

**Reference image** (`type=reference_image`):
- Formats: JPEG, JPG, PNG, WEBP
- Resolution: short side ≥ 400 pixels (720P or higher recommended)
- Max size: 10 MB per image
- Avoid blurry, over-compressed, or very small images

### Character indexing rule

The first `reference_image` in the `media` array maps to `character1`, the second to `character2`, and so on up to `character9`. Reorder the array if you want a specific reference to bind to a specific `characterN`.

### Response (task creation)
- `output.task_id` (string) — valid 24 hours
- `output.task_status` (string) — `PENDING` | `RUNNING` | `SUCCEEDED` | `FAILED` | `CANCELED` | `UNKNOWN`
- `request_id` (string)

### Response (task result, on SUCCEEDED)
- `output.video_url` (string) — generated MP4 (H.264) URL, valid 24 hours
- `output.orig_prompt` (string)
- `output.submit_time` / `output.scheduled_time` / `output.end_time` (string)
- `usage.duration` (integer) — billable duration in seconds
- `usage.output_video_duration` (integer)
- `usage.input_video_duration` (integer) — fixed 0 for r2v
- `usage.SR` (integer) — output resolution tier
- `usage.ratio` (string)
- `usage.video_count` (integer) — fixed 1

## Quick start (Python + HTTP)

```python
import os
import time
import requests

API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"


def create_r2v_task(req: dict) -> str:
    """Create a reference-to-video task and return task_id."""
    refs = req["reference_images"]
    if not 1 <= len(refs) <= 9:
        raise ValueError("Need 1-9 reference images")
    payload = {
        "model": "happyhorse-1.0-r2v",
        "input": {
            "prompt": req["prompt"],
            "media": [{"type": "reference_image", "url": u} for u in refs],
        },
        "parameters": {
            "resolution": req.get("resolution", "1080P"),
            "ratio": req.get("ratio", "16:9"),
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
# Single subject — character1 references the only image
task_id = create_r2v_task({
    "reference_images": ["https://example.com/girl.jpg"],
    "prompt": "character1 walks slowly through a sunlit forest, cinematic shot.",
    "duration": 5,
})

# Multi-subject — character1=girl, character2=fan, character3=earring
task_id = create_r2v_task({
    "reference_images": [
        "https://example.com/girl.jpg",
        "https://example.com/folding-fan.jpg",
        "https://example.com/earring.jpg",
    ],
    "prompt": (
        "身着红色旗袍的女性 character1，轻抬玉手展开折扇 character2 时"
        "流苏耳坠 character3 随头部转动轻盈摆动。"
    ),
    "resolution": "720P",
    "ratio": "16:9",
    "duration": 5,
})
```

## Error handling

| Error | Likely cause | Action |
|---|---|---|
| 401 / `InvalidApiKey` | Missing or invalid `DASHSCOPE_API_KEY` | Check env var or credentials file |
| 400 `InvalidParameter` | Bad resolution/ratio, >9 references, image too small or wrong format | Validate parameters and images |
| `current user api does not support synchronous calls` | Missing `X-DashScope-Async: enable` header | Add the required header |
| `task_status: UNKNOWN` | task_id older than 24 hours | Re-create the task |
| 429 | RPS or quota exceeded | Retry with backoff; query RPS default 20 |

## Output location

- Default output: `output/aliyun-happyhorse-r2v/videos/`
- Override base dir with `OUTPUT_DIR`.

## Anti-patterns

- Do not use any model ID other than `happyhorse-1.0-r2v`.
- Do not call this API synchronously — async header is required.
- Do not pass `first_frame`, `last_frame`, `driving_audio`, or `video` — only `reference_image` entries are accepted.
- Do not exceed 9 reference images, and do not omit the array entirely.
- Do not forget `characterN` tokens in the prompt — without them the model has no link from prompt to image.
- Video URLs expire after 24 hours; download and persist immediately.
- Do not use this skill for pure text-to-video (`aliyun-happyhorse-t2v`), single-image first-frame (`aliyun-happyhorse-i2v`), or video editing (`aliyun-happyhorse-videoedit`).

## Workflow

1) Collect 1-9 high-quality reference images and decide character order.
2) Write a prompt that uses `character1..N` to bind subjects to references.
3) Create async task and poll `/tasks/{task_id}` every ~15s.
4) Download `output.video_url` before the 24-hour expiration.

## References

- See `references/api_reference.md` for full HTTP API details.
- See `references/sources.md` for source links.
