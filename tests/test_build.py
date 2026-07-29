from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load_build_module():
    sys.path.insert(0, str(SCRIPTS))
    module_path = SCRIPTS / "build.py"
    spec = importlib.util.spec_from_file_location("catalog_build", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_cataloglib_module():
    sys.path.insert(0, str(SCRIPTS))
    module_path = SCRIPTS / "cataloglib.py"
    spec = importlib.util.spec_from_file_location("cataloglib_test", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def route_count(payload: object, key: str) -> int:
    if isinstance(payload, dict):
        total = 0
        for name, value in payload.items():
            if name == key and isinstance(value, list):
                total += len(value)
            else:
                total += route_count(value, key)
        return total
    if isinstance(payload, list):
        return sum(route_count(item, key) for item in payload)
    return 0


class CatalogBuildTests(unittest.TestCase):
    def test_invalid_top_level_catalog_types_are_reported_without_crashing(self) -> None:
        cataloglib = load_cataloglib_module()
        provider_dir = ROOT / "providers" / "defillama"
        for payload in (None, [], "invalid", 42):
            errors = cataloglib.validate_provider(payload, provider_dir=provider_dir)
            self.assertTrue(errors)
            self.assertTrue(any("not of type 'object'" in error for error in errors))

    def test_invalid_x402_routes_containers_are_reported_without_crashing(self) -> None:
        cataloglib = load_cataloglib_module()
        provider_dir = ROOT / "providers" / "defillama"
        source = json.loads((provider_dir / "catalog.json").read_text(encoding="utf-8"))
        for routes in (None, 42, {"provider": "invalid"}):
            payload = json.loads(json.dumps(source))
            payload["endpoints"][0]["x402Routes"] = routes
            errors = cataloglib.validate_provider(payload, provider_dir=provider_dir)
            self.assertTrue(errors)
            self.assertTrue(any("x402Routes" in error for error in errors))

    def test_build_failure_is_clean_and_removes_temporary_directory(self) -> None:
        before = set(ROOT.glob(".dist-*"))
        env = dict(os.environ)
        env["SOURCE_DATE_EPOCH"] = "not-an-integer"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "build.py")],
            cwd=ROOT,
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("SOURCE_DATE_EPOCH must be an integer", result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        self.assertEqual(set(ROOT.glob(".dist-*")), before)

    def test_endpoint_use_cases_cover_all_published_mainnet_routes(self) -> None:
        route_copy_count = 0
        for path in (ROOT / "providers").glob("*/catalog.json"):
            catalog = json.loads(path.read_text(encoding="utf-8"))
            for endpoint in catalog["endpoints"]:
                self.assertNotIn("TRON or BSC", endpoint["useCase"], path.name)
                if "matching TRON" in endpoint["useCase"]:
                    self.assertIn("Base Mainnet", endpoint["useCase"], path.name)
                    route_copy_count += 1
        self.assertEqual(route_copy_count, 17)

    def test_defillama_does_not_claim_unpublished_capabilities(self) -> None:
        provider_dir = ROOT / "providers" / "defillama"
        catalog = json.loads((provider_dir / "catalog.json").read_text(encoding="utf-8"))
        public_copy = json.dumps(catalog, ensure_ascii=False).lower()
        public_copy += (provider_dir / "pay.md").read_text(encoding="utf-8").lower()
        self.assertNotIn("fees", public_copy)
        self.assertNotIn("stablecoin", public_copy)
        self.assertNotIn("费用", public_copy)
        self.assertNotIn("稳定币", public_copy)

    def test_tron_pay_docs_cover_default_and_gasfree_schemes(self) -> None:
        for path in (ROOT / "providers").glob("*/pay.md"):
            content = path.read_text(encoding="utf-8")
            self.assertIn("exact_gasfree", content, path.name)
            self.assertIn("x402-cli pay", content, path.name)
            self.assertIn("--network tron:0x2b6653dc", content, path.name)
            self.assertIn("--scheme exact", content, path.name)

    def test_token_launch_docs_include_complete_payment_examples(self) -> None:
        catalog = json.loads(
            (ROOT / "providers" / "sunpump-token-launch" / "catalog.json").read_text(
                encoding="utf-8"
            )
        )
        descriptions = [catalog["description"], catalog["i18n"]["zh-CN"]["description"]]
        pay_doc = (ROOT / "providers" / "sunpump-token-launch" / "pay.md").read_text(
            encoding="utf-8"
        )

        for content in [*descriptions, pay_doc]:
            self.assertIn("curl -sS -X POST", content)
            self.assertIn("x402-cli pay", content)
            self.assertIn("--body", content)
            self.assertIn("--network tron:0x2b6653dc", content)
            self.assertIn("exact_gasfree", content)
            self.assertIn("--network eip155:56", content)
            self.assertIn("--scheme exact", content)
            self.assertNotIn("--scheme exact_gasfree", content)

    def test_tron_docs_and_routes_default_to_permit2(self) -> None:
        for path in (ROOT / "providers").glob("*/catalog.json"):
            catalog = json.loads(path.read_text(encoding="utf-8"))
            descriptions = [catalog["description"]]
            descriptions.extend(
                locale["description"]
                for locale in catalog.get("i18n", {}).values()
                if "description" in locale
            )
            for description in descriptions:
                self.assertNotIn("--scheme exact_gasfree", description, path.name)

            for endpoint in catalog["endpoints"]:
                tron_routes = [
                    route
                    for route in endpoint.get("x402Routes", [])
                    if route["network"].startswith("tron:")
                ]
                if not tron_routes:
                    continue
                self.assertEqual(tron_routes[0]["scheme"], "exact", path.name)
                self.assertEqual(
                    tron_routes[0].get("assetTransferMethod"), "permit2", path.name
                )

    def test_all_providers_publish_base_mainnet_eip3009_routes(self) -> None:
        route_count = 0
        for path in (ROOT / "providers").glob("*/catalog.json"):
            catalog = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn("eip155:8453", catalog["chains"], path.name)
            self.assertNotIn("eip155:84532", catalog["chains"], path.name)
            for endpoint in catalog["endpoints"]:
                base_routes = [
                    route
                    for route in endpoint.get("x402Routes", [])
                    if route["network"] == "eip155:8453"
                ]
                self.assertEqual(len(base_routes), 1, f"{path.name}: {endpoint['path']}")
                self.assertEqual(base_routes[0]["scheme"], "exact", path.name)
                self.assertEqual(
                    base_routes[0]["assetTransferMethod"], "eip3009", path.name
                )
                self.assertTrue(
                    base_routes[0]["provider"].endswith("-base"), path.name
                )
                self.assertNotIn("sepolia", base_routes[0]["url"].lower(), path.name)
                route_count += 1
        self.assertEqual(route_count, 18)

    def test_all_provider_pay_docs_cover_base_mainnet(self) -> None:
        for path in (ROOT / "providers").glob("*/pay.md"):
            content = path.read_text(encoding="utf-8")
            self.assertIn("Base Mainnet", content, path.name)
            self.assertIn("eip155:8453", content, path.name)
            self.assertIn("-base", content, path.name)
            self.assertIn("USDC", content, path.name)
            self.assertIn("EIP-3009", content, path.name)
            self.assertNotIn("Sepolia", content, path.name)
            self.assertNotIn("eip155:84532", content, path.name)

    def test_gasfree_routes_are_tron_only_and_omit_permit2(self) -> None:
        cataloglib = load_cataloglib_module()
        endpoint = {
            "x402Routes": [{
                "provider": "demo",
                "network": "tron:0xcd8690dc",
                "scheme": "exact_gasfree",
                "url": "https://gateway.example/providers/demo/v1",
            }]
        }
        errors: list[str] = []
        cataloglib.validate_x402_routes(endpoint, errors, path="$.endpoints[0]")
        self.assertEqual(errors, [])

        endpoint["x402Routes"][0]["network"] = "eip155:97"
        endpoint["x402Routes"][0]["assetTransferMethod"] = "permit2"
        errors = []
        cataloglib.validate_x402_routes(endpoint, errors, path="$.endpoints[0]")
        self.assertTrue(any("TRON" in error for error in errors))
        self.assertTrue(any("must be omitted" in error for error in errors))

        endpoint["x402Routes"][0].pop("assetTransferMethod")
        endpoint["x402Routes"][0]["network"] = "tron:0xcd8690dc"
        endpoint["x402Routes"][0]["feeConfig"] = {"feeTo": "legacy"}
        errors = []
        cataloglib.validate_x402_routes(endpoint, errors, path="$.endpoints[0]")
        self.assertTrue(any("x402 SDK 1.0.1" in error for error in errors))

        endpoint["x402Routes"][0].pop("feeConfig")
        endpoint["x402Routes"][0]["network"] = "tron:nile"
        errors = []
        cataloglib.validate_x402_routes(endpoint, errors, path="$.endpoints[0]")
        self.assertTrue(any("canonical TRON CAIP-2" in error for error in errors))

    def test_malformed_route_types_are_reported_without_crashing(self) -> None:
        cataloglib = load_cataloglib_module()
        endpoint = {"x402Routes": [{
            "provider": "demo", "network": "tron:0xcd8690dc",
            "scheme": {}, "assetTransferMethod": [], "url": "https://example.test/v1",
        }]}
        errors: list[str] = []
        cataloglib.validate_x402_routes(endpoint, errors, path="$.endpoints[0]")
        self.assertTrue(any("scheme must be one of" in error for error in errors))

    def test_legacy_fee_fields_and_null_gasfree_transfer_are_rejected(self) -> None:
        cataloglib = load_cataloglib_module()
        for route in (
            {"provider": "demo", "network": "eip155:56", "scheme": "exact", "assetTransferMethod": "permit2", "feeConfig": {}},
            {"provider": "demo", "network": "tron:0xcd8690dc", "scheme": "exact_gasfree", "assetTransferMethod": None},
        ):
            route["url"] = "https://example.test/v1"
            errors: list[str] = []
            cataloglib.validate_x402_routes({"x402Routes": [route]}, errors, path="$.endpoints[0]")
            self.assertTrue(errors)

    def test_search_index_preserves_x402_routes(self) -> None:
        build = load_build_module()
        self.assertEqual(build.main(), 0)

        source_routes = sum(
            route_count(json.loads(path.read_text(encoding="utf-8")), "x402Routes")
            for path in (ROOT / "providers").glob("*/catalog.json")
        )
        provider_routes = sum(
            route_count(json.loads(path.read_text(encoding="utf-8")), "x402_routes")
            for path in (ROOT / "dist" / "providers").glob("*.json")
        )
        pay_routes = sum(
            route_count(json.loads(path.read_text(encoding="utf-8")), "x402_routes")
            for path in (ROOT / "dist" / "pay").glob("*.json")
        )
        search_routes = route_count(
            json.loads((ROOT / "dist" / "search-index.json").read_text(encoding="utf-8")),
            "x402_routes",
        )

        self.assertGreater(source_routes, 0)
        self.assertEqual(provider_routes, source_routes)
        self.assertEqual(pay_routes, source_routes)
        self.assertEqual(search_routes, source_routes)


if __name__ == "__main__":
    unittest.main()
