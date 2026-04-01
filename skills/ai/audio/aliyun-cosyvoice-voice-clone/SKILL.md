---
name: aliyun-cosyvoice-voice-clone
description: Use when creating cloned voices with Alibaba Cloud Model Studio CosyVoice customization models, especially cosyvoice-v3.5-plus or cosyvoice-v3.5-flash, from reference audio and then reusing the returned voice_id in later TTS calls.
version: 1.0.0
---

Category: provider

# Model Studio CosyVoice Voice Clone

Use the CosyVoice voice enrollment API to create cloned voices from public reference audio.

## Critical model names

Use `model="voice-enrollment"` and one of these `target_model` values:
- `cosyvoice-v3.5-plus`
- `cosyvoice-v3.5-flash`
- `cosyvoice-v3-plus`
- `cosyvoice-v3-flash`
- `cosyvoice-v2`

Recommended default in this repo:
- `target_model="cosyvoice-v3.5-plus"`

## Region and compatibility

- `cosyvoice-v3.5-plus` and `cosyvoice-v3.5-flash` are available only in China mainland deployment mode (Beijing endpoint).
- In international deployment mode (Singapore endpoint), `cosyvoice-v3-plus` and `cosyvoice-v3-flash` do not support voice clone/design.
- The `target_model` used during enrollment must match the model used later in speech synthesis, otherwise synthesis fails.

## Endpoint

- Domestic: `https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization`
- International: `https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`

## Prerequisites

- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.
- Provide a public audio URL for the enrollment sample.

## Normalized interface (cosyvoice.voice_clone)

### Request
- `model` (string, optional): fixed to `voice-enrollment`
- `target_model` (string, optional): default `cosyvoice-v3.5-plus`
- `prefix` (string, required): letters/digits only, max 10 chars
- `voice_sample_url` (string, required): public audio URL
- `language_hints` (array[string], optional): only first item is used
- `max_prompt_audio_length` (float, optional): only for `cosyvoice-v3.5-plus`, `cosyvoice-v3.5-flash`, `cosyvoice-v3-flash`
- `enable_preprocess` (bool, optional): only for `cosyvoice-v3.5-plus`, `cosyvoice-v3.5-flash`, `cosyvoice-v3-flash`

### Response
- `voice_id` (string): use this as the `voice` parameter in later TTS calls
- `request_id` (string)
- `usage.count` (number, optional)

## Operational guidance

- For Chinese dialect reference audio, keep `language_hints=["zh"]`; control dialect style later in synthesis via text or `instruct`.
- For `cosyvoice-v3.5-plus`, supported `language_hints` include `zh`, `en`, `fr`, `de`, `ja`, `ko`, `ru`, `pt`, `th`, `id`, `vi`.
- Avoid frequent enrollment calls; each call creates a new custom voice and consumes quota.

## Local helper script

Prepare a normalized request JSON:

```bash
python skills/ai/audio/aliyun-cosyvoice-voice-clone/scripts/prepare_cosyvoice_clone_request.py \
  --target-model cosyvoice-v3.5-plus \
  --prefix myvoice \
  --voice-sample-url https://example.com/voice.wav \
  --language-hint zh
```

## Validation

```bash
mkdir -p output/aliyun-cosyvoice-voice-clone
for f in skills/ai/audio/aliyun-cosyvoice-voice-clone/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-cosyvoice-voice-clone/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-cosyvoice-voice-clone/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-cosyvoice-voice-clone/`.
- Include `target_model`, `prefix`, and sample URL in the evidence file.

## References

- `references/api_reference.md`
- `references/sources.md`
