# DashScope SDK Reference (Wan 2.7 Image)

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

Or place `dashscope_api_key` under `[default]` in `~/.alibabacloud/credentials`.

## Models

| Model | Max Resolution | Speed |
|---|---|---|
| wan2.7-image-pro | 4K (4096x4096) | Standard |
| wan2.7-image | 2K (2048x2048) | Faster |

## API endpoints

- **Sync**: `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- **Async**: Same URL under `/image-generation/generation` with header `X-DashScope-Async: enable`
- **Singapore**: Replace `dashscope.aliyuncs.com` with `dashscope-intl.aliyuncs.com`

## Request format

Uses `messages` format with `role: "user"` and `content` array containing `text` and optional `image` objects.

```python
from dashscope.aigc.image_generation import ImageGeneration

response = ImageGeneration.call(
    model="wan2.7-image",
    messages=[{
        "role": "user",
        "content": [
            {"text": "a beautiful sunset over mountains"},
        ]
    }],
    size="2K",
    n=1,
    watermark=False,
    thinking_mode=True,
    seed=42,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)
```

## Parameters

| Parameter | Type | Notes |
|---|---|---|
| size | string | "1K", "2K", "4K" (pro only), or "WxH" pixels |
| n | int | 1-4 (standard), 1-12 (sequential mode) |
| enable_sequential | bool | Group image generation |
| thinking_mode | bool | Enhanced reasoning (text-to-image only, default true) |
| bbox_list | array | Bounding boxes for interactive editing |
| color_palette | array | Custom colors (3-10 items with hex+ratio) |
| watermark | bool | Add "AI generated" watermark |
| seed | int | [0, 2147483647] for reproducibility |

## Image input limits

- Formats: JPEG, JPG, PNG (no transparency), BMP, WEBP
- Resolution: [240, 8000] px per side, aspect ratio [1:8, 8:1]
- File size: ≤ 20MB
- Count: 0-9 images

## Response parsing

```python
content = response.output["choices"][0]["message"]["content"]
images = [item["image"] for item in content if isinstance(item, dict) and item.get("image")]
image_count = response.usage.get("image_count")
size = response.usage.get("size")
```

## Notes

- Image URLs expire after 24 hours; download immediately.
- `thinking_mode` only applies to text-to-image (no image input, no sequential mode).
- `color_palette` ratios must sum to exactly 100.00%.
- 4K output only available for `wan2.7-image-pro` in text-to-image mode.
