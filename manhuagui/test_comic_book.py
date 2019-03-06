import unittest
from comic_book import comic_book


class TestComicBook(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.manhuagui.com/comic/7580/'

    def tearDown(self):
        pass

    def test_comic_book(self):
        book = comic_book('')
        self.assertFalse(book)

        book = comic_book(self.url)
        self.assertTrue(len(book) > 0)
        self.assertEqual(book['url'], self.url)
        self.assertTrue(len(book['book-title']) > 0)
        self.assertTrue(type(book['comics']) is list)
        self.assertTrue(type(book['comics'][0]) is dict)


if __name__ == '__main__':
    unittest.main()
