# CosyVoice Voice Clone API Reference

## Endpoint

- Domestic: `POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization`
- International: `POST https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`

## Minimal request body

```json
{
  "model": "voice-enrollment",
  "input": {
    "action": "create_voice",
    "target_model": "cosyvoice-v3.5-plus",
    "prefix": "myvoice",
    "url": "https://your-audio-file-url",
    "language_hints": ["zh"]
  }
}
```

## Important notes

- `target_model` must match the later speech synthesis model.
- `url` is required for clone mode.
- `prefix` must be recognizable and up to 10 letters/digits.
- `language_hints` uses only the first element.
- `max_prompt_audio_length` range: `[3.0, 30.0]` for supported models.
- `enable_preprocess` can denoise and normalize the input audio for supported models.

## Response

```json
{
  "output": {
    "voice_id": "yourVoiceId"
  },
  "usage": {
    "count": 1
  },
  "request_id": "yourRequestId"
}
```
