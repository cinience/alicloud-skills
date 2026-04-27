# DashScope API Reference (HappyHorse 1.0 Reference-to-Video)

## Model

| Model | Capabilities | Resolution | Ratio | Duration |
|---|---|---|---|---|
| happyhorse-1.0-r2v | 1-9 reference images fused into a single video; prompt cites them as character1..N | 720P, 1080P | 16:9, 9:16, 1:1, 4:3, 3:4 | 3-15s |

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
  "model": "happyhorse-1.0-r2v",
  "input": {
    "prompt": "身着红色旗袍的女性 character1，轻抬玉手展开折扇 character2 时流苏耳坠 character3 随头部转动轻盈摆动。",
    "media": [
      {"type": "reference_image", "url": "https://example.com/girl.jpg"},
      {"type": "reference_image", "url": "https://example.com/folding-fan.jpg"},
      {"type": "reference_image", "url": "https://example.com/earring.jpg"}
    ]
  },
  "parameters": {
    "resolution": "720P",
    "ratio": "16:9",
    "duration": 5
  }
}
```

### input fields

| Field | Type | Required | Description |
|---|---|---|---|
| prompt | string | Yes | Up to 5000 non-CJK / 2500 CJK characters; reference subjects via `character1`..`characterN` matching media order |
| media | array | Yes | 1-9 elements, each `{type:"reference_image", url:"..."}` |

### media types

| type | Description | Formats | Limits |
|---|---|---|---|
| reference_image | Subject/object reference image | JPEG/JPG/PNG/WEBP | short side ≥ 400 px, ≤10 MB; 720P+ recommended |

### Character indexing

Position 1 → `character1`, position 2 → `character2`, …, position 9 → `character9`. Reorder the array to change which image binds to which `characterN`.

### parameters fields

| Field | Type | Default | Description |
|---|---|---|---|
| resolution | string | 1080P | 720P or 1080P |
| ratio | string | 16:9 | 16:9, 9:16, 1:1, 4:3, 3:4 |
| duration | integer | 5 | Video length 3-15 seconds |
| watermark | boolean | true | Add bottom-right "Happy Horse" watermark |
| seed | integer | auto | Range [0, 2147483647] |

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
  "request_id": "35137489-2862-96cb-b6f2-xxxxxx",
  "output": {
    "task_id": "1469cfc3-3004-4d9e-ab10-xxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2026-04-25 15:03:25.848",
    "scheduled_time": "2026-04-25 15:03:25.884",
    "end_time": "2026-04-25 15:04:05.882",
    "orig_prompt": "...",
    "video_url": "https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxxx.mp4"
  },
  "usage": {
    "duration": 5,
    "input_video_duration": 0,
    "output_video_duration": 5,
    "video_count": 1,
    "SR": 720,
    "ratio": "16:9"
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
