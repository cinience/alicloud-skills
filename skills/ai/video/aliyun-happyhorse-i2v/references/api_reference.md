# DashScope API Reference (HappyHorse 1.0 Image-to-Video, First Frame)

## Model

| Model | Capabilities | Resolution | Duration |
|---|---|---|---|
| happyhorse-1.0-i2v | Single first-frame image-to-video; output ratio follows input image | 720P, 1080P | 3-15s |

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
  "model": "happyhorse-1.0-i2v",
  "input": {
    "prompt": "一只猫在草地上奔跑",
    "media": [
      {"type": "first_frame", "url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"}
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 5,
    "watermark": true
  }
}
```

### input fields

| Field | Type | Required | Description |
|---|---|---|---|
| prompt | string | No | Up to 5000 non-CJK / 2500 CJK characters; longer is truncated |
| media | array | Yes | Exactly 1 element with type `first_frame` |

### media types

| type | Description | Formats | Limits |
|---|---|---|---|
| first_frame | First frame image | JPEG/JPG/PNG/WEBP | width and height ≥ 300 px, ratio 1:2.5~2.5:1, ≤10 MB |

### parameters fields

| Field | Type | Default | Description |
|---|---|---|---|
| resolution | string | 1080P | 720P or 1080P |
| duration | integer | 5 | Video length 3-15 seconds |
| watermark | boolean | true | Add bottom-right "Happy Horse" watermark |
| seed | integer | auto | Range [0, 2147483647] |

`ratio` is **not supported** — output aspect ratio follows the input first-frame image automatically.

## Task creation response

```json
{
  "output": {
    "task_status": "PENDING",
    "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
  },
  "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

## Task polling

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
Header: Authorization: Bearer $DASHSCOPE_API_KEY
```

Recommended interval: 15 seconds. RPS limit on the query endpoint defaults to 20.

### Success response

```json
{
  "request_id": "8ae698ba-df2d-966c-abcf-xxxxxx",
  "output": {
    "task_id": "e56d806f-76f9-4037-aefa-xxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2026-04-20 19:33:50.425",
    "scheduled_time": "2026-04-20 19:33:50.463",
    "end_time": "2026-04-20 19:35:34.216",
    "orig_prompt": "一只猫在草地上奔跑",
    "video_url": "https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxx.mp4"
  },
  "usage": {
    "duration": 5,
    "input_video_duration": 0,
    "output_video_duration": 5,
    "video_count": 1,
    "SR": 720
  }
}
```

### Failure response

```json
{
  "request_id": "...",
  "output": {
    "task_id": "...",
    "task_status": "FAILED",
    "code": "InvalidParameter",
    "message": "The parameter is invalid."
  }
}
```

### Expired task

```json
{
  "request_id": "...",
  "output": {
    "task_id": "...",
    "task_status": "UNKNOWN"
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
| UNKNOWN | Not found or older than 24 hours |

## Lifetime constraints

- `task_id`: 24 hours.
- `video_url`: 24 hours — download immediately and persist (e.g., to Alibaba Cloud OSS).

## Output media

- Format: MP4 (H.264, 24 fps).
- Aspect ratio: follows the input first-frame image (no `ratio` parameter).
