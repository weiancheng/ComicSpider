import requests
from bs4 import BeautifulSoup


def comic_book(url):
    if len(url) == 0:
        return None

    data = dict()

    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        print('[Error] status code: ' + str(response.status_code))
        exit(0)

    soup = BeautifulSoup(response.text, 'lxml')

    tags_li = soup.find_all('li')

    data['comics'] = list()

    for li in tags_li:
        a = li.find('a', href=True, class_='status0')
        if not a:
            continue

        data['comics'].append(a)

    return data


def main():
    url = 'https://www.manhuagui.com/comic/7580/'
    comic_book(url)


if __name__ == '__main__':
    main()
