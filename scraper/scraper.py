import argparse
from pathlib import Path
from typing import Any

import requests

from parsers.thebodyshop import parse as parse_thebodyshop
from utils.yaml_loader import load_sites
from utils.json_store import save_json

PARSERS = {
    "thebodyshop": parse_thebodyshop,
}

DEFAULT_OUTPUT_DIR = Path("frontend/sales-frontend/public/data")


def fetch_html(url: str) -> str:
    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0 (compatible; CompanySaleBot/1.0)"},
    )
    response.raise_for_status()
    return response.text


def scrape_site(site: dict, min_discount: int = 50) -> list[dict]:
    parser = PARSERS.get(site["key"])
    if parser is None:
        raise ValueError(f"No parser registered for site key: {site['key']}")

    html = fetch_html(site["url"])
    return parser(html, min_discount=min_discount)


def run(output_dir: Path | str = DEFAULT_OUTPUT_DIR, min_discount: int = 50) -> list[dict]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    sites = load_sites("config/sites.yaml")
    all_items: list[dict] = []

    for site in sites:
        items = scrape_site(site, min_discount=min_discount)
        save_json(output_dir / f"{site['key']}.json", items)
        all_items.extend(items)

    save_json(output_dir / "sale_data.json", {"items": all_items})
    return all_items


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape sale items and export JSON for the dashboard.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where scraped JSON data will be written.",
    )
    parser.add_argument(
        "--min-discount",
        type=int,
        default=50,
        help="Minimum discount percent to include.",
    )
    args = parser.parse_args()

    items = run(output_dir=args.output_dir, min_discount=args.min_discount)
    print(f"Scraped {len(items)} sale items and wrote JSON to {args.output_dir}")
