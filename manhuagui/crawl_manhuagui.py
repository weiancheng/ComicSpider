import requests


def crawl_manhuagui(limited=0):
    index = 1

    url = 'https://www.manhuagui.com/comic/'

    while True:
        response = requests.get(url + str(index))
        if response.status_code != requests.codes.ok:
            break

        yield url + str(index)

        if index == limited and limited != 0:
            break

        index += 1
