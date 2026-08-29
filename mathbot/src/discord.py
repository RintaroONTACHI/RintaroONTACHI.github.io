import requests

from config import DISCORD_WEBHOOK_URL


def send_message(
    title,
    description
):

    payload = {
        "embeds": [
            {
                "title": title,
                "description": description
            }
        ]
    }

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json=payload,
        timeout=30
    )

    response.raise_for_status()
