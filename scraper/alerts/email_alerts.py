# scraper/alerts/email_alerts.py

import smtplib
from email.mime.text import MIMEText

def send_email_alert(new_items, site_name, config):
    """
    Sends an email alert for newly added sale items.
    config must contain:
        SMTP_SERVER
        SMTP_PORT
        SMTP_USER
        SMTP_PASS
        ALERT_EMAIL_FROM
        ALERT_EMAIL_TO
    """

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
    msg["From"] = config["ALERT_EMAIL_FROM"]
    msg["To"] = config["ALERT_EMAIL_TO"]

    with smtplib.SMTP(config["SMTP_SERVER"], config["SMTP_PORT"]) as server:
        server.starttls()
        server.login(config["SMTP_USER"], config["SMTP_PASS"])
        server.send_message(msg)

    print(f"[EMAIL] Sent alert for {len(new_items)} items on {site_name}")
