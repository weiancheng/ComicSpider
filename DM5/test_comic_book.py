from DM5.comic_book import get_episodes
import unittest


class TestGetEpisodes(unittest.TestCase):
    def setUp(self):
        self.URL = 'http://www.dm5.com/manhua-jinyeyuemeiyuanjunwang/'

    def tearDown(self):
        pass

    def test_get_episodes(self):
        results = get_episodes(self.URL)
        self.assertTrue(len(results) > 0)
        for result in results:
            self.assertRegex(result, "m\d+")
            self.assertTrue(type(results[result]) == str)


if __name__ == '__main__':
    unittest.main()
