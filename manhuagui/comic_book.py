import re
import requests
from bs4 import BeautifulSoup


def comic_book(url):
    if len(url) == 0:
        return None

    data = dict()

    data['url'] = url

    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        print('[Error] status code: ' + str(response.status_code))
        exit(0)

    soup = BeautifulSoup(response.text, 'lxml')

    # book title
    book_title = soup.find('div', class_='book-title')
    data['book-title'] = book_title.text

    data['comics'] = list()

    tags_li = soup.find_all('li')
    for li in tags_li:
        a = li.find('a', href=True, class_='status0')
        if not a:
            continue

        r = re.search("/comic/\d+/(\d+)\.html", a['href'])
        if not r:
            continue

        data['comics'].append({r.group(1): [a['title'], 'https://www.manhuagui.com' + a['href']]})

    return data


def main():
    url = 'https://www.manhuagui.com/comic/7580/'
    print(comic_book(url))


if __name__ == '__main__':
    main()
