import unittest
from manhuagui.crawl_manhuagui import crawl_manhuagui


class TestCrawlManhuagui(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_crawl_manhuagui(self):
        for url in crawl_manhuagui(5):
            self.assertTrue(len(url) > 0)


if __name__ == '__main__':
    unittest.main()
