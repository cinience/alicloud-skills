# DashScope API Reference (Wan 2.7 Video Editing)

## Model

| Model | Capabilities | Resolution | Input Duration |
|---|---|---|---|
| wan2.7-videoedit | Style transfer, instruction editing with reference images | 720P, 1080P | 2-10s |

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
  "model": "wan2.7-videoedit",
  "input": {
    "prompt": "将整个画面转换为黏土风格",
    "negative_prompt": "低质量",
    "media": [
      {"type": "video", "url": "https://..."},
      {"type": "reference_image", "url": "https://..."}
    ]
  },
  "parameters": {
    "resolution": "1080P",
    "ratio": "16:9",
    "duration": 0,
    "audio_setting": "auto",
    "prompt_extend": true,
    "watermark": false,
    "seed": 42
  }
}
```

### input fields

| Field | Type | Required | Description |
|---|---|---|---|
| prompt | string | No | Editing instruction, up to 5000 chars |
| negative_prompt | string | No | Negative prompt, up to 500 chars |
| media | array | Yes | Must include exactly 1 video, optionally up to 3 reference_image |

### media types

| type | Description | Formats | Limits |
|---|---|---|---|
| video | Input video (required, exactly 1) | mp4/mov | 2-10s, [240,4096]px, ≤100MB |
| reference_image | Reference image (optional, max 3) | JPEG/JPG/PNG/BMP/WEBP | [240,8000]px, ≤20MB |

### parameters fields

| Field | Type | Default | Description |
|---|---|---|---|
| resolution | string | 1080P | 720P or 1080P |
| ratio | string | (input ratio) | 16:9, 9:16, 1:1, 4:3, 3:4 |
| duration | integer | 0 | Truncate to N seconds (2-10), 0=keep original |
| audio_setting | string | auto | auto (AI decides) or origin (keep original) |
| prompt_extend | boolean | true | AI prompt rewriting |
| watermark | boolean | false | "AI generated" watermark |
| seed | integer | auto | Range [0, 2147483647] |

### Resolution output table

| Resolution | Ratio | Output (W*H) |
|---|---|---|
| 720P | 16:9 | 1280*720 |
| 720P | 9:16 | 720*1280 |
| 720P | 1:1 | 960*960 |
| 720P | 4:3 | 1104*832 |
| 720P | 3:4 | 832*1104 |
| 1080P | 16:9 | 1920*1080 |
| 1080P | 9:16 | 1080*1920 |
| 1080P | 1:1 | 1440*1440 |
| 1080P | 4:3 | 1648*1248 |
| 1080P | 3:4 | 1248*1648 |

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
