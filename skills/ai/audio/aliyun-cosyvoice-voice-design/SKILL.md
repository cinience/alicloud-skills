---
name: aliyun-cosyvoice-voice-design
description: Use when designing custom voices with Alibaba Cloud Model Studio CosyVoice customization models, especially cosyvoice-v3.5-plus or cosyvoice-v3.5-flash, from a voice prompt plus preview text before using the returned voice_id in TTS.
version: 1.0.0
---

Category: provider

# Model Studio CosyVoice Voice Design

Use the CosyVoice voice enrollment API to create designed voices from a natural-language voice description.

## Critical model names

Use `model="voice-enrollment"` and one of these `target_model` values:
- `cosyvoice-v3.5-plus`
- `cosyvoice-v3.5-flash`
- `cosyvoice-v3-plus`
- `cosyvoice-v3-flash`

Recommended default in this repo:
- `target_model="cosyvoice-v3.5-plus"`

## Region and compatibility

- `cosyvoice-v3.5-plus` and `cosyvoice-v3.5-flash` are available only in China mainland deployment mode (Beijing endpoint).
- In international deployment mode (Singapore endpoint), `cosyvoice-v3-plus` and `cosyvoice-v3-flash` do not support voice clone/design.
- The `target_model` must match the later speech synthesis model.

## Endpoint

- Domestic: `https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization`
- International: `https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`

## Prerequisites

- Set `DASHSCOPE_API_KEY` in your environment, or add `dashscope_api_key` to `~/.alibabacloud/credentials`.

## Normalized interface (cosyvoice.voice_design)

### Request
- `model` (string, optional): fixed to `voice-enrollment`
- `target_model` (string, optional): default `cosyvoice-v3.5-plus`
- `prefix` (string, required): letters/digits only, max 10 chars
- `voice_prompt` (string, required): max 500 chars, Chinese or English only
- `preview_text` (string, required): max 200 chars, Chinese or English
- `language_hints` (array[string], optional): `zh` or `en`, and should match `preview_text`
- `sample_rate` (int, optional): e.g. `24000`
- `response_format` (string, optional): e.g. `wav`

### Response
- `voice_id` (string)
- `request_id` (string)
- `status` (string, optional)

## Operational guidance

- Keep `voice_prompt` concrete: timbre, age range, pace, emotion, articulation, and scenario.
- If `language_hints` is used, it should match the language of `preview_text`.
- Designed voice names include a `-vd-` marker in the generated backend naming convention.

## Local helper script

Prepare a normalized request JSON:

```bash
python skills/ai/audio/aliyun-cosyvoice-voice-design/scripts/prepare_cosyvoice_design_request.py \
  --target-model cosyvoice-v3.5-plus \
  --prefix announcer \
  --voice-prompt "沉稳的中年男性播音员，低沉有磁性，语速平稳，吐字清晰。" \
  --preview-text "各位听众朋友，大家好，欢迎收听晚间新闻。" \
  --language-hint zh
```

## Validation

```bash
mkdir -p output/aliyun-cosyvoice-voice-design
for f in skills/ai/audio/aliyun-cosyvoice-voice-design/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-cosyvoice-voice-design/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-cosyvoice-voice-design/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-cosyvoice-voice-design/`.
- Include `target_model`, `prefix`, `voice_prompt`, and `preview_text` in the evidence file.

## References

- `references/api_reference.md`
- `references/sources.md`
