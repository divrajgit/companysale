import argparse
from pathlib import Path
from typing import Any

import requests

from parsers.thebodyshop import parse as parse_thebodyshop
from parsers.supercheapauto import parse as parse_supercheapauto
from parsers.woolworths import parse as parse_woolworths
from parsers.automotivesuperstore import parse as parse_automotivesuperstore
from parsers.coles import parse as parse_coles
from utils.yaml_loader import load_sites
from utils.json_store import save_json

PARSERS = {
    "thebodyshop": parse_thebodyshop,
    "supercheapauto": parse_supercheapauto,
    "woolworths": parse_woolworths,
    "automotivesuperstore": parse_automotivesuperstore,
    "coles": parse_coles,
}

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "frontend" / "sales-frontend" / "public" / "data"
DEFAULT_DATA_DIR = REPO_ROOT / "data"


def fetch_html(url: str) -> str:
    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0 (compatible; CompanySaleBot/1.0)"},
    )
    response.raise_for_status()
    return response.text


def scrape_site(site: dict, min_discount: int = 30) -> list[dict]:
    parser = PARSERS.get(site["key"])
    if parser is None:
        raise ValueError(f"No parser registered for site key: {site['key']}")

    html = fetch_html(site["url"])
    items = parser(html, min_discount=min_discount, site_url=site["url"])
    for item in items:
        item["site_name"] = site["name"]
        item["site_key"] = site["key"]
    return items


def write_site_outputs(output_dir: Path | str, data_dir: Path | str, site_key: str, items: list[dict]) -> None:
    output_dir = Path(output_dir)
    data_dir = Path(data_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    save_json(output_dir / f"{site_key}.json", items)
    save_json(data_dir / f"{site_key}.json", items)


def write_all_sites_output(output_dir: Path | str, data_dir: Path | str, all_items: list[dict]) -> None:
    output_dir = Path(output_dir)
    data_dir = Path(data_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    save_json(output_dir / "sale_data.json", {"items": all_items})
    save_json(data_dir / "all_sites.json", {"items": all_items})


def run(
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
    min_discount: int = 30,
    data_dir: Path | str = DEFAULT_DATA_DIR,
) -> list[dict]:
    output_dir = Path(output_dir)
    data_dir = Path(data_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    sites = load_sites(str(REPO_ROOT / "config" / "sites.yaml"))
    all_items: list[dict] = []

    for site in sites:
        items = scrape_site(site, min_discount=min_discount)
        write_site_outputs(output_dir, data_dir, site["key"], items)
        all_items.extend(items)

    write_all_sites_output(output_dir, data_dir, all_items)

    if not (data_dir / "all_sites.json").exists():
        save_json(data_dir / "all_sites.json", {"items": all_items})
    if not (output_dir / "sale_data.json").exists():
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
        default=30,
        help="Minimum discount percent to include.",
    )
    args = parser.parse_args()

    items = run(output_dir=args.output_dir, min_discount=args.min_discount)
    print(f"Scraped {len(items)} sale items and wrote JSON to {args.output_dir}")
