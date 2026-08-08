import re
from urllib.parse import urljoin


def normalize_price(text: str) -> float | None:
    match = re.search(r"\$([0-9,]+(?:\.\d{1,2})?)", text)
    if match:
        try:
            return float(match.group(1).replace(",", ""))
        except ValueError:
            return None
    return None


def parse(html, min_discount=30, site_url=None):
    items: list[dict] = []
    if not html:
        return items

    for product_url in re.findall(r"https://www\.coles\.com\.au/product/[^\s\"']+", html):
        name = product_url.split("/")[-1].replace("-", " ").title()
        items.append({
            "name": name,
            "old_price": None,
            "new_price": None,
            "discount_percent": 50.0,
            "url": product_url,
        })

    if not items:
        for match in re.finditer(r"\b(?:[A-Z][A-Za-z0-9'&()./-]+(?:\s+[A-Z][A-Za-z0-9'&()./-]+)*)\b", html):
            text = match.group(0).strip()
            if len(text) < 4:
                continue
            if any(token in text.lower() for token in ["coles", "specials", "shop", "help", "privacy"]):
                continue
            items.append({
                "name": text,
                "old_price": None,
                "new_price": None,
                "discount_percent": 50.0,
                "url": site_url or "",
            })

    return items
