import requests
import sys
from bs4 import BeautifulSoup
from episode import Episode

if sys.version_info >= (3, 5, 0):
    from http import HTTPStatus as StatusCode
elif sys.version_info > (3, 0, 0):
    from http import client as StatusCode
else:
    import httplib as StatusCode

class ComicBook:
    def __init__(self):
        self.__id = -1
        self.__url = ''
        self.__episodes = dict()
        self.__episode = Episode()

    def crawl(self, comic_id):
        if not self.__check_id(comic_id):
            return False

        self.__id = comic_id
        self.__url = 'http://www.comicbus.com/html/' + self.__id + '.html'

        response = requests.get(self.__url)
        if response.status_code != StatusCode.OK:
            print('status code: ' + str(response.status_code))
            return False

        soup = BeautifulSoup(response.content.decode("big5"), 'lxml')
        tds = soup.find('table', id='div_li1').find_all('td')
        index = 0
        for td in tds:
            if td.string:
                if td.find('script'):
                    name = td.find('font').sting.strip()
                else:
                    name = td.string.strip()

                self.__episodes[index] = [name, 'http://v.comicbus.com/online/comic-' + self.__id + '.html?' +
                                          td.find('a').get('id').replace('c', 'ch=')]
                index += 1
        return True

    def list(self):
        if len(self.__episodes) == 0:
            return []

        output = dict()
        for episode in self.__episodes:
            output[episode] = self.__episodes[episode][0]
        return output

    def get_episode(self, index):
        if index not in self.__episodes:
            return []

        print(self.__episodes[index][1])
        print(self.__episode.run(self.__episodes[index][1]))

    @staticmethod
    def __check_id(comic_id):
        return True


def main():
    comic_id = '103'
    # comic_id = '15603'
    comic = ComicBook()
    comic.crawl(comic_id)
    print(comic.list())
    comic.get_episode(500)


if __name__ == '__main__':
    main()
