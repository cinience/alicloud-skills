# DashScope SDK Reference (Wan Video)

Keep this reference minimal and update it only when the DashScope SDK behavior changes.

## Install

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```

## Environment

```bash
export DASHSCOPE_API_KEY=your_key
```

If env vars are not set, you can also place `dashscope_api_key` under `[default]` in `~/.alibabacloud/credentials`.

## Suggested mapping

```python
import os
from dashscope import VideoSynthesis

payload = {
    "model": "wan2.6-i2v-flash",
    "prompt": prompt,
    "negative_prompt": negative_prompt,
    "duration": duration,
    "fps": fps,
    "size": size,
    "seed": seed,
    "motion_strength": motion_strength,
    "api_key": os.getenv("DASHSCOPE_API_KEY"),
}

if reference_image:
    # DashScope expects img_url for i2v models; local files are auto-uploaded.
    payload["img_url"] = reference_image

response = VideoSynthesis.call(**payload)
```

## Async handling

If the SDK returns a task ID rather than a direct result URL, poll until completion. Use exponential backoff and a hard timeout; fail gracefully with the task ID for later resumption.

```python
task = VideoSynthesis.async_call(**payload)
final = VideoSynthesis.wait(task)
video_url = final.output.get("video_url")
```

## Response parsing

Normalize to:

- `video_url`
- `duration`
- `fps`
- `seed`

Prefer the first result URL if multiple are returned.

## Notes

- `wan2.6-i2v-flash` requires `img_url`; missing it yields `Field required: input.img_url`.
- `reference_image` can be a URL or local path; the SDK auto-uploads local files.
