---
name: aliyun-mps-video-translation
description: Use when creating or managing Alibaba Cloud IMS video translation jobs via OpenAPI (subtitle/voice/face). Use when you need API-based video translation, status polling, and job management.
version: 1.0.0
---

Category: service

# IMS Video Translation (OpenAPI)

Submit video translation jobs via OpenAPI and poll results for subtitle-level, voice-level, and face-level processing.

## Prerequisites

- Prepare OSS input/output URIs (recommended to match API region).
- Configure AK: `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID` (`ALICLOUD_REGION_ID` can be used as the default region; if unset, choose the most reasonable region and ask when unclear).

## Workflow

1) Prepare source file and output OSS location.  
2) Submit job with `SubmitVideoTranslationJob`.  
3) Poll status and result with `GetSmartHandleJob`.  
4) Use `ListSmartJobs` / `DeleteSmartJob` for job management when needed.  

## Level Selection and Parameters

- Selection rules and fields for subtitle/voice/face levels are in `references/fields.md`.
- Field examples (Input/Output/EditingConfig) are also in `references/fields.md`.

## Notes

- For second-pass editing, set `SupportEditing=true` in the first job and reference `OriginalJobId` later.
- Input and output OSS regions must match the OpenAPI invocation region.
- Use longer polling intervals for large jobs to avoid frequent requests.
## Validation

```bash
mkdir -p output/aliyun-mps-video-translation
echo "validation_placeholder" > output/aliyun-mps-video-translation/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-mps-video-translation/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-mps-video-translation/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## References

- Source list: `references/sources.md`
