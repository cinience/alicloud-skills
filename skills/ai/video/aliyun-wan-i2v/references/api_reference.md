# DashScope API Reference (Wan 2.7 Image-to-Video)

## Model

| Model | Capabilities | Resolution | Duration |
|---|---|---|---|
| wan2.7-i2v | First-frame, first+last frame, video continuation, audio-driven | 720P, 1080P | 2-15s |

## Endpoint

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

Singapore: `https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

## Required headers

| Header | Value |
|---|---|
| Content-Type | application/json |
| Authorization | Bearer $DASHSCOPE_API_KEY |
| X-DashScope-Async | enable |

## Request body

```json
{
  "model": "wan2.7-i2v",
  "input": {
    "prompt": "描述文本",
    "negative_prompt": "不希望出现的内容",
    "media": [
      {"type": "first_frame", "url": "https://..."},
      {"type": "driving_audio", "url": "https://..."}
    ]
  },
  "parameters": {
    "resolution": "1080P",
    "duration": 5,
    "prompt_extend": true,
    "watermark": false,
    "seed": 42
  }
}
```

### input fields

| Field | Type | Required | Description |
|---|---|---|---|
| prompt | string | No | Text prompt, up to 5000 chars |
| negative_prompt | string | No | Negative prompt, up to 500 chars |
| media | array | Yes | Media objects with type and url |

### media types

| type | Description | Formats | Limits |
|---|---|---|---|
| first_frame | First frame image | JPEG/JPG/PNG/BMP/WEBP | [240,8000]px, ≤20MB |
| last_frame | Last frame image | JPEG/JPG/PNG/BMP/WEBP | [240,8000]px, ≤20MB |
| driving_audio | Driving audio | wav/mp3 | 2-30s, ≤15MB |
| first_clip | Video for continuation | mp4/mov | 2-10s, [240,4096]px, ≤100MB |

### Media combinations

| Task | Required media |
|---|---|
| First-frame video | first_frame |
| First+last frame | first_frame + last_frame |
| Audio-driven | first_frame + driving_audio |
| Video continuation | first_clip |

### parameters fields

| Field | Type | Default | Description |
|---|---|---|---|
| resolution | string | 1080P | 720P or 1080P |
| duration | integer | 5 | Video length 2-15 seconds |
| prompt_extend | boolean | true | AI prompt rewriting |
| watermark | boolean | false | "AI generated" watermark |
| seed | integer | auto | Range [0, 2147483647] |

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
    "orig_prompt": "original prompt text",
    "actual_prompt": "rewritten prompt text"
  },
  "usage": {
    "video_count": 1,
    "video_duration": 5
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
