---
name: alicloud-ai-entry-modelstudio-test
description: Run a minimal test matrix for the Model Studio skills that exist in this repo (image/video/TTS). Use to execute one small request per skill and record results.
---

Category: task

# Model Studio 技能最小测试

对本仓库当前已存在的 Model Studio 技能进行最小化验证并记录结果。

## Prerequisites

- 安装 SDK（建议在虚拟环境中，避免 PEP 668 限制）：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```
- 配置 `DASHSCOPE_API_KEY`（环境变量优先；或在 `~/.alibabacloud/credentials` 里设置 `dashscope_api_key`）

## 测试矩阵（当前已支持）

1) 文生图 → `skills/ai/image/alicloud-ai-image-qwen-image/`
2) 文生视频/图生视频 → `skills/ai/video/alicloud-ai-video-wan-video/`
3) 语音合成 TTS → `skills/ai/audio/alicloud-ai-audio-tts/`

若需新增能力测试，请先生成对应技能（可用 `skills/ai/misc/alicloud-ai-misc-crawl-and-skill/` 更新模型清单）。

## 每项最小测试流程

1. 进入子技能目录并阅读 `SKILL.md`。
2. 选 1 个最小输入示例与推荐模型。
3. 执行 SDK 调用或脚本。
4. 记录：模型名、请求摘要、返回摘要、耗时、状态。

## 结果记录模板

保存为 `output/alicloud-ai-entry-modelstudio-test-results.md`：

```
# Model Studio 技能测试结果

- 日期：YYYY-MM-DD
- 环境：region / API_BASE / auth 方式

| 能力 | 子技能 | 模型 | 请求摘要 | 结果摘要 | 状态 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| 文生图 | alicloud-ai-image-qwen-image | <model-id> | ... | ... | pass/fail | ... |
```

## 失败处理

- 参数不确定：回到子技能 `SKILL.md` 或 `references/*.md` 查官方参数。
- 模型不可用：先更新模型清单再重试。
- 认证问题：检查 `DASHSCOPE_API_KEY`（环境变量或 `~/.alibabacloud/credentials`）。
## References

- Source list: `references/sources.md`
