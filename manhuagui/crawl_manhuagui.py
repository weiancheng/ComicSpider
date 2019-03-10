import requests
from manhuagui.constant import MANHUAGUI_COMIC_URL


def crawl_manhuagui(limited=0):
    index = 1

    while True:
        response = requests.get(MANHUAGUI_COMIC_URL + str(index))
        if response.status_code != requests.codes.ok:
            break

        yield MANHUAGUI_COMIC_URL + str(index)

        if index == limited and limited != 0:
            break

        index += 1
