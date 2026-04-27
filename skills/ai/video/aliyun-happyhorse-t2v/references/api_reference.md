# DashScope API Reference (HappyHorse 1.0 Text-to-Video)

## Model

| Model | Capabilities | Resolution | Ratio | Duration |
|---|---|---|---|---|
| happyhorse-1.0-t2v | Pure text-to-video synthesis | 720P, 1080P | 16:9, 9:16, 1:1, 4:3, 3:4 | 3-15s |

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
  "model": "happyhorse-1.0-t2v",
  "input": {
    "prompt": "一座由硬纸板和瓶盖搭建的微型城市，在夜晚焕发出生机。"
  },
  "parameters": {
    "resolution": "720P",
    "ratio": "16:9",
    "duration": 5,
    "watermark": true,
    "seed": 42
  }
}
```

### input fields

| Field | Type | Required | Description |
|---|---|---|---|
| prompt | string | Yes | Up to 5000 non-CJK / 2500 CJK characters; longer is truncated |

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
  "request_id": "99243b47-ec5f-9413-9993-xxxxxx",
  "output": {
    "task_id": "4673458e-28be-4a05-bf2a-xxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2026-04-20 17:55:17.075",
    "scheduled_time": "2026-04-20 17:55:17.129",
    "end_time": "2026-04-20 17:56:36.658",
    "orig_prompt": "...",
    "video_url": "https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxx.mp4"
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
