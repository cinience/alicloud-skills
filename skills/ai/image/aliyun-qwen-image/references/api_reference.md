# DashScope SDK Reference (Qwen Image)

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

Use the normalized `image.generate` request and map fields into the SDK call.
Note: For `qwen-image-max`, the DashScope SDK currently succeeds via `ImageGeneration` (messages-based) rather than `ImageSynthesis`.
The exact parameter names for reference images can vary across SDK versions.

```python
import os
from dashscope.aigc.image_generation import ImageGeneration

messages = [
    {
        "role": "user",
        "content": [{"text": prompt}],
    }
]

if reference_image:
    # Some SDK versions accept {"image": <url|file|bytes>} in messages content.
    messages[0]["content"].insert(0, {"image": reference_image})

response = ImageGeneration.call(
    model="qwen-image-max",
    messages=messages,
    size=size,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    negative_prompt=negative_prompt,
    style=style,
    seed=seed,
)
```

## Response parsing

DashScope SDK response shapes can differ slightly by version. Extract the first result URL and normalize into:

- `image_url`
- `width`
- `height`
- `seed`

Prefer this pattern:

```python
content = response.output["choices"][0]["message"]["content"]
image_url = next((item.get("image") for item in content if isinstance(item, dict) and item.get("image")), None)
width = response.usage.get("width")
height = response.usage.get("height")
seed = seed
```

## Notes

- `negative_prompt`, `style`, and `seed` may be ignored by some deployments; treat them as best-effort.
- If no image URL is returned, fail fast with a clear error and retry with a shorter prompt.
