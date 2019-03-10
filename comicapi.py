from manhuagui.crawl_manhuagui import crawl_manhuagui
from manhuagui.episode import episode
from manhuagui.comic_book import comic_book
from manhuagui.constant import MANHUAGUI_COMIC_URL


class ComicAPI:
    def __init__(self):
        pass

    def get_list(self):
        yield crawl_manhuagui()

    def get_comic_book(self, index):
        url = MANHUAGUI_COMIC_URL + str(index)
        data = comic_book(url)
        return data

    def get_content(self, url):
        return episode(url)


def main():
    comic = ComicAPI()
    print(comic.get_comic_book('https://www.manhuagui.com/comic/7580'))
    print(comic.get_content('https://www.manhuagui.com/comic/3/64331.html'))


if __name__ == '__main__':
    main()
