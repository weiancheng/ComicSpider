import util
import requests
import re


class Episode:
    def __init__(self):
        self.__ti = ''
        self.__cs = ''
        self.__count = 0
        self.__content = ''

    def run(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            print('status code: ' + str(response.status_code))
            return

        self.__content = str(response.content)
        self.get_ti()
        self.get_cs()
        self.get_page_counts()
        return self.get_photos()

    def get_ti(self):
        r = re.search("var ti=([\d]+);", self.__content)
        if r:
            self.__ti = str(r.group(1))

    def get_cs(self):
        r = re.search("var cs=\\\\'([\d\w]+)\\\\';", self.__content)
        if r:
            self.__cs = str(r.group(1))

    def get_page_counts(self):
        r = re.search("var chs=([\d]+);", self.__content)
        if r:
            self.__count = int(r.group(1))

    def get_photos(self):
        photos = list()
        for i in range(self.__count):
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
                  util.nn(util.p) + \
                  '_' + \
                  util.su(okhrp, util.mm(util.p), 3) + \
                  '.jpg'
            photos.append(src)

        return photos
