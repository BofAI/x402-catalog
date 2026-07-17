from __future__ import annotations

import hashlib
import json
import re
from urllib.parse import urlparse
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROVIDERS_DIR = ROOT / "providers"
DIST_DIR = ROOT / "dist"
CATEGORIES = {
    "ai_ml",
    "cloud",
    "compute",
    "data",
    "devtools",
    "finance",
    "identity",
    "media",
    "messaging",
    "other",
    "productivity",
    "search",
    "security",
    "shopping",
    "storage",
    "translation",
}
X402_SCHEMES = {"exact", "exact_gasfree"}
X402_ASSET_TRANSFER_METHODS = {"permit2"}
TRON_NETWORKS = {"tron:0x2b6653dc", "tron:0xcd8690dc", "tron:0x94a9059e"}
SCHEMA_PATH = ROOT / "schemas" / "catalog.schema.json"
SECRET_KEY_RE = re.compile(
    r"(api[_-]?key|secret|password|passwd|token|authorization|bearer|private[_-]?key|provider\.yml|\.env)",
    re.IGNORECASE,
)
SECRET_VALUE_RE = re.compile(
    r"(sk-[A-Za-z0-9_-]{16,}|Bearer\s+[A-Za-z0-9._-]{12,}|0x[a-fA-F0-9]{64})"
)
PRIVATE_URL_RE = re.compile(
    r"(https?://)?(localhost|127\.0\.0\.1|0\.0\.0\.0|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(1[6-9]|2\d|3[0-1])\.\d+\.\d+)",
    re.IGNORECASE,
)


class CatalogError(ValueError):
    pass


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def json_load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def json_dump(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def provider_dirs() -> list[Path]:
    if not PROVIDERS_DIR.exists():
        return []
    return sorted(path for path in PROVIDERS_DIR.iterdir() if path.is_dir())


def content_sha(payload: dict[str, Any], pay_md: str) -> str:
    normalized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256((normalized + "\n" + pay_md).encode("utf-8")).hexdigest()


def require_string(obj: dict[str, Any], key: str, errors: list[str], *, path: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}.{key} must be a non-empty string")
        return ""
    return value.strip()


def require_number(obj: dict[str, Any], key: str, errors: list[str], *, path: str) -> float:
    value = obj.get(key)
    if not isinstance(value, int | float):
        errors.append(f"{path}.{key} must be a number")
        return 0.0
    return float(value)


def require_bool(obj: dict[str, Any], key: str, errors: list[str], *, path: str) -> bool:
    value = obj.get(key)
    if not isinstance(value, bool):
        errors.append(f"{path}.{key} must be a boolean")
        return False
    return value


def scan_public_payload(value: Any, errors: list[str], *, path: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if SECRET_KEY_RE.search(str(key)):
                errors.append(f"{child_path} looks like a secret field")
            scan_public_payload(child, errors, path=child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_public_payload(child, errors, path=f"{path}[{index}]")
    elif isinstance(value, str):
        if SECRET_VALUE_RE.search(value):
            errors.append(f"{path} looks like it contains a secret value")
        if PRIVATE_URL_RE.search(value):
            errors.append(f"{path} points to a private/local address")


def validate_i18n(obj: dict[str, Any], errors: list[str], *, path: str) -> None:
    i18n = obj.get("i18n")
    if not isinstance(i18n, dict):
        errors.append(f"{path}.i18n must include zh-CN translations")
        return
    zh = i18n.get("zh-CN")
    if not isinstance(zh, dict):
        errors.append(f"{path}.i18n.zh-CN must be an object")
        return
    for key in ("title", "subtitle", "description", "useCase"):
        require_string(zh, key, errors, path=f"{path}.i18n.zh-CN")


def validate_x402_routes(endpoint: dict[str, Any], errors: list[str], *, path: str) -> None:
    routes = endpoint.get("x402Routes")
    if routes is None:
        return
    if not isinstance(routes, list) or not routes:
        errors.append(f"{path}.x402Routes must be a non-empty array when present")
        return
    for index, route in enumerate(routes):
        route_path = f"{path}.x402Routes[{index}]"
        if not isinstance(route, dict):
            errors.append(f"{route_path} must be an object")
            continue
        for key in ("provider", "network", "scheme", "url"):
            require_string(route, key, errors, path=route_path)
        network = str(route.get("network", ""))
        if network.startswith("tron:") and network not in TRON_NETWORKS:
            errors.append(
                f"{route_path}.network must use a canonical TRON CAIP-2 ID: "
                f"{sorted(TRON_NETWORKS)}"
            )
        scheme = route.get("scheme")
        if not isinstance(scheme, str) or scheme not in X402_SCHEMES:
            errors.append(f"{route_path}.scheme must be one of {sorted(X402_SCHEMES)}")
        transfer_method = route.get("assetTransferMethod")
        if scheme == "exact" and (
            not isinstance(transfer_method, str)
            or transfer_method not in X402_ASSET_TRANSFER_METHODS
        ):
            errors.append(
                f"{route_path}.assetTransferMethod must be one of "
                f"{sorted(X402_ASSET_TRANSFER_METHODS)}"
            )
        if scheme == "exact_gasfree":
            if not str(route.get("network", "")).startswith("tron:"):
                errors.append(f"{route_path}.exact_gasfree is supported only on TRON networks")
            if "assetTransferMethod" in route:
                errors.append(f"{route_path}.assetTransferMethod must be omitted for exact_gasfree")
        for legacy_fee_key in ("fee", "feeConfig"):
            if legacy_fee_key in route:
                errors.append(
                    f"{route_path}.{legacy_fee_key} is not supported by x402 SDK 1.0.1"
                )


def validate_schema(payload: dict[str, Any], errors: list[str]) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        errors.append("jsonschema dependency is required; install requirements.txt")
        return
    schema = json_load(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(payload), key=lambda item: list(item.absolute_path)):
        location = "$" + "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}"
            for part in error.absolute_path
        )
        errors.append(f"{location}: {error.message}")


def validate_provider(payload: dict[str, Any], *, provider_dir: Path) -> list[str]:
    errors: list[str] = []
    validate_schema(payload, errors)
    if payload.get("version") != 1:
        errors.append("$.version must be 1")
    fqn = require_string(payload, "fqn", errors, path="$")
    if fqn and provider_dir.name != fqn:
        errors.append(f"directory name {provider_dir.name!r} must match fqn {fqn!r}")
    for key in ("title", "subtitle", "description", "useCase", "logo", "category", "serviceUrl"):
        require_string(payload, key, errors, path="$")
    if payload.get("category") not in CATEGORIES:
        errors.append(f"$.category must be one of {sorted(CATEGORIES)}")
    chains = payload.get("chains")
    if not isinstance(chains, list) or not chains or not all(isinstance(item, str) and item for item in chains):
        errors.append("$.chains must be a non-empty string array")
    elif any(item.startswith("tron:") and item not in TRON_NETWORKS for item in chains):
        errors.append(f"$.chains must use canonical TRON CAIP-2 IDs: {sorted(TRON_NETWORKS)}")
    for key in ("isFirstParty", "isFeatured"):
        require_bool(payload, key, errors, path="$")
    featured_tags = payload.get("featuredTags")
    if not isinstance(featured_tags, list) or not all(isinstance(item, str) for item in featured_tags):
        errors.append("$.featuredTags must be a string array")
    validate_i18n(payload, errors, path="$")

    endpoints = payload.get("endpoints")
    if not isinstance(endpoints, list) or not endpoints:
        errors.append("$.endpoints must be a non-empty array")
    else:
        seen_routes: set[tuple[str, str, str, str]] = set()
        for index, endpoint in enumerate(endpoints):
            if not isinstance(endpoint, dict):
                errors.append(f"$.endpoints[{index}] must be an object")
                continue
            path = f"$.endpoints[{index}]"
            for key in ("method", "path", "url", "title", "subtitle", "description", "useCase"):
                require_string(endpoint, key, errors, path=path)
            method = endpoint.get("method")
            if isinstance(method, str) and method.upper() != method:
                errors.append(f"{path}.method must be uppercase")
            if isinstance(endpoint.get("path"), str) and not endpoint["path"].startswith("/"):
                errors.append(f"{path}.path must start with /")
            require_bool(endpoint, "metered", errors, path=path)
            min_price = require_number(endpoint, "minPriceUsd", errors, path=path)
            max_price = require_number(endpoint, "maxPriceUsd", errors, path=path)
            if max_price < min_price:
                errors.append(f"{path}.maxPriceUsd must be >= minPriceUsd")
            validate_i18n(endpoint, errors, path=path)
            validate_x402_routes(endpoint, errors, path=path)
            for route in endpoint.get("x402Routes", []):
                if not isinstance(route, dict):
                    continue
                network = route.get("network")
                if isinstance(network, str) and isinstance(chains, list) and network not in chains:
                    errors.append(f"{path}.x402Routes network {network!r} is missing from $.chains")
                identity = tuple(str(route.get(key, "")) for key in ("provider", "network", "scheme", "url"))
                if identity in seen_routes:
                    errors.append(f"{path}.x402Routes contains duplicate route {identity!r}")
                seen_routes.add(identity)

    status = payload.get("status")
    if status is not None and not isinstance(status, dict):
        errors.append("$.status must be an object")
    scan_public_payload(payload, errors, path="$")
    pay_md = provider_dir / "pay.md"
    if not pay_md.exists():
        errors.append(f"{pay_md.relative_to(ROOT)} is required")
    else:
        scan_public_payload(pay_md.read_text(encoding="utf-8"), errors, path=str(pay_md.relative_to(ROOT)))
    return errors


def load_validated_providers() -> list[tuple[Path, dict[str, Any], str]]:
    failures: list[str] = []
    providers: list[tuple[Path, dict[str, Any], str]] = []
    for provider_dir in provider_dirs():
        catalog_path = provider_dir / "catalog.json"
        if not catalog_path.exists():
            failures.append(f"{provider_dir.relative_to(ROOT)} missing catalog.json")
            continue
        try:
            payload = json_load(catalog_path)
        except Exception as exc:
            failures.append(f"{catalog_path.relative_to(ROOT)} invalid json: {exc}")
            continue
        try:
            errors = validate_provider(payload, provider_dir=provider_dir)
        except Exception as exc:
            failures.append(f"{catalog_path.relative_to(ROOT)} validation failed: {exc}")
            continue
        if errors:
            failures.extend(f"{catalog_path.relative_to(ROOT)}: {error}" for error in errors)
            continue
        providers.append((provider_dir, payload, (provider_dir / "pay.md").read_text(encoding="utf-8")))
    if failures:
        raise CatalogError("\n".join(failures))
    return providers
