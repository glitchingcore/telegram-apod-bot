import requests
import logging
from config_reader import config

API_URL = "https://api.nasa.gov/planetary/apod?api_key={nasa_token}".format(nasa_token=config.nasa_api_token.get_secret_value())

def get_astronomy_picture():
    logging.info("Fetching APOD.")
    res = requests.get(API_URL)
    if not res.ok:
        logging.error("Failed to fetch APOD.")
        return None
    apod = res.json()
    apod["is_image"] = apod["media_type"] == "image"
    if apod["is_image"]:
        apod["image"] = requests.get(apod["url"]).content
    logging.info("Fetching APOD successful.")
    return apod
