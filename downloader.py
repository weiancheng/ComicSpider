import json
import os
import time
from manhuagui.crawler import Crawler


"""
manhuagui {
    count: int
}

album {
    id
    name
    chapter: dict
    {
        cid: [title, [url, ...]]
        ...
    }
}
"""


class MangaDownloader:
    def __init__(self):
        self.TABLE = 'table.json'
        self.table = None
        self.manhuagui_crawler = Crawler()

    def last_time(self):
        # zero means that manhuagui just initialized now
        if self.table['count'] == 0:
            return

        # let's do the current count
        album = self.download_manhuagui_album('https://www.manhuagui.com/comic/' + str(self.table['count']))
        current_album = self.read_album()

        for chapter in album['comics'].keys():
            if chapter in current_album['chapter'].keys():
                continue

            current_album['chapter'][chapter] = [album['comics'][chapter]]

        self.update_album(current_album)

        self.table['count'] += 1

    def read_album(self):
        file_name = str(self.table['count']) + '.json'
        if not os.path.exists(file_name):
            return None

        with open(file_name, 'r') as f:
            content = f.read()

        return json.loads(content)

    def read_manhuagui(self):
        if not os.path.exists(self.TABLE):
            self.init_manhuagui()
            return

        with open(self.TABLE, 'r') as f:
            self.table = json.loads(f.read())

    def init_manhuagui(self):
        self.table = {
            'count': 0
        }

        with open(self.TABLE, 'w') as f:
            f.write(json.dumps(self.table))

    def update_manhuagui(self):
        with open(self.TABLE, 'w') as f:
            f.write(json.dumps(self.table))

    def update_album(self, album):
        file_name = str(album['id']) + '.json'
        with open(file_name, 'w') as f:
            f.write(json.dumps(album))

        self.table['count'] = album['id']

    def download_album(self, url):
        album = self.download_manhuagui_album(url)

        output = dict()
        output['id'] = album['index']
        output['name'] = album['book-title']
        output['chapter'] = dict()

        for ch in album['comics'].keys():
            c = self.download_manhuagui_chapter(album['comics'][ch][1])
            output['chapter'][c['params']['cid']] = [c['cname'], c['pictures']]
            print(output['chapter'][c['params']['cid']])

        return output

    def download_manhuagui_album(self, url):
        time.sleep(3)
        return self.manhuagui_crawler.album(url)

    def download_manhuagui_chapter(self, url):
        time.sleep(3)
        return self.manhuagui_crawler.chapter(url)


def main():
    downloader = MangaDownloader()

    downloader.read_manhuagui()

    current_count = downloader.table['count']

    if current_count == 0:
        current_count = 1

    while True:
        url = 'https://www.manhuagui.com/comic/' + str(current_count)
        album = downloader.download_album(url)
        downloader.update_album(album)
        current_count += 1
        downloader.table['count'] += 1
        downloader.update_manhuagui()
        if current_count == 3:
            break


if __name__ == '__main__':
    main()
