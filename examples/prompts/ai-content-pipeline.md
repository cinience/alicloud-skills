# AI 内容生产流水线

## 目标

生成一套营销素材：图像、视频、配音，并完成上传与内容安全检测。

## 提示词样例

用 `alicloud-ai-image-qwen-image` 生成 3 张 1024x1024 的产品海报，给出每张的 prompt 和负面 prompt。

用 `alicloud-ai-video-wan-video` 基于上面第 1 张海报生成 6 秒视频，fps=24，size=720x1280。

用 `alicloud-ai-audio-tts` 把这段文案转成女声配音并给出保存路径：
“本周上新，限时 7 折，立即下单享受专属优惠。”

用 `alicloud-storage-oss-ossutil` 把生成的图片、视频、音频上传到 `oss://your-bucket/marketing/`。

用 `alicloud-security-content-moderation-green` 对上传后的图片和视频做内容安全检测，输出结果摘要。

用 `alicloud-observability-sls-log-query` 查询最近 30 分钟内容审核失败的日志并按状态聚合。
