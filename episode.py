import util
import requests
import re


class Episode:
    def __init__(self, total):
        self.__ti = ''
        self.__cs = ''
        self.__count = total
        self.__content = ''
        self.__ch = -1
        self.__url = ''

    def run(self, url, ch):
        self.__url = url + '?ch=' + str(ch)
        response = requests.get(self.__url)
        if response.status_code != 200:
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
        response = requests.get(photo)
        if response.status_code != 200:
            return False
        return True

    def get_photo(self, index):
        src = ''
        for i in range(self.__count+1):
            aafbe = util.lc(util.su(self.__cs, i * util.y + 0, 2))
            wivbj = util.lc(util.su(self.__cs, i * util.y + 2, 2))
            okhrp = util.lc(util.su(self.__cs, i * util.y + 4, 40))
            src = 'http://img' + \
                  util.su(aafbe, 0, 1) + \
                  '.8comic.com/' + \
                  util.su(aafbe, 1, 1) + \
                  '/' + \
                  self.__ti + \
                  '/' + \
                  wivbj + \
                  '/' + \
                  util.nn(index) + \
                  '_' + \
                  util.su(okhrp, util.mm(index), 3) + \
                  '.jpg'
            if wivbj == self.__ch:
                break

        if self.is_valid(src):
            return src
        return ''


def main():
    url = 'http://v.comicbus.com/online/comic-103.html'
    episode = Episode(509)
    episode.run(url, 903)
    index = 1
    while True:
        u = episode.get_photo(index)
        if len(u) == 0:
            break
        print(u)
        index += 1


if __name__ == '__main__':
    main()
