---
name: alicloud-ai-audio-cosyvoice-voice-design-test
description: Minimal CosyVoice voice design smoke test for Model Studio voice-enrollment.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Recommended check

```bash
python skills/ai/audio/alicloud-ai-audio-cosyvoice-voice-design/scripts/prepare_cosyvoice_design_request.py \
  --target-model cosyvoice-v3.5-plus \
  --prefix announcer \
  --voice-prompt "沉稳的中年男性播音员，低沉有磁性，语速平稳。" \
  --preview-text "各位听众朋友，大家好。"
```
