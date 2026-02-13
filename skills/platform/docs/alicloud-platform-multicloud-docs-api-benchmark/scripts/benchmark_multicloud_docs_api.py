#!/usr/bin/env python3
"""Benchmark product docs/API docs across major cloud vendors.

Supported vendors:
- Alibaba Cloud
- AWS
- Azure
- GCP
- Tencent Cloud
- Volcano Engine
- Huawei Cloud

Given a product keyword, this script:
1) Discovers candidate official docs links per vendor (or uses user-provided links)
2) Scores docs/API quality signals with a unified rubric
3) Adds Alibaba Cloud OpenAPI metadata signals when resolvable
4) Outputs a benchmark report and JSON evidence
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OUTPUT_ROOT = Path("output/alicloud-platform-multicloud-docs-api-benchmark")
PRESETS_PATH = Path(
    "skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/references/presets.json"
)
SCORING_PATH = Path(
    "skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/references/scoring.json"
)
GCP_DISCOVERY_APIS = "https://discovery.googleapis.com/discovery/v1/apis"
GITHUB_API_SEARCH_CODE = "https://api.github.com/search/code?q="

DEFAULT_SCORING_PROFILE = {
    "link_cap": 8,
    "link_weight": 2,
    "signal_weights": {
        "overview": 12,
        "quick_start": 15,
        "developer_reference": 20,
        "faq_or_troubleshooting": 12,
        "best_practice": 12,
        "changelog": 8,
    },
    "api_bonus": 5,
}


@dataclass(frozen=True)
class Provider:
    key: str
    name: str
    domains: tuple[str, ...]


PROVIDERS = [
    Provider("alicloud", "Alibaba Cloud", ("help.aliyun.com", "aliyun.com", "api.aliyun.com")),
    Provider("aws", "AWS", ("docs.aws.amazon.com", "aws.amazon.com")),
    Provider("azure", "Azure", ("learn.microsoft.com", "azure.microsoft.com")),
    Provider("gcp", "GCP", ("cloud.google.com",)),
    Provider("tencent", "Tencent Cloud", ("cloud.tencent.com", "intl.cloud.tencent.com")),
    Provider("volcengine", "Volcano Engine", ("volcengine.com", "developer.volcengine.com")),
    Provider("huawei", "Huawei Cloud", ("support.huaweicloud.com", "huaweicloud.com")),
]


def fetch_text(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Codex MultiCloud Benchmark)",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def fetch_json(url: str, timeout: int = 20) -> Any:
    return json.loads(fetch_text(url, timeout=timeout))


def fetch_json_with_headers(url: str, headers: dict[str, str], timeout: int = 20) -> Any:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="ignore"))


def load_presets(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def load_scoring_profiles(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"default": DEFAULT_SCORING_PROFILE}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"default": DEFAULT_SCORING_PROFILE}
    profiles = data.get("profiles") if isinstance(data, dict) else None
    if not isinstance(profiles, dict) or not profiles:
        return {"default": DEFAULT_SCORING_PROFILE}
    if "default" not in profiles:
        profiles["default"] = DEFAULT_SCORING_PROFILE
    return profiles


def normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", (s or "").lower())


def domain_allowed(url: str, domains: tuple[str, ...]) -> bool:
    low = url.lower()
    return any(d in low for d in domains)


def discover_with_duckduckgo(provider: Provider, product: str, limit: int) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    queries = [
        f"site:{provider.domains[0]} {product} api reference",
        f"site:{provider.domains[0]} {product} quick start",
        f"site:{provider.domains[0]} {product} overview",
    ]

    for q in queries:
        if len(out) >= limit:
            break
        url = "https://duckduckgo.com/html/?q=" + urllib.parse.quote(q)
        try:
            html = fetch_text(url, timeout=20)
        except Exception:
            continue

        # DuckDuckGo result links
        for link in re.findall(r'class="result__a"[^>]*href="([^"]+)"', html):
            real = urllib.parse.unquote(link)
            # DDG wraps target in uddg=...
            m = re.search(r"[?&]uddg=([^&]+)", real)
            if m:
                real = urllib.parse.unquote(m.group(1))
            if not real.startswith("http"):
                continue
            if not domain_allowed(real, provider.domains):
                continue
            if real in seen:
                continue
            seen.add(real)
            out.append(real)
            if len(out) >= limit:
                break

    return out


def _dedupe_keep_order(links: list[str], domains: tuple[str, ...], limit: int) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for raw in links:
        u = raw.strip()
        if not u or not u.startswith("http"):
            continue
        if not domain_allowed(u, domains):
            continue
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
        if len(out) >= limit:
            break
    return out


def discover_gcp_discovery(product: str, limit: int) -> list[str]:
    qn = normalize(product)
    try:
        payload = fetch_json(GCP_DISCOVERY_APIS)
    except Exception:
        return []
    items = payload.get("items") if isinstance(payload, dict) else None
    if not isinstance(items, list):
        return []
    out: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "")
        title = str(item.get("title") or "")
        desc = str(item.get("description") or "")
        merged = normalize(name + " " + title + " " + desc)
        if qn and qn not in merged:
            continue
        doc = item.get("documentationLink")
        disc = item.get("discoveryRestUrl")
        if isinstance(doc, str):
            out.append(doc)
        if isinstance(disc, str):
            out.append(disc)
        if len(out) >= limit:
            break
    return _dedupe_keep_order(out, ("cloud.google.com", "googleapis.com"), limit)


def discover_github_code_search(product: str, repo: str, path_hint: str, limit: int) -> list[str]:
    q = f"{product} repo:{repo} path:{path_hint}"
    url = GITHUB_API_SEARCH_CODE + urllib.parse.quote(q)
    headers = {
        "User-Agent": "Codex MultiCloud Benchmark",
        "Accept": "application/vnd.github+json",
    }
    try:
        payload = fetch_json_with_headers(url, headers=headers, timeout=25)
    except Exception:
        return []
    items = payload.get("items") if isinstance(payload, dict) else None
    if not isinstance(items, list):
        return []
    out: list[str] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        html_url = it.get("html_url")
        if isinstance(html_url, str):
            out.append(html_url)
        if len(out) >= limit:
            break
    return out


def discover_provider_links(provider: Provider, product: str, limit: int) -> tuple[list[str], str, str, list[str]]:
    notes: list[str] = []
    # source_tier: L0 manual pinned (set in caller), L1 machine-readable API/repo, L2 official-domain search fallback, L3 none
    if provider.key == "gcp":
        links = discover_gcp_discovery(product, limit=limit)
        if links:
            return links, "L1", "high", notes
        notes.append("GCP discovery API did not return matched items; fell back to search.")
    elif provider.key == "aws":
        links = discover_github_code_search(product, "aws/api-models-aws", "model", limit=limit)
        links = _dedupe_keep_order(links, provider.domains + ("github.com",), limit)
        if links:
            return links, "L1", "high", notes
        notes.append("AWS API models code search unavailable or no match; fell back to search.")
    elif provider.key == "azure":
        links = discover_github_code_search(product, "Azure/azure-rest-api-specs", "specification", limit=limit)
        links = _dedupe_keep_order(links, provider.domains + ("github.com",), limit)
        if links:
            return links, "L1", "high", notes
        notes.append("Azure REST specs code search unavailable or no match; fell back to search.")

    links = discover_with_duckduckgo(provider, product, limit=limit)
    if links:
        confidence = "medium" if len(links) >= 3 else "low"
        return links, "L2", confidence, notes
    return [], "L3", "low", notes


def auto_pick_preset(product: str, presets: dict[str, Any]) -> str | None:
    pn = normalize(product)
    if not pn:
        return None
    for preset_name, conf in presets.items():
        if not isinstance(conf, dict):
            continue
        kws = conf.get("trigger_keywords") or []
        if not isinstance(kws, list):
            continue
        for kw in kws:
            if not isinstance(kw, str):
                continue
            if normalize(kw) and normalize(kw) in pn:
                return preset_name
    return None


def merge_seed_links(seed_links: list[str], discovered: list[str], domains: tuple[str, ...], limit: int) -> list[str]:
    return _dedupe_keep_order(seed_links + discovered, domains + ("github.com",), limit)


def classify_links(links: list[str], max_fetch: int = 3) -> dict[str, bool]:
    chunks = ["\n".join(links).lower()]
    for url in links[:max_fetch]:
        try:
            html = fetch_text(url, timeout=12).lower()
        except Exception:
            continue
        # Keep only lightweight textual signals to avoid large memory
        title = re.findall(r"<title[^>]*>(.*?)</title>", html, flags=re.S)
        h_tags = re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", html, flags=re.S)
        raw = " ".join(title + h_tags)
        raw = re.sub(r"<[^>]+>", " ", raw)
        raw = re.sub(r"\s+", " ", raw)
        if raw:
            chunks.append(raw)
    text = "\n".join(chunks)
    return {
        "overview": any(k in text for k in ["overview", "introduction", "概览", "介绍"]),
        "quick_start": any(k in text for k in ["quickstart", "quick-start", "快速入门", "入门"]),
        "developer_reference": any(k in text for k in ["developer-reference", "api", "reference", "sdk"]),
        "faq_or_troubleshooting": any(k in text for k in ["faq", "troubleshoot", "排查", "常见问题"]),
        "best_practice": any(k in text for k in ["best-practice", "best practices", "最佳实践", "use-cases"]),
        "changelog": any(k in text for k in ["release", "changelog", "whats-new", "更新"]),
    }


def alicloud_openapi_signals(product: str) -> dict[str, Any]:
    try:
        zh = fetch_json("https://api.aliyun.com/meta/v1/products.json?language=ZH_CN")
        en = fetch_json("https://api.aliyun.com/meta/v1/products.json?language=EN_US")
    except Exception:
        return {"resolved": False}

    if not isinstance(zh, list) or not isinstance(en, list):
        return {"resolved": False}

    by_code_en = {p.get("code"): p for p in en if isinstance(p, dict) and p.get("code")}
    qn = normalize(product)
    best: dict[str, Any] | None = None
    best_score = -1

    for p in zh:
        if not isinstance(p, dict):
            continue
        code = str(p.get("code") or "")
        if not code:
            continue
        pen = by_code_en.get(code, {})
        cands = [code, p.get("name") or "", p.get("shortName") or "", pen.get("name") or ""]
        score = 0
        for c in cands:
            cn = normalize(str(c))
            if qn and qn == cn:
                score += 100
            elif qn and qn in cn:
                score += 40
        if score > best_score:
            best_score = score
            best = {
                "code": code,
                "defaultVersion": p.get("defaultVersion") or pen.get("defaultVersion"),
                "name_zh": p.get("name"),
                "name_en": pen.get("name"),
            }

    if not best or best_score <= 0:
        return {"resolved": False}

    code = best["code"]
    version = best.get("defaultVersion")
    if not version:
        return {"resolved": True, "product": best, "api_count": None}

    api_url = f"https://api.aliyun.com/meta/v1/products/{code}/versions/{version}/api-docs.json"
    try:
        docs = fetch_json(api_url)
        apis = docs.get("apis") if isinstance(docs, dict) else None
        if isinstance(apis, dict):
            api_count = len(apis)
            deprecated = sum(1 for x in apis.values() if isinstance(x, dict) and x.get("deprecated") is True)
        elif isinstance(apis, list):
            api_count = len(apis)
            deprecated = sum(1 for x in apis if isinstance(x, dict) and x.get("deprecated") is True)
        else:
            api_count = 0
            deprecated = 0
        return {
            "resolved": True,
            "product": best,
            "api_url": api_url,
            "api_count": api_count,
            "deprecated_count": deprecated,
        }
    except Exception:
        return {"resolved": True, "product": best, "api_url": api_url, "api_count": None}


def score_provider(
    link_count: int,
    signals: dict[str, bool],
    scoring: dict[str, Any],
    api_bonus: int = 0,
) -> int:
    link_cap = int(scoring.get("link_cap", 8))
    link_weight = int(scoring.get("link_weight", 2))
    signal_weights = scoring.get("signal_weights") or {}
    if not isinstance(signal_weights, dict):
        signal_weights = {}

    s = 0
    s += min(link_count, link_cap) * link_weight
    for key in [
        "overview",
        "quick_start",
        "developer_reference",
        "faq_or_troubleshooting",
        "best_practice",
        "changelog",
    ]:
        if signals.get(key):
            s += int(signal_weights.get(key, 0))
    s += api_bonus
    return min(100, s)


def build_actions(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    if not rows:
        return []
    best = max(rows, key=lambda x: x["score"])
    actions: list[dict[str, str]] = []
    for r in rows:
        if r["provider"] == best["provider"]:
            continue
        gap = best["score"] - r["score"]
        if gap <= 0:
            continue

        missing = []
        for k in ["quick_start", "developer_reference", "faq_or_troubleshooting", "best_practice", "changelog"]:
            if not r["signals"].get(k):
                missing.append(k)

        priority = "P2"
        if gap >= 25:
            priority = "P0"
        elif gap >= 12:
            priority = "P1"

        actions.append(
            {
                "priority": priority,
                "target": r["provider"],
                "title": f"Close {gap}-point gap vs {best['provider']}",
                "action": "Add or strengthen: " + (", ".join(missing[:4]) if missing else "navigation consistency and examples"),
            }
        )
    return actions


def render_report(
    product: str,
    rows: list[dict[str, Any]],
    actions: list[dict[str, str]],
    out_json: Path,
    active_preset: str | None,
    scoring_profile: str,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    lines = [
        f"# Multi-Cloud Docs/API Benchmark: {product}",
        "",
        f"- Generated(UTC): {now}",
        f"- Providers: {', '.join(r['provider'] for r in rows)}",
        f"- Active preset: {active_preset or 'none'}",
        f"- Scoring profile: {scoring_profile}",
        f"- Evidence JSON: `{out_json}`",
        "",
        "## Scoreboard",
        "",
        "| Provider | Score | Source Tier | Confidence | Links | Overview | Quick Start | Dev Ref/API | FAQ/Troubleshoot | Best Practice | Changelog |",
        "| --- | ---: | --- | --- | ---: | --- | --- | --- | --- | --- | --- |",
    ]

    for r in sorted(rows, key=lambda x: x["score"], reverse=True):
        sg = r["signals"]
        lines.append(
            f"| {r['provider']} | {r['score']} | {r['source_tier']} | {r['confidence']} | {len(r['links'])} | "
            f"{'Y' if sg['overview'] else 'N'} | {'Y' if sg['quick_start'] else 'N'} | "
            f"{'Y' if sg['developer_reference'] else 'N'} | {'Y' if sg['faq_or_troubleshooting'] else 'N'} | "
            f"{'Y' if sg['best_practice'] else 'N'} | {'Y' if sg['changelog'] else 'N'} |"
        )

    lines += ["", "## Top Links", ""]
    for r in rows:
        lines.append(f"### {r['provider']}")
        if r.get("query"):
            lines.append(f"- Query: {r['query']}")
        for n in r.get("notes", []):
            lines.append(f"- Note: {n}")
        for u in r["links"][:8]:
            lines.append(f"- {u}")
        lines.append("")

    lines += ["## Recommended Improvements", ""]
    if not actions:
        lines.append("- No major gap found in current auto-discovered signals.")
    else:
        for a in actions:
            lines.append(f"- {a['priority']} | {a['target']} | {a['title']} | {a['action']}")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark docs/API docs across major cloud providers")
    parser.add_argument("--product", required=True, help="Product keyword, e.g. ECS, object storage, serverless")
    parser.add_argument(
        "--preset",
        default="",
        help="Optional preset name (see references/presets.json), e.g. llm-platform",
    )
    parser.add_argument("--max-links", type=int, default=8)
    parser.add_argument("--scoring-profile", default="default", help="Scoring profile name from references/scoring.json")
    parser.add_argument("--output-dir", default=str(OUTPUT_ROOT))
    # Optional manual links override: comma-separated URLs
    for p in PROVIDERS:
        parser.add_argument(f"--{p.key}-links", default="")
    args = parser.parse_args()

    product = args.product.strip()
    presets = load_presets(PRESETS_PATH)
    scoring_profiles = load_scoring_profiles(SCORING_PATH)
    scoring_profile = args.scoring_profile.strip() or "default"
    scoring = scoring_profiles.get(scoring_profile)
    if not isinstance(scoring, dict):
        scoring_profile = "default"
        scoring = scoring_profiles.get("default", DEFAULT_SCORING_PROFILE)
    active_preset = args.preset.strip()
    if not active_preset:
        guessed = auto_pick_preset(product, presets)
        if guessed:
            active_preset = guessed

    preset_conf = presets.get(active_preset, {}) if active_preset else {}
    if not isinstance(preset_conf, dict):
        preset_conf = {}
    provider_query_map = preset_conf.get("provider_query_map") or {}
    provider_seed_links = preset_conf.get("provider_seed_links") or {}
    if not isinstance(provider_query_map, dict):
        provider_query_map = {}
    if not isinstance(provider_seed_links, dict):
        provider_seed_links = {}

    out_root = Path(args.output_dir)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = out_root / f"benchmark-{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []

    for p in PROVIDERS:
        provider_query = str(provider_query_map.get(p.key) or product)
        preset_seeds_raw = provider_seed_links.get(p.key) or []
        if not isinstance(preset_seeds_raw, list):
            preset_seeds_raw = []
        preset_seeds = [str(x) for x in preset_seeds_raw if isinstance(x, str)]
        preset_seeds = [u for u in preset_seeds if domain_allowed(u, p.domains) or "github.com" in u.lower()]

        manual = getattr(args, f"{p.key}_links", "").strip()
        if manual:
            links = [x.strip() for x in manual.split(",") if x.strip()]
            links = [u for u in links if domain_allowed(u, p.domains)]
            source_tier = "L0"
            confidence = "high" if links else "low"
            notes = ["Using user-pinned official links."]
        else:
            links, source_tier, confidence, notes = discover_provider_links(p, provider_query, limit=args.max_links)
            if preset_seeds:
                links = merge_seed_links(preset_seeds, links, p.domains, args.max_links)
                if source_tier in {"L2", "L3"}:
                    source_tier = "L2"
                    confidence = "medium" if links else confidence
                notes.append(f"Preset seeds applied ({len(preset_seeds)}).")
            if provider_query != product:
                notes.append(f"Provider query override: {provider_query}")

        signals = classify_links(links)
        api_bonus = 0
        ext: dict[str, Any] = {}
        if p.key == "alicloud":
            ali = alicloud_openapi_signals(product)
            ext["alicloud_openapi"] = ali
            if not links and isinstance(ali, dict):
                api_url = ali.get("api_url")
                if isinstance(api_url, str) and api_url.startswith("http"):
                    links = [api_url]
                    source_tier = "L1"
                    confidence = "high"
                    notes = ["Recovered from Alibaba Cloud OpenAPI metadata endpoint."]
            if ali.get("api_count") is not None:
                api_bonus = int(scoring.get("api_bonus", 5))

        score = score_provider(len(links), signals, scoring, api_bonus=api_bonus)
        rows.append(
            {
                "provider": p.name,
                "provider_key": p.key,
                "domains": p.domains,
                "query": provider_query,
                "links": links,
                "source_tier": source_tier,
                "confidence": confidence,
                "notes": notes,
                "signals": signals,
                "score": score,
                "extra": ext,
            }
        )

    actions = build_actions(rows)

    evidence = {
        "product": product,
        "active_preset": active_preset or None,
        "scoring_profile": scoring_profile,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "providers": rows,
        "actions": actions,
        "notes": [
            "Auto-discovery uses official-domain-constrained search and may miss private or localized pages.",
            "Use --<provider>-links to pin authoritative pages for stricter comparison.",
        ],
    }

    json_path = out_dir / "benchmark_evidence.json"
    md_path = out_dir / "benchmark_report.md"
    json_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(
        render_report(
            product,
            rows,
            actions,
            json_path,
            active_preset if active_preset else None,
            scoring_profile,
        ),
        encoding="utf-8",
    )

    print(f"Saved: {json_path}")
    print(f"Saved: {md_path}")


if __name__ == "__main__":
    main()
