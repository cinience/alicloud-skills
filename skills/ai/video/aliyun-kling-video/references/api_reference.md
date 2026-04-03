# DashScope API Reference (Kling V3 Video Generation)

## Models

| Model | Capabilities |
|---|---|
| kling/kling-v3-video-generation | t2v, i2v (first frame, first+last frame), smart storyboard |
| kling/kling-v3-omni-video-generation | All above + reference-to-video, video editing, multi-subject |

## Endpoint

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

Beijing region only. No Singapore endpoint.

## Required headers

| Header | Value |
|---|---|
| Content-Type | application/json |
| Authorization | Bearer $DASHSCOPE_API_KEY |
| X-DashScope-Async | enable |

## Request body

```json
{
  "model": "kling/kling-v3-video-generation",
  "input": {
    "prompt": "一只小猫在月光下奔跑",
    "media": [
      {"type": "first_frame", "url": "https://..."}
    ]
  },
  "parameters": {
    "mode": "pro",
    "aspect_ratio": "16:9",
    "duration": 5,
    "audio": false,
    "watermark": false
  }
}
```

### input fields

| Field | Type | Required | Description |
|---|---|---|---|
| prompt | string | Conditional | Up to 2500 chars. Required for shot_type=intelligence |
| negative_prompt | string | No | Content to exclude |
| media | array | No | Media objects (not needed for t2v) |
| multi_shot | boolean | No | Enable multi-shot (default: false) |
| shot_type | string | Conditional | `intelligence` or `customize` (when multi_shot=true) |
| multi_prompt | array | No | Per-shot prompts (when shot_type=customize) |
| element_list | array | No | Multi-subject elements (omni only) |

### media types

**kling/kling-v3-video-generation**:

| type | Description |
|---|---|
| first_frame | First frame image (1) |
| last_frame | Last frame image (1) |

**kling/kling-v3-omni-video-generation** (all above plus):

| type | Description |
|---|---|
| refer | Reference image |
| base | Base video for editing |
| feature | Feature reference video |

### Media combination rules (omni model)

| Task | Media combination | Limits |
|---|---|---|
| i2v first frame | first_frame | 1 image |
| i2v first+last | first_frame + last_frame | 1 each |
| Reference (video) | feature | 1 video |
| Reference (images) | refer | refer + elements ≤ 7 |
| Reference (video+images) | feature + refer | 1 video, refer + elements ≤ 4 |
| Reference (video+first) | feature + first_frame | 1 video + 1 image |
| Video editing | base | 1 video |
| Video editing + ref | base + refer | 1 video, refer + elements ≤ 4 |

### Media input limits

**Images**: JPEG/JPG/PNG (no transparency), [300,8000]px, ≤10MB

**Videos**: mp4/mov, 3-10s, [720,2160]px, 24-60fps, ≤200MB

### parameters fields

| Field | Type | Default | Description |
|---|---|---|---|
| mode | string | pro | `pro` (1080P) or `std` (720P) |
| aspect_ratio | string | 16:9 | `16:9`, `9:16`, `1:1`. Required for t2v and reference-to-video |
| duration | integer | 5 | [3, 15] seconds (or [3, 10] with reference video) |
| audio | boolean | false | Generate audio (affects pricing) |
| watermark | boolean | false | "可灵 AI" watermark |

### Omni model prompt references

Use `<<<>>>` to reference media in prompts:
- `<<<element_1>>>` — reference an element from element_list
- `<<<image_1>>>` — reference a refer image (by media array order)
- `<<<video_1>>>` — reference a feature video

Example: `一只<<<element_1>>>在月光下奔跑`

## Task creation response

```json
{
  "output": {
    "task_status": "PENDING",
    "task_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  },
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

## Task polling

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
Header: Authorization: Bearer $DASHSCOPE_API_KEY
```

### Success response

```json
{
  "request_id": "...",
  "output": {
    "task_id": "...",
    "task_status": "SUCCEEDED",
    "video_url": "https://...",
    "watermark_video_url": "https://..."
  },
  "usage": {
    "duration": 5,
    "size": "1280*720",
    "fps": 24,
    "video_count": 1,
    "audio": false,
    "SR": "720"
  }
}
```

### Task statuses

| Status | Description |
|---|---|
| PENDING | Queued |
| RUNNING | Processing |
| SUCCEEDED | Complete |
| FAILED | Failed |
| CANCELED | Canceled |
| UNKNOWN | Not found or unknown |
