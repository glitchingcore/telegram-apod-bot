import requests
import logging
from config_reader import config

API_URL = "https://api.telegram.org/bot{bot_token}/".format(bot_token=config.bot_token.get_secret_value())

def send_photo(channel_username: str, photo: bytes, caption: str, parse_mode: str):
    if parse_mode not in ["HTML", "Markdown", "MarkdownV2"]:
        raise ValueError("Invalid argument value. parse_mode can have a value of 'HTML', 'Markdown' or 'MarkdownV2'")

    method = "sendPhoto"
    url = API_URL + method
    params = {"chat_id": channel_username, "caption": caption, "parse_mode": parse_mode}
    files = {"photo": photo}
    response = requests.post(url=url, params=params, files=files)

    if response.status_code == 200:
        logging.info("Photo sent to {channel}".format(channel=channel_username))
    else:
        logging.error(response.text)
        