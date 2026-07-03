# scraper/utils/json_store.py

import json
from pathlib import Path
from typing import Any, List

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def load_json(path: str | Path) -> Any:
    """
    Loads JSON from a file.
    Returns Python object (list or dict).
    """
    path = Path(path)

    if not path.exists():
        return None

    with open(path, "r") as f:
        return json.load(f)


def save_json(path: str | Path, data: Any) -> None:
    """
    Saves Python object to JSON file.
    """
    path = Path(path)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_site_data(site_key: str) -> List[dict]:
    """
    Loads JSON for a specific site.
    Example: data/thebodyshop.json
    """
    path = DATA_DIR / f"{site_key}.json"
    data = load_json(path)
    return data if data else []


def save_site_data(site_key: str, items: List[dict]) -> None:
    """
    Saves JSON for a specific site.
    """
    path = DATA_DIR / f"{site_key}.json"
    save_json(path, items)


def save_all_sites(data: dict) -> None:
    """
    Saves combined JSON for all sites.
    """
    path = DATA_DIR / "all_sites.json"
    save_json(path, data)
