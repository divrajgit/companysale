from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse(html, min_discount=30, site_url=None):
    soup = BeautifulSoup(html, "html.parser")
    items = []

    products = soup.select("div.product-card")

    for product in products:
        name_tag = product.select_one("a.product-card__link")
        price_old_tag = product.select_one("span.product-card__price--old")
        price_new_tag = product.select_one("span.product-card__price--current")

        if not name_tag or not price_new_tag:
            continue

        name = name_tag.get_text(strip=True)
        url = name_tag["href"]
        if not url.startswith("http") and site_url:
            url = urljoin(site_url, url)

        try:
            new_price = float(price_new_tag.get_text(strip=True).replace("$", "").replace(",", ""))
        except ValueError:
            continue

        if price_old_tag:
            try:
                old_price = float(price_old_tag.get_text(strip=True).replace("$", "").replace(",", ""))
            except ValueError:
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
