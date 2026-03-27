---
name: alicloud-ai-video-animate-anyone
description: Generate dance or motion-transfer videos with Alibaba Cloud Model Studio AnimateAnyone (`animate-anyone-gen2`) using a detected character image and an action template. Use when cloning motion from a dance/action video into a target character image.
version: 1.0.0
---

Category: provider

# Model Studio AnimateAnyone

## Validation

```bash
mkdir -p output/alicloud-ai-video-animate-anyone
python -m py_compile skills/ai/video/alicloud-ai-video-animate-anyone/scripts/prepare_animate_anyone_request.py && echo "py_compile_ok" > output/alicloud-ai-video-animate-anyone/validate.txt
```

Pass criteria: command exits 0 and `output/alicloud-ai-video-animate-anyone/validate.txt` is generated.

## Output And Evidence

- Save normalized request payloads, detection outputs, template IDs, and task polling snapshots under `output/alicloud-ai-video-animate-anyone/`.
- Record whether the result should keep the reference image background or the source video background.

Use AnimateAnyone when the task needs motion transfer from a template video rather than plain talking-head animation.

## Critical model names

Use these exact model strings:
- `animate-anyone-detect-gen2`
- `animate-anyone-template-gen2`
- `animate-anyone-gen2`

Selection guidance:
- Run image detection first.
- Run template generation on the source motion video.
- Use `animate-anyone-gen2` for the final video job.

## Prerequisites

- China mainland (Beijing) only.
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.
- Input files must be public HTTP/HTTPS URLs.

## Normalized interface (video.animate_anyone)

### Detect Request
- `model` (string, optional): default `animate-anyone-detect-gen2`
- `image_url` (string, required)

### Template Request
- `model` (string, optional): default `animate-anyone-template-gen2`
- `video_url` (string, required)

### Generate Request
- `model` (string, optional): default `animate-anyone-gen2`
- `image_url` (string, required)
- `template_id` (string, required)
- `use_ref_img_bg` (bool, optional): whether to keep the input image background

### Response
- `task_id` (string)
- `task_status` (string)
- `video_url` (string, when finished)

## Quick start

```bash
python skills/ai/video/alicloud-ai-video-animate-anyone/scripts/prepare_animate_anyone_request.py \
  --image-url "https://example.com/dancer.png" \
  --template-id "tmpl_xxx" \
  --use-ref-img-bg
```

## Operational guidance

- The action template must come from the official template-generation API.
- Full-body images work best when `use_ref_img_bg=false`; half-body images are not recommended in that mode.
- This skill is best for dancing or large body motion transfer, not generic talking-head tasks.

## Output location

- Default output: `output/alicloud-ai-video-animate-anyone/request.json`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/sources.md`
