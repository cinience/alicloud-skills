# IMS 视频翻译参数速查

## 翻译级别选择

- 字幕级：`NeedSpeechTranslate=false` 且 `NeedFaceTranslate=false`，使用 `SubtitleTranslate`。
- 语音级：`NeedSpeechTranslate=true` 且 `NeedFaceTranslate=false`，使用 `SpeechTranslate`。
- 面容级：`NeedFaceTranslate=true` 且 `NeedSpeechTranslate=false`，使用 `FaceTranslate`。

## InputConfig

- `Type`：`Video` / `Audio` / `Subtitle`
- `Video`：视频媒资 ID 或地址（OSS 或公网）
- `Audio`：音频媒资 ID 或地址（OSS 或公网），支持 `mp3`/`wav`
- `Subtitle`：字幕媒资 ID 或地址（OSS 或公网），支持 `srt`

约束：
- 字幕级：`Type` 可为 `Video` 或 `Subtitle`
- 语音级：`Type` 可为 `Video` 或 `Audio`
- 面容级：`Type` 只能为 `Video`

## OutputConfig

- `OutputTarget`：`OSS`（默认）或 `VOD`
- `MediaURL`：输出 OSS 地址（必须带扩展名）
  - `InputConfig.Type=Video` → `mp4`
  - `InputConfig.Type=Audio` → `wav`
  - `InputConfig.Type=Subtitle` → `srt`
- `StorageLocation` / `FileName`：仅 `OutputTarget=VOD` 时填写

## EditingConfig

- `SourceLanguage`：源语言代码（如 `zh`）
- `TargetLanguage`：目标语言代码（如 `en`），多语言用逗号分隔（`en,ja,id`）
- `DetextArea`：字幕擦除区域，`Auto` 或 `[[x,y,w,h]]`
- `SupportEditing`：是否允许二次编辑（默认 `false`）
- `BilingualSubtitle`：是否输出双语字幕（默认 `false`）
- `SubtitleTranslate`：字幕级配置
- `NeedSpeechTranslate` / `SpeechTranslate`：语音级配置
- `NeedFaceTranslate` / `FaceTranslate`：面容级配置

## SubtitleTranslate

- `OcrArea`：`Auto` 或 `[x,y,w,h]`
- `SubtitleConfig`：字幕样式配置（与剪辑合成 SubtitleTrackClip 一致）

## SpeechTranslate

- `OcrArea`：`Auto` 或 `[x,y,w,h]`
- `CustomSrtType`：当输入为 `Subtitle` 时必填
  - `SourceSrt` / `TargetSrt` / `BilingualSrtSrcFirst` / `BilingualSrtTgtFirst`
- `SubtitleTimeForce`：仅翻译字幕时间范围内语音（默认 `false`）
- `SubtitleConfig`：字幕样式配置
- `OriginalJobId`：二次修正时填原任务 ID
- `SkipSong`：是否跳过清唱（0/1，默认 0）

## FaceTranslate

- `OcrArea`：`Auto` 或 `[x,y,w,h]`
- `CustomSrtType`：同 SpeechTranslate
