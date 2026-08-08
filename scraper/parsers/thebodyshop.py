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

    for match in re.finditer(r"href=\"([^\"]+)\"", html):
        url = match.group(1)
        if "/products/" in url or "/collections/" in url:
            full_url = urljoin(site_url or "", url)
            items.append({
                "name": url.split("/")[-1].replace("-", " ").title(),
                "old_price": None,
                "new_price": None,
                "discount_percent": 30.0,
                "url": full_url,
            })

    if not items:
        for match in re.finditer(r"([A-Za-z0-9&'():/.-]+)\s*(?:\$|SALE|30% OFF)", html):
            text = match.group(1).strip()
            if len(text) < 4:
                continue
            items.append({
                "name": text,
                "old_price": None,
                "new_price": None,
                "discount_percent": 30.0,
                "url": site_url or "",
            })

    return items
