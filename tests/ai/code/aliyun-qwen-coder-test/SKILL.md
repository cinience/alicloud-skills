---
name: alicloud-ai-code-qwen-coder-test
description: Minimal coding-model smoke test for Model Studio Qwen Coder.
version: 1.0.0
---

Category: test

# Minimal Viable Test

## Prerequisites

- Target skill: `skills/ai/code/alicloud-ai-code-qwen-coder`

## Executable Example

```bash
.venv/bin/python skills/ai/code/alicloud-ai-code-qwen-coder/scripts/prepare_code_request.py \
  --task "Add one guard clause to validate empty input." \
  --language python
```

Pass criteria: script returns `{"ok": true, ...}` and writes `output/alicloud-ai-code-qwen-coder/requests/request.json`.

