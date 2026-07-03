# scraper/parsers/thebodyshop.py

from bs4 import BeautifulSoup

def parse(html, min_discount=50):
    soup = BeautifulSoup(html, "html.parser")
    items = []

    products = soup.select("div.product-item-info")

    for product in products:
        name_tag = product.select_one("a.product-item-link")
        price_old_tag = product.select_one("span.old-price .price")
        price_new_tag = product.select_one("span.special-price .price")

        if not name_tag or not price_new_tag:
            continue

        name = name_tag.get_text(strip=True)
        url = name_tag["href"]
        if not url.startswith("http"):
            url = "https://www.thebodyshop.com.au" + url

        try:
            new_price = float(price_new_tag.get_text(strip=True).replace("$", ""))
        except ValueError:
            continue

        if price_old_tag:
            try:
                old_price = float(price_old_tag.get_text(strip=True).replace("$", ""))
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
