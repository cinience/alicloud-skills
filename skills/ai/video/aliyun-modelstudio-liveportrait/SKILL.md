---
name: aliyun-modelstudio-liveportrait
description: Generate lightweight talking-head portrait videos with Alibaba Cloud Model Studio LivePortrait (`liveportrait`) from a detected portrait image and speech audio. Use when you need long-form or simple broadcast-style portrait animation beyond the typical short expressive models.
version: 1.0.0
---

Category: provider

# Model Studio LivePortrait

## Validation

```bash
mkdir -p output/aliyun-modelstudio-liveportrait
python -m py_compile skills/ai/video/aliyun-modelstudio-liveportrait/scripts/prepare_liveportrait_request.py && echo "py_compile_ok" > output/aliyun-modelstudio-liveportrait/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-modelstudio-liveportrait/validate.txt` is generated.

## Output And Evidence

- Save normalized request payloads, template choice, and task polling snapshots under `output/aliyun-modelstudio-liveportrait/`.
- Record the exact portrait/audio URLs and motion-strength related parameters.

Use LivePortrait when the job is lightweight portrait animation with speech audio, especially for longer clips or simpler presenter-style motion.

## Critical model names

Use these exact model strings:
- `liveportrait-detect`
- `liveportrait`

Selection guidance:
- Run `liveportrait-detect` first to verify the portrait image.
- Use `liveportrait` for the actual video generation task.

## Prerequisites

- China mainland (Beijing) only.
- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.
- Input image and audio must be public HTTP/HTTPS URLs.

## Normalized interface (video.liveportrait)

### Detect Request
- `model` (string, optional): default `liveportrait-detect`
- `image_url` (string, required)

### Generate Request
- `model` (string, optional): default `liveportrait`
- `image_url` (string, required)
- `audio_url` (string, required)
- `template_id` (string, optional): `normal`, `calm`, or `active`
- `eye_move_freq` (number, optional): `0` to `1`
- `video_fps` (int, optional): `15` to `30`
- `mouth_move_strength` (number, optional): `0` to `1.5`
- `paste_back` (bool, optional)
- `head_move_strength` (number, optional): `0` to `1`

### Response
- `task_id` (string)
- `task_status` (string)
- `video_url` (string, when finished)

## Quick start

```bash
python skills/ai/video/aliyun-modelstudio-liveportrait/scripts/prepare_liveportrait_request.py \
  --image-url "https://example.com/portrait.png" \
  --audio-url "https://example.com/speech.mp3" \
  --template-id calm \
  --video-fps 24 \
  --paste-back
```

## Operational guidance

- Use a clear, front-facing portrait with low occlusion.
- Keep the audio clean and voice-dominant.
- `paste_back=false` outputs only the generated face region; keep it `true` for standard talking-head output.
- LivePortrait is a better fit than EMO when you need longer, simpler presenter-style clips.

## Output location

- Default output: `output/aliyun-modelstudio-liveportrait/request.json`
- Override base dir with `OUTPUT_DIR`.

## References

- `references/sources.md`
