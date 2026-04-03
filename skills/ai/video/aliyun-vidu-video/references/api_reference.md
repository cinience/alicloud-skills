# DashScope API Reference (Vidu Video Generation)

## Models

| Model | Capability | Resolution | Duration |
|---|---|---|---|
| vidu/viduq3-pro_text2video | Text-to-video | 540P, 720P, 1080P | 1-16s |
| vidu/viduq3-turbo_text2video | Text-to-video | 540P, 720P, 1080P | 1-16s |
| vidu/viduq2_text2video | Text-to-video | 540P, 720P, 1080P | 1-10s |
| vidu/viduq3-pro_img2video | Image-to-video | 540P, 720P, 1080P | 1-16s |
| vidu/viduq3-turbo_img2video | Image-to-video | 540P, 720P, 1080P | 1-16s |
| vidu/viduq2-pro_img2video | Image-to-video | 720P, 1080P | 1-10s |
| vidu/viduq2-turbo_img2video | Image-to-video | 720P, 1080P | 1-10s |
| vidu/viduq3-pro_start-end2video | Keyframe (first+last) | 540P, 720P, 1080P | 1-16s |
| vidu/viduq3-turbo_start-end2video | Keyframe (first+last) | 540P, 720P, 1080P | 1-16s |
| vidu/viduq2-pro_start-end2video | Keyframe (first+last) | 540P, 720P, 1080P | 1-10s |
| vidu/viduq2-turbo_start-end2video | Keyframe (first+last) | 540P, 720P, 1080P | 1-10s |
| vidu/viduq2_reference2video | Reference-to-video | 540P, 720P, 1080P | 1-10s |
| vidu/viduq2-pro_reference2video | Reference-to-video | 540P, 720P, 1080P | 1-10s |

## Endpoint

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

Region: Beijing (China Mainland) only.

## Required headers

| Header | Value |
|---|---|
| Content-Type | application/json |
| Authorization | Bearer $DASHSCOPE_API_KEY |
| X-DashScope-Async | enable |

## Request body -- Text-to-video

```json
{
  "model": "vidu/viduq3-turbo_text2video",
  "input": {
    "prompt": "A cat running under moonlight"
  },
  "parameters": {
    "resolution": "540P",
    "size": "960*528",
    "duration": 5,
    "audio": false,
    "watermark": true,
    "seed": 12345
  }
}
```

## Request body -- Image-to-video

```json
{
  "model": "vidu/viduq3-pro_img2video",
  "input": {
    "media": [
      {"type": "image", "url": "https://example.com/image.jpg"}
    ],
    "prompt": "Camera slowly pans upward"
  },
  "parameters": {
    "duration": 5,
    "resolution": "720P",
    "watermark": true
  }
}
```

## Request body -- Keyframe-to-video

```json
{
  "model": "vidu/viduq3-turbo_start-end2video",
  "input": {
    "media": [
      {"type": "image", "url": "https://example.com/first_frame.png"},
      {"type": "image", "url": "https://example.com/last_frame.png"}
    ],
    "prompt": "A cat jumps from windowsill to sofa"
  },
  "parameters": {
    "resolution": "540P",
    "duration": 5,
    "watermark": true
  }
}
```

## Request body -- Reference-to-video (images only)

```json
{
  "model": "vidu/viduq2_reference2video",
  "input": {
    "media": [
      {"type": "image", "url": "https://example.com/ref1.jpg"},
      {"type": "image", "url": "https://example.com/ref2.png"},
      {"type": "image", "url": "https://example.com/ref3.png"}
    ],
    "prompt": "Man playing guitar in a cafe"
  },
  "parameters": {
    "duration": 5,
    "size": "1280*720",
    "resolution": "720P",
    "watermark": true
  }
}
```

## Request body -- Reference-to-video (images + video)

Supported by `vidu/viduq2-pro_reference2video` only.

```json
{
  "model": "vidu/viduq2-pro_reference2video",
  "input": {
    "media": [
      {"type": "video", "url": "https://example.com/ref_video.mp4"},
      {"type": "image", "url": "https://example.com/ref1.png"},
      {"type": "image", "url": "https://example.com/ref2.png"}
    ],
    "prompt": "Man playing guitar in a cafe"
  },
  "parameters": {
    "duration": 5,
    "size": "1280*720",
    "resolution": "720P",
    "watermark": true
  }
}
```

## input fields

| Field | Type | Required | Description |
|---|---|---|---|
| prompt | string | Varies | Text prompt, up to 5000 chars. Required for t2v, keyframe, ref. Optional for i2v. |
| media | array | Varies | Media objects with type and url. Required for i2v, keyframe, ref. Not used for t2v. |

## media element fields

| Field | Type | Required | Values |
|---|---|---|---|
| type | string | Yes | `image` or `video` |
| url | string | Yes | Public HTTP/HTTPS URL |

## Media constraints by mode

| Mode | Images | Videos | Notes |
|---|---|---|---|
| Text-to-video | N/A | N/A | No media input |
| Image-to-video | Exactly 1 | 0 | Single first-frame image |
| Keyframe | Exactly 2 | 0 | First element = first frame, second = last frame |
| Reference (viduq2) | 1-7 | 0 | Images only |
| Reference (viduq2-pro) | 1-4 | 0-2 | Images required, videos optional |

## Image constraints

| Property | Limit |
|---|---|
| Formats | JPG, PNG, WEBP |
| Aspect ratio | 1:4 to 4:1 |
| Max file size | 50MB |

## Video constraints (reference mode)

| Property | Limit |
|---|---|
| Formats | mp4, avi, mov |
| Min resolution | 128x128 |
| Aspect ratio | 1:4 to 4:1 |
| Duration | 1-5s |
| Max file size | 50MB |

## parameters fields

| Field | Type | Default | Description |
|---|---|---|---|
| resolution | string | 720P | 540P, 720P, or 1080P. Affects pricing. |
| size | string | varies | Pixel dimensions width*height. See size tables in SKILL.md. |
| duration | integer | 5 | Video length in seconds. Q3: [1,16], Q2: [1,10]. Affects pricing. |
| audio | boolean | false | Generate audio track. Q3 models only. |
| watermark | boolean | false | Add "AI generated" watermark |
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

Recommended polling interval: 15 seconds.

### Success response

```json
{
  "request_id": "...",
  "output": {
    "task_id": "...",
    "task_status": "SUCCEEDED",
    "submit_time": "2026-03-27 13:32:13.962",
    "scheduled_time": "2026-03-27 13:32:14.008",
    "end_time": "2026-03-27 13:32:43.375",
    "orig_prompt": "original prompt text",
    "video_url": "https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxx"
  },
  "usage": {
    "duration": 5,
    "size": "960*528",
    "output_video_duration": 5,
    "fps": 24,
    "video_count": 1,
    "audio": false,
    "SR": "540"
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
    "message": "The size is not match xxxxxx"
  }
}
```

### Task statuses

| Status | Description |
|---|---|
| PENDING | Queued |
| RUNNING | Processing |
| SUCCEEDED | Complete -- video_url available |
| FAILED | Failed -- check code/message |
| CANCELED | Canceled |
| UNKNOWN | Not found or expired (task_id valid for 24h) |

## Error codes

| Code | Description | Resolution |
|---|---|---|
| InvalidApiKey | API Key missing or invalid | Check DASHSCOPE_API_KEY |
| InvalidParameter | Parameter validation failed | Check size/resolution/duration values |
| Throttling | Rate limit exceeded | Retry with backoff |
| InternalError | Server error | Retry after delay |
