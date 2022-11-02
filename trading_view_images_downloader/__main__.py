import logging
import os

import pandas as pd
import requests
from lxml import html

from trading_view_images_downloader.__version__ import __version__

# TODO: Lucka change print() to logging.info() in all file

__logo__ = """
---------------------------------------------------------------------
trading-view-images-downloader {}
---------------------------------------------------------------------
""".format(__version__)


def download_image_from_tw_url(url, file_path):
    with open(file_path, 'wb') as handle:
        pic_url = parse_image_url_from_page(url)
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)


def build_trade_id(asset, date, direction):
    date_array = date.split(".")
    day = date_array[0]
    month = date_array[1]
    year = date_array[2]

    if len(day) < 2:
        day = "0{}".format(day)

    if len(month) < 2:
        month = "0{}".format(month)

    return "{}{}{}_{}_{}".format(year, month, day, asset, direction)


def parse_image_url_from_page(url):
    response = requests.get(url)

    if not response.ok:
        print(response)
        raise Exception("Problem with parse image url from page")

    html_page = html.fromstring(response.text)
    return html_page.xpath("//img")[0].attrib["src"]


if __name__ == "__main__":
    try:
        print(__logo__)

        images = pd.read_csv("data/images.csv")

        base_directory = "data/output/"
        if not os.path.exists(base_directory):
            os.mkdir(base_directory)

        print("Start download trades images")
        for index, image in images.iterrows():
            try:
                trade_id = build_trade_id(image["Asset"], image["Date"], image["Direction"])

                print("Process trade {}".format(trade_id))
                final_path = base_directory + trade_id

                if not os.path.exists(final_path):
                    os.mkdir(final_path)

                download_image_from_tw_url(image["Context"], "{}/context.png".format(final_path))
                download_image_from_tw_url(image["Detail"], "{}/detail.png".format(final_path))
                download_image_from_tw_url(image["Control"], "{}/control.png".format(final_path))
            except:
                logging.exception("Problem with processing trade - {} {}".format(image["Asset"], image["Date"]))
        print("Finished download trades images")
    except:
        logging.exception("Some problem in application:")
