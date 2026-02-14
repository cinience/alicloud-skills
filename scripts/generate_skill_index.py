#!/usr/bin/env python3
"""Generate localized skill index tables for README files."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
README_FILES = [
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "README.zh-TW.md",
]

BEGIN = "<!-- SKILL_INDEX_BEGIN -->"
END = "<!-- SKILL_INDEX_END -->"


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = {}
    for line in parts[1].splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip()
    return fm


def category_from_path(skill_path: Path) -> str:
    rel = skill_path.relative_to(SKILLS_DIR)
    parts = rel.parts
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"
    return parts[0]


def collect_skills() -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        name = fm.get("name", skill_md.parent.name)
        category = category_from_path(skill_md)
        path = str(skill_md.parent.relative_to(ROOT))
        description = fm.get("description", "")
        rows.append((category, name, path, description))
    rows.sort(key=lambda x: (x[0], x[1]))
    return rows


def _zh_fallback(name: str) -> str:
    return f"技能 `{name}` 的能力说明，详见对应 SKILL.md。"


def _zh_tw_fallback(name: str) -> str:
    return f"技能 `{name}` 的能力說明，詳見對應 SKILL.md。"


def _translate_description(desc: str, name: str, lang: str) -> str:
    if lang == "en":
        return desc or f"See the SKILL.md of `{name}` for details."

    manage_pattern = re.compile(
        r"^Manage Alibaba Cloud (.+?) via OpenAPI/SDK\. "
        r"Use for listing resources, creating or updating configurations, "
        r"querying status, and troubleshooting workflows for this product\.$"
    )
    m = manage_pattern.match(desc)
    if m:
        if lang == "zh-tw":
            return (
                f"透過 OpenAPI/SDK 管理 Alibaba Cloud {m.group(1)}，"
                "用於資源查詢、建立或更新配置、狀態查詢與故障排查。"
            )
        return (
            f"通过 OpenAPI/SDK 管理 Alibaba Cloud {m.group(1)}，"
            "用于资源查询、创建或更新配置、状态查询与故障排查。"
        )

    patterns = [
        (
            "Alibaba Cloud OSS CLI (ossutil 2.0) skill.",
            "Alibaba Cloud OSS CLI（ossutil 2.0）技能，支持命令行安装、配置与 OSS 资源操作。",
            "Alibaba Cloud OSS CLI（ossutil 2.0）技能，支援命令列安裝、設定與 OSS 資源操作。",
        ),
        (
            "Build vector retrieval with DashVector using the Python SDK.",
            "使用 Python SDK 构建 DashVector 向量检索能力，支持集合创建、写入与相似度查询。",
            "使用 Python SDK 建立 DashVector 向量檢索能力，支援集合建立、寫入與相似度查詢。",
        ),
        (
            "Use Document Mind (DocMind) via Node.js SDK",
            "通过 Node.js SDK 使用 Document Mind（DocMind）执行文档解析任务并轮询结果。",
            "透過 Node.js SDK 使用 Document Mind（DocMind）執行文件解析任務並輪詢結果。",
        ),
        (
            "Generate images with Model Studio DashScope SDK",
            "通过 Model Studio DashScope SDK 进行图像生成，覆盖 prompt、size、seed 等核心参数。",
            "透過 Model Studio DashScope SDK 進行圖像生成，涵蓋 prompt、size、seed 等核心參數。",
        ),
        (
            "Generate videos with Model Studio DashScope SDK",
            "通过 Model Studio DashScope SDK 进行视频生成，支持时长、帧率、尺寸等参数控制。",
            "透過 Model Studio DashScope SDK 進行影片生成，支援時長、幀率、尺寸等參數控制。",
        ),
        (
            "Generate human-like speech audio with Model Studio DashScope Qwen TTS models",
            "使用 Model Studio DashScope Qwen TTS 模型生成人声语音，适用于文本转语音与配音场景。",
            "使用 Model Studio DashScope Qwen TTS 模型生成人聲語音，適用於文字轉語音與配音場景。",
        ),
        (
            "Real-time speech synthesis with Alibaba Cloud Model Studio Qwen TTS Realtime models.",
            "使用 Alibaba Cloud Model Studio Qwen TTS Realtime 模型进行实时语音合成。",
            "使用 Alibaba Cloud Model Studio Qwen TTS Realtime 模型進行即時語音合成。",
        ),
        (
            "Voice cloning workflows with Alibaba Cloud Model Studio Qwen TTS VC models.",
            "使用 Alibaba Cloud Model Studio Qwen TTS VC 模型执行声音克隆流程。",
            "使用 Alibaba Cloud Model Studio Qwen TTS VC 模型執行聲音克隆流程。",
        ),
        (
            "Voice design workflows with Alibaba Cloud Model Studio Qwen TTS VD models.",
            "使用 Alibaba Cloud Model Studio Qwen TTS VD 模型执行声音设计流程。",
            "使用 Alibaba Cloud Model Studio Qwen TTS VD 模型執行聲音設計流程。",
        ),
        (
            "Route Alibaba Cloud Model Studio requests to the right local skill",
            "将 Alibaba Cloud Model Studio 请求路由到最合适的本地技能（图像、视频、TTS 等）。",
            "將 Alibaba Cloud Model Studio 請求路由到最合適的本地技能（圖像、影片、TTS 等）。",
        ),
        (
            "Run a minimal test matrix for the Model Studio skills",
            "为仓库中的 Model Studio 技能执行最小化测试矩阵并记录结果。",
            "為倉庫中的 Model Studio 技能執行最小化測試矩陣並記錄結果。",
        ),
        (
            "Use AliCloud Milvus (serverless) with PyMilvus",
            "使用 PyMilvus 对接 AliCloud Milvus（Serverless），用于向量写入与相似度检索。",
            "使用 PyMilvus 對接 AliCloud Milvus（Serverless），用於向量寫入與相似度檢索。",
        ),
        (
            "Use OpenSearch vector search edition via the Python SDK (ha3engine)",
            "通过 Python SDK（ha3engine）使用 OpenSearch 向量检索版，支持文档写入与检索。",
            "透過 Python SDK（ha3engine）使用 OpenSearch 向量檢索版，支援文件寫入與檢索。",
        ),
        (
            "Create and manage Alibaba Cloud IMS video translation jobs via OpenAPI",
            "通过 OpenAPI 创建和管理 Alibaba Cloud IMS 视频翻译任务，支持字幕、语音与人脸相关配置。",
            "透過 OpenAPI 建立與管理 Alibaba Cloud IMS 影片翻譯任務，支援字幕、語音與人臉相關設定。",
        ),
        (
            "Alibaba Cloud DNS (Alidns) CLI skill.",
            "Alibaba Cloud DNS（Alidns）CLI 技能。",
            "Alibaba Cloud DNS（Alidns）CLI 技能，支援查詢、新增與更新 DNS 記錄。",
        ),
        (
            "Manage Function Compute AgentRun resources via OpenAPI",
            "通过 OpenAPI 管理 Function Compute AgentRun 资源，支持运行时、端点与状态查询。",
            "透過 OpenAPI 管理 Function Compute AgentRun 資源，支援執行環境、端點與狀態查詢。",
        ),
        (
            "Manage Alibaba Cloud RDS Supabase (RDS AI Service 2025-05-07) via OpenAPI.",
            "通过 OpenAPI 管理 Alibaba Cloud RDS Supabase，覆盖实例生命周期与关键配置操作。",
            "透過 OpenAPI 管理 Alibaba Cloud RDS Supabase，涵蓋實例生命週期與關鍵設定操作。",
        ),
        (
            "Refresh the Model Studio models crawl and regenerate derived summaries",
            "刷新 Model Studio 模型抓取结果并重新生成派生摘要及相关技能内容。",
            "刷新 Model Studio 模型抓取結果並重新產生衍生摘要與相關技能內容。",
        ),
        (
            "Discover and reconcile Alibaba Cloud product catalogs",
            "发现并对齐 Alibaba Cloud 产品目录与 OpenAPI 元数据，用于覆盖分析和技能规划。",
            "發現並對齊 Alibaba Cloud 產品目錄與 OpenAPI 中繼資料，用於覆蓋分析與技能規劃。",
        ),
        (
            "Automatically review latest Alibaba Cloud product docs and OpenAPI docs",
            "自动评审最新 Alibaba Cloud 产品文档与 OpenAPI 文档，并输出优先级建议与证据。",
            "自動評審最新 Alibaba Cloud 產品文件與 OpenAPI 文件，並輸出優先級建議與證據。",
        ),
        (
            "Benchmark similar product documentation and API documentation",
            "对阿里云及主流云厂商同类产品文档与 API 文档进行基准对比并给出改进建议。",
            "對阿里雲及主流雲廠商同類產品文件與 API 文件進行基準對比並給出改進建議。",
        ),
    ]

    for needle, zh_text, zh_tw_text in patterns:
        if desc.startswith(needle):
            return zh_tw_text if lang == "zh-tw" else zh_text

    return _zh_tw_fallback(name) if lang == "zh-tw" else _zh_fallback(name)


def _readme_lang(path: Path) -> str:
    if path.name == "README.en.md":
        return "en"
    if path.name == "README.zh-TW.md":
        return "zh-tw"
    return "zh"


def render_table(rows: list[tuple[str, str, str, str]], lang: str) -> str:
    if lang == "en":
        lines = ["| Category | Skill | Description | Path |", "| --- | --- | --- | --- |"]
    elif lang == "zh-tw":
        lines = ["| 分類 | 技能 | 技能描述 | 路徑 |", "| --- | --- | --- | --- |"]
    else:
        lines = ["| 分类 | 技能 | 技能描述 | 路径 |", "| --- | --- | --- | --- |"]

    for category, name, path, description in rows:
        localized = _translate_description(description, name, lang)
        lines.append(f"| {category} | {name} | {localized} | `{path}` |")
    return "\n".join(lines)


def update_readme(path: Path, table: str) -> None:
    text = path.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        raise RuntimeError(f"Missing skill index markers in {path}")
    pattern = re.compile(
        re.escape(BEGIN) + r".*?" + re.escape(END),
        flags=re.S,
    )
    replacement = f"{BEGIN}\n{table}\n{END}"
    new_text = pattern.sub(replacement, text)
    path.write_text(new_text, encoding="utf-8")


def main() -> None:
    rows = collect_skills()
    for readme in README_FILES:
        lang = _readme_lang(readme)
        table = render_table(rows, lang)
        update_readme(readme, table)


if __name__ == "__main__":
    main()
