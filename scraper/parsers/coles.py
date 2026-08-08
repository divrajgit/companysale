import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse


def normalize_price(tag_text: str) -> float | None:
    try:
        return float(tag_text.replace("$", "").replace(",", "").strip())
    except ValueError:
        return None


def parse_items(html: str, min_discount: int, site_url: str | None) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    items: list[dict] = []

    products = soup.select(".product-tile, .product-card, .product")

    for product in products:
        name_tag = product.select_one(".product-name, .product-tile__name, .product-card__title, a")
        price_new_tag = product.select_one(".price--special, .price--current")
        price_old_tag = product.select_one(".price--rrp, .price--standard, .price--was, .price--strike")

        if not name_tag or not price_new_tag or not price_old_tag:
            continue

        name = name_tag.get_text(strip=True)
        url = name_tag.get("href", "")
        if url and not url.startswith("http") and site_url:
            url = urljoin(site_url, url)

        new_price = normalize_price(price_new_tag.get_text(strip=True))
        old_price = normalize_price(price_old_tag.get_text(strip=True))
        if new_price is None or old_price is None or old_price <= 0:
            continue

        discount = round((old_price - new_price) / old_price * 100, 2)
        if discount >= min_discount:
            items.append({
                "name": name,
                "old_price": old_price,
                "new_price": new_price,
                "discount_percent": discount,
                "url": url,
            })

    return items


def find_next_page(soup: BeautifulSoup, current_url: str | None) -> str | None:
    selectors = [
        "a[rel='next']",
        "a.next",
        "a[aria-label='Next']",
        "button[aria-label='Next']",
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
        page_items = parse_items(page_html, min_discount, site_url)
        items.extend(page_items)

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

    # Remove duplicates by URL if a product appears on multiple pages.
    unique_items = {}
    for item in items:
        if item.get("url"):
            unique_items[item["url"]] = item
        else:
            unique_items[f"{item['name']}-{item['new_price']}"] = item

    return list(unique_items.values())
