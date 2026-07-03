from parsers.thebodyshop import parse as parse_thebodyshop

PARSERS = {
    "thebodyshop": parse_thebodyshop,
}
from utils.yaml_loader import load_sites
from utils.json_store import (
    load_site_data,
    save_site_data,
    save_all_sites
)
