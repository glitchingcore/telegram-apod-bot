import logging
import time

from nasa.client import NasaSyncClient
from nasa._types import AstronomyPicture

from config_reader import config
from telegram import send_photo



def format_caption(title: str, body: str) -> str:
    # Remove trailing spaces.
    body = " ".join(body.split())

    caption = f"<b>{title}</b>\n\n"
    while len(body) + len(caption) > 1024:
        index = max(body[:-1].rfind(char) for char in ".!?")
        body = body[:index + 1]
    caption += body
    return caption


def fetch_apod(client: NasaSyncClient, storage: dict, channel_username: str):
    logging.info("Fetching APOD")

    astronomy_picture: AstronomyPicture = client.get_astronomy_picture()
    if not astronomy_picture.date == storage["last_date"] and astronomy_picture.is_image:
        # SyncAsset.bytes_asset / AsyncAsset.bytes_asset can be None if the bytes of the asset
        # aren't cached yet. From the docs:
        # https://nasapy-a-nasa-api-python-wrapper.readthedocs.io/en/latest/api_reference/astronomy_pictures.html
        image_bytes = astronomy_picture.image.bytes_asset or astronomy_picture.image.read()
        caption = format_caption(title=astronomy_picture.title, body=astronomy_picture.explanation)
        send_photo(
            channel_username=channel_username,
            photo=image_bytes,
            caption=caption,
            parse_mode='HTML',
        )
        storage["last_date"] = astronomy_picture.date


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Started bot.")

    # Memory storage
    storage = {"last_date": None}

    # Initialize nasa.py sync client
    nasa_token = config.nasa_api_token.get_secret_value()
    client = NasaSyncClient(token=nasa_token)
    
    channel_username = config.channel_username

    while True:
        fetch_apod(client=client, storage=storage, channel_username=channel_username)
        logging.info("Waiting for 15 minutes...")
        time.sleep(15*60)
        

if __name__ == "__main__":
    main()