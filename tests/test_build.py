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
