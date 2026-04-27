---
name: aliyun-happyhorse-t2v
description: Use when generating videos from text prompts with DashScope HappyHorse 1.0 text-to-video model (happyhorse-1.0-t2v). Use when implementing pure text-to-video synthesis via the video-synthesis async API on Alibaba Cloud Model Studio.
---

# HappyHorse 1.0 Text-to-Video

## Validation

```bash
mkdir -p output/aliyun-happyhorse-t2v
python -m py_compile skills/ai/video/aliyun-happyhorse-t2v/scripts/t2v_happyhorse.py && echo "py_compile_ok" > output/aliyun-happyhorse-t2v/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-happyhorse-t2v/validate.txt` is generated.

## Output And Evidence

- Save task IDs, polling responses, and final video URLs to `output/aliyun-happyhorse-t2v/`.
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

- `happyhorse-1.0-t2v` — text-to-video, supports resolution, ratio, duration, watermark and seed control

## Capabilities

| Capability | Description | Required input |
|---|---|---|
| Text-to-video | Generate a physically realistic video from a text prompt only | `prompt` |

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
- `model` (string, required) — fixed `happyhorse-1.0-t2v`
- `input.prompt` (string, required) — up to 5000 non-CJK characters or 2500 CJK characters; longer is truncated
- `parameters.resolution` (string, optional) — `720P` or `1080P` (default: `1080P`)
- `parameters.ratio` (string, optional) — `16:9` (default), `9:16`, `1:1`, `4:3`, `3:4`
- `parameters.duration` (integer, optional) — video length in seconds, range [3, 15] (default: 5)
- `parameters.watermark` (boolean, optional) — add bottom-right "Happy Horse" watermark (default: `true`)
- `parameters.seed` (integer, optional) — range [0, 2147483647]

### Response (task creation)
- `output.task_id` (string) — use for polling, valid 24 hours
- `output.task_status` (string) — `PENDING` | `RUNNING` | `SUCCEEDED` | `FAILED` | `CANCELED` | `UNKNOWN`
- `request_id` (string)

### Response (task result, on SUCCEEDED)
- `output.video_url` (string) — generated MP4 (H.264) URL, valid 24 hours
- `output.orig_prompt` (string)
- `output.submit_time` / `output.scheduled_time` / `output.end_time` (string)
- `usage.duration` (integer) — billable duration in seconds
- `usage.output_video_duration` (integer)
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


def create_t2v_task(req: dict) -> str:
    """Create a text-to-video task and return task_id."""
    payload = {
        "model": "happyhorse-1.0-t2v",
        "input": {"prompt": req["prompt"]},
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
# Minimal — pure text prompt
task_id = create_t2v_task({
    "prompt": "一座由硬纸板和瓶盖搭建的微型城市，在夜晚焕发出生机。",
    "duration": 5,
})

# Vertical short video at 720P
task_id = create_t2v_task({
    "prompt": "A neon cyberpunk alley at midnight, rain reflections, slow dolly forward.",
    "resolution": "720P",
    "ratio": "9:16",
    "duration": 8,
})
```

## Error handling

| Error | Likely cause | Action |
|---|---|---|
| 401 / `InvalidApiKey` | Missing or invalid `DASHSCOPE_API_KEY` | Check env var or credentials file |
| 400 `InvalidParameter` | Unsupported resolution/ratio, duration out of [3,15], wrong model name | Validate parameters |
| `current user api does not support synchronous calls` | Missing `X-DashScope-Async: enable` header | Add the required header |
| `task_status: UNKNOWN` | task_id older than 24 hours | Re-create the task |
| 429 | RPS or quota exceeded | Retry with backoff; query RPS default 20 |

## Output location

- Default output: `output/aliyun-happyhorse-t2v/videos/`
- Override base dir with `OUTPUT_DIR`.

## Anti-patterns

- Do not use any model ID other than `happyhorse-1.0-t2v`.
- Do not call this API synchronously — async header is required.
- Do not pass `media`, `first_frame`, or `reference_image` — t2v takes only a text prompt.
- Video and task URLs expire after 24 hours; download and persist immediately.
- Do not use this skill for image- or video-conditioned generation — use `aliyun-happyhorse-i2v`, `aliyun-happyhorse-r2v`, or `aliyun-happyhorse-videoedit` instead.

## Workflow

1) Confirm pure text-to-video intent (no input image/video).
2) Build the prompt and choose `resolution`, `ratio`, `duration`.
3) Create async task and poll `/tasks/{task_id}` every ~15s.
4) Download `output.video_url` before the 24-hour expiration.

## References

- See `references/api_reference.md` for full HTTP API details.
- See `references/sources.md` for source links.
