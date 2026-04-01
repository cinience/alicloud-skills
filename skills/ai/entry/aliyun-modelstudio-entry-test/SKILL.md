---
name: aliyun-modelstudio-entry-test
description: Run a minimal test matrix for the Model Studio skills that exist in this repo, including image/video/audio, realtime speech, omni, visual reasoning, embedding, rerank, and edit variants. Use to execute one small request per skill and record results.
version: 1.0.0
---

Category: task

# Model Studio Skills Minimal Test

Run minimal validation for currently available Model Studio skills in this repo and record results.

## Prerequisites

- Install SDK (virtual environment recommended to avoid PEP 668 restrictions):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```
- Configure `DASHSCOPE_API_KEY` (environment variable preferred; or `dashscope_api_key` in `~/.alibabacloud/credentials`).

## Test Matrix (currently supported)

1) Text-to-image → `skills/ai/image/aliyun-modelstudio-qwen-image/`
2) Image editing → `skills/ai/image/aliyun-modelstudio-qwen-image-edit/`
3) Text-to-video / Image-to-video (i2v) → `skills/ai/video/aliyun-modelstudio-wan-video/`
4) Reference-to-video (r2v) → `skills/ai/video/aliyun-modelstudio-wan-r2v/`
5) TTS → `skills/ai/audio/aliyun-modelstudio-tts/`
6) ASR transcription (non-realtime) → `skills/ai/audio/aliyun-modelstudio-asr/`
7) Realtime ASR → `skills/ai/audio/aliyun-modelstudio-asr-realtime/`
8) Realtime TTS → `skills/ai/audio/aliyun-modelstudio-tts-realtime/`
9) Live speech translation → `skills/ai/audio/aliyun-modelstudio-livetranslate/`
10) CosyVoice voice clone → `skills/ai/audio/aliyun-modelstudio-cosyvoice-voice-clone/`
11) CosyVoice voice design → `skills/ai/audio/aliyun-modelstudio-cosyvoice-voice-design/`
12) Voice clone → `skills/ai/audio/aliyun-modelstudio-tts-voice-clone/`
13) Voice design → `skills/ai/audio/aliyun-modelstudio-tts-voice-design/`
14) Omni multimodal → `skills/ai/multimodal/aliyun-modelstudio-qwen-omni/`
15) Visual reasoning → `skills/ai/multimodal/aliyun-modelstudio-qvq/`
16) Text embedding → `skills/ai/search/aliyun-modelstudio-text-embedding/`
17) Rerank → `skills/ai/search/aliyun-modelstudio-rerank/`
18) Video editing → `skills/ai/video/aliyun-modelstudio-wan-edit/`

If new capability tests are needed, create corresponding skill first (use `skills/ai/misc/aliyun-modelstudio-crawl-and-skill/` to refresh model list).

## Minimal Flow Per Capability

1. Open target sub-skill directory and read `SKILL.md`.
2. Choose one minimal input example and recommended model.
3. Run SDK call or script.
4. Record model, request summary, response summary, duration, and status.

## Result Template

Save as `output/aliyun-modelstudio-entry-test-results.md`:

```
# Model Studio Skill Test Results

- Date: YYYY-MM-DD
- Environment: region / API_BASE / auth method

| Capability | Sub-skill | Model | Request summary | Result summary | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Text-to-image | aliyun-modelstudio-qwen-image | <model-id> | ... | ... | pass/fail | ... |
| Image editing | aliyun-modelstudio-qwen-image-edit | <model-id> | ... | ... | pass/fail | ... |
| Image-to-video (i2v) | aliyun-modelstudio-wan-video | <model-id> | ... | ... | pass/fail | ... |
| Reference-to-video (r2v) | aliyun-modelstudio-wan-r2v | <model-id> | ... | ... | pass/fail | ... |
| TTS | aliyun-modelstudio-tts | <model-id> | ... | ... | pass/fail | ... |
| ASR (non-realtime) | aliyun-modelstudio-asr | <model-id> | ... | ... | pass/fail | ... |
| Realtime ASR | aliyun-modelstudio-asr-realtime | <model-id> | ... | ... | pass/fail | ... |
| Realtime TTS | aliyun-modelstudio-tts-realtime | <model-id> | ... | ... | pass/fail | ... |
| Live speech translation | aliyun-modelstudio-livetranslate | <model-id> | ... | ... | pass/fail | ... |
| CosyVoice voice clone | aliyun-modelstudio-cosyvoice-voice-clone | <model-id> | ... | ... | pass/fail | ... |
| CosyVoice voice design | aliyun-modelstudio-cosyvoice-voice-design | <model-id> | ... | ... | pass/fail | ... |
| Voice clone | aliyun-modelstudio-tts-voice-clone | <model-id> | ... | ... | pass/fail | ... |
| Voice design | aliyun-modelstudio-tts-voice-design | <model-id> | ... | ... | pass/fail | ... |
| Omni multimodal | aliyun-modelstudio-qwen-omni | <model-id> | ... | ... | pass/fail | ... |
| Visual reasoning | aliyun-modelstudio-qvq | <model-id> | ... | ... | pass/fail | ... |
| Text embedding | aliyun-modelstudio-text-embedding | <model-id> | ... | ... | pass/fail | ... |
| Rerank | aliyun-modelstudio-rerank | <model-id> | ... | ... | pass/fail | ... |
| Video editing | aliyun-modelstudio-wan-edit | <model-id> | ... | ... | pass/fail | ... |
```

## Failure Handling

- If parameters are unclear, check target sub-skill `SKILL.md` or `references/*.md`.
- If model is unavailable, refresh model list and retry.
- For auth issues, verify `DASHSCOPE_API_KEY` (env var or `~/.alibabacloud/credentials`).
## Validation

```bash
mkdir -p output/aliyun-modelstudio-entry-test
echo "validation_placeholder" > output/aliyun-modelstudio-entry-test/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-modelstudio-entry-test/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-modelstudio-entry-test/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## Workflow

1) Confirm user intent, region, identifiers, and whether the operation is read-only or mutating.
2) Run one minimal read-only query first to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.

## References

- Source list: `references/sources.md`
