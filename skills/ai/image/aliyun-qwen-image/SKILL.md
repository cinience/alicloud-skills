---
name: aliyun-qwen-image
description: Use when generating images with Model Studio DashScope SDK using Qwen Image generation models (qwen-image, qwen-image-plus, qwen-image-max, qwen-image-2.0 series and snapshots). Use when implementing or documenting image.generate requests/responses, mapping prompt/negative_prompt/size/seed/reference_image, or integrating image generation into the video-agent pipeline.
version: 1.0.0
---

Category: provider

# Model Studio Qwen Image

## Validation

```bash
mkdir -p output/aliyun-qwen-image
python -m py_compile skills/ai/image/aliyun-qwen-image/scripts/generate_image.py && echo "py_compile_ok" > output/aliyun-qwen-image/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-qwen-image/validate.txt` is generated.

## Output And Evidence

- Write generated image URLs, prompts, and metadata to `output/aliyun-qwen-image/`.
- Keep at least one sample JSON response per run.

Build consistent image generation behavior for the video-agent pipeline by standardizing `image.generate` inputs/outputs and using DashScope SDK (Python) with the exact model name.

## Prerequisites

- Install SDK (recommended in a venv to avoid PEP 668 limits):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials` (env takes precedence).

## Critical model names

Use one of these exact model strings:
- `qwen-image`
- `qwen-image-plus`
- `qwen-image-max`
- `qwen-image-2.0`
- `qwen-image-2.0-pro`
- `qwen-image-2.0-2026-03-03`
- `qwen-image-2.0-pro-2026-03-03`
- `qwen-image-max-2025-12-30`
- `qwen-image-plus-2026-01-09`

## Normalized interface (image.generate)

### Request
- `prompt` (string, required)
- `negative_prompt` (string, optional)
- `size` (string, required) e.g. `1024*1024`, `768*1024`
- `style` (string, optional)
- `seed` (int, optional)
- `reference_image` (string | bytes, optional)

### Response
- `image_url` (string)
- `width` (int)
- `height` (int)
- `seed` (int)

## Quickstart (normalized request + preview)

Minimal normalized request body:

```json
{
  "prompt": "a cinematic portrait of a cyclist at dusk, soft rim light, shallow depth of field",
  "negative_prompt": "blurry, low quality, watermark",
  "size": "1024*1024",
  "seed": 1234
}
```

Preview workflow (download then open):

```bash
curl -L -o output/aliyun-qwen-image/images/preview.png "<IMAGE_URL_FROM_RESPONSE>" && open output/aliyun-qwen-image/images/preview.png
```

Local helper script (JSON request -> image file):

```bash
python skills/ai/image/aliyun-qwen-image/scripts/generate_image.py \\
  --request '{"prompt":"a studio product photo of headphones","size":"1024*1024"}' \\
  --output output/aliyun-qwen-image/images/headphones.png \\
  --print-response
```

## Parameters at a glance

| Field | Required | Notes |
|------|----------|-------|
| `prompt` | yes | Describe a scene, not just keywords. |
| `negative_prompt` | no | Best-effort, may be ignored by backend. |
| `size` | yes | `WxH` format, e.g. `1024*1024`, `768*1024`. |
| `style` | no | Optional stylistic hint. |
| `seed` | no | Use for reproducibility when supported. |
| `reference_image` | no | URL/file/bytes, SDK-specific mapping. |

## Quick start (Python + DashScope SDK)

Use the DashScope SDK and map the normalized request into the SDK call.
Note: For `qwen-image-max`, the DashScope SDK currently succeeds via `ImageGeneration` (messages-based) rather than `ImageSynthesis`.
If the SDK version you are using expects a different field name for reference images, adapt the `input` mapping accordingly.

```python
import os
from dashscope.aigc.image_generation import ImageGeneration

# Prefer env var for auth: export DASHSCOPE_API_KEY=...
# Or use ~/.alibabacloud/credentials with dashscope_api_key under [default].


def generate_image(req: dict) -> dict:
    messages = [
        {
            "role": "user",
            "content": [{"text": req["prompt"]}],
        }
    ]

    if req.get("reference_image"):
        # Some SDK versions accept {"image": <url|file|bytes>} in messages content.
        messages[0]["content"].insert(0, {"image": req["reference_image"]})

    response = ImageGeneration.call(
        model=req.get("model", "qwen-image-max"),
        messages=messages,
        size=req.get("size", "1024*1024"),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # Pass through optional parameters if supported by the backend.
        negative_prompt=req.get("negative_prompt"),
        style=req.get("style"),
        seed=req.get("seed"),
    )

    # Response is a generation-style envelope; extract the first image URL.
    content = response.output["choices"][0]["message"]["content"]
    image_url = None
    for item in content:
        if isinstance(item, dict) and item.get("image"):
            image_url = item["image"]
            break
    return {
        "image_url": image_url,
        "width": response.usage.get("width"),
        "height": response.usage.get("height"),
        "seed": req.get("seed"),
    }
```

## Error handling

| Error | Likely cause | Action |
|------|--------------|--------|
| 401/403 | Missing or invalid `DASHSCOPE_API_KEY` | Check env var or `~/.alibabacloud/credentials`, and access policy. |
| 400 | Unsupported size or bad request shape | Use common `WxH` and validate fields. |
| 429 | Rate limit or quota | Retry with backoff, or reduce concurrency. |
| 5xx | Transient backend errors | Retry with backoff once or twice. |

## Output location

- Default output: `output/aliyun-qwen-image/images/`
- Override base dir with `OUTPUT_DIR`.

## Operational guidance

- Store the returned image in object storage and persist only the URL in metadata.
- Cache results by `(prompt, negative_prompt, size, seed, reference_image hash)` to avoid duplicate costs.
- Add retries for transient 429/5xx responses with exponential backoff.
- Some backends ignore `negative_prompt`, `style`, or `seed`; treat them as best-effort inputs.
- If the response contains no image URL, surface a clear error and retry once with a simplified prompt.

## Size notes

- Use `WxH` format (e.g. `1024*1024`, `768*1024`).
- Prefer common sizes; unsupported sizes can return 400.

## Anti-patterns

- Do not invent model names or aliases; use official model IDs only.
- Do not store large base64 blobs in DB rows; use object storage.
- Do not omit user-visible progress for long generations.

## Workflow

1) Confirm user intent, region, identifiers, and whether the operation is read-only or mutating.
2) Run one minimal read-only query first to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.

## References

- See `references/api_reference.md` for a more detailed DashScope SDK mapping and response parsing tips.
- See `references/prompt-guide.md` for prompt patterns and examples.
- For edit workflows, use `skills/ai/image/aliyun-qwen-image-edit/`.

- Source list: `references/sources.md`
