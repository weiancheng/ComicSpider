import requests
import sys
import re
from bs4 import BeautifulSoup

if sys.version_info >= (3, 5, 0):
    from http import HTTPStatus as StatusCode
elif sys.version_info > (3, 0, 0):
    from http import client as StatusCode
else:
    import httplib as StatusCode


class ComicIndex:
    def __init__(self):
        self.__url = 'http://www.comicbus.com/comic/all.html'
        self.__index_as_key = dict()

        self.__crawl()

    def __crawl(self):
        response = requests.get(self.__url)
        if response.status_code != StatusCode.OK:
            print('status code: ' + str(response.status_code))
            return

        soup = BeautifulSoup(response.content, 'lxml')
        tags = soup.find_all('a', href=True, onmouseout=True)
        for tag in tags:
            r = re.search("/html/([\d]+)\.html", tag.get('href'))
            if r:
                i = str(r.group(1))
            else:
                i = ''

            if len(i) > 0:
                self.__index_as_key[i] = tag.text

    def find_by_index(self, index):
        return self.__index_as_key[index]

    def get_list(self):
        return self.__index_as_key


def main():
    ci = ComicIndex()
    print(ci.get_list())


if __name__ == '__main__':
    main()
