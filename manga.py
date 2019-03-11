from manhuagui.crawl_manhuagui import crawl_manhuagui
from manhuagui.episode import episode
from manhuagui.comic_book import comic_book


def comic_book_list(start=0, end=0):
    result_list = list()

    for url in crawl_manhuagui(start, end):
        print(url)
        result_list.append(url)

    return result_list


def comic_book_album(url):
    return comic_book(url)


def comic_book_chapter(url):
    return episode(url)
