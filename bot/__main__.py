import logging
import time

from config_reader import config
from telegram import send_photo
from apod import get_astronomy_picture

TG_CAPTION_CHAR_LIMIT = 1024


def format_caption(title: str, body: str) -> str:
    # Remove trailing spaces.
    body = " ".join(body.split())

    caption = f"<b>{title}</b>\n\n"
    while len(body) + len(caption) > TG_CAPTION_CHAR_LIMIT:
        index = max(body[:-1].rfind(char) for char in ".!?")
        body = body[: index + 1]
    caption += body
    return caption


def fetch_apod(storage: dict, channel_username: str):
    astronomy_picture = get_astronomy_picture()
    if (
        (astronomy_picture is None)
        or (astronomy_picture["date"] == storage["last_date"])
        or (not astronomy_picture["is_image"])
    ):
        return

    image_bytes = astronomy_picture["image"]
    caption = format_caption(
        title=astronomy_picture["title"], body=astronomy_picture["explanation"]
    )
    send_photo(
        channel_username=channel_username,
        photo=image_bytes,
        caption=caption,
        parse_mode="HTML",
    )
    storage["last_date"] = astronomy_picture["date"]


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Started bot.")

    # Memory storage
    storage = {"last_date": None}

    channel_username = config.channel_username

    while True:
        fetch_apod(storage=storage, channel_username=channel_username)
        logging.info("Waiting for 15 minutes...")
        time.sleep(15 * 60)


if __name__ == "__main__":
    main()
