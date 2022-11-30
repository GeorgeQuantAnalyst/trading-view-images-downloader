import logging
import logging.config
import os

import pandas as pd
import requests
from lxml import html

from trading_view_images_downloader.__version__ import __version__

# Constants
__logo__ = """
---------------------------------------------------------------------
trading-view-images-downloader {}
---------------------------------------------------------------------
""".format(__version__)

LOGGER_CONFIG_FILE_PATH = "logger.conf"


def download_image_from_tw_url(url: str, file_path: str) -> None:
    if pd.isna(url):
        logging.warning("Invalid url [{}], image will not be download.".format(url))
        return

    with open(file_path, 'wb') as handle:
        pic_url = parse_image_url_from_page(url)
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            logging.info(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)


def build_trade_id(asset: str, date: str, direction: str) -> str:
    date_array = date.split(".")
    day = date_array[0]
    month = date_array[1]
    year = date_array[2]

    if len(day) < 2:
        day = "0{}".format(day)

    if len(month) < 2:
        month = "0{}".format(month)

    return "{}{}{}_{}_{}".format(year, month, day, asset, direction)


def parse_image_url_from_page(url: str) -> str:
    response = requests.get(url)

    if not response.ok:
        logging.info(response)
        raise Exception("Problem with parse image url from page")

    html_page = html.fromstring(response.text)
    return html_page.xpath("//img")[0].attrib["src"]


if __name__ == "__main__":
    try:
        logging.config.fileConfig(fname=LOGGER_CONFIG_FILE_PATH, disable_existing_loggers=False)
        logging.info(__logo__)

        images = pd.read_csv("data/images.csv")

        base_directory = "data/output/"
        if not os.path.exists(base_directory):
            os.mkdir(base_directory)

        logging.info("Start download trades images")
        for index, image in images.iterrows():
            try:
                trade_id = build_trade_id(image["Asset"], image["Date"], image["Direction"])

                logging.info("Start processing trade {}".format(trade_id))
                final_path = base_directory + trade_id

                if not os.path.exists(final_path):
                    os.mkdir(final_path)

                logging.info("Processing picture in column Context")
                download_image_from_tw_url(image["Context"], "{}/{}_context.png".format(final_path, trade_id))

                logging.info("Processing picture in column Detail")
                download_image_from_tw_url(image["Detail"], "{}/{}_detail.png".format(final_path,trade_id))

                logging.info("Processing picture in column Detail2")
                download_image_from_tw_url(image["Detail2"], "{}/{}_detail2.png".format(final_path, trade_id))

                logging.info("Processing picture in column Control")
                download_image_from_tw_url(image["Control"], "{}/{}_control.png".format(final_path, trade_id))

                logging.info("Finished processing trade {}".format(trade_id))

            except:
                logging.exception("Problem with processing trade - {} {}".format(image["Asset"], image["Date"]))
        logging.info("Finished download trades images")
    except:
        logging.exception("Some problem in application:")
