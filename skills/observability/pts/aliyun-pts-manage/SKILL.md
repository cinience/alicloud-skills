---
name: aliyun-pts-manage
description: Use when managing Alibaba Cloud Performance Testing Service (PTS) via OpenAPI/SDK, including scene lifecycle operations, test start/stop control, report retrieval, and metadata-driven API discovery before production changes.
version: 1.0.0
---

Category: service

# Alibaba Cloud Performance Testing Service (PTS)

## Purpose

Use Alibaba Cloud PTS OpenAPI to support:

- test scene inventory and inspection
- pressure test planning and lifecycle automation
- report and metrics retrieval for verification and troubleshooting

## Prerequisites

- Configure least-privilege Alibaba Cloud credentials.
- Install Python SDKs (virtual environment recommended):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U alibabacloud_pts20201020 alibabacloud_tea_openapi
```

- Prefer environment variables:
  - `ALICLOUD_ACCESS_KEY_ID`
  - `ALICLOUD_ACCESS_KEY_SECRET`
  - optional `ALICLOUD_REGION_ID`
- Before mutating operations, run read-only API discovery and current-state checks.

## AccessKey Priority

1) Environment variables: `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
2) Shared credentials file: `~/.alibabacloud/credentials`

If region/environment is unclear, confirm with user before mutating operations.

## Workflow

1) Identify target region, test scene identifiers, and operation scope.
2) Run API discovery to confirm API names and required parameters.
3) Execute read-only APIs first (`List*` / `Get*` / `Describe*`).
4) Execute mutating operations only after confirming rollback and change window.
5) Save outputs and evidence to `output/aliyun-pts-manage/`.

## API Discovery

- Product code: `PTS`
- Default API version: `2020-10-20`
- Metadata source: `https://api.aliyun.com/meta/v1/products/PTS/versions/2020-10-20/api-docs.json`

## Minimal Executable Quickstart

```bash
python skills/observability/pts/aliyun-pts-manage/scripts/list_openapi_meta_apis.py
```

Optional arguments:

```bash
python skills/observability/pts/aliyun-pts-manage/scripts/list_openapi_meta_apis.py \
  --product-code PTS \
  --version 2020-10-20 \
  --output-dir output/aliyun-pts-manage
```

List scenes (read-only):

```bash
python skills/observability/pts/aliyun-pts-manage/scripts/list_pts_scenes.py \
  --region cn-hangzhou \
  --page-number 1 \
  --page-size 10 \
  --output output/aliyun-pts-manage/scenes.txt
```

Start one scene (mutating):

```bash
python skills/observability/pts/aliyun-pts-manage/scripts/start_pts_scene.py \
  --region cn-hangzhou \
  --scene-id <scene-id> \
  --wait \
  --output output/aliyun-pts-manage/start-result.json
```

Stop one scene (mutating):

```bash
python skills/observability/pts/aliyun-pts-manage/scripts/stop_pts_scene.py \
  --region cn-hangzhou \
  --scene-id <scene-id> \
  --wait \
  --output output/aliyun-pts-manage/stop-result.json
```

## Common Operation Map

- Scene inventory: `ListPtsScene`, `GetPtsScene`, `ListOpenJMeterScenes`, `GetOpenJMeterScene`
- Scene lifecycle: `CreatePtsScene`, `SavePtsScene`, `ModifyPtsScene`, `DeletePtsScene`, `DeletePtsScenes`
- Test execution control: `StartPtsScene`, `StopPtsScene`, `StartTestingJMeterScene`, `StopTestingJMeterScene`
- Debug control: `StartDebugPtsScene`, `StopDebugPtsScene`, `StartDebuggingJMeterScene`, `StopDebuggingJMeterScene`
- Reports/metrics: `ListPtsReports`, `GetPtsReportDetails`, `GetPtsSceneRunningData`, `GetPtsSceneRunningStatus`

See `references/api_quick_map.md` for grouped API lists.

## Script Catalog

- `scripts/list_openapi_meta_apis.py`: fetch metadata and generate API inventory files.
- `scripts/list_pts_scenes.py`: list PTS scenes with pagination.
- `scripts/start_pts_scene.py`: start a scene and optionally poll running status.
- `scripts/stop_pts_scene.py`: stop a scene and optionally poll until non-running.

## Output Policy

Write generated files and execution evidence to:
`output/aliyun-pts-manage/`

## Validation

```bash
mkdir -p output/aliyun-pts-manage
for f in skills/observability/pts/aliyun-pts-manage/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/aliyun-pts-manage/validate.txt
```

Pass criteria: command exits 0 and `output/aliyun-pts-manage/validate.txt` is generated.

## Output And Evidence

- Save artifacts, command outputs, and API response summaries under `output/aliyun-pts-manage/`.
- Include key parameters (region/resource id/time range) in evidence files for reproducibility.

## References

- Source list: `references/sources.md`
- API quick map: `references/api_quick_map.md`
- request/response templates: `references/templates.md`
