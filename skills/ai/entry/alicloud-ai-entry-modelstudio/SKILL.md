---
name: alicloud-ai-entry-modelstudio
description: Route Alibaba Cloud Model Studio requests to the right local skill (Qwen Image, Wan Video, Qwen TTS). Use when the user asks for Model Studio without specifying a capability.
---

Category: task

# 阿里云 Model Studio 入口（路由）

将需求路由到已存在的本仓库技能，避免重复模型/参数内容。

## Prerequisites

- 安装 SDK（建议在虚拟环境中，避免 PEP 668 限制）：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```
- 配置 `DASHSCOPE_API_KEY`（环境变量优先；或在 `~/.alibabacloud/credentials` 里设置 `dashscope_api_key`）

## 路由表（当前仓库已支持）

| 需求 | 目标技能 |
| --- | --- |
| 文生图 / 图像生成 | `skills/ai/image/alicloud-ai-image-qwen-image/` |
| 文生视频 / 图生视频（i2v） | `skills/ai/video/alicloud-ai-video-wan-video/` |
| 语音合成（TTS） | `skills/ai/audio/alicloud-ai-audio-tts/` |
| 向量检索 | `skills/ai/search/alicloud-ai-search-dashvector/` 或 `skills/ai/search/alicloud-ai-search-opensearch/` 或 `skills/ai/search/alicloud-ai-search-milvus/` |
| 文档理解 | `skills/ai/text/alicloud-ai-text-document-mind/` |
| 模型清单抓取/更新 | `skills/ai/misc/alicloud-ai-misc-crawl-and-skill/` |

## 不匹配时

- 先澄清模型能力或输入输出类型。
- 若仓库缺少对应能力，建议新增技能后再执行。

## 本仓库暂缺的常见能力（可优先补齐）

- 文本生成/对话（LLM）与多模态理解
- 文本/多模态向量与 Rerank
- ASR 语音识别/转写/翻译
- 图像编辑（扩图/抠图/修复等）
- 视频编辑（风格/口型/剪辑）

- 多模态/ASR 下载失败：优先用上面的公开 URL。
- ASR 参数报错：使用 `input_audio.data` 的 data URI。
- 多模态向量 400：确认 `input.contents` 是数组。

## 异步任务轮询模板（视频/长耗时任务）

当 `X-DashScope-Async: enable` 返回 `task_id` 时，用以下方式轮询：

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/<task_id>
Authorization: Bearer $DASHSCOPE_API_KEY
```

结果字段示例（成功）：

```
{
  "output": {
    "task_status": "SUCCEEDED",
    "video_url": "https://..."
  }
}
```

说明：
- 轮询间隔建议 15–20 秒，最多 10 次。
- 成功后下载 `output.video_url`。

## 选择问题（不确定时提问）

1. 你要处理的是文本、图片、音频还是视频？
2. 这是“生成”还是“编辑/理解/检索”？
3. 是否需要语音（TTS/ASR）或向量检索（Embedding/Rerank）？
4. 你要直接运行 SDK 脚本，还是只需要 API/参数说明？

## 参考

- 模型清单与链接：`output/alicloud-model-studio-models-summary.md`
- 具体 API/参数/示例：对应子技能的 `SKILL.md` 与 `references/*.md`

- 官方文档来源清单：`references/sources.md`
