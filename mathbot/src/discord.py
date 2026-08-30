import os
import requests

from config import DISCORD_WEBHOOK_URL
from latex_renderer import render_latex


def send_message(
    title,
    description
):
    image_path = "tmp/discord_message.png"

    render_latex(
        f"""
        <h1>{title}</h1>
        <div>
            {description}
        </div>
        """,
        image_path
    )

    with open(image_path, "rb") as image:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            files={
                "file": (
                    "mathbot.png",
                    image,
                    "image/png"
                )
            },
            data={
                "payload_json": "{}"
            },
            timeout=60
        )

    response.raise_for_status()
