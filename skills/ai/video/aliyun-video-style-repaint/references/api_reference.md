# DashScope API Reference (Video Style Repaint)

## Model

| Model | Capabilities | Styles |
|---|---|---|
| video-style-transform | Video artistic style transformation | 8 preset styles (manga, comics, cartoon, ink painting, etc.) |

## Endpoint

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

Note: This API is only available in the Beijing region. Do not use Singapore endpoint.

## Required headers

| Header | Value |
|---|---|
| Content-Type | application/json |
| Authorization | Bearer $DASHSCOPE_API_KEY |
| X-DashScope-Async | enable |

## Request body

```json
{
  "model": "video-style-transform",
  "input": {
    "video_url": "https://example.com/video.mp4"
  },
  "parameters": {
    "style": 0,
    "video_fps": 15,
    "animate_emotion": true,
    "min_len": 720,
    "use_SR": false
  }
}
```

### input fields

| Field | Type | Required | Description |
|---|---|---|---|
| video_url | string | Yes | Public HTTP/HTTPS URL of the input video |

### Video requirements

| Constraint | Value |
|---|---|
| Formats | MP4, AVI, MKV, MOV, FLV, TS, MPG, MXF |
| Resolution | [256, 4096] pixels per side, aspect ratio max 1.8:1 |
| Duration | Up to 30 seconds |
| Max size | 100MB |

### parameters fields

| Field | Type | Default | Description |
|---|---|---|---|
| style | int | 0 | Style ID: 0=Japanese Manga, 1=American Comics, 2=Fresh Comics, 3=3D Cartoon, 4=Chinese Cartoon, 5=Paper Art, 6=Simple Illustration, 7=Chinese Ink Painting |
| video_fps | int | 15 | Output frame rate, range [15, 25] |
| animate_emotion | bool | true | Facial expression optimization |
| min_len | int | 720 | Output short-side pixels (540 or 720) |
| use_SR | bool | false | Super-resolution enhancement (free, increases processing time) |

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
    "submit_time": "2024-05-16 13:50:01.247",
    "scheduled_time": "2024-05-16 13:50:01.354",
    "end_time": "2024-05-16 13:50:27.795",
    "output_video_url": "http://xxx/result.mp4"
  },
  "usage": {
    "duration": 3,
    "SR": 720
  }
}
```

### Task statuses

| Status | Description |
|---|---|
| PENDING | Queued |
| RUNNING | Processing |
| SUSPENDED | Suspended |
| SUCCEEDED | Complete |
| FAILED | Failed |
| UNKNOWN | Not found or unknown |
