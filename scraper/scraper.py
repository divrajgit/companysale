# scraper/scraper.py
import json
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup

CONFIG_PATH = Path("config/sites.yaml")
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

ALERT_EMAIL_FROM = "your-email@example.com"
ALERT_EMAIL_TO = "recipient@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "your-smtp-user"
SMTP_PASS = "your-smtp-pass"

# If you want SMS via Twilio, you can add it similarly.


def load_sites():
    with open(CONFIG_PATH, "r") as f:
        cfg = yaml.safe_load(f)
    return cfg["sites"]


def parse_thebodyshop(html, min_discount=50):
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


PARSERS = {
    "thebodyshop": parse_thebodyshop,
    # later: "another_site": parse_another_site,
}


def fetch_site(site, min_discount=50):
    key = site["key"]
    url = site["url"]

    print(f"Fetching {site['name']} ({url})")

    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    parser = PARSERS.get(key)
    if not parser:
        print(f"No parser defined for key={key}, skipping.")
        return []

    items = parser(resp.text, min_discount=min_discount)
    return items


def load_previous_data(site_key):
    path = DATA_DIR / f"{site_key}.json"
    if not path.exists():
        return []
    with open(path, "r") as f:
        return json.load(f)


def save_current_data(site_key, items):
    path = DATA_DIR / f"{site_key}.json"
    with open(path, "w") as f:
        json.dump(items, f, indent=2)


def diff_new_items(old_items, new_items):
    old_names = {item["name"] for item in old_items}
    return [item for item in new_items if item["name"] not in old_names]


def send_email_alert(new_items, site_name):
    if not new_items:
        return

    subject = f"New 50%+ sale items on {site_name}"
    body_lines = []
    for item in new_items:
        body_lines.append(
            f"{item['name']} — {item['discount_percent']}% off "
            f"(was ${item['old_price']}, now ${item['new_price']})\n{item['url']}\n"
        )
    body = "\n".join(body_lines)

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = ALERT_EMAIL_FROM
    msg["To"] = ALERT_EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    print(f"Sent email alert for {len(new_items)} items on {site_name}")


def main():
    sites = load_sites()
    all_results = {}

    for site in sites:
        key = site["key"]
        name = site["name"]

        old_items = load_previous_data(key)
        new_items = fetch_site(site, min_discount=50)

        save_current_data(key, new_items)

        newly_added = diff_new_items(old_items, new_items)
        if newly_added:
            print(f"{len(newly_added)} new items on {name}")
            send_email_alert(newly_added, name)

        all_results[key] = new_items

    # Optional: write combined file
    with open(DATA_DIR / "all_sites.json", "w") as f:
        json.dump(all_results, f, indent=2)


if __name__ == "__main__":
    main()
