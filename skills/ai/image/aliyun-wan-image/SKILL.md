---
name: aliyun-wan-image
description: Use when generating or editing images with DashScope Wan 2.7 image models (wan2.7-image, wan2.7-image-pro). Use when implementing text-to-image, image editing, interactive editing with bounding boxes, sequential group image generation, or color palette control via the multimodal-generation API.
---

# Wan 2.7 Image Generation & Editing

## Validation

```bash
mkdir -p output/aliyun-wan-image
python -m py_compile skills/ai/image/aliyun-wan-image/scripts/generate_image.py && echo "py_compile_ok" > output/aliyun-wan-image/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-wan-image/validate.txt` is generated.

## Output And Evidence

- Write generated image URLs, prompts, and metadata to `output/aliyun-wan-image/`.
- Keep at least one sample JSON response per run.

## Prerequisites

- Install SDK (recommended in a venv):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Critical model names

- `wan2.7-image-pro` — professional version, supports 4K output
- `wan2.7-image` — faster generation, up to 2K

## Capabilities

| Capability | Description |
|---|---|
| Text-to-image | Generate images from text prompts |
| Image editing | Edit images with text instructions (1-9 input images) |
| Interactive editing | Edit specific regions via bounding boxes (`bbox_list`) |
| Group generation | Generate consistent multi-image sequences (`enable_sequential=true`, up to 12 images) |
| Color palette | Control color theme with custom hex+ratio palette (3-10 colors) |
| Thinking mode | Enhanced reasoning for better quality (text-to-image only) |

## API endpoint

**Sync (recommended):**
```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

**Async (for long tasks):**
```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation
Header: X-DashScope-Async: enable
```

## Normalized interface (image.generate)

### Request
- `prompt` (string, required) — up to 5000 characters
- `size` (string, optional) — `1K`, `2K` (default), `4K` (pro only), or `WxH` pixel values
- `n` (int, optional) — number of images, 1-4 (default 4), or 1-12 with `enable_sequential`
- `seed` (int, optional) — range [0, 2147483647]
- `reference_image` (string/array, optional) — URL or base64, up to 9 images
- `enable_sequential` (bool, optional) — group image generation mode
- `thinking_mode` (bool, optional, default true) — enhanced reasoning (text-to-image only)
- `bbox_list` (array, optional) — bounding boxes for interactive editing
- `color_palette` (array, optional) — custom color theme (3-10 colors with hex+ratio)
- `watermark` (bool, optional, default false)

### Response
- `image_url` (string) — PNG, valid for 24 hours
- `image_count` (int)
- `size` (string) — actual output resolution
- `seed` (int)

## Quick start (Python + DashScope SDK)

```python
import os
from dashscope.aigc.image_generation import ImageGeneration

def generate_image(req: dict) -> dict:
    messages = [
        {
            "role": "user",
            "content": [{"text": req["prompt"]}],
        }
    ]

    # Add reference images if provided
    ref_images = req.get("reference_images") or []
    if req.get("reference_image"):
        ref_images = [req["reference_image"]] + ref_images
    for img in ref_images:
        messages[0]["content"].append({"image": img})

    params = {
        "model": req.get("model", "wan2.7-image"),
        "messages": messages,
        "size": req.get("size", "2K"),
        "n": req.get("n", 1),
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
        "seed": req.get("seed"),
        "watermark": req.get("watermark", False),
    }

    if req.get("enable_sequential"):
        params["enable_sequential"] = True
    if req.get("thinking_mode") is not None:
        params["thinking_mode"] = req["thinking_mode"]
    if req.get("bbox_list"):
        params["bbox_list"] = req["bbox_list"]
    if req.get("color_palette"):
        params["color_palette"] = req["color_palette"]

    response = ImageGeneration.call(**params)

    content = response.output["choices"][0]["message"]["content"]
    images = [item["image"] for item in content if isinstance(item, dict) and item.get("image")]

    return {
        "image_urls": images,
        "image_count": response.usage.get("image_count"),
        "size": response.usage.get("size"),
    }
```

## Size reference

| Model | Supported sizes | Default |
|---|---|---|
| wan2.7-image-pro | 1K, 2K, 4K (text-to-image only), or [768, 4096] px | 2K |
| wan2.7-image | 1K, 2K, or [768, 2048] px | 2K |

## Error handling

| Error | Likely cause | Action |
|---|---|---|
| 401/403 | Missing or invalid `DASHSCOPE_API_KEY` | Check env var or credentials file. |
| 400 `InvalidParameter` | Unsupported size, bad n value, or missing required image | Validate parameters against model limits. |
| 429 | Rate limit or quota | Retry with backoff. |

## Output location

- Default output: `output/aliyun-wan-image/images/`
- Override base dir with `OUTPUT_DIR`.

## Anti-patterns

- Do not invent model names; use `wan2.7-image` or `wan2.7-image-pro` only.
- Do not use 4K size with `wan2.7-image` (only pro supports 4K).
- Do not use `enable_sequential` with `bbox_list` — they are separate modes.
- Image URLs expire after 24 hours; download and persist immediately.

## Workflow

1) Confirm user intent: text-to-image, image editing, group generation, or interactive editing.
2) Select appropriate model (pro for 4K or higher quality, standard for speed).
3) Execute with explicit parameters and bounded scope.
4) Download and save generated images before URL expiration.

## References

- See `references/api_reference.md` for full HTTP API details.
- See `references/sources.md` for source links.
