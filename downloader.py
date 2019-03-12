import json
import argparse
from manga import comic_book_album
from manga import comic_book_chapter
from manhuagui.constant import MANHUAGUI_COMIC_URL


def download(start_index=0, end_index=0):
    comic_books = dict()

    for index in range(start_index, end_index + 1):
        comic_books.clear()
        album = comic_book_album(MANHUAGUI_COMIC_URL + str(index))
        comic_books['title'] = album['book-title']
        comic_books['uri'] = album['url']
        comic_books['album'] = list()
        for chapter in album['comics']:
            c = dict()
            c['uri'] = chapter[2]
            c['title'] = chapter[1]
            c['pics'] = comic_book_chapter(chapter[2])
            comic_books['album'].append(c)

        file_name = str(index) + '.json'
        output = json.dumps(comic_books)
        with open(file_name, 'w') as f:
            f.write(output)


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-s',
        '--start',
        type=int,
        help='start comic id',
        dest='start_index',
        required=False
    )

    parser.add_argument(
        '-e',
        '--end',
        type=int,
        help='end comic id',
        dest='end_index',
        required=False
    )

    args = parser.parse_args()

    start = args.start_index if args.start_index else 0
    end = args.end_index if args.end_index else 0

    return start, end


def main():
    start_index, end_index = get_args()

    if start_index > end_index:
        print('Error: start index must smaller than end index')
        exit(-1)

    download(start_index, end_index)


if __name__ == '__main__':
    main()
