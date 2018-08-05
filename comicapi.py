from search_comic import ComicIndex
from comicbook import ComicBook


class ComicAPI:
    def __init__(self):
        self.__ci = ComicIndex()
        self.__book = ComicBook()

    def get_list(self):
        return self.__ci.get_list()

    def get_comic_book(self, index):
        pass

    def get_content(self, index, episode):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
