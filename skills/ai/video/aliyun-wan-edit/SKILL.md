---
name: aliyun-wan-edit
description: Use when Alibaba Cloud Model Studio Wan video editing models are needed for style transfer, keyframe-controlled editing, or animation remix workflows.
version: 1.0.0
---

Category: provider

# Model Studio Wan Video Edit

## Validation

```bash
mkdir -p output/aliyun-wan-edit
python -m py_compile skills/ai/video/aliyun-wan-edit/scripts/prepare_video_edit_request.py && echo "py_compile_ok" > output/aliyun-wan-edit/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-wan-edit/validate.txt` is generated.

## Critical model names

Use one of these exact model strings as needed:
- `wanx2.1-vace-plus`
- `wanx2.1-kf2v-plus`
- `wan2.2-animate-mix`
- `VideoRetalk`

## Typical use

- Video style transformation
- Keyframe-to-video guided editing
- Animation remix

## Quick start

```bash
python skills/ai/video/aliyun-wan-edit/scripts/prepare_video_edit_request.py \
  --output output/aliyun-wan-edit/request.json
```

## Notes

- Use `skills/ai/video/aliyun-wan-video/` for Wan generation.
- Use `skills/ai/video/aliyun-videoretalk/` for dedicated lip-sync replacement.
- Use this skill only when the user wants to modify existing video material.

## References

- `references/sources.md`
