from manhuagui.crawl_manhuagui import crawl_manhuagui
from manhuagui.episode import episode
from manhuagui.comic_book import comic_book
import requests


def comic_book_list(start=0, end=0):
    result_list = list()

    for url in crawl_manhuagui(start, end):
        print(url)
        result_list.append(url)

    return result_list


def comic_book_album(session, url):
    return comic_book(session, url)


def comic_book_chapter(session, url):
    return episode(session, url)


def main():
    session = requests.Session()
    album = comic_book(session, 'https://www.manhuagui.com/comic/7580')

    for chapter in album['comics']:
        print(episode(session, chapter[2]))


if __name__ == '__main__':
    main()
