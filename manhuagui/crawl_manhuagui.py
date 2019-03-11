import requests
from manhuagui.constant import MANHUAGUI_COMIC_URL


def crawl_manhuagui(start=0, end=0):
    index = start

    while True:
        response = requests.get(MANHUAGUI_COMIC_URL + str(index))
        if response.status_code != requests.codes.ok:
            break

        yield MANHUAGUI_COMIC_URL + str(index)

        if index == end and end != 0:
            break

        index += 1
