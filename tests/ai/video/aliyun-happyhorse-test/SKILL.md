---
name: aliyun-happyhorse-test
description: Minimal smoke test matrix for the four Model Studio HappyHorse 1.0 video skills (t2v, i2v, r2v, video-edit).
version: 1.0.0
---

Category: test

# Minimal Viable Test (HappyHorse 1.0 Family)

## Goals

- Validate the smallest viable request payload for each of the four HappyHorse skills (`t2v`, `i2v`, `r2v`, `video-edit`).
- If execution fails, record exact error details (HTTP status, `code`, `message`, `request_id`) without guessing parameters.

## Prerequisites

- Authentication: `DASHSCOPE_API_KEY` exported, or `dashscope_api_key` configured in `~/.alibabacloud/credentials`.
- Region: Beijing endpoint by default (override with `DASHSCOPE_BASE_URL` if testing Singapore).
- Target skills under test:
  - `skills/ai/video/aliyun-happyhorse-t2v`
  - `skills/ai/video/aliyun-happyhorse-i2v`
  - `skills/ai/video/aliyun-happyhorse-r2v`
  - `skills/ai/video/aliyun-happyhorse-videoedit`

## Test Steps (Minimal)

For each model, send the smallest valid request and poll until terminal status. Save the full response JSON to `output/aliyun-happyhorse-test/<model>.json`.

### 1. t2v — `happyhorse-1.0-t2v`

```bash
.venv/bin/python skills/ai/video/aliyun-happyhorse-t2v/scripts/t2v_happyhorse.py \
  --prompt "A red kite flying over a green hill at sunset." \
  --resolution 720P \
  --duration 3 \
  --output output/aliyun-happyhorse-test/t2v
```

### 2. i2v — `happyhorse-1.0-i2v`

```bash
.venv/bin/python skills/ai/video/aliyun-happyhorse-i2v/scripts/i2v_happyhorse.py \
  --first-frame https://cdn.translate.alibaba.com/r/wanx-demo-1.png \
  --prompt "A cat running on grass." \
  --resolution 720P \
  --duration 3 \
  --output output/aliyun-happyhorse-test/i2v
```

### 3. r2v — `happyhorse-1.0-r2v`

```bash
.venv/bin/python skills/ai/video/aliyun-happyhorse-r2v/scripts/r2v_happyhorse.py \
  --reference-image https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/mvzfud/hh-v2v-girl.jpg \
  --prompt "character1 turns slowly to face the camera." \
  --resolution 720P \
  --ratio 16:9 \
  --duration 3 \
  --output output/aliyun-happyhorse-test/r2v
```

### 4. video-edit — `happyhorse-1.0-video-edit`

```bash
.venv/bin/python skills/ai/video/aliyun-happyhorse-videoedit/scripts/edit_happyhorse.py \
  --video https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260409/dozxak/Wan_Video_Edit_33_1.mp4 \
  --prompt "Convert the scene to a watercolor painting style." \
  --resolution 720P \
  --audio-setting origin \
  --output output/aliyun-happyhorse-test/videoedit
```

## Offline-only fallback (no API key)

If `DASHSCOPE_API_KEY` is unavailable, run only the static syntax checks and record results:

```bash
mkdir -p output/aliyun-happyhorse-test
for s in t2v i2v r2v videoedit; do
  case "$s" in
    videoedit) script="edit_happyhorse.py" ;;
    *)         script="${s}_happyhorse.py"  ;;
  esac
  python -m py_compile "skills/ai/video/aliyun-happyhorse-$s/scripts/$script" \
    && echo "py_compile_ok $s" >> output/aliyun-happyhorse-test/offline.txt
done
```

## Pass criteria

- Each of the four executable examples exits 0 with `task_status: SUCCEEDED` and a downloadable `video_url`, OR — in offline-only mode — `output/aliyun-happyhorse-test/offline.txt` contains four `py_compile_ok` lines (one per model).
- For any FAILED task, `code` and `message` are recorded verbatim under `output/aliyun-happyhorse-test/<model>.json`.

## Result Template

- Date: YYYY-MM-DD
- Skills under test:
  - skills/ai/video/aliyun-happyhorse-t2v
  - skills/ai/video/aliyun-happyhorse-i2v
  - skills/ai/video/aliyun-happyhorse-r2v
  - skills/ai/video/aliyun-happyhorse-videoedit
- Mode: live / offline-only
- Conclusion per model: t2v=pass|fail, i2v=pass|fail, r2v=pass|fail, videoedit=pass|fail
- Notes:
