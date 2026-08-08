import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scraper import write_outputs


class OutputWriterTests(unittest.TestCase):
    def test_write_outputs_populates_public_and_repo_data_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir) / "public"
            data_dir = Path(tmp_dir) / "data"
            items = [
                {
                    "name": "Test product",
                    "old_price": 100.0,
                    "new_price": 50.0,
                    "discount_percent": 50.0,
                    "url": "https://example.com/product",
                }
            ]

            write_outputs(output_dir, data_dir, "demo", items, all_items=items)

            public_payload = json.loads((output_dir / "demo.json").read_text())
            repo_payload = json.loads((data_dir / "demo.json").read_text())
            all_sites_payload = json.loads((data_dir / "all_sites.json").read_text())

            self.assertEqual(public_payload[0]["name"], "Test product")
            self.assertEqual(repo_payload[0]["name"], "Test product")
            self.assertEqual(all_sites_payload["items"][0]["name"], "Test product")


if __name__ == "__main__":
    unittest.main()
