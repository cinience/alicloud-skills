# DashScope SDK Reference (Qwen TTS)

## Install

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```

## Environment

```bash
export DASHSCOPE_API_KEY=your_key
```

If env vars are not set, you can also place `dashscope_api_key` under `[default]` in `~/.alibabacloud/credentials`.

## Suggested mapping

```python
import os
import dashscope

# Beijing region; for Singapore use: https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

response = dashscope.MultiModalConversation.call(
    model="qwen3-tts-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    text=text,
    voice=voice,
    language_type=language_type,
    stream=False,
)

audio_url = response.output.audio.url
```

## Streaming example (PCM)

```python
import os
import base64
import dashscope

# Beijing region; for Singapore use: https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

response = dashscope.MultiModalConversation.call(
    model="qwen3-tts-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    text=text,
    voice=voice,
    language_type=language_type,
    stream=True,
)

pcm_chunks = []
for chunk in response:
    audio = chunk.output.audio
    if audio.data:
        pcm_chunks.append(base64.b64decode(audio.data))
    if chunk.output.finish_reason == "stop":
        break

pcm_bytes = b"".join(pcm_chunks)
```

## Notes

- SDK versions: Python >= 1.24.6 (per doc); Java >= 2.21.9.
- `stream=False` returns a temporary `audio_url` valid for 24 hours.
- Streaming output is Base64 PCM at 24kHz.
