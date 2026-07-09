from __future__ import annotations

import importlib.util
import threading
import unittest
import urllib.error
import urllib.request
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory


def load_serve_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "serve.py"
    spec = importlib.util.spec_from_file_location("catalog_serve", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def serve_directory(directory: Path):
    serve = load_serve_module()
    handler = partial(serve.CatalogHandler, directory=str(directory))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


class CatalogServerTests(unittest.TestCase):
    def test_catalog_server_disables_directory_listing(self) -> None:
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            api_dir = directory / "api"
            api_dir.mkdir()
            (api_dir / "status.json").write_text('{"status":"ok"}', encoding="utf-8")

            server = serve_directory(directory)
            try:
                base_url = f"http://127.0.0.1:{server.server_port}"
                with urllib.request.urlopen(f"{base_url}/api/status.json", timeout=3) as response:
                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
                    self.assertEqual(response.read(), b'{"status":"ok"}')

                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(f"{base_url}/api/", timeout=3)
                self.assertEqual(error.exception.code, 404)
            finally:
                server.shutdown()
                server.server_close()


if __name__ == "__main__":
    unittest.main()
