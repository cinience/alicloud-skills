# DashScope API Reference (Wan 2.2 Animate Move)

## Model

| Model | Capabilities | Modes |
|---|---|---|
| wan2.2-animate-move | Motion transfer from reference video to character image | wan-std, wan-pro |

## Endpoint

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis
```

Singapore: `https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

## Required headers

| Header | Value |
|---|---|
| Content-Type | application/json |
| Authorization | Bearer $DASHSCOPE_API_KEY |
| X-DashScope-Async | enable |

## Request body

```json
{
  "model": "wan2.2-animate-move",
  "input": {
    "image_url": "https://example.com/person.jpg",
    "video_url": "https://example.com/dance.mp4",
    "watermark": false
  },
  "parameters": {
    "mode": "wan-std",
    "check_image": true
  }
}
```

### input fields

| Field | Type | Required | Description |
|---|---|---|---|
| image_url | string | Yes | Public HTTP/HTTPS URL of the character image |
| video_url | string | Yes | Public HTTP/HTTPS URL of the reference motion video |
| watermark | boolean | No | Add "AI generated" watermark (default: false) |

### Image requirements

| Constraint | Value |
|---|---|
| Formats | JPG, JPEG, PNG, BMP, WEBP |
| Resolution | [200, 4096] pixels per side |
| Aspect ratio | 1:3 to 3:1 |
| Max size | 5MB |
| Content | Single person, facing camera, face fully visible, moderate proportion |

### Video requirements

| Constraint | Value |
|---|---|
| Formats | MP4, AVI, MOV |
| Duration | 2-30s |
| Resolution | [200, 2048] pixels per side |
| Aspect ratio | 1:3 to 3:1 |
| Max size | 200MB |
| Content | Single person, facing camera, face fully visible, moderate proportion |

### parameters fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| mode | string | Yes | - | `wan-std` (standard) or `wan-pro` (professional) |
| check_image | boolean | No | true | Whether to perform image detection |

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
    "video_url": "https://..."
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
