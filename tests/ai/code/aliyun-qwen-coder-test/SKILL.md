---
name: aliyun-qwen-coder-test
description: Minimal coding-model smoke test for Model Studio Qwen Coder.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/code/aliyun-qwen-coder`

## Executable Example

```bash
.venv/bin/python skills/ai/code/aliyun-qwen-coder/scripts/prepare_code_request.py \
  --task "Add one guard clause to validate empty input." \
  --language python
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/aliyun-qwen-coder/requests/request.json`.

