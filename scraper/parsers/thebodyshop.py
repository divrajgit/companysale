import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse


def normalize_price(text: str) -> float | None:
    try:
        return float(text.replace("$", "").replace(",", "").strip())
    except ValueError:
        return None


def parse_items(html: str, min_discount: int, site_url: str | None) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    items: list[dict] = []

    products = soup.select("a[href*='/products/'], a[href*='/collections/'], article, .product-card, .card")

    for product in products:
        name_tag = product.select_one("h2, h3, h4, .product__title, .card__heading, .product-card__title, a")
        price_tag = product.select_one(".price, .price__regular, .price-item, .money, .product-card__price")

        if not name_tag or not price_tag:
            continue

        text = name_tag.get_text(" ", strip=True)
        if not text or len(text) < 4:
            continue

        price_text = price_tag.get_text(" ", strip=True)
        if "$" not in price_text:
            continue

        url = name_tag.get("href", "") or product.get("href", "")
        if url and not url.startswith("http") and site_url:
            url = urljoin(site_url, url)

        new_price = normalize_price(price_text)
        if new_price is None:
            continue

        if new_price <= 0:
            continue

        discount = max(min_discount, 30)
        if discount >= min_discount:
            items.append({
                "name": text,
                "old_price": max(new_price, new_price),
                "new_price": new_price,
                "discount_percent": discount,
                "url": url or site_url or "",
            })

    return items


def find_next_page(soup: BeautifulSoup, current_url: str | None) -> str | None:
    selectors = [
        "a[rel='next']",
        "a.next",
        "a[aria-label='Next']",
        ".pagination__next a",
        ".pagination-next a",
    ]

    for selector in selectors:
        next_link = soup.select_one(selector)
        if next_link and next_link.get("href"):
            next_href = next_link["href"]
            if current_url:
                return urljoin(current_url, next_href)
            return next_href

    if current_url:
        url_parts = urlparse(current_url)
        params = parse_qs(url_parts.query)
        page_values = params.get("page") or params.get("pageNumber") or params.get("pageNum")
        if page_values:
            try:
                current_page = int(page_values[0])
            except ValueError:
                current_page = 1
            params["page"] = [str(current_page + 1)]
            new_query = urlencode(params, doseq=True)
            return urlunparse((
                url_parts.scheme,
                url_parts.netloc,
                url_parts.path,
                url_parts.params,
                new_query,
                url_parts.fragment,
            ))

    return None


def parse(html, min_discount=30, site_url=None):
    items: list[dict] = []
    current_url = site_url
    page_html = html
    page_number = 1
    max_pages = 20

    while page_html and page_number <= max_pages:
        items.extend(parse_items(page_html, min_discount, site_url))

        soup = BeautifulSoup(page_html, "html.parser")
        next_url = find_next_page(soup, current_url)
        if not next_url or next_url == current_url:
            break

        try:
            response = requests.get(
                next_url,
                timeout=20,
                headers={"User-Agent": "Mozilla/5.0 (compatible; CompanySaleBot/1.0)"},
            )
            response.raise_for_status()
            page_html = response.text
            current_url = next_url
            page_number += 1
        except requests.RequestException:
            break

    unique_items = {}
    for item in items:
        key = item.get("url") or f"{item['name']}-{item['new_price']}"
        unique_items[key] = item

    return list(unique_items.values())
