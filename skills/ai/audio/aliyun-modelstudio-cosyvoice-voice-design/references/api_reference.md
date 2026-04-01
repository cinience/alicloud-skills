# CosyVoice Voice Design API Reference

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
    "voice_prompt": "沉稳的中年男性播音员，音色低沉浑厚，富有磁性，语速平稳，吐字清晰。",
    "preview_text": "各位听众朋友，大家好，欢迎收听晚间新闻。",
    "prefix": "announcer",
    "language_hints": ["zh"]
  },
  "parameters": {
    "sample_rate": 24000,
    "response_format": "wav"
  }
}
```

## Important notes

- `voice_prompt` is required in design mode and supports only Chinese or English.
- `preview_text` is required in design mode and supports Chinese or English.
- If `language_hints` is used, it should match the language of `preview_text`.
- `prefix` must be up to 10 letters/digits.

## Response

The service returns a `voice_id` that can be used later in the TTS API.
