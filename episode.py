import util
import requests
import re
from http import HTTPStatus
import urllib


class Episode:
    def __init__(self):
        self.__ti = ''
        self.__cs = ''
        self.__content = ''
        self.__ch = -1
        self.__url = ''

    def run(self, url, ch):
        self.__url = url + '?ch=' + str(ch)
        response = requests.get(self.__url)
        if response.status_code != HTTPStatus.OK:
            print('status code: ' + str(response.status_code))
            return None

        self.__content = response.content.decode("big5")
        self.__ch = str(ch)
        self.get_ti()
        self.get_cs()

    def get_ti(self):
        if len(self.__content) == 0:
            return

        r = re.search("var ti=([\d]+);", self.__content)
        if r:
            self.__ti = str(r.group(1))

    def get_cs(self):
        if len(self.__content) == 0:
            return

        r = re.search("var cs=\\'([\d\w]+)\\';", self.__content)
        if r:
            self.__cs = str(r.group(1))

    @staticmethod
    def is_valid(photo):
        try:
            urllib.request.urlopen(photo)
        except urllib.error.HTTPError:
            return False
        except urllib.error.URLError:
            return False
        return True

    def get_photo(self, index):
        i = 0
        while True:
            aafbe = util.lc(util.su(self.__cs, i * util.y + 0, 2))
            wivbj = util.lc(util.su(self.__cs, i * util.y + 2, 2))
            okhrp = util.lc(util.su(self.__cs, i * util.y + 4, 40))
            if aafbe == self.__ch:
                src = 'http://img' + \
                      util.su(wivbj, 0, 1) + \
                      '.8comic.com/' + \
                      util.su(wivbj, 1, 1) + \
                      '/' + \
                      self.__ti + \
                      '/' + \
                      aafbe + \
                      '/' + \
                      util.nn(index) + \
                      '_' + \
                      util.su(okhrp, util.mm(index), 3) + \
                      '.jpg'
                break
            i += 1

        if self.is_valid(src):
            return src
        return ''


def main():
    url = 'http://v.comicbus.com/online/comic-103.html'
    episode = Episode()
    episode.run(url, 903)
    for i in range(1, 19):
        print(episode.get_photo(i))


if __name__ == '__main__':
    main()
