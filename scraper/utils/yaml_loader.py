# scraper/utils/yaml_loader.py

import yaml
from pathlib import Path

def load_yaml(path: str | Path) -> dict:
    """
    Loads a YAML file and returns a Python dictionary.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {path}")

    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_sites(config_path: str | Path = "config/sites.yaml") -> list:
    """
    Loads the list of sites from config/sites.yaml.
    Returns a list of site dictionaries.
    """
    data = load_yaml(config_path)

    if "sites" not in data:
        raise KeyError("Missing 'sites' key in YAML config")

    return data["sites"]
