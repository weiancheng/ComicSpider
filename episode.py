import util
import requests
import re
import sys
import urllib

if sys.version_info >= (3, 5, 0):
    from http import HTTPStatus as StatusCode
elif sys.version_info > (3, 0, 0):
    from http import client as StatusCode
else:
    import httplib as StatusCode


class Episode:
    def __init__(self):
        self.__ti = ''
        self.__cs = ''
        self.__content = ''
        self.__ch = -1
        self.__url = ''
        self.__parameters = dict()
        self.__count = 0

    def run(self, url, ch):
        self.__url = url + '?ch=' + str(ch)
        response = requests.get(self.__url)
        if response.status_code != StatusCode.OK:
            print('status code: ' + str(response.status_code))
            return None

        self.__content = response.content.decode("big5")
        self.__ch = str(ch)
        self.get_ti()
        self.get_cs()
        self.get_parameters()

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

    def get_parameters(self):
        if len(self.__content) == 0 or len(self.__cs) == 0:
            return

        r = re.search("var cs=\\'[\d\w]+\\';"
                      "for\(var i=0;i<([\d]+);i\+\+\)"
                      "{var ([\w]+)\s*=\s*lc\(su\(cs,i\*y\+([\d]+),([\d]+)\)\);"
                      "var ([\w]+)\s*=\s*lc\(su\(cs,i\*y\+([\d]+),([\d]+)\)\);"
                      "var ([\w]+)\s*=\s*lc\(su\(cs,i\*y\+([\d]+),([\d]+)\)\);"
                      "var ([\w]+)\s*=\s*lc\(su\(cs,i\*y\+([\d]+),([\d]+)\)\);", self.__content)

        if r:
            self.__count = int(r.group(1))
            self.__parameters[str(r.group(2))] = lambda i: util.lc(util.su(self.__cs,
                                                                           i * util.y + int(r.group(3)),
                                                                           int(r.group(4))))
            self.__parameters[str(r.group(5))] = lambda i: util.lc(util.su(self.__cs,
                                                                           i * util.y + int(r.group(6)),
                                                                           int(r.group(7))))
            self.__parameters[str(r.group(8))] = lambda i: util.lc(util.su(self.__cs,
                                                                           i * util.y + int(r.group(9)),
                                                                           int(r.group(10))))
            self.__parameters[str(r.group(11))] = lambda i: util.lc(util.su(self.__cs,
                                                                            i * util.y + int(r.group(12)),
                                                                            int(r.group(13))))

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
        r = re.search("if\(([\w]+)== ch\){ci=i;ge\('TheImg'\)\.src='http://img'\+su\(([\w]+), 0, "
                      "1\)\+'\.8comic\.com/'\+su\(([\w]+),1,1\)\+'/'\+ti\+'/'\+([\w]+)\+'/'\+\s+"
                      "nn\(p\)\+'_'\+su\(([\w]+),mm\(p\),3\)\+'\.jpg'", self.__content)

        while True:
            if self.__parameters[str(r.group(1))](i) == self.__ch:
                src = 'http://img' + \
                      util.su(self.__parameters[str(r.group(2))](i), 0, 1) + \
                      '.8comic.com/' + \
                      util.su(self.__parameters[str(r.group(3))](i), 1, 1) + \
                      '/' + \
                      self.__ti + \
                      '/' + \
                      self.__parameters[str(r.group(4))](i) + \
                      '/' + \
                      util.nn(index) + \
                      '_' + \
                      util.su(self.__parameters[str(r.group(5))](i), util.mm(index), 3) + \
                      '.jpg'
                break
            i += 1
        if self.is_valid(src):
            return src
        return ''


def main():
    url = 'http://v.comicbus.com/online/comic-14438.html'
    episode = Episode()
    episode.run(url, 5)
    for i in range(1, 20):
        print(episode.get_photo(i))


if __name__ == '__main__':
    main()
