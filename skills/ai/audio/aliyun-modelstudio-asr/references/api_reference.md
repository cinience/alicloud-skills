# Qwen ASR API Notes (Non-Realtime)

## Endpoints

- Sync (OpenAI-compatible):
  - `POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
- Async long-file (DashScope protocol):
  - `POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription`
- Auth header: `Authorization: Bearer <DASHSCOPE_API_KEY>`
- Async header: `X-DashScope-Async: enable` (for long-file mode)

## Recommended models

- `qwen3-asr-flash`
- `qwen-audio-asr`
- `qwen3-asr-flash-filetrans`

## Sync request skeleton (OpenAI-compatible)

```json
{
  "model": "qwen3-asr-flash",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_audio",
          "input_audio": {
            "data": "https://example.com/audio.wav"
          }
        }
      ]
    }
  ],
  "stream": false
}
```

## Local file payload pattern (sync)

When local files are used, build a data URI and submit through `messages[*].content[*].input_audio.data`:

```json
{
  "model": "qwen-audio-asr",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_audio",
          "input_audio": {
            "data": "data:audio/wav;base64,<BASE64_AUDIO>"
          }
        }
      ]
    }
  ]
}
```

## Async request skeleton (filetrans)

```json
{
  "model": "qwen3-asr-flash-filetrans",
  "input": {
    "file_url": "https://example.com/audio.wav"
  }
}
```

## Async task polling

- Submit with `X-DashScope-Async: enable`
- Poll:
  - `GET https://dashscope.aliyuncs.com/api/v1/tasks/<task_id>`

## Common normalized output extraction

Prefer these fields in order:
1. `choices[0].message.content`
2. `output.transcription.text`
3. `output.results[*].transcription.text`
4. fallback: first text-like field under response
