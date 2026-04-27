---
name: alicloud-ai-audio-cosyvoice-voice-clone-test
description: Minimal CosyVoice voice clone smoke test for Model Studio voice-enrollment.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Recommended check

```bash
python skills/ai/audio/alicloud-ai-audio-cosyvoice-voice-clone/scripts/prepare_cosyvoice_clone_request.py \
  --target-model cosyvoice-v3.5-plus \
  --prefix myvoice \
  --voice-sample-url https://example.com/voice.wav
```
