import requests
from manhuagui.constant import MANHUAGUI_COMIC_URL


def crawl_manhuagui(session=None, start=1, end=0):
    index = start

    output = list()

    manhuagui_session = session
    if not manhuagui_session:
        manhuagui_session = requests.session()

    output.append(manhuagui_session)

    while True:
        response = manhuagui_session.get(MANHUAGUI_COMIC_URL + str(index))
        if response.status_code != requests.codes.ok:
            break

        output.append(MANHUAGUI_COMIC_URL + str(index))

        if index == end and end != 0:
            break

        index += 1

    return output
