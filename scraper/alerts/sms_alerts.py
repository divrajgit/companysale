# scraper/alerts/sms_alerts.py

from twilio.rest import Client

def send_sms_alert(new_items, site_name, config):
    """
    Sends SMS alerts using Twilio.
    config must contain:
        TWILIO_SID
        TWILIO_AUTH
        TWILIO_FROM
        TWILIO_TO
    """

    if not new_items:
        return

    client = Client(config["TWILIO_SID"], config["TWILIO_AUTH"])

    for item in new_items:
        message = (
            f"{site_name}: {item['name']} — {item['discount_percent']}% off\n"
            f"${item['new_price']} (was ${item['old_price']})\n{item['url']}"
        )

        client.messages.create(
            body=message,
            from_=config["TWILIO_FROM"],
            to=config["TWILIO_TO"]
        )

    print(f"[SMS] Sent {len(new_items)} SMS alerts for {site_name}")
