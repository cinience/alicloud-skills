---
name: alicloud-ai-video-wan-video
description: Generate videos with Model Studio DashScope SDK using the wan2.6-i2v-flash model. Use when implementing or documenting video.generate requests/responses, mapping prompt/negative_prompt/duration/fps/size/seed/reference_image/motion_strength, or integrating video generation into the video-agent pipeline.
---

Category: provider

# Model Studio Wan Video

Provide consistent video generation behavior for the video-agent pipeline by standardizing `video.generate` inputs/outputs and using DashScope SDK (Python) with the exact model name.

## Critical model name

Use ONLY this exact model string:
- `wan2.6-i2v-flash`

Do not add date suffixes or aliases.

## Prerequisites

- Install SDK (recommended in a venv to avoid PEP 668 limits):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials` (env takes precedence).

## Normalized interface (video.generate)

### Request
- `prompt` (string, required)
- `negative_prompt` (string, optional)
- `duration` (number, required) seconds
- `fps` (number, required)
- `size` (string, required) e.g. `1280*720`
- `seed` (int, optional)
- `reference_image` (string | bytes, required for `wan2.6-i2v-flash`)
- `motion_strength` (number, optional)

### Response
- `video_url` (string)
- `duration` (number)
- `fps` (number)
- `seed` (int)

## Quick start (Python + DashScope SDK)

Video generation is usually asynchronous. Expect a task ID and poll until completion.
Note: `wan2.6-i2v-flash` requires an input image; map `reference_image` to `img_url`.

```python
import os
from dashscope import VideoSynthesis

# Prefer env var for auth: export DASHSCOPE_API_KEY=...
# Or use ~/.alibabacloud/credentials with dashscope_api_key under [default].

def generate_video(req: dict) -> dict:
    payload = {
        "model": "wan2.6-i2v-flash",
        "prompt": req["prompt"],
        "negative_prompt": req.get("negative_prompt"),
        "duration": req.get("duration", 4),
        "fps": req.get("fps", 24),
        "size": req.get("size", "1280*720"),
        "seed": req.get("seed"),
        "motion_strength": req.get("motion_strength"),
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
    }

    if req.get("reference_image"):
        # DashScope expects img_url for i2v models; local files are auto-uploaded.
        payload["img_url"] = req["reference_image"]

    response = VideoSynthesis.call(**payload)

    # Some SDK versions require polling for the final result.
    # If a task_id is returned, poll until status is SUCCEEDED.
    result = response.output.get("results", [None])[0]

    return {
        "video_url": None if not result else result.get("url"),
        "duration": response.output.get("duration"),
        "fps": response.output.get("fps"),
        "seed": response.output.get("seed"),
    }
```

## Async handling (polling)

```python
import os
from dashscope import VideoSynthesis

task = VideoSynthesis.async_call(
    model="wan2.6-i2v-flash",
    prompt=req["prompt"],
    img_url=req["reference_image"],
    duration=req.get("duration", 4),
    fps=req.get("fps", 24),
    size=req.get("size", "1280*720"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)

final = VideoSynthesis.wait(task)
video_url = final.output.get("video_url")
```

## Operational guidance

- Video generation can take minutes; expose progress and allow cancel/retry.
- Cache by `(prompt, negative_prompt, duration, fps, size, seed, reference_image hash, motion_strength)`.
- Store video assets in object storage and persist only URLs in metadata.
- `reference_image` can be a URL or local path; the SDK auto-uploads local files.
- If you get `Field required: input.img_url`, the reference image is missing or not mapped.

## Size notes

- Use `WxH` format (e.g. `1280*720`).
- Prefer common sizes; unsupported sizes can return 400.

## Output location

- Default output: `output/ai-video-wan-video/videos/`
- Override base dir with `OUTPUT_DIR`.

## Anti-patterns

- Do not invent model names or aliases; use `wan2.6-i2v-flash` only.
- Do not block the UI without progress updates.
- Do not retry blindly on 4xx; handle validation failures explicitly.

## References

- See `references/api_reference.md` for DashScope SDK mapping and async handling notes.

- Source list: `references/sources.md`
