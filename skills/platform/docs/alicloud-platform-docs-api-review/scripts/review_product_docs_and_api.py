#!/usr/bin/env python3
"""Auto-review Alibaba Cloud product docs and API docs for one product name.

Given a product name/code (e.g. "ECS", "云服务器", "OpenSearch"), this script:
1) Resolves the product from OpenAPI metadata (latest version by defaultVersion)
2) Fetches API docs metadata and computes quality signals
3) Finds product page and help-doc links, then evaluates doc structure coverage
4) Writes a structured markdown report + JSON evidence under output/
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OPENAPI_PRODUCTS_ZH = "https://api.aliyun.com/meta/v1/products.json?language=ZH_CN"
OPENAPI_PRODUCTS_EN = "https://api.aliyun.com/meta/v1/products.json?language=EN_US"
PRODUCT_LIST_URL = "https://www.aliyun.com/product/list"
OUTPUT_ROOT = Path("output/alicloud-platform-docs-api-review")


@dataclass
class ProductMatch:
    code: str
    name_zh: str
    name_en: str
    short_name: str
    default_version: str
    versions: list[str]
    category: str
    score: int


def fetch_url(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Codex Skill Reviewer)",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def fetch_json(url: str, timeout: int = 30) -> Any:
    return json.loads(fetch_url(url, timeout=timeout))


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", (text or "").lower())


def load_products() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    zh = fetch_json(OPENAPI_PRODUCTS_ZH)
    en = fetch_json(OPENAPI_PRODUCTS_EN)
    if not isinstance(zh, list) or not isinstance(en, list):
        raise RuntimeError("Unexpected OpenAPI products payload")
    return zh, en


def resolve_product(query: str, products_zh: list[dict[str, Any]], products_en: list[dict[str, Any]]) -> ProductMatch:
    qn = norm(query)
    by_code_en = {p.get("code"): p for p in products_en if p.get("code")}

    best: ProductMatch | None = None

    for pzh in products_zh:
        code = pzh.get("code") or ""
        if not code:
            continue
        pen = by_code_en.get(code, {})

        name_zh = pzh.get("name") or ""
        name_en = pen.get("name") or ""
        short_name = pzh.get("shortName") or pen.get("shortName") or ""
        versions = pzh.get("versions") or pen.get("versions") or []
        default_version = pzh.get("defaultVersion") or pen.get("defaultVersion") or (versions[-1] if versions else "")

        fields = [query, code, name_zh, name_en, short_name]
        score = 0

        if qn == norm(code):
            score += 120
        if qn == norm(short_name):
            score += 100
        if qn == norm(name_zh) or qn == norm(name_en):
            score += 95

        for f in fields[1:]:
            fn = norm(f)
            if not fn:
                continue
            if qn and qn in fn:
                score += 40
            if qn and fn in qn:
                score += 20

        if score <= 0:
            continue

        cand = ProductMatch(
            code=code,
            name_zh=name_zh,
            name_en=name_en,
            short_name=short_name,
            default_version=default_version,
            versions=list(versions),
            category=pzh.get("categoryName") or "",
            score=score,
        )
        if best is None or cand.score > best.score:
            best = cand

    if best is None:
        raise RuntimeError(f"Cannot resolve product for query: {query}")
    return best


def extract_anchors(html: str) -> list[tuple[str, str]]:
    pattern = re.compile(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.I | re.S)
    out: list[tuple[str, str]] = []
    for href, body in pattern.findall(html):
        text = re.sub(r"<[^>]+>", " ", body)
        text = re.sub(r"\s+", " ", text).strip()
        out.append((href, text))
    return out


def choose_product_page_url(query: str, match: ProductMatch) -> str | None:
    html = fetch_url(PRODUCT_LIST_URL)
    anchors = extract_anchors(html)

    qn = norm(query)
    mn = {norm(match.code), norm(match.short_name), norm(match.name_zh), norm(match.name_en)}
    mn.discard("")

    best_url: str | None = None
    best_score = -1

    for href, text in anchors:
        if not href.startswith("https://www.aliyun.com/product"):
            continue
        tn = norm(text)
        if not tn:
            continue

        score = 0
        for token in mn:
            if token and token in tn:
                score += 40
        if qn and qn in tn:
            score += 50
        if f"/{match.code.lower()}" in href.lower():
            score += 80
        if href.rstrip("/").lower() == f"https://www.aliyun.com/product/{match.code.lower()}":
            score += 120

        if score > best_score:
            best_score = score
            best_url = href

    if best_url:
        return best_url

    fallback = f"https://www.aliyun.com/product/{match.code.lower()}"
    try:
        fetch_url(fallback, timeout=15)
        return fallback
    except Exception:
        return None


def extract_help_links(html: str) -> list[str]:
    links = set(re.findall(r"https://help\.aliyun\.com/[^\"'\s)]+", html))
    return sorted(links)


def pick_primary_help_links(help_links: list[str], code: str) -> list[str]:
    selected: list[str] = []
    for link in help_links:
        low = link.lower()
        if any(k in low for k in ["/developer-reference", "/api-", "/overview", "/user-guide", "/quick-start", f"/zh/{code.lower()}/"]):
            selected.append(link)
    if not selected:
        selected = help_links[:8]
    return selected[:12]


def parse_api_docs(api_docs: dict[str, Any]) -> dict[str, Any]:
    apis_obj = api_docs.get("apis") or {}
    if isinstance(apis_obj, dict):
        items = [(name, item) for name, item in apis_obj.items() if isinstance(item, dict)]
    elif isinstance(apis_obj, list):
        items = []
        for item in apis_obj:
            if isinstance(item, dict):
                name = item.get("name") or item.get("apiName") or "unknown"
                items.append((str(name), item))
    else:
        items = []

    total = len(items)
    deprecated = 0
    missing_summary = 0
    no_error_codes = 0
    no_examples = 0
    param_sizes: list[int] = []

    samples: list[dict[str, Any]] = []

    for idx, (name, item) in enumerate(items):
        if item.get("deprecated") is True:
            deprecated += 1
        summary = item.get("summary") or item.get("title")
        if not summary:
            missing_summary += 1

        params = item.get("parameters") or []
        if isinstance(params, list):
            param_sizes.append(len(params))
        else:
            param_sizes.append(0)

        err = item.get("errorCodes") or []
        if not err:
            no_error_codes += 1

        demo = item.get("responseDemo")
        if not demo:
            no_examples += 1

        if idx < 12:
            samples.append(
                {
                    "api": name,
                    "summary": summary or "",
                    "deprecated": bool(item.get("deprecated")),
                    "param_count": param_sizes[-1],
                    "error_code_count": len(err) if isinstance(err, list) else 0,
                }
            )

    avg_params = round(sum(param_sizes) / total, 2) if total else 0.0

    return {
        "api_count": total,
        "deprecated_count": deprecated,
        "missing_summary_count": missing_summary,
        "no_error_codes_count": no_error_codes,
        "no_response_demo_count": no_examples,
        "avg_param_count": avg_params,
        "samples": samples,
    }


def docs_signals(help_links: list[str]) -> dict[str, Any]:
    text = "\n".join(help_links).lower()
    return {
        "overview": any(k in text for k in ["/overview", "api-overview", "概览", "介绍", "introduction"]),
        "quick_start": any(k in text for k in ["quick-start", "快速入门", "快速开始"]),
        "developer_reference": any(k in text for k in ["developer-reference", "api-", "api_", "/api/"]),
        "user_guide": any(k in text for k in ["user-guide", "使用", "指南"]),
        "best_practice": any(k in text for k in ["best-practice", "最佳实践", "use-cases"]),
        "faq_or_troubleshooting": any(k in text for k in ["faq", "troubleshoot", "排查", "常见问题"]),
    }


def build_recommendations(api_stats: dict[str, Any], doc_stats: dict[str, Any]) -> list[dict[str, str]]:
    recs: list[dict[str, str]] = []

    if not doc_stats.get("developer_reference"):
        recs.append(
            {
                "priority": "P0",
                "title": "补齐开发者参考入口",
                "reason": "已发现文档链接中缺少明确 Developer Reference/API 入口，开发者难以从产品文档直达接口说明。",
                "action": "在产品总览页首屏增加“API参考”直达卡片，并在快速开始末尾增加双向跳转。",
            }
        )

    if api_stats["missing_summary_count"] > 0:
        recs.append(
            {
                "priority": "P0",
                "title": "补齐缺失 API 摘要",
                "reason": f"检测到 {api_stats['missing_summary_count']} 个 API 缺少 summary/title，影响接口选择与检索。",
                "action": "为所有缺失摘要的 API 增加一句话“用途 + 适用场景 + 关键限制”。",
            }
        )

    if api_stats["no_error_codes_count"] > 0:
        recs.append(
            {
                "priority": "P1",
                "title": "增强错误码覆盖",
                "reason": f"检测到 {api_stats['no_error_codes_count']} 个 API 缺少错误码说明，故障排查效率低。",
                "action": "为每个 API 至少补充 3 类错误：鉴权、参数校验、配额/资源状态，并给出处理建议。",
            }
        )

    if api_stats["no_response_demo_count"] > 0:
        recs.append(
            {
                "priority": "P1",
                "title": "补充响应示例",
                "reason": f"检测到 {api_stats['no_response_demo_count']} 个 API 缺少 response demo，不利于 SDK 映射和单测构造。",
                "action": "为高频 API 提供最小成功样例 + 边界样例（空列表/分页末页/可选字段缺省）。",
            }
        )

    if not doc_stats.get("quick_start"):
        recs.append(
            {
                "priority": "P1",
                "title": "增加 10 分钟快速开始",
                "reason": "未发现明确的 quick-start 导航，首次接入门槛偏高。",
                "action": "新增“控制台体验 + OpenAPI 调用 + SDK 调用”三段式快速开始。",
            }
        )

    if not doc_stats.get("faq_or_troubleshooting"):
        recs.append(
            {
                "priority": "P2",
                "title": "补充 FAQ/排障章节",
                "reason": "未发现 FAQ/排障入口，用户问题会过度流向工单。",
                "action": "按报错关键词组织 FAQ，并附带排查命令和日志字段。",
            }
        )

    if not recs:
        recs.append(
            {
                "priority": "P2",
                "title": "维持当前质量并做持续巡检",
                "reason": "当前自动扫描未发现显著结构缺失。",
                "action": "建议按月跑一次自动评审，监控 deprecated API 与文档入口可用性。",
            }
        )

    return recs


def score(api_stats: dict[str, Any], doc_stats: dict[str, Any]) -> int:
    s = 100
    s -= min(api_stats["missing_summary_count"], 10) * 3
    s -= min(api_stats["no_error_codes_count"], 10) * 2
    s -= min(api_stats["no_response_demo_count"], 10) * 1
    s -= 8 if not doc_stats.get("quick_start") else 0
    s -= 10 if not doc_stats.get("developer_reference") else 0
    s -= 6 if not doc_stats.get("faq_or_troubleshooting") else 0
    return max(0, s)


def render_markdown(
    query: str,
    match: ProductMatch,
    api_url: str,
    product_page_url: str | None,
    help_links: list[str],
    api_stats: dict[str, Any],
    doc_stats: dict[str, Any],
    recommendations: list[dict[str, str]],
    final_score: int,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

    lines: list[str] = []
    lines.append(f"# {match.name_zh or match.name_en} 文档与 API 自动评审")
    lines.append("")
    lines.append(f"- 评审时间(UTC): {now}")
    lines.append(f"- 输入产品名: `{query}`")
    lines.append(f"- 识别产品: `{match.code}` / `{match.name_zh}` / `{match.name_en}`")
    lines.append(f"- 默认版本: `{match.default_version}`")
    lines.append(f"- API 文档源: {api_url}")
    lines.append(f"- 产品页: {product_page_url or '未识别'}")
    lines.append("")

    lines.append("## 评分")
    lines.append("")
    lines.append(f"- 总分: **{final_score}/100**")
    lines.append("")

    lines.append("## 文档发现结果")
    lines.append("")
    lines.append(f"- 发现帮助文档链接数: {len(help_links)}")
    for link in help_links[:20]:
        lines.append(f"- {link}")
    lines.append("")

    lines.append("## 文档结构信号")
    lines.append("")
    for k, v in doc_stats.items():
        lines.append(f"- {k}: {'yes' if v else 'no'}")
    lines.append("")

    lines.append("## API 统计")
    lines.append("")
    lines.append(f"- API 总数: {api_stats['api_count']}")
    lines.append(f"- Deprecated API 数: {api_stats['deprecated_count']}")
    lines.append(f"- 缺少摘要 API 数: {api_stats['missing_summary_count']}")
    lines.append(f"- 缺少错误码 API 数: {api_stats['no_error_codes_count']}")
    lines.append(f"- 缺少响应示例 API 数: {api_stats['no_response_demo_count']}")
    lines.append(f"- 平均参数数: {api_stats['avg_param_count']}")
    lines.append("")

    lines.append("## 高频 API 样本")
    lines.append("")
    for item in api_stats["samples"]:
        lines.append(
            f"- `{item['api']}` | deprecated={item['deprecated']} | params={item['param_count']} | errors={item['error_code_count']}"
        )
    lines.append("")

    lines.append("## 改进建议（按优先级）")
    lines.append("")
    for rec in recommendations:
        lines.append(f"### {rec['priority']} - {rec['title']}")
        lines.append(f"- 问题依据: {rec['reason']}")
        lines.append(f"- 建议动作: {rec['action']}")
        lines.append("")

    lines.append("## 可执行下一步")
    lines.append("")
    lines.append("1. 先处理所有 P0：保证 API 入口、摘要与关键导航完整。")
    lines.append("2. 再处理 P1：补齐错误码和响应示例，提升接入效率。")
    lines.append("3. 最后处理 P2：完善 FAQ 与最佳实践，降低支持成本。")
    lines.append("")

    return "\n".join(lines)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto-review Alibaba Cloud product docs and API docs")
    parser.add_argument("--product", required=True, help="Product name/code, e.g. ECS/云服务器/OpenSearch")
    parser.add_argument("--output-dir", default=str(OUTPUT_ROOT))
    args = parser.parse_args()

    query = args.product.strip()
    out_root = Path(args.output_dir)

    products_zh, products_en = load_products()
    match = resolve_product(query, products_zh, products_en)

    api_url = (
        f"https://api.aliyun.com/meta/v1/products/{match.code}/"
        f"versions/{match.default_version}/api-docs.json"
    )
    api_docs = fetch_json(api_url)

    product_page = choose_product_page_url(query, match)

    help_links: list[str] = []
    if product_page:
        try:
            product_html = fetch_url(product_page)
            help_links = extract_help_links(product_html)
        except (urllib.error.URLError, urllib.error.HTTPError):
            help_links = []

    help_links = pick_primary_help_links(help_links, match.code)

    api_stats = parse_api_docs(api_docs)
    doc_stats = docs_signals(help_links)
    recommendations = build_recommendations(api_stats, doc_stats)
    final_score = score(api_stats, doc_stats)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    product_dir = out_root / f"{match.code}-{stamp}"
    ensure_dir(product_dir)

    evidence = {
        "query": query,
        "resolved_product": {
            "code": match.code,
            "name_zh": match.name_zh,
            "name_en": match.name_en,
            "short_name": match.short_name,
            "default_version": match.default_version,
            "versions": match.versions,
            "category": match.category,
            "score": match.score,
        },
        "sources": {
            "openapi_products_zh": OPENAPI_PRODUCTS_ZH,
            "openapi_products_en": OPENAPI_PRODUCTS_EN,
            "api_docs": api_url,
            "product_page": product_page,
            "help_links": help_links,
        },
        "doc_signals": doc_stats,
        "api_stats": api_stats,
        "recommendations": recommendations,
        "final_score": final_score,
    }

    json_path = product_dir / "review_evidence.json"
    md_path = product_dir / "review_report.md"

    json_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(
        render_markdown(
            query=query,
            match=match,
            api_url=api_url,
            product_page_url=product_page,
            help_links=help_links,
            api_stats=api_stats,
            doc_stats=doc_stats,
            recommendations=recommendations,
            final_score=final_score,
        ),
        encoding="utf-8",
    )

    print(f"Resolved product: {match.code} ({match.name_zh or match.name_en})")
    print(f"Saved: {json_path}")
    print(f"Saved: {md_path}")


if __name__ == "__main__":
    main()
