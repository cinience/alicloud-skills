---
name: aliyun-modelstudio-crawl-and-skill
description: Use when refreshing the Model Studio models crawl and regenerate derived summaries and `skills/ai/**` skills. Use when the models list or generated skills must be updated.
version: 1.0.0
---

Category: task

# Alibaba Cloud Model Studio Crawl and Skill Generation

## Prerequisites

- Node.js (for `npx`)
- Python 3
- Network access to the models page

## Workflow

1) Crawl models page (raw markdown)

```bash
npx -y @just-every/crawl \"https://help.aliyun.com/zh/model-studio/models\" > alicloud-model-studio-models.md
```

2) Rebuild summary (models + API/usage links)

```bash
python3 skills/ai/misc/aliyun-modelstudio-crawl-and-skill/scripts/refresh_models_summary.py
```

3) Regenerate skills (creates/updates `skills/ai/**`)

```bash
python3 skills/ai/misc/aliyun-modelstudio-crawl-and-skill/scripts/refresh_alicloud_skills.py
```

## Outputs

- `alicloud-model-studio-models.md`: raw crawl output
- `output/alicloud-model-studio-models-summary.md`: cleaned summary
- `output/alicloud-model-studio-models.json`: structured model list
- `output/alicloud-model-studio-skill-scan.md`: skill coverage report
- `skills/ai/**`: generated skills

## Notes

- Do not invent model IDs or API endpoints; only use links present on the models page.
- After regeneration, update `README.md`, `README.en.md`, and `README.zh-TW.md` if skills list changed.
## Validation

```bash
mkdir -p output/aliyun-modelstudio-crawl-and-skill
for f in skills/ai/misc/aliyun-modelstudio-crawl-and-skill/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-modelstudio-crawl-and-skill/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-modelstudio-crawl-and-skill/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-modelstudio-crawl-and-skill/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## References

- Source list: `references/sources.md`
