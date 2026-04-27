# DashScope API Reference (HappyHorse 1.0 Video Editing)

## Model

| Model | Capabilities | Resolution | Output Duration |
|---|---|---|---|
| happyhorse-1.0-video-edit | Style transfer, instruction-based editing with optional reference images | 720P, 1080P | 3-15s (output ratio follows input) |

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
  "model": "happyhorse-1.0-video-edit",
  "input": {
    "prompt": "让视频中的马头人身角色穿上图片中的条纹毛衣",
    "media": [
      {"type": "video", "url": "https://example.com/input.mp4"},
      {"type": "reference_image", "url": "https://example.com/sweater.webp"}
    ]
  },
  "parameters": {
    "resolution": "720P",
    "audio_setting": "origin",
    "watermark": true
  }
}
```

### input fields

| Field | Type | Required | Description |
|---|---|---|---|
| prompt | string | Yes | Up to 5000 non-CJK / 2500 CJK characters describing the edit |
| media | array | Yes | Exactly 1 `video` element + 0-5 `reference_image` elements |

### media types

| type | Required | Count | Formats | Limits |
|---|---|---|---|---|
| video | Yes | exactly 1 | MP4/MOV (H.264 recommended) | 3-60s, long side ≤2160 px, short side ≥320 px, ratio 1:2.5~2.5:1, fps >8, ≤100 MB |
| reference_image | No | 0-5 | JPEG/JPG/PNG/WEBP | width and height ≥300 px, ratio 1:2.5~2.5:1, ≤10 MB |

### Output duration rule

| Input duration | Output duration |
|---|---|
| ≤ 15s | Equal to input |
| > 15s | Truncated to first 15s, output ≤ 15s |

### parameters fields

| Field | Type | Default | Description |
|---|---|---|---|
| resolution | string | 1080P | 720P or 1080P |
| audio_setting | string | auto | `auto` (model decides) or `origin` (keep input audio) |
| watermark | boolean | true | Add bottom-right "Happy Horse" watermark |
| seed | integer | auto | Range [0, 2147483647] |

`ratio` and `duration` are **not supported** — output ratio follows the input video and output duration follows the truncation rule.

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
  "request_id": "c11018a8-3f83-9591-a636-xxxxxx",
  "output": {
    "task_id": "051c7b40-b2c5-4341-aee4-xxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2026-04-26 14:13:14.373",
    "scheduled_time": "2026-04-26 14:13:14.419",
    "end_time": "2026-04-26 14:14:13.679",
    "orig_prompt": "...",
    "video_url": "https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxxx.mp4"
  },
  "usage": {
    "duration": 13.24,
    "input_video_duration": 6.62,
    "output_video_duration": 6.62,
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
    "message": "The resolution is not valid xxxxxx"
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
