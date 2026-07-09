#!/usr/bin/env python3
from __future__ import annotations

import shutil
from typing import Any

from cataloglib import (
    CATEGORIES,
    DIST_DIR,
    CatalogError,
    content_sha,
    json_dump,
    load_validated_providers,
    now_iso,
)

CATEGORY_META = {
    "ai_ml": {"label": "AI/ML", "label_zh": "AI / 机器学习"},
    "cloud": {"label": "Cloud", "label_zh": "云服务"},
    "compute": {"label": "Compute", "label_zh": "计算"},
    "data": {"label": "Data", "label_zh": "数据"},
    "devtools": {"label": "DevTools", "label_zh": "开发工具"},
    "finance": {"label": "Finance", "label_zh": "金融"},
    "identity": {"label": "Identity", "label_zh": "身份"},
    "media": {"label": "Media", "label_zh": "媒体"},
    "messaging": {"label": "Messaging", "label_zh": "消息"},
    "other": {"label": "Other", "label_zh": "其他"},
    "productivity": {"label": "Productivity", "label_zh": "效率"},
    "search": {"label": "Search", "label_zh": "搜索"},
    "security": {"label": "Security", "label_zh": "安全"},
    "shopping": {"label": "Shopping", "label_zh": "购物"},
    "storage": {"label": "Storage", "label_zh": "存储"},
    "translation": {"label": "Translation", "label_zh": "翻译"},
}

CHAIN_META = {
    "eip155:56": {"kind": "bnb", "label": "BNB Chain", "label_zh": "BNB Chain"},
    "eip155:97": {
        "kind": "bnb",
        "label": "BNB Smart Chain Testnet",
        "label_zh": "BNB 测试网",
    },
    "tron:mainnet": {"kind": "tron", "label": "TRON Mainnet", "label_zh": "TRON 主网"},
    "tron:nile": {"kind": "tron", "label": "TRON Nile Testnet", "label_zh": "TRON Nile 测试网"},
    "tron:shasta": {
        "kind": "tron",
        "label": "TRON Shasta Testnet",
        "label_zh": "TRON Shasta 测试网",
    },
}


def category_meta(category: str) -> dict[str, Any]:
    meta = CATEGORY_META.get(category, {"label": category, "label_zh": category})
    return {"id": category, **meta}


def chain_meta(chain: str) -> dict[str, Any]:
    meta = CHAIN_META.get(chain)
    if meta:
        return {"id": chain, **meta}
    if chain.startswith("eip155:"):
        return {"id": chain, "kind": "evm", "label": chain, "label_zh": chain}
    if chain.startswith("tron:"):
        return {"id": chain, "kind": "tron", "label": chain, "label_zh": chain}
    return {"id": chain, "kind": "other", "label": chain, "label_zh": chain}


def zh_copy(payload: dict[str, Any]) -> dict[str, Any]:
    i18n = payload.get("i18n")
    if not isinstance(i18n, dict):
        return {}
    zh = i18n.get("zh-CN")
    return zh if isinstance(zh, dict) else {}


def snake_provider(payload: dict[str, Any], sha: str) -> dict[str, Any]:
    endpoints = payload["endpoints"]
    prices = [endpoint["minPriceUsd"] for endpoint in endpoints] + [
        endpoint["maxPriceUsd"] for endpoint in endpoints
    ]
    zh = zh_copy(payload)
    chains = payload["chains"]
    return {
        "fqn": payload["fqn"],
        "title": payload["title"],
        "title_zh": zh.get("title") or payload["title"],
        "main_title_zh": zh.get("mainTitle") or (payload.get("mainTitle") or payload["title"]),
        "sub_title_zh": zh.get("subtitle") or (payload.get("subTitle") or payload["subtitle"]),
        "main_title": payload.get("mainTitle") or payload["title"],
        "sub_title": payload.get("subTitle") or payload["subtitle"],
        "subtitle": payload["subtitle"],
        "description": payload["description"],
        "use_case": payload["useCase"],
        "i18n": payload["i18n"],
        "logo": payload["logo"],
        "category": payload["category"],
        "category_meta": category_meta(payload["category"]),
        "chains": chains,
        "chain_kinds": sorted({chain_meta(chain)["kind"] for chain in chains}),
        "chains_meta": [chain_meta(chain) for chain in chains],
        "is_first_party": payload["isFirstParty"],
        "is_featured": payload["isFeatured"],
        "featured_tags": payload["featuredTags"],
        "service_url": payload["serviceUrl"],
        "endpoint_count": len(endpoints),
        "has_metering": any(endpoint["metered"] for endpoint in endpoints),
        "has_free_tier": any(endpoint["minPriceUsd"] == 0 for endpoint in endpoints),
        "min_price_usd": min(prices),
        "max_price_usd": max(prices),
        "sha": sha,
    }


def detail_provider(payload: dict[str, Any], sha: str) -> dict[str, Any]:
    detail = snake_provider(payload, sha)
    detail["endpoints"] = [
        {
            "method": endpoint["method"],
            "path": endpoint["path"],
            "url": endpoint["url"],
            "title": endpoint["title"],
            "subtitle": endpoint["subtitle"],
            "description": endpoint["description"],
            "use_case": endpoint["useCase"],
            "i18n": endpoint["i18n"],
            "metered": endpoint["metered"],
            "min_price_usd": endpoint["minPriceUsd"],
            "max_price_usd": endpoint["maxPriceUsd"],
            **({"x402_routes": endpoint["x402Routes"]} if "x402Routes" in endpoint else {}),
        }
        for endpoint in payload["endpoints"]
    ]
    detail["status"] = payload.get(
        "status",
        {
            "catalog": "listed",
            "gateway": "unknown",
            "payment": "unknown",
            "upstream": "unknown",
        },
    )
    return detail


def pay_json(payload: dict[str, Any], sha: str) -> dict[str, Any]:
    zh = zh_copy(payload)
    chains = payload["chains"]
    return {
        "version": 1,
        "fqn": payload["fqn"],
        "title": payload["title"],
        "title_zh": zh.get("title") or payload["title"],
        "main_title_zh": zh.get("mainTitle") or (payload.get("mainTitle") or payload["title"]),
        "sub_title_zh": zh.get("subtitle") or (payload.get("subTitle") or payload["subtitle"]),
        "main_title": payload.get("mainTitle") or payload["title"],
        "sub_title": payload.get("subTitle") or payload["subtitle"],
        "subtitle": payload["subtitle"],
        "description": payload["description"],
        "use_case": payload["useCase"],
        "i18n": payload["i18n"],
        "service_url": payload["serviceUrl"],
        "chains": chains,
        "chain_kinds": sorted({chain_meta(chain)["kind"] for chain in chains}),
        "chains_meta": [chain_meta(chain) for chain in chains],
        "sha": sha,
        "endpoints": [
            {
                "method": endpoint["method"],
                "path": endpoint["path"],
                "url": endpoint["url"],
                "description": endpoint["description"],
                "metered": endpoint["metered"],
                "min_price_usd": endpoint["minPriceUsd"],
                "max_price_usd": endpoint["maxPriceUsd"],
                **({"x402_routes": endpoint["x402Routes"]} if "x402Routes" in endpoint else {}),
            }
            for endpoint in payload["endpoints"]
        ],
    }


def search_doc(summary: dict[str, Any], detail: dict[str, Any]) -> dict[str, Any]:
    return {
        "fqn": summary["fqn"],
        "title": summary["title"],
        "subtitle": summary["subtitle"],
        "description": summary["description"],
        "use_case": summary["use_case"],
        "category": summary["category"],
        "category_meta": summary["category_meta"],
        "chains": summary["chains"],
        "chain_kinds": summary["chain_kinds"],
        "chains_meta": summary["chains_meta"],
        "featured_tags": summary["featured_tags"],
        "service_url": summary["service_url"],
        "endpoints": [
            {
                "method": endpoint["method"],
                "path": endpoint["path"],
                "title": endpoint["title"],
                "description": endpoint["description"],
                **({"x402_routes": endpoint["x402Routes"]} if "x402Routes" in endpoint else {}),
            }
            for endpoint in detail["endpoints"]
        ],
    }


def main() -> int:
    try:
        providers = load_validated_providers()
    except CatalogError as exc:
        print(str(exc))
        return 1

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    generated_at = now_iso()
    summaries: list[dict[str, Any]] = []
    details: list[dict[str, Any]] = []
    search_docs: list[dict[str, Any]] = []
    used_categories: dict[str, int] = {}
    used_chains: dict[str, int] = {}

    for provider_dir, payload, pay_md in providers:
        sha = content_sha(payload, pay_md)
        summary = snake_provider(payload, sha)
        detail = detail_provider(payload, sha)
        summaries.append(summary)
        details.append(detail)
        search_docs.append(search_doc(summary, detail))
        used_categories[summary["category"]] = used_categories.get(summary["category"], 0) + 1
        for chain in summary["chains"]:
            used_chains[chain] = used_chains.get(chain, 0) + 1

        fqn = summary["fqn"]
        json_dump(DIST_DIR / "providers" / f"{fqn}.json", detail)
        json_dump(DIST_DIR / "pay" / f"{fqn}.json", pay_json(payload, sha))
        (DIST_DIR / "pay").mkdir(parents=True, exist_ok=True)
        (DIST_DIR / "pay" / f"{fqn}.md").write_text(pay_md, encoding="utf-8")

    summaries.sort(key=lambda item: (not item["is_featured"], item["category"], item["fqn"]))
    base_url = "https://x402-catalog.bankofai.io/api"
    catalog = {
        "version": 1,
        "generated_at": generated_at,
        "provider_count": len(summaries),
        "first_party_count": sum(1 for provider in summaries if provider["is_first_party"]),
        "chain_count": len(used_chains),
        "base_url": base_url,
        "frontend": {
            "featured_fqns": [provider["fqn"] for provider in summaries if provider["is_featured"]],
            "categories": [
                {**category_meta(category), "count": used_categories.get(category, 0)}
                for category in sorted(CATEGORIES)
                if used_categories.get(category, 0)
            ],
            "chains": [
                {**chain_meta(chain), "count": count}
                for chain, count in sorted(used_chains.items())
            ],
        },
        "providers": summaries,
    }
    json_dump(DIST_DIR / "catalog.json", catalog)
    json_dump(DIST_DIR / "categories.json", catalog["frontend"]["categories"])
    json_dump(DIST_DIR / "search-index.json", {"version": 1, "generated_at": generated_at, "documents": search_docs})
    json_dump(
        DIST_DIR / "status.json",
        {
            "version": 1,
            "generated_at": generated_at,
            "provider_count": len(summaries),
            "status": "ok",
        },
    )
    print(f"built {len(summaries)} provider(s) into {DIST_DIR.relative_to(DIST_DIR.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
