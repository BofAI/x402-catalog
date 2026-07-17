from __future__ import annotations

import importlib.util
import json
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
        self.assertTrue(any("1.0.1-beta.4" in error for error in errors))

        endpoint["x402Routes"][0].pop("feeConfig")
        endpoint["x402Routes"][0]["network"] = "tron:nile"
        errors = []
        cataloglib.validate_x402_routes(endpoint, errors, path="$.endpoints[0]")
        self.assertTrue(any("canonical TRON CAIP-2" in error for error in errors))

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
